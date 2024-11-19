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

        # Získání ID vyplněné otázky
        cursor.execute("""
            SELECT filled_question_id
            FROM Filled_question
            WHERE filled_test_id = ? AND question_id = ?
        """, (filled_test_id, question_id))
        row = cursor.fetchone()

        conn.close()
        return row[0] if row else None