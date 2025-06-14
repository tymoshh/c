#!/home/k24_c/mio/.homepage/c/run_cgi
import dbcon

ID = None
PASSWD = None

print("TESTOWE LOGOWANIE")
ID = input("Podaj ID : ")
PASSWD = input("Podaj haslo : ")

userObject = dbcon.userClass(ID, PASSWD)
userObject.createPasswdHash()

userObject.fetchToken()
userObject.viewToken()
