import os
import hashlib
from dotenv import load_dotenv
import mysql.connector
import secrets
import string
import re

load_dotenv(os.environ["HOME"] + "/.c/.env")

db_connection = None


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

    def setToken(self, targetToken):
        self.token = targetToken

    def fetchToken(self):
        initiateConnection()
        cursor = db_connection.cursor()
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

    def getToken(self):
        return self.token

    def createToken(self):
        self.token = getHash(generateRandomString(255))

    def createUser(self):
        initiateConnection()
        print(db_connection.is_connected())
        query = """
        INSERT INTO usertable (id, passwdhash, token)
        VALUES (%s, %s, %s)
        """
        values = (
            sanitizeInput(self.id),
            sanitizeInput(self.passwdhash),
            sanitizeInput(self.token),
        )
        db_connection.cursor().execute(query, values)
        db_connection.commit()
        closeConnection()

    def fetchBalance(self):
        initiateConnection()
        cursor = db_connection.cursor()
        query = "SELECT balance FROM usertable WHERE token = %s"
        values = (sanitizeInput(self.token),)  # <-- krotka z jednym elementem
        cursor.execute(query, values)  # <-- używamy tego samego kursora
        result = cursor.fetchone()
        userBalance = result[0] if result else None
        closeConnection()
        return userBalance

    def updateBalance(self, balanceModifier):
        initiateConnection()
        db_connection.cursor()
        # add/remove balance
        query = "UPDATE usertable SET balance = balance + %s WHERE token = %s"
        values = (balanceModifier, sanitizeInput(self.token))
        db_connection.cursor().execute(query, values)
        # add to moneyspent
        if balanceModifier < 0:
            query = "UPDATE usertable SET moneyspent = moneyspent + %s WHERE token = %s"
            values = (balanceModifier, sanitizeInput(self.token))
            db_connection.cursor().execute(query, values)
        db_connection.commit()
        closeConnection()

    def updatePlayedgames(self):
        initiateConnection()
        db_connection.cursor()
        query = "UPDATE usertable SET playedgames = playedgames + %s WHERE token = %s"
        values = (1, sanitizeInput(self.token))
        db_connection.cursor().execute(query, values)
        db_connection.commit()
        closeConnection()


def sanitizeInput(inputStr):
    inputStr = re.sub(r"\s+", "", inputStr)
    inputStr = re.sub(r"[^a-zA-Z0-9_]", "", inputStr)
    inputStr = inputStr[:255]
    return inputStr


def initiateConnection():
    global db_connection
    if db_connection is not None:
        return
    db_connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_USERNAME"),
    )
    db_connection.cursor().execute("""
        CREATE DATABASE IF NOT EXISTS `mio` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

        USE `mio`;

        -- Main user table
        CREATE TABLE IF NOT EXISTS `usertable` (
        `id` VARCHAR(255) NOT NULL,
        `passwdhash` VARCHAR(255) NOT NULL,
        `token` VARCHAR(255) NOT NULL,
        `balance` DECIMAL(15,2) DEFAULT 0.00,
        `moneyspent` DECIMAL(15,2) DEFAULT 0.00,
        `playedgames` INT DEFAULT 0,
        `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        UNIQUE KEY `token_UNIQUE` (`token`),
        INDEX `idx_token` (`token`),
        INDEX `idx_id` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """)
    db_connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_USERNAME"),
    )


def closeConnection():
    global db_connection
    db_connection.close()
    db_connection = None


def getHash(mystring):
    return hashlib.sha256(mystring.encode()).hexdigest()


def generateRandomString(length):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
