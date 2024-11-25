from data.DBConnection import get_db_connection


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

def get_filled_test_for_user_details(user_id, test_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
                SELECT filled_test_id, date_time_beginning
                FROM Filled_test
                WHERE user_id = ? AND test_id = ?
            """, (user_id, test_id))
    row = cursor.fetchone()

    conn.close()
    return row


def calculate_score(test_id, filled_test_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Count of correct filled questions for this filled test
    cursor.execute("""
        SELECT COUNT(*)
        FROM Filled_question
        WHERE filled_test_id = ? AND is_correct = 1
    """, (filled_test_id,))
    correct_count = cursor.fetchone()[0]

    # Total number of questions in the test
    cursor.execute("""
        SELECT COUNT(*)
        FROM Question
        WHERE test_id = ?
    """, (test_id,))
    total_questions = cursor.fetchone()[0]

    conn.close()
    return (correct_count / total_questions) * 100 if total_questions > 0 else 0