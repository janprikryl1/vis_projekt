from data.DBConnection import get_db_connection


def save_correct_solution(question_id, correct_solution):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Correct_solution (correct_solution_id, correct_solution_text, case_sensitive, question_id) VALUES (?, ?, ?, ?)",
                   (correct_solution['correct_solution_id'], correct_solution['correct_solution_text'], correct_solution['case_sensitive'], question_id))
    conn.commit()
    conn.close()


def update_correct_solution(question_id, correct_solution_id, correct_solution):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if correct solution exists
    cursor.execute("SELECT correct_solution_id FROM Correct_solution WHERE correct_solution_id = ?",
                   (correct_solution_id,))
    exists = cursor.fetchone()

    if exists: # Update existing correct solution
        cursor.execute(
            "UPDATE Correct_solution SET correct_solution_text = ?, case_sensitive = ? WHERE correct_solution_id = ?",
            (correct_solution['correct_solution_text'], correct_solution['case_sensitive'], correct_solution_id)
        )
    else: # Insert new correct solution
        cursor.execute(
            """
            INSERT INTO Correct_solution (correct_solution_id, correct_solution_text, case_sensitive, question_id) 
            VALUES (?, ?, ?, ?)
            """,
            (correct_solution_id, correct_solution['correct_solution_text'], correct_solution['case_sensitive'], question_id)
        )

    conn.commit()
    conn.close()

def delete_outdated_correct_solutions(question_id, current_correct_solution_ids):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch existing correct solution IDs for the question
    cursor.execute("SELECT correct_solution_id FROM Correct_solution WHERE question_id = ?", (question_id,))
    existing_correct_solution_ids = {row[0] for row in cursor.fetchall()}

    # Identify correct solution IDs to delete
    correct_solution_ids_to_delete = existing_correct_solution_ids - current_correct_solution_ids
    for correct_solution_id in correct_solution_ids_to_delete:
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

    correct_choices = [
        {
            'correct_solution_text': row[0],
            'case_sensitive': bool(row[1])
        }
        for row in cursor.fetchall()
    ]

    conn.close()
    return correct_choices

