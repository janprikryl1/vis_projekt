from data.CorrectSolutionData import save_correct_solution, update_correct_solution, delete_outdated_correct_solutions, \
    get_correct_choices_for_question
from data.ProfileData import get_user_info_by_token
from data.QuestionData import save_question, update_question, delete_outdated_questions
from data.TestData import save_test, update_test, get_test_statistics, get_filled_test_detail_for_student, \
    calculate_score, get_questions_for_test, create_filled_test


class TestService:
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

    def is_teacher(self):
        return self.user_type == "T"

    def save_new_test(self, title, description, subject, sequence, max_time, questions):
        test_id = save_test(self.user_id, title, description, subject, sequence, max_time)
        for question in questions:
            question_id = save_question(test_id, question)
            for correct_solution in question['corrects']:
                save_correct_solution(question_id, correct_solution)
        return test_id

    def update_test(self, test_id, title, description, subject, sequence, max_time, questions):
        update_test(self.user_id, test_id, title, description, subject, sequence, max_time)
        current_question_ids = {question['id'] for question in questions}
        delete_outdated_questions(test_id, current_question_ids)
        for question in questions:
            question_id = update_question(test_id, question.get('id'), question)
            current_correct_solution_ids = {correct.get('correct_solution_id') for correct in question['corrects']}
            delete_outdated_correct_solutions(question_id, current_correct_solution_ids)
            for correct_solution in question['corrects']:
                update_correct_solution(question_id, correct_solution.get('correct_solution_id'), correct_solution)

    def evaluate_test(self, question_id, solution):
        correct_choices = get_correct_choices_for_question(question_id)
        for correct_choice in correct_choices:
            correct_text = correct_choice['correct_solution_text']
            if correct_choice['case_sensitive']:
                if solution == correct_text:
                    return True
            else:
                if solution.lower() == correct_text.lower():
                    return True
        return False

    def get_test_statistics(self, test_id, user_id):
        return get_test_statistics(test_id, user_id)

    def get_filled_test_details(self, user_id, test_id):
        return get_filled_test_detail_for_student(user_id, test_id)

    def calculate_score(self, test_id, filled_test_id):
        return calculate_score(test_id, filled_test_id)

    def get_questions(self, test_id):
        return get_questions_for_test(test_id)

    def create_filled_test(self, user_id, test_id):
        return create_filled_test(user_id, test_id)
