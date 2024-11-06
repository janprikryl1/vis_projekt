from data.DBConnection import get_db_connection


def get_filled_tests_for_student(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Filled_test.filled_test_id, Test.title, Filled_test.date_time_beginning
        FROM Filled_test
        JOIN Test ON Test.test_id = Filled_test.test_id
        WHERE Filled_test.user_id = ?
        ORDER BY date_time_beginning DESC
    """, (user_id,))

    result = cursor.fetchall()
    conn.close()

    return [
        {'test_id': row[0], 'test_title': row[1], 'date_time': row[2]}
        for row in result
    ]


def get_created_tests_for_teacher(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT test_id, title, datetime
        FROM Test
        WHERE creator_id = ?
        ORDER BY user_id DESC
    """, (user_id,))

    result = cursor.fetchall()
    conn.close()

    return [
        {'test_id': row[0], 'title': row[1], 'created_at': row[2]}
        for row in result
    ]