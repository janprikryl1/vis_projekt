from data.DBConnection import get_db_connection


def create_test(user_id, title, description, subject, sequence, max_time):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Test (user_id, title, description, subject, sequence, max_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, title, description, subject, sequence, max_time))
    test_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return test_id


def update_test(user_id, test_id, title, description, subject, sequence, max_time):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Test
        SET title = ?, description = ?, subject = ?, sequence = ?, max_time = ?
        WHERE user_id = ? AND test_id = ?
    """, (title, description, subject, sequence, max_time, user_id, test_id))
    conn.commit()
    conn.close()


def get_test_by_id(test_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Test WHERE test_id = ?", (test_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def delete_test(test_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Test WHERE test_id = ?", (test_id,))
    conn.commit()
    conn.close()


# CRUD functions for FilledTest
def create_filled_test(user_id, test_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Filled_test (test_id, user_id, date_time_beginning)
        VALUES (?, ?, datetime('now'))
    """, (test_id, user_id))
    filled_test_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return filled_test_id


def get_filled_tests_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Test.test_id, Test.title, Filled_test.date_time_beginning
        FROM Filled_test
        JOIN Test ON Test.test_id = Filled_test.test_id
        WHERE Filled_test.user_id = ?
        ORDER BY date_time_beginning DESC
    """, (user_id,))
    result = cursor.fetchall()
    conn.close()
    return result


def get_all_tests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Test")
    result = cursor.fetchall()
    conn.close()
    return result


def get_tests_not_filled_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get filled test IDs
    cursor.execute("""
        SELECT test_id
        FROM Filled_test
        WHERE user_id = ?
    """, (user_id,))
    filled_test_ids = {row[0] for row in cursor.fetchall()}

    # Get unfilled tests
    if filled_test_ids:
        cursor.execute("""
            SELECT *
            FROM Test
            WHERE test_id NOT IN ({})
        """.format(",".join("?" * len(filled_test_ids))), tuple(filled_test_ids))
    else:
        cursor.execute("SELECT * FROM Test")

    result = cursor.fetchall()
    conn.close()
    return result