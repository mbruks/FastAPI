from fastapi import FastAPI, Cookie, Response
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    username: str
    password: str


sample_user: dict = {"username": "user123", "password": "password123"}
db: list[User] = [User(**sample_user)]

# имитируем хранилище сессий
sessions: dict = {}  # это можно хранить в кэше, например в Redis

# основная логика программы
@app.post('/login')
async def login(user: User, response: Response):
    for person in db:
        if person.username == user.username and person.password == user.password:
            session_token = "abc123xyz456"
            sessions[session_token] = user  # сохранили у себя в словаре сессию, где токен - это ключ, а значение - объект юзера
            response.set_cookie(key="session_token", value=session_token,
                                httponly=True)  # тут установили куки с защищенным флагом httponly - недоступны для вредоносного JS; флаг secure означает, что куки идут только по HTTPS
            return {"message": "куки установлены"}
    return {"message": "Invalid username or password"}


@app.get('/user')
async def user_info(session_token=Cookie()):
    user = sessions.get(
        session_token)  # ищем в сессиях был ли такой токен создан, и если был, то возвращаем связанного с ним юзера
    if user:
        return user.dict()  # у pydantic моделей есть метод dict(), который делает словарь из модели
    return {"message": "Unauthorized"}