import jwt
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    password: str
    role: str


# наша бд с пользователями и их ролями
data_base = {
    "admin": {"username": "admin", "password": "adminpass", "role": "admin"},
    "user": {"username": "user", "password": "userpass", "role": "user"},
    "guest": {"username": "guest", "password": "guestpass", "role": "guest"}
}

# функция создания веб токена
def create_jwt(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


# функция верификации токена
def verify_jwt(token: str):
    try:
        decode_data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return decode_data
    except jwt.PyJWTError:
        return None


# регистрация юзера
@app.post("/register")
def register_user(username: str, password: str):
    hashed_password = pwd_context.hash(password)
    return {"username": username, "hashed_password": hashed_password}

def get_user(username: str):
    if username in data_base:
        user = data_base[username]
        return User(**user)
    return None


# аутентификация юзера
@app.post("/token")
def authenticate_user(username: str, password: str):
    user = get_user(username) # получаем юзера из бд
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    is_password_correct = pwd_context.verify(password, user.hashed_password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    jwt_token = create_jwt({"sub": user.username})
    return {"access_token": jwt_token, "token_type": "bearer"}


# Получение текущего пользователя
def get_current_user(token: str = Depends(oauth2_scheme)):
    decoded_data = verify_jwt(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = get_user(decoded_data["sub"])  # Получение пользователя из базы данных
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user

@app.get("/users/me")
def get_user_me(current_user: User = Depends(get_current_user)):
    return current_user

# проверка роли юзера
def user_role(role: str):
    def role_validator(current_user: User = Depends(get_current_user)):
        if role not in current_user.roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_validator

@app.get("/admin")
def get_admin(current_user: User = Depends(user_role("admin"))):
    return {"message": "Welcome, admin!"}

@app.get("/user")
def get_user(current_user: User = Depends(user_role("user"))):
    return {"message": "Welcome, user!"}

@app.get("/guest")
def get_guest(current_user: User = Depends(user_role("guest"))):
    return {"message": "Welcome, guest!"}



