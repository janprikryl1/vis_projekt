from data.FilledQuestionDTO import FilledQuestionDTO
from data.FilledTestDTO import get_filled_tests_by_user, get_tests_not_filled_by_user, create_filled_test
from data.TestDTO import (create_test, update_test, get_all_tests)
from data.QuestionDTO import save_question, update_question, delete_outdated_questions, get_question_exists, get_test_question_ids
from data.CorrectSolutionDTO import (
    save_correct_solution,
    update_correct_solution,
    get_outdated_correct_solutions,
    delete_outdated_correct_solution,
    get_correct_solution_for_question,
    get_exists_correct_solution, update_filled_question_result, save_filled_question_result,
)
from domain.BaseService import BaseService


class TestService(BaseService):
    def __init__(self, auth_header):
        super().__init__(auth_header)

    def is_teacher(self):
        return self.user_type == "T"

    def save_new_test(self, title, description, subject, sequence, max_time, questions):
        if not self.is_teacher():
            return {'error': 'Permission denied'}

        # Create a new test
        test_id = create_test(self.user_id, title, description, subject, sequence, max_time)

        # Save questions and their correct solutions
        for question in questions:
            save_question(test_id, question)
            for correct_solution in question['corrects']:
                save_correct_solution(question['id'], correct_solution['correct_solution_id'], correct_solution['correct_solution_text'], correct_solution['case_sensitive'])

        return {'test_id': test_id}

    def update_test(self, test_id, title, description, subject, sequence, max_time, questions):
        if not self.is_teacher():
            return {'error': 'Permission denied'}

        # Update the test details
        update_test(self.user_id, test_id, title, description, subject, sequence, max_time)

        # Manage questions and their correct solutions
        current_question_ids = {question.get('id') for question in questions if question.get('id')}
        existing_question_ids = get_test_question_ids(test_id)
        question_ids_to_delete = existing_question_ids - current_question_ids
        for question_id in question_ids_to_delete:
            delete_outdated_questions(question_id)

        for question in questions:
            question_id = question.get('id')

            # Insert or update existing question
            if question_id and get_question_exists(question_id):
                update_question(test_id, question_id, question)
            else:
                save_question(test_id, question)

            # Question_id has to be valid before managing correct solutions
            if not question_id:
                raise ValueError(f"Invalid question_id for question: {question}")

            # Manage correct solutions
            current_correct_solution_ids = {
                correct.get('correct_solution_id') for correct in question['corrects'] if
                correct.get('correct_solution_id')
            }
            correct_solution_ids_to_delete = get_outdated_correct_solutions(question_id)
            correct_solution_ids_to_delete = correct_solution_ids_to_delete - current_correct_solution_ids
            for correct_solution_id in correct_solution_ids_to_delete:
                delete_outdated_correct_solution(correct_solution_id)

            for correct_solution in question['corrects']:
                if 'correct_solution_id' in correct_solution:
                    if get_exists_correct_solution(correct_solution['correct_solution_id']):
                        update_correct_solution(correct_solution['correct_solution_id'], correct_solution)
                    else:
                        save_correct_solution(question_id, correct_solution['correct_solution_id'], correct_solution['correct_solution_text'], correct_solution['case_sensitive'])
                else:
                    save_correct_solution(question_id, correct_solution['correct_solution_id'], correct_solution['correct_solution_text'], correct_solution['case_sensitive'])

        return {'status': 'success'}

    def evaluate_test(self, question_id, solution):
        correct_choices = get_correct_solution_for_question(question_id)

        # Compare solution with correct choices
        for correct_choice in correct_choices:
            correct_text, case_sensitive = correct_choice
            if case_sensitive:
                if solution == correct_text:
                    return True
            else:
                if solution.lower() == correct_text.lower():
                    return True

        return False

    def get_filled_tests(self):
        if self.user_type == "P":
            return get_filled_tests_by_user(self.user_id)
        elif self.user_type == "T":
            return get_all_tests()
        else:
            return {'error': 'Invalid user type'}

    def get_unfilled_tests(self):
        if self.user_type != "P":
            return {'error': 'Permission denied'}
        return get_tests_not_filled_by_user(self.user_id)

    def create_filled_test(self, test_id):
        if self.user_type != "P":
            return {'error': 'Permission denied'}
        return create_filled_test(self.user_id, test_id)

    def evaulate(self, question_id, solution, filled_test_id):
        is_correct = self.evaluate_test(question_id, solution)

        # Get or create a filled question record
        existing_filled_question_id = FilledQuestionDTO.get_filled_question_id(filled_test_id, question_id)
        if existing_filled_question_id:
            update_filled_question_result(existing_filled_question_id, solution, is_correct)
            filled_question_id = existing_filled_question_id
        else:
            filled_question_id = save_filled_question_result(filled_test_id, question_id, solution, is_correct)
        return filled_question_id, is_correct


