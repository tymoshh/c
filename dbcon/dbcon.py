import os
import hashlib
from dotenv import load_dotenv
import mysql.connector

load_dotenv("/home/k24_c/cebularz7/.c/.env")

dbcon = None

def initiateConnection():
    try:
        print(os.getenv("DB_PASSWORD"))
        global dbcon
        dbcon = mysql.connector.connect(
            host=os.getenv("DB_HOST"), 
            user=os.getenv("DB_USERNAME"), 
            password=os.getenv("DB_PASSWORD"), 
            database=os.getenv("DB_USERNAME")
        )
        return 0
    except:
        return 1
    
def closeConnection():
    global dbcon
    dbcon.close()

def getHash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def getToken(username, passwordHash):
    print("TEST")
