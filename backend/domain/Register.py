from data.ProfileData import email_exists, create_user


class Register:
    def register_user(self, name, surname, email, password, user_type='P'):
        if email_exists(email):
            return {'status': 'error', 'message': 'Email is already in use'}

        user_id, token = create_user(name, surname, email, password, user_type)

        return {
            'status': 'success',
            'token': token,
            'user_id': user_id,
            'name': name,
            'surname': surname,
            'email': email,
            'user_type': "Pupil" if user_type == "P" else "Teacher" if user_type == "T" else "Admin"
        } if user_id else {'status': 'error', 'message': 'Registration failed'}