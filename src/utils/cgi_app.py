import logging
from collections.abc import Callable

from json import dumps, loads
from os import environ
from sys import stdin
from traceback import format_exception_only

from dbconn import User


def get_cookies() -> dict:
    """
    Returns client's cookies
    :return: dict of cookies
    """
    cookies_raw = environ.get("HTTP_COOKIE", "")
    return dict(v.split("=") for v in cookies_raw.split("; ")) if cookies_raw != "" else dict()


class CgiApp:
    """
    Usage:
    app = CgiApp()
    @app.action("get_answer")
    def main(data: dict) -> dict:
        # do something with data
        return {"answer":42}
    app.run()
    data - json passed to stdin
    return will be printed to stdout as json

    If run with require_login=True it will authenticate user with token in cookies
    import dbconn
    app = CgiApp()
    @app.action("get_money", require_login=True)
    def main(data: dict, user: dbconn.User) -> dict:
        # do something with data
        user.update_balance(100)
        return {"status":"win"}
    app.run()
    """

    def __init__(self):
        self.actions: dict[str | None, Callable[[dict], dict]] = dict()
        self.ran = False

    def __del__(self):
        if not self.ran:
            logging.warn(f"CgiApp {self!r} was not run, actions: {", ".join(map(str, self.actions.keys()))}")

    def action(self, name: str | None = None,
               func1: Callable[[dict], dict] | Callable[[dict, User], dict] | None = None, *,
               require_login: bool = False, admin_only: bool = False):
        if admin_only and not require_login:
            raise ValueError("admin_only requries authentication")
        def wrapper(func: Callable[[dict], dict] | Callable[[dict, User], dict]):
            def inner(data: dict) -> dict:
                if require_login:
                    cookies = get_cookies()
                    if "token" in data:
                        token = data.pop("token")
                    elif "token" in cookies:
                        token = cookies["token"]
                    else:
                        logging.error(f"token not found, data: {data}, cookies: {cookies}")
                        return {"error": "Token not found"}
                    user = User.auth(token)
                    if admin_only and not user.admin:
                        return {"error": "Chcialbys (nie masz admina)"}
                    args = [data, user]
                else:
                    args = [data]
                return func(*args)
            if name in self.actions:
                raise ValueError(f"Action {name} already exists")
            self.actions[name] = inner

        if func1 is None:
            return wrapper
        return wrapper(func1)

    def run(self):
        self.ran = True
        print("Content-Type: application/json\n")
        logging.basicConfig(
            filename="/tmp/mio-c-err.log",  # noqa: S108
            format="%(asctime)s %(message)s",
            datefmt="[%Y-%m-%d %H:%M:%S]",
            level=logging.DEBUG,
        )
        logging.info("working")
        raw_length = environ.get("CONTENT_LENGTH")
        if raw_length and raw_length.isdigit():
            content_length = int(raw_length)
        else:
            content_length = 0
        raw_data = stdin.read(content_length) if content_length > 0 else input()
        data = loads(raw_data)
        action = data.pop("action", None)
        func = self.actions[action]
        try:
            res = func(data)
        except Exception as e:
            logging.exception("Error", exc_info=e)
            res = {"error": "Error: " + "".join(format_exception_only(e))}
        print(dumps(res))
