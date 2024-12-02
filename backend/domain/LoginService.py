from hashlib import sha256

from data.LoginDTO import LoginDTO


class LoginService:
    @staticmethod
    def login_user(email, password):
        user_data = LoginDTO.get_user_by_credentials(email, sha256(password.encode()).hexdigest())

        if user_data:
            token, user_id, name, surname, email, user_type = user_data
            return {
                'token': token,
                'user_id': user_id,
                'name': name,
                'surname': surname,
                'email': email,
                'user_type': 'Pupil' if user_type == 'P' else 'Teacher' if user_type == 'T' else 'Admin'
            }

        return None
