from passlib.context import CryptContext

# Configures the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash plain text password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if a plain password matches the hashed one."""
    return pwd_context.verify(plain_password, hashed_password)
