from src.reports import working_or_weekend_expenses
from src.services import search_transfers_individuals
from src.utils import PATH_TO_XLSX, read_excel_transactions
from src.views import views


true_list_transactions = read_excel_transactions(PATH_TO_XLSX)


def views_main(file_path, source_date):
    return views(file_path, source_date)


def search_transfers_main(file_path):
    return search_transfers_individuals(file_path)


def working_or_weekend_main(file_path, date=None):
    return working_or_weekend_expenses(file_path, date)


if __name__ == '__main__':
    print(views_main(PATH_TO_XLSX, '2021-11-12 13:13:13'))
    print(search_transfers_main(true_list_transactions))
    print(working_or_weekend_main(PATH_TO_XLSX))
