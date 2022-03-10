## log analyzer (python3) - анализатор логов nginx

Задание в рамках обучения на курсе **Python Developer. Professional** (otus.ru)

#### Запуск скрипта

```
python3 log_analyzer.py [--config config.json]
```

#### Запуск тестов

```
python3 test_log_analyzer.py
```

#### config.json example

```
{
    "ERRORS_LIMIT": 1,
    "MAX_REPORT_SIZE": 1000,
    "REPORTS_DIR": "./reports",
    "LOGS_DIR": "./log",
    "LOG_FILE": "./log/log",
}
```

## Parameters

| Param           | Decsription                             |
| --------------- | --------------------------------------- |
| ERRORS_LIMIT    | % ошибок для прерывания обработки       |
| MAX_REPORT_SIZE | максимальное число строк в отчете       |
| REPORTS_DIR     | путь к каталогу с отчетами              |
| LOGS_DIR        | путь к каталогу с исходными логами      |
| LOG_FILE        | путь к файлу с логом работы анализатора |
