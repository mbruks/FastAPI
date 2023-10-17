from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

class User(BaseModel):
    username: str
    password: str

# симуляция базы данных юзеров
user_data = [User(**{"username": "user1", "password": "pass1"}), User(**{"username": "user2", "password": "pass2"})]

#Эта функция проверяет учетные данные пользователя по базе данных и выдает ошибку HTTP 401 Unauthorized, если они недействительны.
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise
    HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

#получение информации о пользователе и его пароле
def get_user_from_db(username: str):
    for user in user_data:
        if user.username == username:
            return user
        return None

@app.get("/protected_resource/")
def get_protected_resource(user: User = Depends(authenticate_user)):
    return {"message": "You have access to the protected resource!", "user_info": user}