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

if jsonData.get("action") == 'roll':
    try:
        betValue = int(jsonData["betvalue"])
    except (ValueError, TypeError):
        print(json.dumps({"error": "Invalid bet value"}))
        sys.exit(1)

    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    total = dice1 + dice2

    if 2 <= total <= 6:
        winValue = betValue
    elif 8 <= total <= 12:
        winValue = betValue * 2
    else:
        winValue = 0

    print(json.dumps({
        "dice1": dice1,
        "dice2": dice2,
        "total": total,
        "winvalue": winValue
    }))
else:
    print(json.dumps({"error": "Invalid action"}))
