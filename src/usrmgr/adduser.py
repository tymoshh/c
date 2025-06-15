#!/home/k24_c/mio/.homepage/c/run_cgi
from dbconn import User, DbConn

print("DODAWANIE UZYTKOWNIKOW DO KASYNA")
ID = input("Podaj ID : ")
db = DbConn()
if not db.user_exists(ID):
    PASSWD = input("Podaj haslo : ")
    user = User.register(ID, PASSWD)
    print("Uzytkownik dodany!")
else:
    user = User(ID)
    print("Uzytkownik istnieje")

admin = input("Czy admin? [y/N] : ")
user.admin = admin.lower() == "y"

print(user.view_info())
