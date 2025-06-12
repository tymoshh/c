#!/usr/bin/env python3
import cgi
import cgitb
import json
import os
import http.cookies as Cookie

cgitb.enable()

print("Content-Type: application/json")

# Użycie ciasteczka do przechowywania salda
cookie = Cookie.SimpleCookie(os.environ.get("HTTP_COOKIE"))
balance = 1000
if "balance" in cookie:
    try:
        balance = int(cookie["balance"].value)
    except:
        balance = 1000

cost = 10
symbols = ["🍒", "🍋", "🍇", "🍉", "🔔", "⭐", "7️⃣"]
payouts = {
    "🍒": 200,
    "🍋": 300,
    "🍇": 400,
    "🍉": 500,
    "🔔": 750,
    "⭐": 1000,
    "7️⃣": 2000
}

if balance < cost:
    print()
    print(json.dumps({
        "result": ["❌", "❌", "❌"],
        "win": 0,
        "balance": balance,
        "message": "Brak środków na zakręcenie"
    }))
    exit()

import random

balance -= cost
result = [random.choice(symbols) for _ in range(3)]

if result[0] == result[1] == result[2]:
    win = payouts[result[0]]
else:
    win = 0

balance += win

# Ustaw nowe ciasteczko
new_cookie = Cookie.SimpleCookie()
new_cookie["balance"] = str(balance)
new_cookie["balance"]["path"] = "/"
print(new_cookie.output())

print()
print(json.dumps({
    "result": result,
    "win": win,
    "balance": balance,
    "message": f"Gratulacje! Wygrałeś {win}$!" if win > 0 else "Niestety, brak wygranej"
}))
