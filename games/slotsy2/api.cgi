#!/usr/bin/env python3

print("Content-Type: application/json\n")

import os
import cgi
import json
import sys
import random

sys.path.insert(0, "/home/k24_c/cebularz7/local/usr/lib/python3/dist-packages")

try:
    contentLength = int(os.environ.get('CONTENT_LENGTH', 0))
except (TypeError, ValueError):
    contentLength = 0
rawData = sys.stdin.read(contentLength) if contentLength > 0 else ''
try:
    jsonData = json.loads(rawData)
except json.JSONDecodeError:
    print(json.dumps({"error": "Invalid JSON"}))
    sys.exit(1)

slotMap = {
    1: "7",
    2: "Bell",
    3: "Grape",
    4: "Cherry",
    6: "Lemon"
}

import dbcon
if jsonData["action"] == 'bet':
    # create user object
    userObject = userClass(None, None)
    userObject.setToken(jsonData["token"])
    # get bet amount
    betValue = int(jsonData["betvalue"])
    # remove bet value
    userObject.updateBalance(-betValue)
    # random 3 slots
    symbol1 = random.choice(list(slotMap.values()))
    symbol2 = random.choice(list(slotMap.values()))
    symbol3 = random.choice(list(slotMap.values()))
    # game logic
    if symbol1 == symbol2 == symbol3:
        if symbol1 == "7":
            winValue = betValue * 100
        elif symbol1 == "Bell":
            winValue = betValue * 10
        else:
            winValue = betValue * 5
    elif symbol1 == symbol2 or symbol1 == symbol3 or symbol2 == symbol3:
        winValue = betValue * 2
    else:
        winValue = 0
    # modify user bal
    userObject.updateBalance(winValue)
    # return json
    print(json.dumps(
        {
            "win": winValue
            "symbol1": symbol1
            "symbol2": symbol2
            "symbol3": symbol3
        }
    ))
