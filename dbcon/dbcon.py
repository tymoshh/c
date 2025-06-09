import os
import hashlib
from dotenv import load_dotenv
import mysql.connector
import secrets
import string

load_dotenv("/home/k24_c/cebularz7/.c/.env")

dbcon = None

class userClass:
    def __init__(self, id, password):
        self.id = id
        self.password = password

    def viewInfo(self):
        print("ID : " + self.id)
        print("Password : " + self.password)
        print("Token : " + self.token)
        print("Passwdhash : " + self.passwdhash)
    
    def createPasswdHash(self):
        self.passwdhash = getHash(self.password)

    def fetchToken(self):
        initiateConnection()
        self.createPasswdHash()
        cursor = dbcon.cursor()
        query = "SELECT passwdhash, token FROM usertable WHERE id = %s"
        cursor.execute(query, (sanitizeInput(self.id),))
        result = cursor.fetchone()
        if result:
            stored_passwdhash, fetchedtoken = result
            if stored_passwdhash == self.passwdhash:
                closeConnection()
                self.token = fetchedtoken
                return 0
            else:
                closeConnection()
                return 1
        else:
            closeConnection()
            return 1
        
    def viewToken(self):
        print("Token : " + self.token)

    def createToken(self):
        self.token = getHash(generateRandomString(255))

    def createUser(self):        
        initiateConnection()
        cursor = dbcon.cursor()
        query = """
        INSERT INTO usertable (id, passwdhash, token)
        VALUES (%s, %s, %s)
        """
        values = (sanitizeInput(self.id), sanitizeInput(self.passwdhash), sanitizeInput(self.token))
        dbcon.cursor().execute(query, values)
        dbcon.commit()
        closeConnection()

import re

def sanitizeInput(inputStr):
    inputStr = re.sub(r'\s+', '', inputStr)
    inputStr = re.sub(r'[^a-zA-Z0-9_]', '', inputStr)
    inputStr = inputStr[:255]
    return inputStr

def initiateConnection():
    try:
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

def getHash(mystring):
    return hashlib.sha256(mystring.encode()).hexdigest()

def generateRandomString(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

