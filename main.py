from fastapi import FastAPI
from app.models.models import User, UserAge, Feedback, Item

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


@app.get("/limit_users/")
def limit_users(limit: int = 10):
    return dict(list(fake_users.items())[:limit])

# маршрут для отправки пользователями отзывов
lst = []
@app.post("/feedback")
async def feedback(feedback: Feedback):
    lst.append({"name": feedback.name, "comments": feedback.message})
    return f"Feedback received. Thank you, {feedback.name}!"

# получение обратного ответа
@app.get("/comments")
async def show_feedback():
    return lst

@app.post("/items/")
async def create_item(item: Item) -> Item: # тут мы передали в наш обработчик Pydantic модель, чтобы она проверяла все запросы на соответствие этой модели (все поля и типы данных в них должны соответствовать модели
    return item


@app.get("/items/")
async def read_items() -> list[Item]: # тут мы не принимаем никаких данных, но указываем, что возвращаться будет список, содержащий в себе Pydantic модели
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/fake_items/") #http://127.0.0.1:8000/items/?skip=0&limit=10
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]