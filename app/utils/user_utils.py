from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

users_db = {
    "user1": User(username="user1", password="password1"),
    "user2": User(username="user2", password="password2"),
}