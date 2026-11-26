import hashlib

def register_user(users, username, password):
    users[username] = hashlib.md5(password.encode()).hexdigest()

def login(users, username, password):
    return users.get(username, None) == hashlib.md5(password.encode()).hexdigest()