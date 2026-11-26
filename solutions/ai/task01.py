import os
import hashlib
import hmac

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    iterations = 600_000

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations
    )

    return f"pbkdf2_sha256${iterations}${salt.hex()}${hashed.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algorithm, iterations, salt_hex, hash_hex = stored.split("$")

        if algorithm != "pbkdf2_sha256":
            return False

        iterations = int(iterations)
        if not 1 <= iterations <= 10_000_000:
            return False

        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations
        )

        return hmac.compare_digest(actual_hash, expected_hash)

    except (ValueError, TypeError, AttributeError):
        return False