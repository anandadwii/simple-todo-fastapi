from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException
from models import TodoResult, Todo
from pymongo.cursor import Cursor
from util import hashed_password

client = MongoClient("mongodb://localhost:27017/")
database = client["todoappnew"]

users_collection = database["users"]
todos_collections = database["todos"]
users_collection.create_index('email', unique=True)


async def find_user(email: str):
    """ find user """
    return users_collection.find_one({"email": email})


async def create_user(user: dict):
    """ create new user"""
    user['password'] = hashed_password(user['password'])
    try:
        check = users_collection.find_one({"email": user['email']})
        if check:
            raise HTTPException(404, 'User already exist')
        users_collection.insert_one(user)
    except DuplicateKeyError:
        raise HTTPException(404, 'User already exist')
    return user


async def delete_user(email: str):
    """delete user"""
    search = users_collection.find_one({'email': email})
    if search:
        users_collection.delete_one({'email': email})
        todos_collections.delete_many({'owner': email})
        return "deleted"
    raise HTTPException(status_code=404, detail='user not found')


async def db_parser(cursor: Cursor):
    """ parse data from database into lists """
    notes = []
    for doc in cursor:
        notes.append(
            TodoResult(**doc))
    return notes


async def find_all_todo(current_user: str):
    """fetch all todo list from current user"""
    find = todos_collections.find({"owner": current_user})
    result = await db_parser(find)
    return result


async def find_todo_by_title(current_user: str, title: str):
    """ fetch every note from owner by title """
    query = todos_collections.find(
        {'title': {"$regex": title}, 'owner': current_user})
    result = await db_parser(query)
    return result


async def create_todo(todo: dict, current_user: str):
    """ create note """
    todo['owner'] = current_user
    todos_collections.insert_one(todo)
    return todo


async def delete_todo(title: str, current_user: str):
    """delete todo by current user"""
    delete = todos_collections.delete_one({"title": title, "owner": current_user})
    if delete:
        return True
    raise HTTPException(status_code=404, detail='user not found')


async def update_todo(title: str, is_complete: bool, current_user: str):
    """update todo status from current user"""
    todos_collections.find_one_and_update({"title": title, "owner": current_user}, {"$set": {"is_complete": is_complete}})
    return todos_collections.find({"title": title})
