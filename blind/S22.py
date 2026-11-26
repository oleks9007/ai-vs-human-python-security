import secrets


def generate_api_key(length=40):
    generated_key = secrets.token_urlsafe(length)
    return generated_key
