import json
import logging
import os

from src.utils import (
    json_data,
    json_file_user_reading,
    list_date_transactions,
    present_time,
    price_ticket_data,
    read_excel_transactions,
    reading_api_data,
    sorted_amount,
)

json_list = {
    "greeting": None,
    "cards": [{"last_digits": None, "total_spent": None, "cashback": None}],
    "top_transactions": [
        {"date": None, "amount": None, "category": None, "description": None},
        {"date": None, "amount": None, "category": None, "description": None},
    ],
    "currency_rates": [{"currency": None, "rate": None}, {"currency": None, "rate": None}],
    "stock_prices": [
        {"stock": None, "price": None},
        {"stock": None, "price": None},
        {"stock": None, "price": None},
        {"stock": None, "price": None},
        {"stock": None, "price": None},
    ],
}

abs_path = os.path.abspath(__file__)
src_dir = os.path.dirname(abs_path)
views_path = os.path.join(os.path.dirname(src_dir), "logs", "views_log.txt")

views_logger = logging.getLogger()
views_handler = logging.FileHandler(views_path, "w")
views_formater = logging.Formatter("%(name)s %(asctime)s %(levelname)s: %(message)s")
views_handler.setFormatter(views_formater)
views_logger.addHandler(views_handler)
views_logger.setLevel(logging.DEBUG)


def views(file_path, file_data: str) -> str:
    """Главная"""
    views_logger.info("Starting app...")
    card_info = sorted_amount(list_date_transactions(read_excel_transactions(file_path), file_data))
    json_info = json_file_user_reading(json_data)
    values_list = []
    tickets_list = []
    json_list["greeting"] = present_time()
    json_list["cards"] = []
    json_list["top_transactions"] = []
    views_logger.info("Перебор валют...")
    for i, info in enumerate(json_list["currency_rates"]):
        values_list.append(json_info.get("user_currencies")[i])
        info["currency"] = json_info["user_currencies"][i]
        info["rate"] = reading_api_data(values_list[i])
    views_logger.info("Перебор тикетов...")
    for i, info in enumerate(json_list["stock_prices"]):
        tickets_list.append(json_info.get("user_stocks")[i])
        info["stock"] = json_info["user_stocks"][i]
        info["price"] = price_ticket_data(tickets_list[i])
    views_logger.info("Перебор составляющих ответа...")
    for card in card_info:
        last_digits = str(card.get("Номер карты")).replace("*", "")
        total_spent = card.get("Сумма операции с округлением")
        cashback = card.get("Кэшбэк")
        date = card.get("Дата платежа")
        amount = card.get("Сумма операции")
        category = card.get("Категория")
        description = card.get("Описание")
        json_list["cards"].append({"last_digits": last_digits, "total_spent": total_spent, "cashback": cashback})
        views_logger.info("Настройка транзакций...")
        if len(json_list["top_transactions"]) < 5:
            json_list["top_transactions"].append(
                {"date": date, "amount": amount, "category": category, "description": description}
            )
        views_logger.info("Finished app...")
    return json.dumps(json_list, indent=2)
