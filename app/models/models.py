from fastapi import FastAPI
from pydantic import BaseModel

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
