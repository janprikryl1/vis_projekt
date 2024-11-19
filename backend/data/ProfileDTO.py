from data.DBConnection import get_db_connection


class ProfileDTO:
    @staticmethod
    def get(email):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Profile WHERE email = ?", (email,))
        conn.close()
        return cursor.fetchall()

    @staticmethod
    def create(name, surname, email, encrypted_password, user_type='P'):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
                    INSERT INTO Profile (name, surname, email, password, user_type)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, surname, email, encrypted_password, user_type))
        conn.close()
        return cursor.lastrowid