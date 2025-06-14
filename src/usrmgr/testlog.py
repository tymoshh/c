#!/home/k24_c/mio/.homepage/c/run_cgi
import dbcon

print("TESTOWE LOGOWANIE")
ID = input("Podaj ID : ")
PASSWD = input("Podaj haslo : ")

user_object = dbcon.userClass(ID, PASSWD)
user_object.createPasswdHash()

user_object.fetchToken()
user_object.viewToken()
