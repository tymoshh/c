#!/home/k24_c/mio/.homepage/c/run_cgi
import json
import os
import random
import sys

from dbconn import User
from pydantic import BaseModel, ValidationError

print("Content-Type: application/json\n")


class Data(BaseModel):
    token: str
    bet_value: int


try:
    content_length = int(os.environ.get("CONTENT_LENGTH", "0"))
except (TypeError, ValueError):
    content_length = 0
raw_data = sys.stdin.read(content_length) if content_length > 0 else ""

try:
    data = Data.model_validate_json(raw_data)
except ValidationError as e:
    print(json.dumps({"error": "Invalid JSON" + str(e)}))
    sys.exit(1)

slot_map = {1: "Seven", 2: "Bell", 3: "Grape", 4: "Cherry", 6: "Lemon"}

try:
    user = User.auth(data.token)
except ValueError as e:
    print(json.dumps({"error": e.args[0]}))
    sys.exit(1)
bet_value = data.bet_value
user.update_balance(-bet_value)
user.update_played_games()
symbols = random.choices(list(slot_map.values()), k=3)
if symbols[0] == symbols[1] == symbols[2]:
    if symbols[0] == "Seven":
        win_value = bet_value * 100
    elif symbols[0] == "Bell":
        win_value = bet_value * 10
    else:
        win_value = bet_value * 5
elif len(set(symbols)) == 2:
    win_value = bet_value * 2
else:
    win_value = 0

user.update_balance(win_value)
print(json.dumps({"winvalue": win_value, "symbols": symbols}))
