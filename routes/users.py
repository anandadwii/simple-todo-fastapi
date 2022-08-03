from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from models import User, UserResult
import database as database


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/', response_model=UserResult)
async def create_user(user: User):
    """create new user"""
    response = await database.create_user(user.dict())
    return response


@router.get('/{email}', response_model=UserResult)
async def find_user_by_email(email: str):
    """find user by email"""
    find = await database.find_user(email)
    if find:
        return find
    raise HTTPException(404, 'User not found')


@router.delete('/{email}')
async def delete_user_by_email(email: str):
    """delete user by email"""
    response = await database.delete_user(email)
    if response:
        return response
    raise HTTPException(404, 'User not found')
