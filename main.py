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