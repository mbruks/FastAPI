import pymongo
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi import FastAPI

class ToDoModel(BaseModel):
    title: str
    description: str
    completed: bool = False

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["Post"]

