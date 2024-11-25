from datetime import datetime
from data.FilledQuestionDTO import FilledQuestionDTO
from data.FilledTestDTO import get_filled_test_for_user_details, create_filled_test, calculate_score
from data.TestDTO import get_test_by_id
from domain.BaseService import BaseService


class TestDetailService(BaseService):
    def __init__(self, auth_header):
        super().__init__(auth_header)

    def get_test_detail(self, test_id):
        if self.error:
            return {'error': self.error}

        if self.user_type == "P":  # Student
            return self._get_test_detail_for_student(test_id)
        elif self.user_type == "T":  # Teacher
            return self._get_test_detail_for_teacher(test_id)
        else:
            return {'error': 'Invalid user type'}

    def _get_test_detail_for_student(self, test_id):
        test_detail = get_test_by_id(test_id)
        if not test_detail:
            return {}

        filled_test_detail = self._get_or_create_filled_test_detail(test_id)

        questions = FilledQuestionDTO.fetch_questions_for_test(test_id, self.user_type)
        score = calculate_score(test_id, filled_test_detail['filled_test_id'])
        return {
            'filled_test_id': filled_test_detail['filled_test_id'],
            'date_time_beginning': filled_test_detail['date_time_beginning'],
            'score': score,
            'test': {
                'test_id': test_detail['test_id'],
                'title': test_detail['title'],
                'description': test_detail['description'],
                'subject': test_detail['subject'],
                'datetime': test_detail['datetime'],
                'sequence': test_detail['sequence'],
                'max_time': test_detail['max_time'],
                'questions': questions
            }
        }

    def _get_test_detail_for_teacher(self, test_id):
        test_detail = get_test_by_id(test_id)
        if not test_detail or test_detail['user_id'] != self.user_id:
            return {'error': 'Test not found or permission denied'}

        questions = FilledQuestionDTO.fetch_questions_for_test(test_id, self.user_type)

        return {
            'test_id': test_detail['test_id'],
            'test_title': test_detail['title'],
            'created_at': test_detail['datetime'],
            'description': test_detail['description'],
            'subject': test_detail['subject'],
            'sequence': test_detail['sequence'],
            'max_time': test_detail['max_time'],
            'questions': questions
        }

    def _get_or_create_filled_test_detail(self, test_id):
        filled_test_detail = get_filled_test_for_user_details(self.user_id, test_id)

        # If not found, create a new one
        if not filled_test_detail:
            filled_test_id = create_filled_test(self.user_id, test_id)
            return {
                'filled_test_id': filled_test_id,
                'date_time_beginning': datetime.now()
            }

        return {
            'filled_test_id': filled_test_detail[0],
            'date_time_beginning': filled_test_detail[1]
        }