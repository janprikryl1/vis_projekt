from data.ProfileData import get_user_info_by_token
from data.QuestionData import get_test_questions
from data.TestData import get_filled_test_detail_for_student, get_test_detail_for_teacher, get_test_detail_for_student, \
    get_questions_for_test, create_filled_test, calculate_score


class TestDetailService:
    def __init__(self, auth_header):
        token = auth_header.split(" ")[1]

        user_data = get_user_info_by_token(token)
        if not user_data:
            self.error = 'Invalid token'
        else:
            self.user_id = user_data['user_id']
            self.user_type = user_data['user_type']
            self.error = None

    def get_test_detail(self, test_id):
        if self.user_type == "P":
            test_detail = get_test_detail_for_student(test_id)
            filled_test_detail = get_filled_test_detail_for_student(self.user_id, test_id)

            if not test_detail:
                return {}

            if not filled_test_detail:
                filled_test_detail = create_filled_test(self.user_id, test_id)

            questions = get_questions_for_test(test_id)
            score = calculate_score(test_id, filled_test_detail['filled_test_id'])

            return {
                'filled_test_id': filled_test_detail['filled_test_id'],
                'date_time_beginning': filled_test_detail['date_time_beginning'],
                'date_time_end': filled_test_detail['date_time_end'],
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
        elif self.user_type == "T":
            test_id, title, created_at, description, subject, sequence, max_time = get_test_detail_for_teacher(self.user_id, test_id)
            questions = get_test_questions(test_id)
            return {'test_id': test_id, 'test_title': title, 'created_at': created_at, 'description': description, 'subject': subject, 'sequence': sequence, 'max_time': max_time, 'questions':questions}
