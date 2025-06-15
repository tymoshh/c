#!/home/k24_c/mio/.homepage/c/run_cgi
from dbconn import User

print("TESTOWE LOGOWANIE")
ID = input("Podaj ID : ")
PASSWD = input("Podaj haslo : ")

user = User.login(ID, PASSWD)
print(user.token)
