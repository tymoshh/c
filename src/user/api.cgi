#!/home/k24_c/mio/.homepage/c/run_cgi
from dbconn import User
from cgi_helper import cgi_main, get_cookies

@cgi_main
def main(data):
    if data["action"] == "login":
        user = User.login(data["username"], data["password"])
        return {"token": user.token}
    elif data["action"] == "getbal":
        cookies = get_cookies()
        user = User.auth(cookies["token"])
        return {"balance": user.balance}
