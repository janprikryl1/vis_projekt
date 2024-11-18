from datetime import datetime

from data.DBConnection import get_db_connection


def get_not_filled_tests(user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if user_id:
        cursor.execute("""
            SELECT test_id
            FROM Filled_test
            WHERE user_id = ?
        """, (user_id,))
        filled_test_ids = {row[0] for row in cursor.fetchall()}

        cursor.execute("""
            SELECT *
            FROM Test
            WHERE test_id NOT IN ({})
        """.format(",".join("?" * len(filled_test_ids))), tuple(filled_test_ids))
    else:
        cursor.execute("SELECT * FROM Test")

    result = cursor.fetchall()
    conn.close()

    return [
        {'test_id': row[0], 'title': row[1], 'created_at': row[2], 'description': row[3], 'subject': row[4],
         'sequence': row[5], 'max_time': row[6]}
        for row in result
    ]


def get_filled_tests_for_student(user_id):
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


def get_all_tests():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Test")

    result = cursor.fetchall()
    conn.close()

    return [
        {'test_id': row[0], 'title': row[1], 'created_at': row[2], 'description': row[3], 'subject': row[4],
         'sequence': row[5], 'max_time': row[6]}
        for row in result
    ]

def get_test_detail_for_student(test_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch test details
    cursor.execute("""
        SELECT test_id, title, description, subject, datetime, sequence, max_time
        FROM Test
        WHERE test_id = ?
    """, (test_id,))

    test_row = cursor.fetchone()
    conn.close()

    if not test_row:
        return {}

    return {
        'test_id': test_row['test_id'],
        'title': test_row['title'],
        'description': test_row['description'],
        'subject': test_row['subject'],
        'datetime': test_row['datetime'],
        'sequence': bool(test_row['sequence']),
        'max_time': test_row['max_time']
    }

def get_filled_test_detail_for_student(user_id, test_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch filled test details
    cursor.execute("""
        SELECT filled_test_id, date_time_beginning, date_time_end
        FROM Filled_test
        WHERE user_id = ? AND test_id = ?
    """, (user_id, test_id))

    filled_test_row = cursor.fetchone()
    if not filled_test_row:
        conn.close()
        return {}

    # Calculate score: correct filled questions / total questions
    cursor.execute("""
        SELECT COUNT(*) 
        FROM Filled_question
        WHERE filled_test_id = ? AND is_correct = 1
    """, (filled_test_row['filled_test_id'],))
    correct_answers_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM Question
        WHERE test_id = ?
    """, (test_id,))
    total_questions_count = cursor.fetchone()[0]

    score = correct_answers_count / total_questions_count if total_questions_count else 0

    conn.close()

    return {
        'filled_test_id': filled_test_row['filled_test_id'],
        'date_time_beginning': filled_test_row['date_time_beginning'],
        'date_time_end': filled_test_row['date_time_end'],
        'score': score
    }

def get_questions_for_test(test_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Question.question_id AS id, Question.title, Question.task, Question.help,
               Filled_question.solution, Filled_question.is_correct
        FROM Question
        LEFT JOIN Filled_question ON Question.question_id = Filled_question.question_id
        WHERE Question.test_id = ?
    """, (test_id,))

    questions = [
        {
            'question': {
                'id': row['id'],
                'title': row['title'],
                'task': row['task'],
                'help': row['help']
            },
            'solution': row['solution'],
            'is_correct': row['is_correct']
        }
        for row in cursor.fetchall()
    ]

    conn.close()
    return questions

def calculate_score(test_id, filled_test_id):
    # Calculate the score: correct answers / total questions
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

def create_filled_test(user_id, test_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert a new filled test record with the current timestamp for `date_time_beginning`
    cursor.execute("""
        INSERT INTO Filled_test (test_id, user_id, date_time_beginning)
        VALUES (?, ?, datetime('now'))
    """, (test_id, user_id))

    # Get the newly created filled test ID
    filled_test_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        'filled_test_id': filled_test_id,
        'date_time_beginning': datetime.now(),  # assuming datetime is imported
        'date_time_end': None
    }

def get_test_detail_for_teacher(user_id, test_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Test
        WHERE user_id = ? AND test_id = ?
    """, (user_id, test_id))

    row = cursor.fetchone()
    conn.close()

    return row['test_id'], row['title'], row['datetime'], row['description'], row['subject'], row['sequence'] == True, \
    row['max_time']


def save_test(user_id, title, description, subject, sequence, max_time):
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

def get_test_statistics(test_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name || ' ' || p.surname AS student, 
               (COUNT(CASE WHEN fq.is_correct = 1 THEN 1 END) * 100.0 / COUNT(fq.filled_question_id)) AS success
        FROM Filled_test ft
        JOIN Profile p ON ft.user_id = p.user_id
        JOIN Filled_question fq ON ft.filled_test_id = fq.filled_test_id
        WHERE ft.test_id = ? AND ft.user_id = ?
        GROUP BY p.user_id
    """, (test_id, user_id))
    result = cursor.fetchall()
    conn.close()
    return result