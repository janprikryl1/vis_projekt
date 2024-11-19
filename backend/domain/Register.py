import os
from hashlib import sha256
from data.ProfileDTO import ProfileDTO
from data.TokenDTO import TokenDTO


class Register:
    def register_user(self, name, surname, email, password, user_type='P'):
        if self.email_exists(email):
            return {'status': 'error', 'message': 'Email is already in use'}

        user_id, token = self.create_user(name, surname, email, password, user_type)

        return {
            'status': 'success',
            'token': token,
            'user_id': user_id,
            'name': name,
            'surname': surname,
            'email': email,
            'user_type': "Pupil" if user_type == "P" else "Teacher" if user_type == "T" else "Admin"
        } if user_id else {'status': 'error', 'message': 'Registration failed'}

    def email_exists(self, email):
        return ProfileDTO.get(email) > 0

    def create_user(self, name, surname, email, password, user_type='P'):
        encrypted_password = sha256(password.encode()).hexdigest()
        user_id = ProfileDTO.create(name, surname, email, encrypted_password, user_type)

        token = os.urandom(32).hex()
        TokenDTO.create(token)
        return user_id, token