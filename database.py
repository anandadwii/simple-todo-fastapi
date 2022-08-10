from pymongo import MongoClient
from fastapi import HTTPException
from models import TodoResult
from pymongo.cursor import Cursor
from util import hashed_password, verify_password
from config import base

settings = base.Settings()
client = MongoClient(settings.MONGO_URI)
database = client[settings.DB_NAME]

users_collection = database["users"]
todos_collections = database["todos"]
users_collection.create_index('username', unique=True)


async def find_user(username: str):
    """ find user """
    return users_collection.find_one({"username": username})


async def create_user(user: dict, current_user: dict):
    """ create new user"""
    authorities = ['admin', 'user']
    for authority in authorities:
        if authority == user['authority']:
            duplicate_check = await find_user(user['username'])
            if duplicate_check:
                raise HTTPException(400, 'user already exist')
            if current_user['authority'] == 'user':
                raise HTTPException(403, 'limited access for user')
            if current_user['authority'] == 'admin' and not user['authority'] == 'user':
                raise HTTPException(403, 'dont do that, admin')
            user['password'] = hashed_password(user['password'])
            users_collection.insert_one(user)
            return user
    raise HTTPException(404, 'role not found')


async def delete_user(username: str, current_user: dict):
    """delete user by admin or higher"""
    if current_user['authority'] == 'user' or username == 'super_admin':
        raise HTTPException(403, 'user forbidden')
    search = users_collection.find_one({'username': username})
    if search:
        users_collection.delete_one({'username': username})
        todos_collections.delete_many({'owner': username})
        return f'{username} deleted by {current_user["username"]}'
    raise HTTPException(status_code=404, detail='user not found')


async def change_password_user(password: dict, current_user: dict):
    """change password by current user"""
    find = users_collection.find_one({'username': current_user['username']})
    if find:
        verify = await verify_password(password['old_password'], find['password'])
        print(verify)
        if verify is True:
            new_pass = hashed_password(password['new_password'])
            users_collection.update_one({'username': current_user['username']},
                                                 {"$set": {'password': new_pass}})
            return {
                "old hashed password": find['password'],
                "new hashed password": new_pass
            }
        raise HTTPException(404, 'password not match!')

    raise HTTPException(404, 'user not found')


async def change_password_by_username(username: str, password: dict, current_user: dict):
    """change password by admin or higher"""
    if username == 'super_admin' and current_user['authority'] == 'admin':
        raise HTTPException(403, 'forbidden to change super_admin')
    if current_user['authority'] == 'user':
        raise HTTPException(403, 'user forbidden to use this')
    find = users_collection.find_one({'username': username})

    if find:
        new_pass = hashed_password(password['new_password'])
        users_collection.update_one({'username': username},
                                        {"$set": {'password': new_pass}})
        return f'password edited'
    raise HTTPException(404, 'user not found')


async def db_parser(cursor: Cursor):
    """ parse data from database into lists """
    notes = []
    for doc in cursor:
        notes.append(
            TodoResult(**doc))
    return notes


async def find_all_todo(current_user: dict):
    """fetch all todo list from current user"""
    if current_user['authority'] == 'user':
        find = todos_collections.find({"owner": current_user.get("username")})
    else:
        find = todos_collections.find({})
    result = await db_parser(find)
    return result


async def find_todo_by_title(current_user: dict, title: str):
    """ fetch every note from owner by title """
    if current_user.get("authority") == 'user':
        query = todos_collections.find({'title': title, 'owner': current_user.get("username")})
    else:
        query = todos_collections.find({'title': title})

    result = await db_parser(query)
    return result


async def create_todo(todo: dict, current_user: dict):
    """ create note by current user"""
    todo['owner'] = current_user
    todos_collections.insert_one(todo)
    return todo


async def delete_todo(title: str, owner: str, current_user: str):
    """delete todo by current user"""
    if not current_user.get("authority") == 'super_admin':
        raise HTTPException(403, 'not authorized')
    delete = todos_collections.delete_one({"title": title, "owner": owner})
    if delete:
        return True
    raise HTTPException(status_code=404, detail='user not found')


async def update_todo(title: str, is_complete: bool, owner: str, current_user: str):
    """update todo status from current user"""
    if not current_user.get("authority") == 'super_Admin':
        raise HTTPException(403, 'not authorized')
    todos_collections.find_one_and_update({"title": title, "owner": owner}, {"$set": {"is_complete": is_complete}})
    return todos_collections.find({"title": title})
