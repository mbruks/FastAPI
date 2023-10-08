from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()
class User(BaseModel):
    id: int
    name: str

class UserAge(BaseModel):
    id: int
    name: str
    age: int
    is_adult: bool = False

class Feedback(BaseModel):
    name: str
    message: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


class UserCreate(BaseModel):
    name: str
    email: EmailStr #EmailStr - это тип данных из Pydantic, который валидирует, что строка имеет правильный формат электронной почты.
    age: int | None = Field(default = None, lt=126) # Field - обозначает по умолчанию
    is_subscribed: bool = False