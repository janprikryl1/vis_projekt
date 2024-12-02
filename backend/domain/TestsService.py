from data.FilledTestDTO import get_filled_tests_by_user, get_tests_not_filled_by_user
from data.TestDTO import (create_test, update_test, get_test_by_id, delete_test, get_all_tests)
from domain.BaseService import BaseService


class TestsService(BaseService):
    def __init__(self, auth_header):
        super().__init__(auth_header)

    def get_tests(self):
        if self.error:
            return {'error': self.error}

        if self.user_type == "P":  # Student
            filled_tests = get_filled_tests_by_user(self.user_id)
            not_filled_tests = get_tests_not_filled_by_user(self.user_id)
            return {'filled_tests': filled_tests, 'tests': not_filled_tests}

        elif self.user_type == "T":  # Teacher
            created_tests = get_all_tests()  # Adjust to filter by teacher
            return {'tests': created_tests}

        elif self.user_type == "A":  # Admin
            return {'tests': get_all_tests()}

        return {'error': 'Invalid user type'}

    def create_test(self, title, description, subject, sequence, max_time):
        if self.error or self.user_type != "T":
            return {'error': 'Permission denied'}
        test_id = create_test(self.user_id, title, description, subject, sequence, max_time)
        return {'test_id': test_id}

    def update_test(self, test_id, title, description, subject, sequence, max_time):
        if self.error or self.user_type != "T":
            return {'error': 'Permission denied'}
        update_test(self.user_id, test_id, title, description, subject, sequence, max_time)
        return {'status': 'success'}

    def get_test_detail(self, test_id):
        if self.error:
            return {'error': self.error}
        test = get_test_by_id(test_id)
        if not test:
            return {'error': 'Test not found'}
        return test

    def delete_test(self, test_id):
        if self.error or self.user_type != "T":
            return {'error': 'Permission denied'}
        delete_test(test_id)
        return {'status': 'deleted'}