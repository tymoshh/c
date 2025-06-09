#!/usr/bin/env python3
import cgi
import cgitb
import json
import random
import os
from http import cookies

cgitb.enable()

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

SPIN_COST = 10
START_BALANCE = 1000

def load_balance():
    cookie = cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
    try:
        balance = int(cookie["balance"].value)
    except (KeyError, ValueError):
        balance = START_BALANCE
    return balance, cookie

def save_balance(balance, cookie):
    cookie["balance"] = str(balance)
    cookie["balance"]["path"] = "/"
    print(cookie.output())

def get_result():
    return [random.choice(symbols) for _ in range(3)]

def evaluate_spin(result):
    if result[0] == result[1] == result[2]:
        win = payouts.get(result[0], 0)
        return win, f"🎉 Wygrałeś {win}$!"
    return 0, "😢 Nic nie wygrałeś. Spróbuj ponownie!"

def main():
    print("Content-Type: application/json")
    method = os.environ.get("REQUEST_METHOD", "GET")

    balance, cookie = load_balance()

    if method == "GET":
        save_balance(balance, cookie)
        print()
        print(json.dumps({"balance": balance}))
        return

    if method == "POST":
        if balance < SPIN_COST:
            print()
            print(json.dumps({
                "result": ["❌", "❌", "❌"],
                "win": 0,
                "balance": balance,
                "message": "💸 Brak środków!"
            }))
            return

        balance -= SPIN_COST
        result = get_result()
        win, message = evaluate_spin(result)
        balance += win

        save_balance(balance, cookie)
        print()
        print(json.dumps({
            "result": result,
            "win": win,
            "balance": balance,
            "message": message
        }))

main()
