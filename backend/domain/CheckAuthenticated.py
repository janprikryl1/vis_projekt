from data.ProfileDTO import is_valid_token
from domain.BaseService import BaseService


class CheckAuthenticated(BaseService):
    def __init__(self, auth_header):
        self.token = auth_header.split(" ")[1] if auth_header else None
        super().__init__(auth_header)

    def is_authenticated(self):
        user_id, name, surname, email, user_type = is_valid_token(self.token)
        return {
            'user_id': user_id,
            'name': name,
            'surname': surname,
            'email': email,
            'user_type': user_type
        } if user_id else {
            'user_id': None
        }
