from typing import List
from routes.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException
import database as database
from models import TodoResult, Todo
from util import successful_response
router = APIRouter(
    prefix='/todo',
    tags=['Todos']
)


@router.get('/', response_model=List[TodoResult])
async def find_all(title: str = '', current_user: str = Depends(get_current_user)):
    request = await database.find_all_todo(current_user)
    return request


@router.get('/{title}', response_model=List[TodoResult])
async def find_todo_by_title(title: str, current_user: str = Depends(get_current_user)):
    request = await database.find_todo_by_title(current_user, title)
    return request


@router.post('/', response_model=TodoResult)
async def create_todos(todo: Todo, current_user: str = Depends(get_current_user)):
    query = await database.create_todo(todo.dict(), current_user)
    if query:
        return query
    raise HTTPException(status_code=404, detail='user not found')


@router.delete('/{title}' )
async def delete_todo(title: str, current_user: str = Depends(get_current_user)):
    query = await database.delete_todo(title,current_user)
    if query:
        return successful_response(204, 'deleted')
    raise HTTPException(status_code=404, detail='todo not found')


@router.put('/{title}', )
async def update_todo(title: str, is_complete: bool, current_user: str = Depends(get_current_user)):
    update = await database.update_todo(title, is_complete, current_user)
    if update:
        return update
    raise HTTPException(status_code=404, detail='wrong title dude')
