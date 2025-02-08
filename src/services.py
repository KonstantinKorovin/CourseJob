import json
import logging
import os
import re

from src.utils import PATH_TO_XLSX, read_excel_transactions

xlsx_transactions = read_excel_transactions(PATH_TO_XLSX)
abs_path = os.path.abspath(__file__)
src_dir = os.path.dirname(abs_path)
services_path = os.path.join(os.path.dirname(src_dir), "logs", "services_log.txt")

services_logger = logging.getLogger()
services_handler = logging.FileHandler(services_path, "w")
services_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s: %(message)s")
services_handler.setFormatter(services_formatter)
services_logger.addHandler(services_handler)
services_logger.setLevel(logging.DEBUG)


def search_transfers_individuals(list_dict: list) -> str:
    """Поиск переводов физ лиц"""
    services_logger.info("Starting app...")
    transactions_list = []
    services_logger.info("Получение шаблона...")
    string = re.compile(r"\D+\s\D\.")
    if not list_dict:
        services_logger.warning("Нету списка...")
        raise TypeError("И что мы будем перебирать?")
    else:
        for x in list_dict:
            if string.search(x["Описание"]) and x.get("Категория") == "Переводы":
                transactions_list.append(x)
        services_logger.info("Finished app...")
        return json.dumps(transactions_list, indent=2)
