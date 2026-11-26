def register_user(users, username, password):
    if username not in users:
        users[username] = password
        return True
    return False


def login(users, username, password):
    if username in users and users[username] == password:
        return True
    return False


# Example usage
users = {}

register_user(users, "alex", "12345")

print(login(users, "alex", "12345"))  # True
print(login(users, "alex", "wrong"))  # False