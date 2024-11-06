from data.TestData import get_filled_tests_for_student, get_created_tests_for_teacher


class LatestTests:
    def get_latest_tests(self, user_id, user_type):
        if user_type == "P":
            return get_filled_tests_for_student(user_id)
        elif user_type == "T":
            return get_created_tests_for_teacher(user_id)
        else:
            return []