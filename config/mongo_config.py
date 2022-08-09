from fastapi.exceptions import HTTPException
import pymongo
from . import base


def mongo():
    try:
        settings = base.Settings()
        client = pymongo.MongoClient(settings.MONGO_URI)
        db = client["todov2"]
        users_collection = db['users']
        todos_collection = db['todos']
        return client, users_collection, todos_collection
    except:
        raise HTTPException(400, 'error connect mongo')
