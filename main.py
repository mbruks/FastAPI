from fastapi import FastAPI
from app.models.models import User, UserAge

users = User(id = 1, name = "Mary")
user = UserAge(id=1, name = "Mary", age = 8, is_adult = False)
app = FastAPI()
@app.get("/users", response_model=User)# тут указали модель (формат) ответа
async def user_root():
    return users


# тут добавили проверку данных на основании модели
@app.post("/user")
async def user_age(user: UserAge):
    if int(user.age) >= 18:
        user.is_adult = True
        return user
    else:
        return user

    fake_users = {
        1: {"username": "Mary", "firstname": "Latyn"},
        2: {"username": "Nina", "firstname": "Buryt"},
    }

# по id находим пользователя и получаем с помощью get запроса
    @app.get("/fake_users/{user_id}")
    def read_user(user_id: int):
        if user_id in fake_users:
            return fake_users[user_id]
            return {"error": "User not found"}