from fastapi import FastAPI
from app.models.models import User


user = User(id = 1, name = "Mary")
app = FastAPI()
@app.get("/users", response_model=User)
def user_root():
    return user

