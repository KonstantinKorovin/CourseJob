import unittest
from unittest.mock import patch

import json

from src.reports import working_or_weekend_expenses
from src.utils import PATH_TO_XLSX


class TestWorkingOrWeekendExpenses(unittest.TestCase):

    @patch('src.utils.read_excel_transactions')
    def test_no_date(self, mock_read_excel):
        mock_read_excel.return_value = [
            {"Дата операции": "01.10.2021 12:00:00", "Сумма операции": 100},
            {"Дата операции": "02.10.2021 12:00:00", "Сумма операции": 200},
            {"Дата операции": "07.10.2019 12:00:00", "Сумма операции": 300},
            {"Дата операции": "08.10.2018 12:00:00", "Сумма операции": 400},
            {"Дата операции": "15.10.2019 12:00:00", "Сумма операции": 500},
            {"Дата операции": "04.09.2020 12:00:00", "Сумма операции": 600},
        ]

        expected = {
            'Траты в выходные дни': 272.56734513274336,
            'Траты в рабочие дни': 112.1082175925926
        }
        result = working_or_weekend_expenses(PATH_TO_XLSX)
        self.assertEqual(json.loads(result), expected)

    @patch('src.utils.read_excel_transactions')
    def test_within_period(self, mock_read_excel):
        mock_read_excel.return_value = [
            {"Дата операции": "01.10.2020 12:00:00", "Сумма операции": 100},
            {"Дата операции": "02.10.2020 12:00:00", "Сумма операции": 200},
            {"Дата операции": "07.10.2020 12:00:00", "Сумма операции": 300},
            {"Дата операции": "08.10.2019 12:00:00", "Сумма операции": 400},
            {"Дата операции": "15.10.2019 12:00:00", "Сумма операции": 500},
            {"Дата операции": "04.09.2019 12:00:00", "Сумма операции": 600},
        ]

        date = "15.10.2021 12:00:00"
        expected = {
            'Траты в выходные дни': 311.2394736842105,
            'Траты в рабочие дни': 1378.027522123894
        }
        result = working_or_weekend_expenses(PATH_TO_XLSX, date)
        self.assertEqual(json.loads(result), expected)

    @patch('src.utils.read_excel_transactions')
    def test_outside_period(self, mock_read_excel):
        mock_read_excel.return_value = [
            {"Дата операции": "01.10.2023 12:00:00", "Сумма операции": 100},
            {"Дата операции": "02.10.2023 12:00:00", "Сумма операции": 200},
            {"Дата операции": "07.10.2023 12:00:00", "Сумма операции": 300},
            {"Дата операции": "08.10.2023 12:00:00", "Сумма операции": 400},
            {"Дата операции": "15.10.2023 12:00:00", "Сумма операции": 500},
            {"Дата операции": "04.09.2023 12:00:00", "Сумма операции": 600},
        ]

        with self.assertRaises(TypeError):
            working_or_weekend_expenses(PATH_TO_XLSX, "01.09.2023 12:00:00")
