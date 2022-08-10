from typing import Optional
from models import TokenData, Token
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError
from starlette import status
import database as database
from util import verify_password
from config import base

settings = base.Settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
EXPIRE_TIME_TOKEN = 20

router = APIRouter(
    prefix='/auth',
    tags=['OAuth2']
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth")


@router.post('/')
async def user_login_get_token(user_credential: OAuth2PasswordRequestForm = Depends()):
    """login to obtain JWT token"""
    query = await database.find_user(user_credential.username)
    if query:
        if not query['is_active']:
            raise HTTPException(404, 'user not active')
        if await verify_password(user_credential.password, query['password']):
            access_token_expires = timedelta(minutes=EXPIRE_TIME_TOKEN)
            access_token = create_access_token(data={"username": user_credential.username,
                                                     "authority": query['authority']},
                                               expires_delta=access_token_expires
                                               )
            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
        raise HTTPException(404, 'invalid credentials')
    raise HTTPException(404, 'user not found')


def verify_access_token(token: str, credentials_exception: HTTPException):
    """ verify access token """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        # authority: str = payload.get("authority")
        if username is None:
            raise credentials_exception
        # token_data = TokenData(username=username, authority=authority)
    except JWTError as exc:
        raise credentials_exception from exc
    return payload


async def get_current_user(token: str = Depends(oauth2_bearer)):
    """get current verify user login by decode the JWT"""
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                          detail='could not validate credentials',
                                          headers={"WWW-Authenticate": "Bearer"})
    token_access = verify_access_token(token, credentials_exception)
    user = await database.find_user(token_access['username'])
    if user:
        return user
    raise HTTPException(404, 'Please log in')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """create JWT for user login"""
    encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=EXPIRE_TIME_TOKEN)
    encode.update({"exp": expire})
    encode_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


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
