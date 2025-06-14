#!/home/k24_c/mio/.homepage/c/run_cgi
import dbcon

print("DODAWANIE UZYTKOWNIKOW DO KASYNA")
ID = input("Podaj ID : ")
PASSWD = input("Podaj haslo : ")

userObject = dbcon.userClass(ID, dbcon.get_hash(PASSWD))

userObject.createPasswdHash()
userObject.createToken()

print(userObject.viewInfo())

userObject.createUser()
print("Uzytkownik dodany!")