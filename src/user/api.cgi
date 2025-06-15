#!/home/k24_c/mio/.homepage/c/run_cgi
import logging

from cgi_helper import cgi_main, get_cookies
from dbconn import User

@cgi_main
def main(data: dict):
    if data["action"] == "login":
        user = User.login(data["username"], data["password"])
        return {"token": user.token}
    if data["action"] == "info":
        cookies = get_cookies()
        token = cookies.get("token") or data.get("token")
        if token is None:
            raise ValueError("Token not found")
        user = User.auth(token)
        return {"balance": user.balance, "username": user.username}
    logging.error(f"unknown action, data: {data}")
    return {"error": "Unknown action"}
