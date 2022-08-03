from typing import List
from routes.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
import database as database
from models import TodoResult, Todo
router = APIRouter(
    prefix='/todo',
    tags=['Todos']
)


@router.get('/', response_model=List[TodoResult], status_code=status.HTTP_200_OK)
async def find_all(current_user: str = Depends(get_current_user)):
    """fetch all todos in current login user"""
    request = await database.find_all_todo(current_user)
    return request


@router.get('/{title}', response_model=List[TodoResult], status_code=status.HTTP_200_OK)
async def find_todo_by_title(title: str, current_user: str = Depends(get_current_user)):
    """find todo by title in current user user login"""
    request = await database.find_todo_by_title(current_user, title)
    return request


@router.post('/', response_model=TodoResult, status_code=status.HTTP_201_CREATED)
async def create_todos(todo: Todo, current_user: str = Depends(get_current_user)):
    """create todo in current user login"""
    query = await database.create_todo(todo.dict(), current_user)
    if query:
        return query
    raise HTTPException(status_code=404, detail='user not found')


@router.delete('/{title}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(title: str, current_user: str = Depends(get_current_user)):
    """delete todo by title in current user login"""
    query = await database.delete_todo(title,current_user)
    if query:
        return {"message":"deleted"}
    raise HTTPException(status_code=404, detail='todo not found')


@router.put('/{title}', status_code= status.HTTP_202_ACCEPTED)
async def update_todo(title: str, is_complete: bool, current_user: str = Depends(get_current_user)):
    """update todo in current user login"""
    update = await database.update_todo(title, is_complete, current_user)
    if update:
        return update
    raise HTTPException(status_code=404, detail='wrong title dude')
