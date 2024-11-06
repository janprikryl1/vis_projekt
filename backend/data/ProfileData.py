from hashlib import sha256
import os
from data.DBConnection import get_db_connection


def email_exists(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Profile WHERE email = ?", (email,))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists


def create_user(name, surname, email, password, user_type='P'):
    conn = get_db_connection()
    cursor = conn.cursor()

    encrypted_password = sha256(password.encode()).hexdigest()

    cursor.execute("""
        INSERT INTO Profile (name, surname, email, password, user_type)
        VALUES (?, ?, ?, ?, ?)
    """, (name, surname, email, encrypted_password, user_type))

    user_id = cursor.lastrowid

    token = os.urandom(32).hex()
    cursor.execute("INSERT INTO Tokens (user_id, token) VALUES (?, ?)", (user_id, token))

    conn.commit()
    conn.close()
    return user_id, token

def login_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    encrypted_password = sha256(password.encode()).hexdigest()

    cursor.execute("""
        SELECT Tokens.token, Profile.user_id, Profile.name, Profile.surname, Profile.email, Profile.user_type
        FROM Profile
        JOIN Tokens ON Tokens.user_id = Profile.user_id
        WHERE Profile.email = ? AND Profile.password = ?
    """, (email, encrypted_password))

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0], result[1], result[2], result[3], "Pupil" if result[4] == "P" else "Teacher" if result[4] == "T" else "Admin", result[5]
    return None


def is_valid_token(token):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Profile.user_id, Profile.name, Profile.surname, Profile.email, Profile.user_type
        FROM Tokens 
        JOIN Profile ON Profile.user_id = Tokens.user_id 
        WHERE token = ?
    """, (token,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0], result[1], result[2], result[3], "Pupil" if result[4] == "P" else "Teacher" if result[4] == "T" else "Admin"
    return None


def get_user_info_by_token(token):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Profile.user_id, Profile.user_type
        FROM Tokens
        JOIN Profile ON Profile.user_id = Tokens.user_id
        WHERE Tokens.token = ?
    """, (token,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return {'user_id': result[0], 'user_type': result[1]}

    return None