from src.reports import working_or_weekend_expenses
from src.services import search_transfers_individuals
from src.utils import file_xlsx, PATH_TO_XLSX
from src.views import views


def views_main():
    return views("2021-12-12 12:12:12")


def search_transfers_main():
    return search_transfers_individuals(file_xlsx)


def working_or_transfers_main():
    return working_or_weekend_expenses(PATH_TO_XLSX)


if __name__ == '__main__':
    print(views_main())
    print(search_transfers_main())
    print(working_or_transfers_main())
