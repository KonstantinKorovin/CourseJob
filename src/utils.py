import json
import logging
import os
from datetime import datetime, time
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

abs_path = os.path.abspath(__file__)
src_dir = os.path.dirname(abs_path)
utils_path = os.path.join(os.path.dirname(src_dir), "logs", "utils_log.txt")
PATH_TO_XLSX = os.path.join(os.path.dirname(src_dir), "data", "operations.xlsx")
json_data = os.path.join(os.path.dirname(src_dir), "user_settings.json")


root_logger = logging.getLogger()
file_handler = logging.FileHandler(utils_path, "w")
file_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
root_logger.addHandler(file_handler)
root_logger.setLevel(logging.DEBUG)

root_logger.info("Starting app...")
load_dotenv()
root_logger.info("Получение файла...")


def read_excel_transactions(file_path: Any) -> Any:
    """Чтение excel файла"""
    root_logger.info("Чтение файла...")
    return pd.read_excel(file_path).to_dict(orient="records")


def greeting(date: Any) -> Any:
    """Парсинг даты в формат "datetime.datetime" """
    root_logger.info("Парсинг даты...")
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


def new_date_format(file_date: Any) -> Any:
    """Форматирование даты"""
    for x in file_date:
        x["Дата операции"] = (
            f"{x['Дата операции'][6:10]}-{x['Дата операции'][3:5]}-"
            f"{x['Дата операции'][0:2]} {x['Дата операции'][11:19]}"
        )
    return file_date


file_xlsx = new_date_format(read_excel_transactions(PATH_TO_XLSX))


def sorted_amount(file_as_sorted: Any) -> Any:
    """Возврат суммы платежей в порядке убывания"""
    return sorted(file_as_sorted, key=lambda x: x.get("Сумма операции"), reverse=True)


def present_time() -> Any:
    """Приветственное сообщение"""
    date_time = datetime.now().time()
    date_morning = time(6, 0)
    date_day = time(12, 0)
    date_evening = time(18, 0)
    date_night = time(0, 0)
    if date_day > date_time > date_morning:
        return "Доброе утро"
    elif date_evening > date_time > date_day:
        return "Добрый день"
    elif date_night > date_time > date_evening:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def list_date_transactions(list_data: Any, file_data: Any = None) -> Any:
    """Получение списка в определенном диапазоне дат"""
    date_max = greeting(file_xlsx[0]["Дата операции"])  # 2021-12-31 16:44:00
    date_min = greeting(file_xlsx[-1]["Дата операции"])  # 2018-01-01 12:49:53
    date_one = datetime(greeting(file_data).year, greeting(file_data).month, 1)
    user_date = greeting(file_data)
    if user_date > date_max or user_date < date_min:
        raise ValueError("Введенная вами дата не входит в диапазон вывода транзакций")
    else:
        new_list = []
        for row in list_data:
            date_operation = row["Дата операции"]
            if str(date_one)[:10] <= date_operation[:10] <= str(user_date)[:10]:
                new_list.append(row)
        return new_list


def json_file_user_reading(file_data: Any) -> Any:
    """Чтение пользовательских данных"""
    root_logger.info("Чтение пользовательского файла...")
    with open(file_data, "r", encoding="utf-8") as file:
        root_logger.info("Преобразование пользовательского файла от json...")
        return json.load(file)


data = json_file_user_reading(json_data)


def reading_api_usd_data() -> Any:
    """Получение курса доллара относительно рубля"""
    root_logger.info("Создание url для usd...")
    url = (
        f"https://api.apilayer.com/exchangerates_data/convert?to={'RUB'}"
        f"&from={data['user_currencies'][0]}&amount={1}&date={datetime.now().strftime('%Y-%m-%d')}"
    )
    api_key = os.getenv("API-KEY")
    headers = {"apikey": api_key}
    root_logger.info("Запрос данных...")
    response = requests.request("GET", url, headers=headers)

    status_code = response.status_code
    result = response.text
    root_logger.info("Получение ответа...")
    if status_code != 200:
        root_logger.warning(f"error {status_code}!")
        return f"error {status_code}!"
    root_logger.info("Успешно!")
    return json.loads(result)["result"]


