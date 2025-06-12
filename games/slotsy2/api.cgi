#!/usr/bin/env python3

print("Content-Type: text/plain\n")

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
    for element in jsonData:
        print(element)
except json.JSONDecodeError:
    print("invalid json")
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
    userObject = dbcon.userClass(None, None)
    userObject.setToken(jsonData["token"])
    # get bet value
    betValue = jsonData["betvalue"]
    # remove bet value
    userObject.updateBalance(-betValue)
    userObject.updatePlayedgames()
    # choose symbols
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
    # add win value
    if winValue > 0:
        userObject.updateBalance(winValue)
    # debug data
    print("symbol1: " + symbol1)
    print("symbol2: " + symbol2)
    print("symbol3: " + symbol3)
    print("winValue: " + str(winValue))
    

