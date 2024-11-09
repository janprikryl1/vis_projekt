from data.DBConnection import get_db_connection


def save_question(test_id, question):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Question (question_id, title, task, help, test_id) VALUES (?,?, ?, ?, ?)",
                   (question['id'], question['title'], question['task'], question['help'], test_id))
    conn.commit()
    conn.close()


def update_question(test_id, question_id, question):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if question exists
    cursor.execute("SELECT question_id FROM Question WHERE question_id = ?", (question_id,))
    exists = cursor.fetchone()

    if exists:
        # Update existing question
        cursor.execute(
            "UPDATE Question SET title = ?, task = ?, help = ?, test_id = ? WHERE question_id = ?",
            (question['title'], question['task'], question['help'], test_id, question_id)
        )
    else:
        # Insert new question
        cursor.execute(
            "INSERT INTO Question (question_id, title, task, help, test_id) VALUES (?, ?, ?, ?, ?)",
            (question_id, question['title'], question['task'], question['help'], test_id)
        )

    conn.commit()
    conn.close()


def delete_outdated_questions(test_id, current_question_ids):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT question_id FROM Question WHERE test_id = ?", (test_id,))
    existing_question_ids = {row[0] for row in cursor.fetchall()}

    question_ids_to_delete = existing_question_ids - current_question_ids
    for question_id in question_ids_to_delete:
        cursor.execute("DELETE FROM Correct_solution WHERE question_id = ?", (question_id,))
        cursor.execute("DELETE FROM Question WHERE question_id = ?", (question_id,))

    conn.commit()
    conn.close()


def get_test_questions(test_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch questions along with their correct choices for the given test ID
    cursor.execute("""
        SELECT q.question_id, q.title, q.task, q.help, q.test_id,
               c.correct_solution_id, c.correct_solution_text, c.case_sensitive
        FROM Question q
        LEFT JOIN Correct_solution c ON q.question_id = c.question_id
        WHERE q.test_id = ?
    """, (test_id,))

    rows = cursor.fetchall()
    conn.close()

    # Process data to organize questions and their correct choices
    questions = {}
    for row in rows:
        question_id = row[0]
        if question_id not in questions:
            questions[question_id] = {
                "id": question_id,
                "title": row[1],
                "task": row[2],
                "help": row[3],
                "test_id": row[4],
                "corrects": []
            }

        # Append correct choice if it exists
        correct_solution_id = row[5]
        if correct_solution_id:
            questions[question_id]["corrects"].append({
                "correct_solution_id": correct_solution_id,
                "correct_solution_text": row[6],
                "case_sensitive": row[7]
            })

    # Convert the dictionary to a list of questions
    return list(questions.values())