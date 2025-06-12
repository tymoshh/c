#!/usr/bin/env python3
import cgi
import cgitb
import json
import os
import random

# Włączenie debugowania
cgitb.enable()

# Ścieżka do pliku przechowującego saldo użytkownika (np. tymczasowo w katalogu tmp)
BALANCE_FILE = "/tmp/balance.txt"
COST = 50

def get_balance():
    if not os.path.exists(BALANCE_FILE):
        return 1000
    with open(BALANCE_FILE, "r") as f:
        return int(f.read().strip())

def save_balance(balance):
    with open(BALANCE_FILE, "w") as f:
        f.write(str(balance))

def main():
    print("Content-Type: application/json\n")

    balance = get_balance()

    if balance < COST:
        print(json.dumps({
            "result": [1, 1],
            "sum": 2,
            "message": "Brak środków!",
            "win": 0,
            "balance": balance
        }))
        return

    balance -= COST
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    total = dice1 + dice2
    win = 0
    message = ""

    if 2 <= total <= 6:
        win = 50
        message = "🎉 Wygrałeś (nisko)!"
    elif 8 <= total <= 12:
        win = 75
        message = "🎉 Wygrałeś (wysoko)!"
    else:
        message = "💀 Przegrałeś (suma = 7)"

    balance += win
    save_balance(balance)

    print(json.dumps({
        "result": [dice1, dice2],
        "sum": total,
        "message": message,
        "win": win,
        "balance": balance
    }))

if __name__ == "__main__":
    main()
