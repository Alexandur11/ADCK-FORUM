from fastapi import Query
from pydantic import BaseModel, Field, EmailStr
from typing import List
from datetime import datetime


class User(BaseModel):
    username: str = Field(..., max_length=45)
    password: str = Field(..., max_length=45)
    firstname: str = Field(..., max_length=45)
    lastname: str = Field(..., max_length=45)
    e_mail: EmailStr
    birth_date: str = Field(..., max_length=10)


class Topic(BaseModel):
    name: str = Field(..., max_length=45)
    user_id: int = Field(..., gt=0)
    category_id: int = Field(..., gt=0)



class Reply(BaseModel):
    user_id: int = Field(..., gt=0)
    topic_id: int = Field(..., gt=0)
    content: str = Field(..., min_length=2)


class Category(BaseModel):
    title: str = Field(..., min_length=3)


class Message(BaseModel):
    text: str = Field(..., min_length=1)
    conversation_id: int = Field(..., gt=0)

class Conversation(BaseModel):
    name: str

class AccessControl(BaseModel):
    user_id: int = Field(..., gt=0)
    category_id: int = Field(..., gt=0)



