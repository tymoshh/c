#!/home/k24_c/mio/.homepage/c/run_cgi
import dbcon

print("DODAWANIE UZYTKOWNIKOW DO KASYNA")
ID = input("Podaj ID : ")
PASSWD = input("Podaj haslo : ")

user_object = dbcon.userClass(ID, dbcon.get_hash(PASSWD))

user_object.createPasswdHash()
user_object.createToken()

print(user_object.viewInfo())

user_object.createUser()
print("Uzytkownik dodany!")
