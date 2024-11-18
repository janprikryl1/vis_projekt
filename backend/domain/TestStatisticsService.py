from data.ProfileData import get_user_info_by_token
from data.TestStatisticsData import fetch_test_statistics


class TestStatisticsService:
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

    def get_test_statistics(self, test_id):
        return fetch_test_statistics(test_id)