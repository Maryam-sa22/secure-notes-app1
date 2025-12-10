from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    return generate_password_hash(password)

def verify_password(hashed: str, plain: str) -> bool:
    return check_password_hash(hashed, plain)
