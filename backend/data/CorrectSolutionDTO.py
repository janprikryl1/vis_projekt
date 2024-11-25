from data.DBConnection import get_db_connection


def save_correct_solution(question_id, correct_solution_id, correct_solution_text, case_sensitive):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO Correct_solution (correct_solution_id, correct_solution_text, case_sensitive, question_id) 
        VALUES (?, ?, ?, ?)
        """,
        (correct_solution_id, correct_solution_text, case_sensitive,
         question_id)
    )

    conn.commit()
    conn.close()


def get_exists_correct_solution(correct_solution_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT correct_solution_id FROM Correct_solution WHERE correct_solution_id = ?",
                   (correct_solution_id,))
    exists = cursor.fetchone()

    conn.close()
    return exists

def update_correct_solution(correct_solution_id, correct_solution):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE Correct_solution SET correct_solution_text = ?, case_sensitive = ? WHERE correct_solution_id = ?",
        (correct_solution['correct_solution_text'], correct_solution['case_sensitive'], correct_solution_id)
    )

    conn.commit()
    conn.close()

def get_outdated_correct_solutions(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch existing correct solution IDs for the question
    cursor.execute("SELECT correct_solution_id FROM Correct_solution WHERE question_id = ?", (question_id,))
    existing_correct_solution_ids = {row[0] for row in cursor.fetchall()}
    conn.close()

    return existing_correct_solution_ids

def delete_outdated_correct_solution(correct_solution_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Correct_solution WHERE correct_solution_id = ?", (correct_solution_id,))

    conn.commit()
    conn.close()


def get_correct_choices_for_question(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT correct_solution_text, case_sensitive
        FROM Correct_solution
        WHERE question_id = ?
    """, (question_id,))

    conn.close()
    return [
        {
            'correct_solution_text': row[0],
            'case_sensitive': bool(row[1])
        }
        for row in cursor.fetchall()
    ]


def get_correct_solution_for_question(question_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
               SELECT correct_solution_text, case_sensitive
               FROM Correct_solution
               WHERE question_id = ?
           """, (question_id,))
    correct_choices = cursor.fetchall()

    conn.close()
    return correct_choices


def update_filled_question_result(filled_question_id, solution, is_correct):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Filled_question
        SET solution = ?, is_correct = ?
        WHERE filled_question_id = ?
    """, (solution, is_correct, filled_question_id))

    conn.commit()
    conn.close()


def save_filled_question_result(filled_test_id, question_id, solution, is_correct):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Filled_question (filled_test_id, question_id, solution, is_correct)
        VALUES (?, ?, ?, ?)
    """, (filled_test_id, question_id, solution, is_correct))
    filled_question_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return filled_question_id