import pytest

from src.reports import working_or_weekend_expenses
from src.utils import PATH_TO_XLSX


def test_working_or_weekend_expenses():
    assert working_or_weekend_expenses(PATH_TO_XLSX).to_dict() == {
        "Траты в выходные дни": {0: -272.56734513274336},
        "Траты в рабочие дни": {0: -112.1082175925926},
    }
    assert working_or_weekend_expenses(PATH_TO_XLSX, "09.09.2019 12:12:12").to_dict() == {
        "Траты в выходные дни": {0: -389.8050961538462},
        "Траты в рабочие дни": {0: 334.10868263473054},
    }
    assert working_or_weekend_expenses(PATH_TO_XLSX, "09.09.2020 12:15:18").to_dict() == {
        "Траты в выходные дни": {0: 318.171},
        "Траты в рабочие дни": {0: 339.903137254902},
    }
    assert working_or_weekend_expenses(PATH_TO_XLSX, "09.09.2021 10:14:19").to_dict() == {
        "Траты в выходные дни": {0: -71.92851351351351},
        "Траты в рабочие дни": {0: -892.0936956521739},
    }


def test_raises():
    with pytest.raises(Exception):
        assert (
            working_or_weekend_expenses(PATH_TO_XLSX, "09.09.2022 12:12:12")
            == "Введенная вами дата выходит за пределы поиска!"
        )
    with pytest.raises(Exception):
        assert (
            working_or_weekend_expenses(PATH_TO_XLSX, "09.09.2007 12:12:12")
            == "Введенная вами дата выходит за пределы поиска!"
        )
