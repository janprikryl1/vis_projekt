from data.TablesData import get_all_tables, get_all_table_data


class Tables:
    def get_tables(self):
        return get_all_tables()

    def get_table_data(self, table_name):
        return get_all_table_data(table_name)