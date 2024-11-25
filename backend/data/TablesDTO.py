from data.DBConnection import get_db_connection


def get_all_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table';
    """, )

    result = cursor.fetchall()
    conn.close()

    return [row[0] for row in result]


def get_all_table_data(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = f"SELECT * FROM {table_name};"
    cursor.execute(query)

    result = cursor.fetchall()
    conn.close()

    return [row for row in result]
