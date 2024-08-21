import base64
import hmac
import hashlib
import json
from typing import Optional
from fastapi import FastAPI, Form, Cookie, Body
from fastapi.responses import Response

def sign_data(data: str) -> str:
    """Возвращаем подписанные данные data"""
    return hmac.new(
        SECRET_KEY.encode(),
        msg = data.encode(),
        digestmod = hashlib.sha256
    ).hexdigest().upper()

def get_username_from_cookie(username_sign: str) -> Optional[str]:
    username64, sign = username_sign.split(".")
    username = base64.b64decode(username64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return  username
    
def verify_password(username: str, password: str) -> bool: #check hash-password
    password_hash = hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest().lower()
    save_password = users[username]['password'].lower()
    return password_hash == save_password



SECRET_KEY = "a2e3bd0bf6af8dbe63a7733f52c5a807978c52288f7abbf9ea79a11a74ed1e83"
PASSWORD_SALT = "13a68ce4223ea9a3fd070236a8e9d742ea6307abfb793b2d6645b51e2398fc24"

app = FastAPI()
users = {'dmitro@user.com': 
         {"name":'Dmitry', 'password':"9c808e09e03b51617d1a34f32f851770249886aea8ed81680d8f87922b16a518", "balance": 10000},
         'delon@user.com': 
         {"name":'Delon', 'password':"a6c602a03cd395370e1d5f4d875fa69c2cc55a2c180fd5d124e217b8f6bd0bd0", "balance": 20000}
         }

@app.get("/")       #index HTML page and check key-cookie
def index_page(username: Optional[str] = Cookie(default = None)):
    with open('site/login.html', 'r') as f:
        login_page = f.read()
    if not username:
        return Response(login_page, media_type="text/html")
    valid_username = get_username_from_cookie(username)
    if not valid_username:
        response = Response(login_page, media_type="text/html")
        response.delete_cookie(key = "username")
        return response
    try:
        user = users[valid_username]
    except KeyError:
        response = Response('User is not registered!', media_type="text/html")
        response.delete_cookie(key = "username")
        return response
    return Response('I know you!!!', media_type="text/html")

@app.post("/login")         #sign in page and creat key-coockies
def login_page_process (data: dict = Body(...)):
    username = data["username"]
    password = data["password"]
    user = users.get(username)
    if not user or not verify_password(username, password):
        return Response(
            json.dumps({
                "success" : False,
                "message" : "I dont know you!"
                }),
                media_type="application/json")
    else:
        response = Response(
            json.dumps({
                "success" : True,
                "message" : f'Hi {user["name"]}!<br />Balance: {user["balance"]} $'
                }),
                media_type="application/json")
        username_sign = base64.b64encode(username.encode()).decode() + '.' + sign_data(username)
        response.set_cookie(key = 'username', value = username_sign)
        return response