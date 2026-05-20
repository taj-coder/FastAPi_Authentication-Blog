from pwdlib import PasswordHash

# Initialize the modern password hashing , Argon2 algorithm
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Hashes a plain text password safely using modern standards."""
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against the stored database hash."""
    return password_hash.verify(plain_password, hashed_password)
