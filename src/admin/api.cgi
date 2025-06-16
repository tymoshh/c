#!/home/k24_c/mio/.homepage/c/run_cgi
from cgi_app import CgiApp
from dbconn import User, DbConn

app = CgiApp()


@app.action("get_all_users", require_login=True, admin_only=True)
def get_all_users_data(data: dict, user: User) -> dict:
    db = DbConn()
    return {"users": db.get_all_users_data()}


@app.action("get_user", require_login=True, admin_only=True)
def get_user_data(data: dict, user: User) -> dict:
    username = data.get("username")
    if not username:
        return {"error": "Username is required"}
    db = DbConn()
    return {"user": db.get_detailed_user_data(username)}


@app.action("add_balance", require_login=True, admin_only=True)
def add_balance(data: dict, user: User) -> dict:
    username = data.get("username")
    amount = data.get("value")
    if not username:
        return {"error": "Username is required"}
    if amount is None:
        return {"error": "Amount is required"}

    target_user = User(username)
    target_user.update_balance(amount)
    return {"success": True, "message": f"Balance updated by {amount}"}


@app.action("remove_balance", require_login=True, admin_only=True)
def remove_balance(data: dict, user: User) -> dict:
    username = data.get("username")
    amount = data.get("value")
    if not username:
        return {"error": "Username is required"}
    if amount is None:
        return {"error": "Amount is required"}

    target_user = User(username)
    target_user.update_balance(-amount)
    return {"success": True, "message": f"Balance updated by {-amount}"}


@app.action("set_balance", require_login=True, admin_only=True)
def set_balance(data: dict, user: User) -> dict:
    username = data.get("username")
    new_balance = data.get("value")
    if not username:
        return {"error": "Username is required"}
    if new_balance is None:
        return {"error": "New balance is required"}

    target_user = User(username)
    target_user.update_balance(new_balance - target_user.balance)
    return {"success": True, "message": f"Balance set to {new_balance}"}


@app.action("set_admin", require_login=True, admin_only=True)
def set_admin(data: dict, user: User) -> dict:
    username = data.get("username")
    admin_status = data.get("admin_status")
    if not username:
        return {"error": "Username is required"}
    if admin_status is None:
        return {"error": "Admin status is required"}

    target_user = User(username)
    target_user.admin = admin_status
    status_text = "granted" if admin_status else "revoked"
    return {"success": True, "message": f"Admin privileges {status_text}"}


app.run()