import hashlib, uuid

def hash_password(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((password + salt).encode()).hexdigest()
    return salt + "$" + hashed_password

def verify_password(password, stored):
    salt, hashed_password = stored.split("$")
    return hashlib.sha512((password + salt).encode()).hexdigest() == hashed_password