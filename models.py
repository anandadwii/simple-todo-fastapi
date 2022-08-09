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
    username: str
    email: EmailStr
    password: str
    authority: str
    is_active: bool = True

    class Config:
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
    username: str
    is_active: bool


class Todo(BaseModel):
    # id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    priority: int = Field(gt=0, lt=6, description='the priority between 1-5')  # range 1-5
    is_complete: bool

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


class Token(BaseModel):
    access_token: str
    token_type: str

    # class Config:
    #     alias_generator = camel.case


class TokenData(BaseModel):
    """ check email """
    username: Optional[str] = None
    authority: Optional[str] = None


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class NewPassword(BaseModel):
    new_password: str
