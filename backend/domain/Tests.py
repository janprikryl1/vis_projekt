from data.TestDTO import (
    create_test, update_test, get_test_by_id, delete_test, create_filled_test,
    get_filled_tests_by_user, get_all_tests, get_tests_not_filled_by_user
)
from data.ProfileData import get_user_info_by_token


class TestsService:
    def __init__(self, auth_header):
        token = auth_header.split(" ")[1]
        user_data = get_user_info_by_token(token)
        if not user_data:
            self.error = 'Invalid token'
        else:
            self.user_id = user_data['user_id']
            self.user_type = user_data['user_type']
            self.error = None

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