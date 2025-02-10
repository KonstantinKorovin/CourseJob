import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.utils import (
    PATH_TO_XLSX,
    greeting,
    json_data,
    json_file_user_reading,
    list_date_transactions,
    new_date_format,
    read_excel_transactions,
    sorted_amount, reading_api_data, price_ticket_data,
)

d1 = new_date_format(read_excel_transactions(PATH_TO_XLSX))
d2 = new_date_format(read_excel_transactions(PATH_TO_XLSX))


def test_reading_transactions():
    assert d1[0]["Дата операции"] == "2021-12-31 16:44:00"
    assert d2[-1]["Дата операции"] == "2018-01-01 12:49:53"
    assert read_excel_transactions(PATH_TO_XLSX)[329]["Сумма операции"] == -119.8
    assert read_excel_transactions(PATH_TO_XLSX)[3131]["Сумма операции"] == -49.99
    assert read_excel_transactions(PATH_TO_XLSX)[983]["Статус"] == "OK"
    assert read_excel_transactions(PATH_TO_XLSX)[3679]["Статус"] == "OK"
    assert read_excel_transactions(PATH_TO_XLSX)[0]["Категория"] == "Супермаркеты"
    assert read_excel_transactions(PATH_TO_XLSX)[-1]["Категория"] == "Переводы"


def test_greeting():
    assert greeting("2021-12-12 12:12:12") == datetime(2021, 12, 12, 12, 12, 12)


def test_new_date_format():
    assert d1[0]["Дата операции"] == "2021-12-31 16:44:00"
    assert d2[-1]["Дата операции"] == "2018-01-01 12:49:53"


def test_sorted_amount():
    assert sorted_amount(d1)[0]["Сумма платежа"] == 190044.51
    assert sorted_amount(d1)[-1]["Сумма платежа"] == -190044.51


def test_date_transactions():
    with pytest.raises(Exception):
        assert (
            list_date_transactions(d1, "2022-12-31 13:13:14")
            == "Введенная вами дата не входит в диапазон вывода транзакций"
        )


def test_file_user_reading():
    assert json_file_user_reading(json_data) == {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
    }


@patch("requests.request")
def test_reading_api_error(mock_api):
    mock_response = mock_api.return_value
    mock_response.status_code = 404
    mock_response.text = '{"error": "Not found"}'
    result = reading_api_data('EUR')
    result2 = reading_api_data('USD')
    assert result == "error 404!"
    assert result2 == "error 404!"
    mock_api.assert_called()


class TestPriceTicketFunctions(unittest.TestCase):

    @patch("requests.get")
    def test_price_ticket_apple(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"Global Quote": {"05. price": "100.0"}}'
        mock_get.return_value = mock_response
        self.assertEqual(price_ticket_data("AAPL"), 100.0)

    @patch("requests.get")
    def test_price_ticket_apple_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response
        self.assertEqual(price_ticket_data("AAPL"), "error 404!")

    @patch("requests.get")
    def test_price_ticket_amazon(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"Global Quote": {"05. price": "200.0"}}'
        mock_get.return_value = mock_response
        self.assertEqual(price_ticket_data("AMZN"), 200.0)

    @patch("requests.get")
    def test_price_ticket_amazon_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response
        self.assertEqual(price_ticket_data("AMZN"), "error 404!")
