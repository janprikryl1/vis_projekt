from data.TestStatisticsDTO import fetch_test_statistics
from domain.BaseService import BaseService


class TestStatisticsService(BaseService):
    def __init__(self, auth_header):
        super().__init__(auth_header)

    def get_test_statistics(self, test_id):
        return fetch_test_statistics(test_id)