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
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    total = dice1 + dice2
    #game logic
    if 2 <= total <= 6:
        winValue = 50
    elif 8 <= total <= 12:
        winValue = 75
    else:
        winValue = 0
    #add win value
    if winValue > 0:
        userObject.updateBalance(winValue)
    #return data as json
        print(json.dumps({
       "winvalue": winValue,
       "dice1": dice1,
       "dice2": dice2
    }))
