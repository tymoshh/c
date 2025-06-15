import logging
from collections.abc import Callable
from json import dumps, loads
from os import environ
from sys import stdin

from dbconn import User
def get_cookies() -> dict:
    cookies_raw = environ.get("HTTP_COOKIE", "")
    return dict(v.split("=") for v in cookies_raw.split("; "))

def cgi_main(func1: Callable[[dict], dict] | Callable[[dict, User], dict] | None = None, *, require_login: bool = False):
    """
    Usage:
    @main
    def main(data: dict) -> dict:
        # do something with data
        return {"answer":42}
    data - json passed to stdin
    return will be printed to stdout as json

    If run with require_login=True it will authenticate user with token in cookies
    import dbconn
    @main(require_login=True)
    def main(data: dict, user: dbconn.User) -> dict:
        # do something with data
        user.update_balance(100)
        return {"status":"win"}
    """

    def wrapper(func: Callable[[dict], dict] | Callable[[dict, User], dict]):
        print("Content-Type: application/json\n")
        logging.basicConfig(
            filename="/tmp/mio-c-err.log",  # noqa: S108
            format="%(asctime)s %(message)s",
            datefmt="[%Y-%m-%d %H:%M:%S]",
            level=logging.DEBUG,
        )

        try:
            content_length = int(environ.get("CONTENT_LENGTH", "0"))
        except (TypeError, ValueError):
            content_length = 0
        raw_data = stdin.read(content_length) if content_length > 0 else input()
        data = loads(raw_data)
        if require_login:
            if "token" not in cookies:
                print('{"error": "Token not found"}')
                return
            token = cookies["token"]
            try:
                user = User.auth(token)
            except ValueError as e:
                logging.exception("error", exc_info=e)
                print('{"error": "Error: ' + str(e) + '"}')
                return
            args = [data, user]
        else:
            args = [data]
        try:
            ret = func(*args)
        except Exception as e:
            logging.exception("Error", exc_info=e)
            print('{"error": "Error: ' + str(e) + ", notes:" + " ".join(e.__notes__) + '"}')
            return
        print(dumps(ret))

    if func1 is None:
        return wrapper
    return wrapper(func1)
