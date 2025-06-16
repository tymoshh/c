#!/home/k24_c/mio/.homepage/c/run_cgi
from cgi_app import CgiApp
from dbconn import User

app = CgiApp()

@app.action("login")
def login(data: dict):
    user = User.login(data["username"], data["password"])
    return {"token": user.token}

@app.action("info", require_login=True)
def info(data: dict, user: User):
    return {"balance": user.balance, "username": user.username}

app.run()