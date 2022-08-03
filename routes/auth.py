from typing import Optional
from models import TokenData
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError
from starlette import status
import database as database
from util import verify_password

SECRET_KEY = "lmaoxd1234!"
ALGORITHM = "HS256"


router = APIRouter(
    prefix='/auth',
    tags=['OAuth2']
)


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth")


@router.post('/')
async def user_login_get_token(user_credential: OAuth2PasswordRequestForm = Depends()):
    query = await database.find_user(user_credential.username)
    if query:
        if verify_password(user_credential.password, query['password']):
            access_token = create_access_token(data={"email": user_credential.username}
            )
        return {
            "access token": access_token,
            "token type": "bearer"
        }
        raise HTTPException(404,'invalid credentials')
    raise HTTPException(404, 'user not found')


def verify_access_token(token: str, credentials_exception: HTTPException):
    """ verify access token """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("email")
        if user_email is None:
            raise credentials_exception
        token_data = TokenData(email=user_email)
    except JWTError as exc:
        raise credentials_exception from exc
    return token_data


async def get_current_user(token:str = Depends(oauth2_bearer)):
    """get current verify user login by decode the JWT"""
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                          detail='could not validate credentials',
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = await database.find_user(token.email)
    if user:
        return user['email']
    raise HTTPException(404, 'Please log in')


def create_access_token(data: dict):
    """create JWT for user login"""
    encode = data.copy()

    expire = datetime.now() + timedelta(minutes=20)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_user_exception():
    """raise exception when user's credential not validate"""
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": 'Bearer'}
    )
    return credential_exception


async def token_exception():
    """exception to raise incorrect token"""
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="incorrect username/password",
        headers={"WWW-Authenticate": "Bearer"})
    return token_exception_response
