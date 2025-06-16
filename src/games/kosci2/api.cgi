#!/home/k24_c/mio/.homepage/c/run_cgi
from secrets import randbelow
from cgi_app import CgiApp
from dbconn import User

app = CgiApp()

@app.action("roll", require_login=True)
def roll(data: dict, user: User):
    bet_value = data["bet_value"]
    user.update_balance(-bet_value)
    user.update_played_games()
    dices = [randbelow(6) for i in range(2)]
    result = sum(dices)
    if result == 11:
        win = 5
    elif result > 7:
        win = 2
    else:
        win = 0
    user.update_balance(win * bet_value)
    return {"dice": dices, "win": win}

app.run()