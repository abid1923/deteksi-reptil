from utils.database import get_db_connection
from datetime import datetime

def save_detection_history(username, nama_reptil, confidence):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO riwayat_deteksi (username, nama_reptil, confidence, waktu) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (username, nama_reptil, confidence, datetime.now()))
    conn.commit()
    conn.close()

def get_detection_history(username=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if username:
        query = "SELECT * FROM riwayat_deteksi WHERE username = %s ORDER BY waktu DESC"
        cursor.execute(query, (username,))
    else:
        query = "SELECT * FROM riwayat_deteksi ORDER BY waktu DESC"
        cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result