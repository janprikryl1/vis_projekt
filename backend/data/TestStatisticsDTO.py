from data.DBConnection import get_db_connection

def fetch_test_statistics(test_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.name || ' ' || p.surname AS student, 
               (COUNT(CASE WHEN fq.is_correct = 1 THEN 1 END) * 100.0 / COUNT(fq.filled_question_id)) AS success
        FROM Filled_test ft
        JOIN Profile p ON ft.user_id = p.user_id
        JOIN Filled_question fq ON ft.filled_test_id = fq.filled_test_id
        WHERE ft.test_id = ?
        GROUP BY p.user_id
    """, (test_id,))

    result = cursor.fetchall()
    conn.close()

    return [
        {'student': row[0], 'success': row[1]} for row in result
    ]