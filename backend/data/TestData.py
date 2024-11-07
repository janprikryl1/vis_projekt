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
        WHERE user_id = ?
        ORDER BY datetime DESC
    """, (user_id,))

    result = cursor.fetchall()
    conn.close()

    return [
        {'test_id': row[0], 'title': row[1], 'created_at': row[2]}
        for row in result
    ]

def get_filled_test_detail_for_student(user_id, test_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Filled_test.filled_test_id, Test.title, Filled_test.date_time_beginning, Filled_test.score
        FROM Filled_test
        JOIN Test ON Test.test_id = Filled_test.test_id
        WHERE Filled_test.user_id = ? AND Filled_test.filled_test_id = ?
    """, (user_id, test_id))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            'filled_test_id': row['filled_test_id'],
            'test_title': row['title'],
            'date_time_beginning': row['date_time_beginning'],
            'score': row['score']
        }
    return {}


def get_test_detail_for_teacher(user_id, test_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT test_id, title, datetime, description
        FROM Test
        WHERE user_id = ? AND test_id = ?
    """, (user_id, test_id))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            'test_id': row['test_id'],
            'title': row['title'],
            'datetime': row['datetime'],
            'description': row['description']
        }
    return {}

def save_test(self, title, description, subject, sequence, max_time):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Test (user_id, title, description, subject, sequence, max_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (self.user_id, title, description, subject, sequence, max_time))

    test_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "test_id": test_id
    }