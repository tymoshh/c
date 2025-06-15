#!/home/k24_c/mio/.homepage/c/run_cgi
from dbconn import User

print("DODAWANIE UZYTKOWNIKOW DO KASYNA")
ID = input("Podaj ID : ")
PASSWD = input("Podaj haslo : ")

user = User.register(ID, PASSWD)

print(user.view_info())
print("Uzytkownik dodany!")
