#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import gzip
import io
import json
import logging
import os
import re
import statistics
from collections import namedtuple
from datetime import datetime
from string import Template

# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

LOG_RECORD_RE = re.compile(
    "^"
    "\S+ "  # remote_addr
    "\S+\s+"  # remote_user (note: ends with double space)
    "\S+ "  # http_x_real_ip
    "\[\S+ \S+\] "  # time_local [datetime tz] i.e. [29/Jun/2017:10:46:03 +0300]
    '"\S+ (?P<href>\S+) \S+" '  # request "method href proto" i.e. "GET /api/v2/banner/23815685 HTTP/1.1"
    "\d+ "  # status
    "\d+ "  # body_bytes_sent
    '"\S+" '  # http_referer
    '".*" '  # http_user_agent
    '"\S+" '  # http_x_forwarded_for
    '"\S+" '  # http_X_REQUEST_ID
    '"\S+" '  # http_X_RB_USER
    "(?P<time>\d+\.\d+)"  # request_time
)

DEFAULT_CONFIG_PATH = "./config.json"
default_config = {
    "ERRORS_LIMIT": 1,
    "MAX_REPORT_SIZE": 1000,
    "REPORTS_DIR": "./reports",
    "LOGS_DIR": "./log",
    # "LOG_FILE": "./log/log",
}

REPORT_TEMPLATE_PATH = "./report.html"

NamedLogInfo = namedtuple("NamedLogInfo", ["path", "date"])


def load_conf(conf_path):
    try:
        with open(conf_path, "rb") as conf_file:
            conf_from_file = json.load(conf_file)
        config = default_config.copy()
        config.update(conf_from_file)
        return config
    except FileNotFoundError:
        print(f"Error: config file {conf_path} was not found")
        return None
    except json.JSONDecodeError:
        print(f"Error: can't parse file {conf_path} correctly")
        return None


####################################
# Analyzing
####################################


def create_report(records, max_records):
    total_records = 0
    total_time = 0.0
    intermediate_data = {}

    for href, response_time in records:
        r_time = float(response_time)
        total_records += 1
        total_time += r_time

        href_data = intermediate_data.get(href)
        if not href_data:
            href_data = {
                "count": 0,
                "time_sum": 0,
                "times_list": [],
            }
            intermediate_data[href] = href_data

        href_data["count"] += 1
        href_data["time_sum"] += r_time
        href_data["times_list"].append(r_time)

    # list of tuples sorted by time_sum descending
    sorted_list = sorted(
        intermediate_data.items(),
        key=lambda item: item[1]["time_sum"],
        reverse=True,
    )

    output_data = []
    for href, href_data in sorted_list:
        line = {}
        line["url"] = href
        line["count"] = href_data["count"]
        line["count_perc"] = round(href_data["count"] * 100 / total_records, 3)
        line["time_sum"] = round(sum(href_data["times_list"]), 3)
        line["time_perc"] = round(line["time_sum"] * 100 / total_time, 3)
        line["time_avg"] = round(statistics.mean(href_data["times_list"]), 3)
        line["time_max"] = round(max(href_data["times_list"]), 3)
        line["time_med"] = round(statistics.median(href_data["times_list"]), 3)

        output_data.append(line)

        if len(output_data) > max_records:
            break

    return output_data


def get_log_records(log_path, errors_limit=None):
    open_fn = gzip.open if is_gzip_file(log_path) else io.open
    errors = 0
    records = 0
    log_records = []
    with open_fn(log_path, mode="rb") as log_file:
        for line in log_file:
            records += 1
            string = line.decode("utf-8").strip()
            match = LOG_RECORD_RE.match(string)
            if match:
                log_records.append(
                    (match.groupdict()["href"], match.groupdict()["time"])
                )
            else:
                errors += 1

    if (
        errors_limit is not None
        and records > 0
        and errors / float(records) > errors_limit
    ):
        raise RuntimeError("Errors limit exceeded")

    return log_records


####################################
# Utils
####################################


def setup_logger(log_path):
    if log_path is not None:
        log_dir = os.path.split(log_path)[0]
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="[%(asctime)s] %(levelname).1s %(message)s",
        datefmt="%Y.%m.%d %H:%M:%S",
    )


def get_latest_log_info(log_dir):
    if not os.path.isdir(log_dir):
        return None

    latest_date = datetime.fromtimestamp(0)
    latest_path = None
    for filename in os.listdir(log_dir):
        match = re.match(r"^nginx-access-ui\.log-(?P<date>\d{8})(\.gz)?$", filename)
        if not match:
            continue
        file_date = datetime.strptime(match.groupdict()["date"], "%Y%m%d")
        if latest_date < file_date:
            latest_path = os.path.join(log_dir, filename)
            latest_date = file_date

    return NamedLogInfo(latest_path, latest_date) if latest_path else None


def is_gzip_file(file_path):
    return file_path.split(".")[-1] == "gz"


def render_template(template_path, to, data):
    if data is None:
        data = []

    with open(template_path, "r") as tmpl:
        tmpl_str = tmpl.read()

    with open(to, "w") as report:
        report.write(Template(tmpl_str).safe_substitute(table_json=json.dumps(data)))


def main(config):
    # resolving an actual log
    latest_log_info = get_latest_log_info(config["LOGS_DIR"])
    if not latest_log_info:
        logging.info("Ooops. No log files yet")
        return

    report_date_string = latest_log_info.date.strftime("%Y.%m.%d")
    report_filename = f"report-{report_date_string}.html"
    report_dir = config["REPORTS_DIR"]
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    report_file_path = os.path.join(report_dir, report_filename)
    if os.path.isfile(report_file_path):
        logging.info("Looks like everything is up-to-date")
        return

    # report creation
    logging.info(f'Collecting data from "{os.path.normpath(latest_log_info.path)}"')
    log_records = get_log_records(latest_log_info.path, config.get("ERRORS_LIMIT"))
    report_data = create_report(log_records, config["MAX_REPORT_SIZE"])

    render_template(REPORT_TEMPLATE_PATH, report_file_path, report_data)

    logging.info(f'Report saved to "{os.path.normpath(report_file_path)}"')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", help="Config file path", default=DEFAULT_CONFIG_PATH
    )
    args = parser.parse_args()

    config = load_conf(args.config)
    if config:
        setup_logger(config.get("LOG_FILE"))
        try:
            main(config)
        except:
            logging.exception("Unexpected exception occuered")
