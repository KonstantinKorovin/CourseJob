import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any

from src.utils import PATH_TO_XLSX, read_excel_transactions

abs_path = os.path.abspath(__file__)
src_dir = os.path.dirname(abs_path)
reports_path = os.path.join(os.path.dirname(src_dir), "logs", "reports_log.txt")

path = PATH_TO_XLSX
reports_logger = logging.getLogger()
reports_handler = logging.FileHandler(reports_path, "w")
reports_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s: %(message)s")
reports_handler.setFormatter(reports_formatter)
reports_logger.addHandler(reports_handler)
reports_logger.setLevel(logging.DEBUG)


def dec_working_or_weekend(func):
    """Логирование одноименной функции"""

    def wrapper(*args, **kwargs):
        result = f"{func.__name__} была вызвана с аргументами: {func()}"
        return result

    return wrapper


function_results = {}


def save_result(filename: str = "default.json") -> Any:
    """Декоратор для сохранения результата выполнения функции."""

    def inner(func):
        def wrapper(*args, **kwargs):
            true_filename = os.path.join(os.path.dirname(src_dir), "data", filename)
            with open(true_filename, "w", encoding="utf-8") as file:
                result = func(*args, **kwargs)
                function_name = func.__name__
                params_key = (args, tuple(sorted(kwargs.items())))
                function_results[(function_name, params_key)] = result
                file.write(result)
            return result

        return wrapper

    return inner


@save_result("default.json")
def working_or_weekend_expenses(transactions: str, date: str = None) -> str:
    """Выводит среднюю сумму трат в рабочие/выходные дни за последние три месяца от переданной даты"""
    reports_logger.info("Starting app...")
    df = read_excel_transactions(transactions)
    reports_logger.info("Форматирование максимальных дат в обьект времени...")
    date_max = datetime.strptime(df[0]["Дата операции"], "%d.%m.%Y %H:%M:%S")
    date_min = datetime.strptime(df[-1]["Дата операции"], "%d.%m.%Y %H:%M:%S")
    job_days = []
    free_days = []
    time_delta = timedelta(days=90)
    reports_logger.info("Проверка есть ли вообще дата...")
    if not date:
        date = date_max
    elif date is not None:
        date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
        reports_logger.info("Проверка вхождения даты между максимальной и минимальной...")
        if date < date_min or date > date_max:
            raise TypeError("Введенная вами дата выходит за пределы поиска!")
    three_months_ago = date - time_delta
    reports_logger.info("Перебор дата фрейма...")
    for x in df:
        operation_date = datetime.strptime(x["Дата операции"], "%d.%m.%Y %H:%M:%S")
        reports_logger.info("Проверка условия вхождения даты...")
        if three_months_ago <= operation_date <= date:
            reports_logger.info("Проверка рабочих дней...")
            if operation_date.isoweekday() in [1, 2, 3, 4, 5]:
                job_days.append(x.get("Сумма операции"))
            reports_logger.info("Проверка выходных...")
            if operation_date.isoweekday() in [6, 7]:
                free_days.append(x.get("Сумма операции"))
    reports_logger.info("Подсчет трат по будням и выходным ...")
    transactions_job = str(sum(job_days) / len(job_days)).replace("-", "")
    transactions_free = str(sum(free_days) / len(free_days)).replace("-", "")
    reports_logger.info("Парсинг json...")
    df1 = {"Траты в рабочие дни": float(transactions_job), "Траты в выходные дни": float(transactions_free)}
    reports_logger.info("Finished app...")
    return json.dumps(df1)
