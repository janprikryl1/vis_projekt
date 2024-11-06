from data.ProfileData import is_valid_token


class CheckAuthenticated:
    def is_authenticated(self, token):
        user_id, name, surname, email, user_type = is_valid_token(token)
        return {'user_id': user_id, 'name':name, 'surname':surname, 'email': email, 'user_type':user_type} if user_id else {'user_id': None}
