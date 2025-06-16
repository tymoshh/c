#!/home/k24_c/mio/.homepage/c/run_cgi
import random

from cgi_app import CgiApp
from dbconn import User

app = CgiApp()

@app.action(require_login=True)
def main(data: dict, user: User):
    slot_map = {1: "Seven", 2: "Bell", 3: "Grape", 4: "Cherry", 6: "Lemon"}
    bet_value = data["bet_value"]
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
    return {"winvalue": win_value, "symbols": symbols}

app.run()