from hashlib import sha256
from data.DBConnection import get_db_connection


class LoginDTO:
    @staticmethod
    def get_user_by_credentials(email, password):  # Retrieve user data along with their token using email and password.
        # Encrypt the password
        encrypted_password = sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT Tokens.token, Profile.user_id, Profile.name, Profile.surname, Profile.email, Profile.user_type
            FROM Profile
            LEFT JOIN Tokens ON Tokens.user_id = Profile.user_id
            WHERE Profile.email = ? AND Profile.password = ?
        """, (email, encrypted_password))

        user_data = cursor.fetchone()
        conn.close()

        return user_data

    @staticmethod
    def create_token(user_id, token):  # Create a new token for the specified user.
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Tokens (user_id, token)
            VALUES (?, ?)
        """, (user_id, token))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()

        return last_id