def reading_api_euro_data() -> Any:
    """Получение курса доллара относительно рубля"""
    root_logger.info("Создание url для euro...")
    url = (
        f"https://api.apilayer.com/exchangerates_data/convert?to={'RUB'}"
        f"&from={data['user_currencies'][1]}&amount={1}&date={datetime.now().strftime('%Y-%m-%d')}"
    )
    api_key = os.getenv("API-KEY")
    headers = {"apikey": api_key}
    root_logger.info("Запрос данных...")
    response = requests.request("GET", url, headers=headers)

    status_code = response.status_code
    result = response.text
    root_logger.info("Получение ответа...")
    if status_code != 200:
        root_logger.warning(f"error {status_code}!")
        return f"error {status_code}!"
    root_logger.info("Успешно!")
    return json.loads(result)["result"]


def price_ticket_apple() -> Any:
    """Получение цены тикета Apple"""
    api_key = os.getenv("API-KEY-TICKETS")
    root_logger.info("Создание url для apple...")
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={data['user_stocks'][0]}&apikey={api_key}"
    root_logger.info("Запрос данных...")
    response = requests.get(url)
    status_code = response.status_code
    result = response.text
    root_logger.info("Получение ответа...")
    if status_code != 200:
        root_logger.warning(f"error {status_code}!")
        return f"error {status_code}!"
    root_logger.info("Успешно!")
    return float(json.loads(result)["Global Quote"]["05. price"])


def price_ticket_amazon() -> Any:
    """Получение цены тикета Amazon"""
    api_key = os.getenv("API-KEY-TICKETS")
    root_logger.info("Создание url для amazon...")
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={data['user_stocks'][1]}&apikey={api_key}"
    root_logger.info("Запрос данных...")
    response = requests.get(url)
    status_code = response.status_code
    result = response.text
    root_logger.info("Получение ответа...")
    if status_code != 200:
        root_logger.warning(f"error {status_code}!")
        return f"error {status_code}!"
    root_logger.info("Успешно!")
    return float(json.loads(result)["Global Quote"]["05. price"])


def price_ticket_google() -> Any:
    """Получение цены тикета Google"""
    api_key = os.getenv("API-KEY-TICKETS")
    root_logger.info("Создание url для google...")
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={data['user_stocks'][2]}&apikey={api_key}"
    root_logger.info("Запрос данных...")
    response = requests.get(url)
    status_code = response.status_code
    result = response.text
    root_logger.info("Получение ответа...")
    if status_code != 200:
        root_logger.warning(f"error {status_code}!")
        return f"error {status_code}!"
    root_logger.info("Успешно!")
    return float(json.loads(result)["Global Quote"]["05. price"])


def price_ticket_msft() -> Any:
    """Получение цены тикета MSFT"""
    api_key = os.getenv("API-KEY-TICKETS")
    root_logger.info("Создание url для msft...")
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={data['user_stocks'][3]}&apikey={api_key}"
    root_logger.info("Запрос данных...")
    response = requests.get(url)
    status_code = response.status_code
    result = response.text
    root_logger.info("Получение ответа...")
    if status_code != 200:
        root_logger.warning(f"error {status_code}!")
        return f"error {status_code}!"
    root_logger.info("Успешно!")
    return float(json.loads(result)["Global Quote"]["05. price"])


def price_ticket_tesla() -> Any:
    """Получение цены тикета Tesla"""
    api_key = os.getenv("API-KEY-TICKETS")
    root_logger.info("Создание url для tesla...")
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={data['user_stocks'][4]}&apikey={api_key}"
    root_logger.info("Запрос данных...")
    response = requests.get(url)
    status_code = response.status_code
    result = response.text
    root_logger.info("Получение ответа...")
    if status_code != 200:
        root_logger.warning(f"error {status_code}!")
        return f"error {status_code}!"
    root_logger.info("Успешно!")
    return float(json.loads(result)["Global Quote"]["05. price"])
