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