from data.ProfileData import login_user

class Login:
    def login_user(self, email, password):
        user_data = login_user(email, password)

        if user_data is None:
            return {'user_id': None}

        return {
            'token': user_data[0],
            'user_id': user_data[1],
            'name': user_data[2],
            'surname': user_data[3],
            'email': user_data[4],
            'user_type': user_data[5]
        }