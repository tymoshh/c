#!/usr/bin/env python3

import random
import json

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

# Losuj 3 symbole
r1 = random.choice(symbols)
r2 = random.choice(symbols)
r3 = random.choice(symbols)
result = [r1, r2, r3]

# Oblicz wygraną
win = 0
message = "😢 Spróbuj ponownie!"
if r1 == r2 == r3:
    win = payouts[r1]
    message = f"🎉 Jackpot! 3x {r1} = +{win}$!"
elif r1 == r2 or r2 == r3 or r1 == r3:
    message = "👌 Dwa takie same symbole (bez wygranej)"

# Zwróć dane JSON
print("Content-Type: application/json\n")
print(json.dumps({
    "result": result,
    "win": win,
    "message": message
}))
