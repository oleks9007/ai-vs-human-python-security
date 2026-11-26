import sqlite3


def check_login(db_path, username, password):
    user = username
    pswd = password

    db = sqlite3.connect(db_path)
    c = db.cursor()
    c.execute('SELECT * from users WHERE username="%s" AND password="%s"' % (user, pswd))
    if c.fetchone() is not None:
        return True
    else:
        return False