from data.DBConnection import get_db_connection


class TokenDTO:
    @staticmethod
    def get(token):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Tokens WHERE token = ?", (token,))
        conn.close()

        return cursor.fetchall()

    @staticmethod
    def create(user_id, token):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
                    INSERT INTO Tokens (user_id, token)
                    VALUES (?, ?)
                """, (user_id, token))
        conn.commit()
        conn.close()
        return cursor.lastrowid

    @staticmethod
    def get_user_info_by_token(token):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
                SELECT t.user_id, p.user_type
                FROM Tokens t
                JOIN Profile p ON t.user_id = p.user_id
                WHERE t.token = ?
            """, (token,))
        result = cursor.fetchone()
        conn.close()
        return result