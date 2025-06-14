import hashlib
import os
import re
import secrets
import string

import mysql.connector
from dotenv import load_dotenv
from mysql.connector.abstracts import MySQLConnectionAbstract

load_dotenv(os.environ.get("HOME", "/home/k24_c/mio") + "/.c/.env")


def sanitizeInput(input_str: str):
    input_str = re.sub(r"\s+", "", input_str)
    input_str = re.sub(r"[^a-zA-Z0-9_]", "", input_str)
    input_str = input_str[:255]
    return input_str


class DbConn:
    db_connection: MySQLConnectionAbstract | None = None
    num_active: int = 0

    def __init__(self):
        self.num_active += 1
        if self.db_connection is None:
            self.db_connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USERNAME"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_USERNAME"),
            )
            self.db_connection.cursor().execute("""
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

    def __del__(self):
        self.num_active -= 1
        if self.num_active == 0 and self.db_connection is not None and not self.db_connection:
            self.db_connection.close()
            self.db_connection = None

    def get_user_data(self, username: str, what: str) -> tuple | None:
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT %s FROM usertable WHERE id = %s", (what, sanitizeInput(username),))
        return cursor.fetchone()

    def user_exists(self, username: str) -> bool:
        # https://stackoverflow.com/a/4254003
        return self.get_user_data(username, "COUNT(1)") is not None

    def user_balance(self, username: str) -> int:
        return self.get_user_data(username, "balance")[0]

    def user_token(self, username: str) -> int:
        return self.get_user_data(username, "token")[0]

    def user_password_hash(self, username: str) -> int:
        return self.get_user_data(username, "passwdhash")[0]

    def create_user(self, username: str, password_hash: str, token: str):
        query = """
        INSERT INTO usertable (id, passwdhash, token)
        VALUES (%s, %s, %s)
        """
        values = (
            sanitizeInput(username),
            sanitizeInput(password_hash),
            sanitizeInput(token),
        )
        self.db_connection.cursor().execute(query, values)

    def update_user_data(self, username: str, data: str, values: tuple = ()):
        query = f"UPDATE usertable SET {data} WHERE id = %s"
        values = values + (sanitizeInput(username),)
        self.db_connection.cursor().execute(query, values)

    def update_user_balance(self, username: str, diff: int):
        self.update_user_data(username, "balance = balance + %s", (diff,))

    def update_user_spent(self, username: str, spent: int):
        self.update_user_data(username, "moneyspent = moneyspent + %s", (spent,))

    def update_played_games(self, username: str):
        self.update_user_data(username, "playedgames = playedgames + 1")

    def update_user_token(self, username: str, token: str):
        self.update_user_data(username, "token = %s", (sanitizeInput(token),))


class User:
    @staticmethod
    def register(cls, username, password_hash):
        db = DbConn()
        token = get_hash(generate_random_string(255))
        db.create_user(username, password_hash, token)
        return cls(username, password_hash, no_check=True)

    def __init__(self, username, password_hash, no_check: bool = False):
        self.username = username
        self.password_hash = password_hash
        self._token = None
        self.db = DbConn()
        if not no_check:
            if not self.db.user_exists(username):
                raise ValueError("User does not exist")
            if self.db.user_password_hash(self.username) != password_hash:
                raise ValueError("Invalid password")

    def view_info(self):
        return (
            f"ID : {self.username}\n"
            f"Token : {self.token}\n"
            f"Password Hash : {self.password_hash}"
        )

    @property
    def token(self):
        if self._token is None:
            self._token = self.db.user_token(self.username)
        return self._token

    @token.setter
    def token(self, value):
        self._token = value
        self.db.update_user_token(self.username, value)

    def balance(self):
        return self.db.user_balance(self.username)

    def update_balance(self, balance_modifier):
        self.db.update_user_balance(self.username, balance_modifier)
        if balance_modifier < 0:
            self.db.update_user_spent(self.username, -balance_modifier)

    def update_playedgames(self):
        self.db.update_played_games(self.username)


def get_hash(mystring):
    return hashlib.sha256(mystring.encode()).hexdigest()


def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
