#!/home/k24_c/mio/.homepage/c/run_cgi
import json
import os
import sys
import logging
import traceback

from dbconn import User

logging.basicConfig(filename="/tmp/mio-c-err.log", format="%(asctime)s %(message)s", datefmt="[%Y-%m-%d %H:%M:%S]", level=logging.DEBUG)
log = logging.error
log("working")
print("Content-Type: application/json\n")

try:
    content_length = int(os.environ.get("CONTENT_LENGTH", "0"))
except (TypeError, ValueError):
    content_length = 0
raw_data = sys.stdin.read(content_length) if content_length > 0 else input()
try:
    json_data = json.loads(raw_data)
except json.JSONDecodeError as e:
    print(json.dumps({"error": "Invalid JSON " + str(e)}))
    sys.exit(1)

try:
    if json_data["action"] == "login":
        user = User.login(json_data["username"], json_data["password"])
        log(json_data)
        print(json.dumps({"token": user.token}))
    elif json_data["action"] == "getbal":
        user = User.auth(json_data["token"])
        print(json.dumps({"balance": user.balance}))
    else:
        print('"works!"')
except Exception as e:
    log(traceback.format_exc())
    print(json.dumps({"error": str(e)}))
