from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid objectid")
#         return ObjectId(v)
#
#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")


class User(BaseModel):
    """model for User validation"""
    username: str
    email: EmailStr
    password: str
    authority: str
    is_active: bool = True

    class Config:
        """config and example of user input"""
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "simalakama",
                "email": "simalakama@mailservice.com",
                "password": "isisendiri",
                "authority":"user",
                "is_active": True
            }
        }


class UserResult(BaseModel):
    """model for user search"""
    username: str
    is_active: bool


class Todo(BaseModel):
    """model for todo validation"""
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    priority: int = Field(gt=0, lt=6, description='the priority between 1-5')  # range 1-5
    is_complete: bool

    class Config:
        """config and example of todo input"""
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
    """model for todo search"""
    owner: str


class Token(BaseModel):
    """model for token"""
    access_token: str
    token_type: str

    # class Config:
    #     alias_generator = camel.case


class TokenData(BaseModel):
    """ model for data of jwt data """
    username: Optional[str] = None
    authority: Optional[str] = None


class ChangePassword(BaseModel):
    """model for user's change password"""
    old_password: str
    new_password: str


class NewPassword(BaseModel):
    """model change user's password by admin or higher"""
    new_password: str
