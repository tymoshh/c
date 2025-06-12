#!/usr/bin/env python3
import cgi
import json
import random

print("Content-Type: application/json\n")

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

# koszt zakręcenia
cost = 10
start_balance = 1000

# wczytanie danych z przeglądarki (ale my nie używamy żadnych danych wejściowych)
form = cgi.FieldStorage()

# losujemy 3 symbole
result = [random.choice(symbols) for _ in range(3)]
win = 0
message = "❌ Spróbuj ponownie!"

# jeśli wszystkie 3 takie same – wygrana
if result[0] == result[1] == result[2]:
    win = payouts[result[0]]
    message = "🎉 Gratulacje! Wygrałeś!"

# saldo po jednej turze (klient odliczył już 10$ lokalnie)
balance = start_balance - cost + win

response = {
    "result": result,
    "win": win,
    "message": message,
    "balance": balance
}

print(json.dumps(response))
