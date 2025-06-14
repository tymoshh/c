#!/home/k24_c/mio/.homepage/c/run_cgi
import json
import os
import sys
from pathlib import Path

import dbcon

sys.stderr = Path("/tmp/mio-c-err.log").open(mode="w")  # noqa: S108 SIM115
print("Content-Type: application/json\n")


try:
    content_length = int(os.environ.get("CONTENT_LENGTH", "0"))
except (TypeError, ValueError):
    content_length = 0
raw_data = sys.stdin.read(content_length) if content_length > 0 else ""
try:
    json_data = json.loads(raw_data)
except json.JSONDecodeError:
    print(json.dumps({"error": "Invalid JSON"}))
    sys.exit(1)

if json_data["action"] == "login":
    user_object = dbcon.userClass(json_data["username"], json_data["password"])
    user_object.createPasswdHash()
    user_object.fetchToken()
    token_var = user_object.getToken()
    print(json.dumps({"token": token_var}))
elif json_data["action"] == "getbal":
    user_object = dbcon.userClass(None, None)
    user_object.setToken(json_data["token"])
    balance_var = user_object.fetchBalance()
    print(json.dumps({"balance": balance_var}))
else:
    print('"works!"')
