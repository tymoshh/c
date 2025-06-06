import dbcon

ID = None
PASSWD = None

print("DODAWANIE UZYTKOWNIKOW DO KASYNA")
ID = input("Podaj ID : ")
PASSWD = input("Podaj haslo : ")

userObject = dbcon.userClass(ID, PASSWD)

userObject.createPasswordHash()
userObject.createToken()

print()
userObject.checkInfo()

userObject.createUser()

print()
print("Uzytkownik dodany!")
print()
input("Nacisnij enter, aby kontynuowac ...")