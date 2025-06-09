import dbcon

ID = None
PASSWD = None

print("TESTOWE LOGOWANIE")
ID = input("Podaj ID : ")
PASSWD = input("Podaj haslo : ")

userObject = dbcon.userClass(ID, PASSWD)

userObject.fetchToken()
userObject.viewToken()