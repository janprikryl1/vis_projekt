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

def get_all_tests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Test")
    result = cursor.fetchall()
    conn.close()
    return result