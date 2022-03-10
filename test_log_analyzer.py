import unittest
import log_analyzer
import os

# test environment
TMP_DIR = "./test_tmp"
LOGS = (
    "nginx-access-ui.log-20220308",  # latest log file by date, must be first in tuple
    "nginx-access-ui.log-20170630.gz",
    "nginx-access-ui.log-20220309.bz2",  # file with invalid extention and newest date
)


class TestMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")
        if not os.path.exists(TMP_DIR):
            os.makedirs(TMP_DIR)

        for log in LOGS:
            with open(os.path.join(TMP_DIR, log), "w"):
                pass

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")
        if os.path.exists(TMP_DIR):
            for log in LOGS:
                os.remove(os.path.join(TMP_DIR, log))
            os.rmdir(TMP_DIR)

    # def setUp(self):
    #     print("setUp")

    # def tearDown(self):
    #     print("tearDown")

    def test_is_gzip_file(self):
        print("test_is_gzip_file")
        self.assertTrue(log_analyzer.is_gzip_file("./test.gz"))
        self.assertFalse(log_analyzer.is_gzip_file("./test.bz2"))
        self.assertFalse(log_analyzer.is_gzip_file("./test"))

    def test_get_latest_log_info(self):
        latest_log_info = log_analyzer.get_latest_log_info(TMP_DIR)
        self.assertEqual(latest_log_info.path, os.path.join(TMP_DIR, LOGS[0]))


if __name__ == "__main__":
    unittest.main()
