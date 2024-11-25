from data.FilledTestDTO import get_filled_tests_by_user
from data.TestDTO import get_all_tests
from domain.BaseService import BaseService


class LatestTests(BaseService):
    def __init__(self, auth_header):
        super().__init__(auth_header)

    def get_latest_tests(self):
        if self.error:
            return {'error': self.error}

        if self.user_type == "P":  # Student
            return self._get_latest_tests_for_student()
        elif self.user_type == "T":  # Teacher
            return self._get_latest_tests_for_teacher()
        else:
            return {'error': 'Invalid user type'}

    def _get_latest_tests_for_student(self):
        filled_tests = get_filled_tests_by_user(self.user_id)
        return {'latest_tests': filled_tests}

    def _get_latest_tests_for_teacher(self):
        created_tests = get_all_tests()
        return {'latest_tests': created_tests}