#!/usr/bin/env python3
import os
import json
import sys
import dbcon

print("Content-Type: application/json\n")


try:
    contentLength = int(os.environ.get("CONTENT_LENGTH", 0))
except (TypeError, ValueError):
    contentLength = 0
rawData = sys.stdin.read(contentLength) if contentLength > 0 else ""
try:
    jsonData = json.loads(rawData)
except json.JSONDecodeError:
    print(json.dumps({"error": "Invalid JSON"}))
    sys.exit(1)

if jsonData["action"] == "login":
    userObject = dbcon.userClass(jsonData["username"], jsonData["password"])
    userObject.createPasswdHash()
    userObject.fetchToken()
    tokenVar = userObject.getToken()
    print(json.dumps({"token": tokenVar}))
elif jsonData["action"] == "getbal":
    userObject = dbcon.userClass(None, None)
    userObject.setToken(jsonData["token"])
    balanceVar = userObject.fetchBalance()
    print(json.dumps({"balance": balanceVar}))
