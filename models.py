from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_active: bool = True


class UserResult(BaseModel):
    email: EmailStr
    is_active: bool


class Todo(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    priority: int
    is_complete: bool = False

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "pergi ke langit ke 7",
                "description": "mencari surga",
                "priority": 5,
                "is_complete": False
            }
        }


class TodoResult(Todo):
    owner: str


class TokenData(BaseModel):
    ''' check email '''
    email: Optional[str] = None
