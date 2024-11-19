from data.TokenDTO import TokenDTO
from data.FilledQuestionDTO import FilledQuestionDTO

class FilledQuestionStatisticsService:
    def __init__(self, auth_header):
        self.error = None
        self.user_id = None
        self.user_type = None

        if not auth_header or not auth_header.startswith("Bearer "):
            self.error = 'Authorization token not provided'
            return

        token = auth_header.split(" ")[1]

        user_data = TokenDTO.get_user_info_by_token(token)
        if not user_data:
            self.error = 'Invalid token'
            return

        self.user_id = user_data['user_id']
        self.user_type = user_data['user_type']

    def get_question_statistics(self, question_id):
        if self.error:
            return {"error": self.error}

        statistics = FilledQuestionDTO.get_statistics_by_question_id(question_id)
        if not statistics:
            return {"error": "No statistics found for the given question"}

        # Transformace dat do čitelného formátu
        return [
            {"user": row["user"], "solution": row["solution"], "is_correct": row["is_correct"]}
            for row in statistics
        ]