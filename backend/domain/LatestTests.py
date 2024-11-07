from data.TestData import get_filled_tests_for_student, get_created_tests_for_teacher
from data.ProfileData import get_user_info_by_token

class LatestTests:
    def __init__(self, auth_header):
        if not auth_header or not auth_header.startswith("Bearer "):
            self.error = 'Authorization token not provided'

        token = auth_header.split(" ")[1]

        user_data = get_user_info_by_token(token)
        if not user_data:
            self.error = 'Invalid token'

        self.user_id = user_data['user_id']
        self.user_type = user_data['user_type']
        self.error = None

    def get_latest_tests(self):
        if self.user_type == "P":
            return get_filled_tests_for_student(self.user_id)
        elif self.user_type == "T":
            return get_created_tests_for_teacher(self.user_id)
        else:
            return []