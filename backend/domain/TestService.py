from data.CorrectSolutionData import save_correct_solution, update_correct_solution, delete_outdated_correct_solutions, \
    get_correct_choices_for_question
from data.ProfileData import get_user_info_by_token
from data.DBConnection import get_db_connection
from data.QuestionData import save_question, update_question, delete_outdated_questions
from data.TestData import save_test, update_test


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
            save_question(test_id, question)
            for correct_solution in question['corrects']:
                save_correct_solution(question['id'], correct_solution)
        return test_id

    def update_test(self, test_id, title, description, subject, sequence, max_time, questions):
        update_test(self.user_id, test_id, title, description, subject, sequence, max_time)
        current_question_ids = {question['id'] for question in questions}
        delete_outdated_questions(test_id, current_question_ids)
        for question in questions:
            update_question(test_id, question.get('id'), question)
            current_correct_solution_ids = {correct.get('correct_solution_id') for correct in question['corrects']}
            delete_outdated_correct_solutions(question['id'], current_correct_solution_ids)
            for correct_solution in question['corrects']:
                update_correct_solution(question['id'], correct_solution.get('correct_solution_id'), correct_solution)

    def evaluate_test(self, question_id, solution):
        # Retrieve correct choices for the question
        correct_choices = get_correct_choices_for_question(question_id)

        # Determine if the provided solution matches any correct choice
        for correct_choice in correct_choices:
            correct_text = correct_choice['correct_solution_text']
            if correct_choice['case_sensitive']:
                if solution == correct_text:
                    return True
            else:
                if solution.lower() == correct_text.lower():
                    return True

        return False

    def filled_question_exists(self, test_id, question_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT filled_question_id
            FROM Filled_question
            WHERE filled_test_id = ? AND question_id = ?
        """, (test_id, question_id))

        filled_question = cursor.fetchone()
        conn.close()
        print(filled_question)
        return filled_question[0] if filled_question else None

    def update_filled_question_result(self, filled_question_id, solution, is_correct):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Filled_question
            SET solution = ?, is_correct = ?
            WHERE filled_question_id = ?
        """, (solution, is_correct, filled_question_id))

        conn.commit()
        conn.close()

    def save_filled_question_result(self, test_id, question_id, solution, is_correct):
        filled_question_id = self.filled_question_exists(test_id, question_id)

        if filled_question_id:
            self.update_filled_question_result(filled_question_id, solution, is_correct)
        else:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Filled_question (filled_test_id, question_id, solution, is_correct)
                VALUES (?, ?, ?, ?)
            """, (test_id, question_id, solution, is_correct))

            filled_question_id = cursor.lastrowid
            conn.commit()
            conn.close()

        return filled_question_id