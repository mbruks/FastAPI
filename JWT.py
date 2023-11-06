import jwt

SECRET_KEY = "mysecretkey" # используется что то вроде команды Bash (Linux) 'openssl rand -hex 32'
ALGORITHM = "HS256" #еще должно быть время жизни токена

user_data = [{"username": "admin", "password": "adminpass"}] # в реальной БД мы храним только ХЭШИ паролей (можете прочитать про библиотеку, к примеру, 'passlib') + соль (известная только нам добавка к паролю)

# Функция для создания JWT токена
def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM) # кодируем токен, передавая в него наш словарь с тем, что мы хотим там разместить

# Функция получения User'а по токену
def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # декодируем токен
        return payload.get("sub") # из JWT-токена возвращаем всю информацию об юзере (subject, iis, expiration time)
    except jwt.ExpiredSignatureError:
        pass # тут какая-то логика обработки ошибки декодирования токена

# Функция для получения пользовательских данных на основе имени пользователя
def get_user(username: str):
    for user in user_data:
        if user.get("username") == username:
            return user
        return None

# закодируем токен, внеся в него словарь с утверждением о пользователе
token = create_jwt_token({"sub": "admin"})
print(token)

# декодируем токен и излечем из него информацию о юзере, которую мы туда зашили
username = get_user_from_token(token)
print(username)

# и теперь пойдем в нашу базу данных искать такого юзера по юзернейму
current_user = get_user(username)
print(current_user)