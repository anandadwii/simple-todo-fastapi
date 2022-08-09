from fastapi import APIRouter, HTTPException, Depends, status
from routes.auth import get_current_user
from models import User, UserResult, ChangePassword, NewPassword
import database as database


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User, current_user: dict = Depends(get_current_user)):
    """create new user"""
    user = user.dict()

    response = await database.create_user(user, current_user)
    return response


@router.get('/{username}', response_model=UserResult)
async def find_user_by_username(username: str, current_user: dict = Depends(get_current_user)):
    """find user by email"""
    if (not current_user['authority'] == 'super_admin') or username == 'super_admin':
        raise HTTPException(403, 'forbids to find')
    find = await database.find_user(username)
    if find:
        return find


@router.put('/', status_code=status.HTTP_202_ACCEPTED)
async def change_password(password: ChangePassword, current_user: dict = Depends(get_current_user)):
    """change password current user login"""
    password_parse = password.dict()
    response = await database.change_password_user(password_parse, current_user)
    if response:
        return response
    raise HTTPException(404, 'invalid credentials')


@router.put('/{username}', status_code=status.HTTP_202_ACCEPTED)
async def change_password_by_username(username: str, password: NewPassword, current_user: dict = Depends(get_current_user)):
    """change password by admin and super admin"""
    response = await database.change_password_by_username(username, password.dict(), current_user)
    if response:
        return response
    raise HTTPException(404, 'invalid credentials')


@router.delete('/{username}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_username(username: str, current_user: dict = Depends(get_current_user)):
    """delete user by email"""

    response = await database.delete_user(username, current_user)
    if response:
        return response
    raise HTTPException(404, 'User not found')
