# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    username: str
    email: str

class Post(BaseModel):
    id: int
    userId: int = Field(alias="userId")
    title: str
    body: str

class ErrorResponse(BaseModel):
    detail: str
