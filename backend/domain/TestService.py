from data.FilledQuestionDTO import FilledQuestionDTO
from data.ProfileData import get_user_info_by_token
from data.DBConnection import get_db_connection
from data.TestDTO import (
    create_test,
    update_test,
    create_filled_test,
    get_filled_tests_by_user,
    get_all_tests,
    get_tests_not_filled_by_user
)
from data.QuestionData import save_question, update_question, delete_outdated_questions
from data.CorrectSolutionData import save_correct_solution, update_correct_solution, delete_outdated_correct_solutions


class TestService:
    def __init__(self, auth_header):
        self.error = None

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

    def is_teacher(self):
        return self.user_type == "T"

    def save_new_test(self, title, description, subject, sequence, max_time, questions):
        if not self.is_teacher():
            return {'error': 'Permission denied'}

        # Create a new test
        test_id = create_test(self.user_id, title, description, subject, sequence, max_time)

        # Save questions and their correct solutions
        for question in questions:
            print(question)
            save_question(test_id, question)
            for correct_solution in question['corrects']:
                save_correct_solution(question['id'], correct_solution)

        return {'test_id': test_id}

    def update_test(self, test_id, title, description, subject, sequence, max_time, questions):
        if not self.is_teacher():
            return {'error': 'Permission denied'}

        # Update the test details
        update_test(self.user_id, test_id, title, description, subject, sequence, max_time)

        # Manage questions and their correct solutions
        current_question_ids = {question.get('id') for question in questions if question.get('id')}
        delete_outdated_questions(test_id, current_question_ids)

        for question in questions:
            question_id = question.get('id')

            # Insert or update question
            if question_id:
                update_question(test_id, question_id, question)
            else:
                save_question(test_id, question)

            # Ensure question_id is valid before managing correct solutions
            if not question_id:
                raise ValueError(f"Invalid question_id for question: {question}")

            # Manage correct solutions
            current_correct_solution_ids = {
                correct.get('correct_solution_id') for correct in question['corrects'] if
                correct.get('correct_solution_id')
            }
            delete_outdated_correct_solutions(question_id, current_correct_solution_ids)

            for correct_solution in question['corrects']:
                if 'correct_solution_id' in correct_solution:
                    update_correct_solution(question_id, correct_solution['correct_solution_id'], correct_solution)
                else:
                    save_correct_solution(question_id, correct_solution)

        return {'status': 'success'}

    def evaluate_test(self, question_id, solution):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get correct choices for the question
        cursor.execute("""
            SELECT correct_solution_text, case_sensitive
            FROM Correct_solution
            WHERE question_id = ?
        """, (question_id,))
        correct_choices = cursor.fetchall()

        conn.close()

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
        # Ověření odpovědi
        is_correct = self.evaluate_test(question_id, solution)

        # Získání nebo vytvoření záznamu o vyplněné otázce
        existing_filled_question_id = FilledQuestionDTO.get_filled_question_id(filled_test_id, question_id)
        if existing_filled_question_id:
            self.update_filled_question_result(existing_filled_question_id, solution, is_correct)
            filled_question_id = existing_filled_question_id
        else:
            filled_question_id = self.save_filled_question_result(filled_test_id, question_id, solution,
                                                                          is_correct)
        return filled_question_id, is_correct

    def update_filled_question_result(self, filled_question_id, solution, is_correct):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Aktualizace vyplněné otázky
        cursor.execute("""
            UPDATE Filled_question
            SET solution = ?, is_correct = ?
            WHERE filled_question_id = ?
        """, (solution, is_correct, filled_question_id))

        conn.commit()
        conn.close()

    def save_filled_question_result(self, filled_test_id, question_id, solution, is_correct):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Vložení nové vyplněné otázky
        cursor.execute("""
            INSERT INTO Filled_question (filled_test_id, question_id, solution, is_correct)
            VALUES (?, ?, ?, ?)
        """, (filled_test_id, question_id, solution, is_correct))
        filled_question_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return filled_question_id