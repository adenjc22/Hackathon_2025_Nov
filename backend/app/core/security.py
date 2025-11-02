from passlib.context import CryptContext

# Configures the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash plain text password. Truncates to 72 bytes due to bcrypt limitation."""
    # Bcrypt has a 72-byte limit on password length
    truncated_password = password[:72] if len(password) > 72 else password
    return pwd_context.hash(truncated_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if a plain password matches the hashed one."""
    # Truncate the password for verification too
    truncated_password = plain_password[:72] if len(plain_password) > 72 else plain_password
    return pwd_context.verify(truncated_password, hashed_password)
