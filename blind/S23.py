import sqlite3

def check_login(db_path, username, password):
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        return cursor.fetchone() is not None
    finally:
        conn.close()