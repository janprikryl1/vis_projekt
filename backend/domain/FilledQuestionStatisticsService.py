from data.DBConnection import get_db_connection
from data.ProfileData import get_user_info_by_token


class FilledQuestionStatisticsService:
    def __init__(self, auth_header):
        if not auth_header or not auth_header.startswith("Bearer "):
            self.error = 'Authorization token not provided'
            return

        token = auth_header.split(" ")[1]

        user_data = get_user_info_by_token(token)
        if not user_data:
            self.error = 'Invalid token'
            return

        self.user_id = user_data['user_id']
        self.user_type = user_data['user_type']
        self.error = None

    def get_question_statistics(self, question_id):
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