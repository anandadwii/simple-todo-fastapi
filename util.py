from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def successful_response(status_code: int, message: str):
    return {
        'status code': status_code,
        'transaction': message
    }


def hashed_password(password):
    """hash the password"""
    return bcrypt_context.hash(password)


async def verify_password(plain_password, hashed_password):
    """verify password input and hashed password"""
    return bcrypt_context.verify(plain_password, hashed_password)