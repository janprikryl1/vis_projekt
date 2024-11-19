from datetime import datetime

from data.ProfileData import get_user_info_by_token
from data.TestDTO import (
    get_test_by_id,
    create_filled_test,
    get_filled_tests_by_user,
    get_tests_not_filled_by_user,
    get_all_tests
)
from data.DBConnection import get_db_connection


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
        if self.error:
            return {'error': self.error}

        if self.user_type == "P":  # Student
            return self._get_test_detail_for_student(test_id)
        elif self.user_type == "T":  # Teacher
            return self._get_test_detail_for_teacher(test_id)
        else:
            return {'error': 'Invalid user type'}

    def _get_test_detail_for_student(self, test_id):
        # Use TestDTO to fetch test details
        test_detail = get_test_by_id(test_id)
        if not test_detail:
            return {}

        # Get or create filled test details
        filled_test_detail = self._get_or_create_filled_test_detail(test_id)

        # Fetch questions and calculate score
        questions = self._fetch_questions_for_test(test_id)
        score = self._calculate_score(test_id, filled_test_detail['filled_test_id'])
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

    def _get_test_detail_for_teacher(self, test_id):
        test_detail = get_test_by_id(test_id)
        if not test_detail or test_detail['user_id'] != self.user_id:
            return {'error': 'Test not found or permission denied'}

        questions = self._fetch_questions_for_test(test_id)

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
        conn = get_db_connection()
        cursor = conn.cursor()

        # Try fetching filled test detail
        cursor.execute("""
            SELECT filled_test_id, date_time_beginning, date_time_end
            FROM Filled_test
            WHERE user_id = ? AND test_id = ?
        """, (self.user_id, test_id))
        row = cursor.fetchone()

        # If not found, create a new one
        if not row:
            filled_test_id = create_filled_test(self.user_id, test_id)
            return {
                'filled_test_id': filled_test_id,
                'date_time_beginning': datetime.now(),
                'date_time_end': None
            }

        conn.close()
        return {
            'filled_test_id': row[0],
            'date_time_beginning': row[1],
            'date_time_end': row[2]
        }

    def _fetch_questions_for_test(self, test_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                q.question_id AS id, 
                q.title, 
                q.task, 
                q.help,
                fq.solution, 
                fq.is_correct,
                cs.correct_solution_id, 
                cs.correct_solution_text, 
                cs.case_sensitive
            FROM Question q
            LEFT JOIN Filled_question fq ON q.question_id = fq.question_id
            LEFT JOIN Correct_solution cs ON q.question_id = cs.question_id
            WHERE q.test_id = ?
            ORDER BY q.question_id, cs.correct_solution_id
        """, (test_id,))

        # Zpracování dat do požadované struktury
        questions = {}
        for row in cursor.fetchall():
            question_id = row[0]
            if question_id not in questions:
                questions[question_id] = {
                    'id': question_id,
                    'question': row[1],
                    'task': row[2],
                    'help': row[3],
                    'solution': row[4],
                    'is_correct': row[5],
                    self.user_type == "T" and 'corrects': []  # Inicializace prázdného pole pro správné odpovědi
                }

            # Přidání správných možností (correct solutions) k otázce
            if row[6] and self.user_type == "T":  # Pokud existuje správná možnost
                questions[question_id]['corrects'].append({
                    'correct_solution_id': row[6],
                    'correct_solution_text': row[7],
                    'case_sensitive': row[8]
                })

        conn.close()

        # Vrácení seznamu otázek
        return list(questions.values())

    def _calculate_score(self, test_id, filled_test_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Count of correct filled questions for this filled test
        cursor.execute("""
            SELECT COUNT(*)
            FROM Filled_question
            WHERE filled_test_id = ? AND is_correct = 1
        """, (filled_test_id,))
        correct_count = cursor.fetchone()[0]

        # Total number of questions in the test
        cursor.execute("""
            SELECT COUNT(*)
            FROM Question
            WHERE test_id = ?
        """, (test_id,))
        total_questions = cursor.fetchone()[0]

        conn.close()
        return (correct_count / total_questions) * 100 if total_questions > 0 else 0