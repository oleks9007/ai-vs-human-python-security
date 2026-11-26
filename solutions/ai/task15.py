import mysql.connector

def get_all_users():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="your_database"
    )

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
