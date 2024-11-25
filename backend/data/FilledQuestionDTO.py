from data.DBConnection import get_db_connection

class FilledQuestionDTO:
    @staticmethod
    def get_statistics_by_question_id(question_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name || ' ' || p.surname AS user, 
                   fq.solution, 
                   fq.is_correct
            FROM Filled_question fq
            JOIN Filled_test ft ON fq.filled_test_id = ft.filled_test_id
            JOIN Profile p ON ft.user_id = p.user_id
            WHERE fq.question_id = ?
        """, (question_id,))
        result = cursor.fetchall()
        conn.close()
        return result


    @staticmethod
    def get_filled_question_id(filled_test_id, question_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get ID of the filled question
        cursor.execute("""
            SELECT filled_question_id
            FROM Filled_question
            WHERE filled_test_id = ? AND question_id = ?
        """, (filled_test_id, question_id))
        row = cursor.fetchone()

        conn.close()
        return row[0] if row else None

    @staticmethod
    def fetch_questions_for_test(test_id, user_type):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                q.question_id AS id, 
                q.title, 
                q.task, 
                q.help,
                fq.solution, 
                fq.is_correct,
                cs.correct_solution_id, 
                cs.correct_solution_text, 
                cs.case_sensitive
            FROM Question q
            LEFT JOIN Filled_question fq ON q.question_id = fq.question_id
            LEFT JOIN Correct_solution cs ON q.question_id = cs.question_id
            WHERE q.test_id = ?
            ORDER BY q.question_id, cs.correct_solution_id
        """, (test_id,))

        questions = {}
        for row in cursor.fetchall():
            question_id = row[0]
            if question_id not in questions:
                questions[question_id] = {
                    'id': question_id,
                    'title': row[1],
                    'task': row[2],
                    'help': row[3],
                    'solution': row[4],
                    'is_correct': row[5],
                    user_type == "T" and 'corrects': []
                }

            # Add correct solutions to the question
            if row[6] and user_type == "T":  # If correct solution exists
                questions[question_id]['corrects'].append({
                    'correct_solution_id': row[6],
                    'correct_solution_text': row[7],
                    'case_sensitive': row[8]
                })

        conn.close()
        return list(questions.values())