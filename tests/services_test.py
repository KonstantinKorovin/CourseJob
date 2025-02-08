import json

import pytest

from src.services import search_transfers_individuals


@pytest.mark.parametrize(
    "dicts, expected_result",
    [
        (
            [
                {"Описание": "Константин К.", "Категория": "Переводы"},
                {"Описание": "vorona Def", "Категория": "Переводы"},
                {"Описание": "Андрей Д.", "Категория": "DEf"},
                {"Описание": "Ситидрайв", "Категория": "ОПЛАТА"},
            ],
            [{"Описание": "Константин К.", "Категория": "Переводы"}],
        )
    ],
)
def test_fiz_name_transactions(dicts, expected_result):
    assert json.loads(search_transfers_individuals(dicts)) == expected_result
    with pytest.raises(Exception):
        assert json.loads(search_transfers_individuals([])) == "И что мы будем перебирать?"
