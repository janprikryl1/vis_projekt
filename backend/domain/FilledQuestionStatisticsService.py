from data.FilledQuestionDTO import FilledQuestionDTO
from domain.BaseService import BaseService


class FilledQuestionStatisticsService(BaseService):
    def __init__(self, auth_header):
        super().__init__(auth_header)

    def get_question_statistics(self, question_id):
        if self.error:
            return {"error": self.error}

        statistics = FilledQuestionDTO.get_statistics_by_question_id(question_id)
        if not statistics:
            return {"error": "No statistics found for the given question"}

        return [
            {"user": row["user"], "solution": row["solution"], "is_correct": row["is_correct"]}
            for row in statistics
        ]
