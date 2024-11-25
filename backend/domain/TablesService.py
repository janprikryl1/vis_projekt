from data.TablesDTO import get_all_tables, get_all_table_data
from domain.BaseService import BaseService


class Tables(BaseService):
    def __init__(self, auth_header):
        super().__init__(auth_header)

    def get_tables(self):
        return get_all_tables()

    def get_table_data(self, table_name):
        return get_all_table_data(table_name)