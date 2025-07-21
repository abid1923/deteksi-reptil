from utils.database import get_db_connection
import mysql.connector

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, password))
        conn.commit()
        return True
    except mysql.connector.Error:
        return False
    finally:
        conn.close()

def verify_login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT id FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None