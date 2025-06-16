#!/home/k24_c/mio/.homepage/c/run_cgi
import hashlib
import os
import re
import secrets
import string
from logging import getLogger
from typing import Self

import mysql.connector
from dotenv import load_dotenv
from mysql.connector.abstracts import MySQLConnectionAbstract

load_dotenv(os.environ.get("HOME", "/home/k24_c/mio") + "/.c/.env")
logger = getLogger()


def sanitize_input(input_str: str):
    input_str = re.sub(r"\s+", "", input_str)
    input_str = re.sub(r"[^a-zA-Z0-9_]", "", input_str)
    return input_str[:255]


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
                `balance` INT DEFAULT 0,
                `moneyspent` INT DEFAULT 0,
                `playedgames` INT DEFAULT 0,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                `admin` BOOL DEFAULT 0,
                PRIMARY KEY (`id`),
                UNIQUE KEY `token_UNIQUE` (`token`),
                INDEX `idx_token` (`token`),
                INDEX `idx_id` (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)
            self.db_connection.commit()

    def __del__(self):
        self.num_active -= 1
        if self.num_active == 0 and self.db_connection is not None and not self.db_connection:
            self.db_connection.close()
            self.db_connection = None

    def get_user_data(self, username: str, what: str) -> tuple | None:
        cursor = self.db_connection.cursor()
        cursor.execute(f"SELECT {what} FROM usertable WHERE id = %s", (sanitize_input(username),))  # noqa: S608
        return cursor.fetchone()

    def user_exists(self, username: str) -> bool:
        # https://stackoverflow.com/a/4254003
        logger.info(self.get_user_data(username, "1"))
        return self.get_user_data(username, "1") is not None

    def user_balance(self, username: str) -> int:
        return self.get_user_data(username, "balance")[0]

    def user_token(self, username: str) -> int:
        return self.get_user_data(username, "token")[0]

    def user_password_hash(self, username: str) -> int:
        return self.get_user_data(username, "passwdhash")[0]

    def user_admin(self, username: str):
        return self.get_user_data(username, "admin")[0]

    def get_detailed_user_data(self, username: str):
        """Get detailed data for a specific user"""
        row = self.get_user_data(username, "id, balance, moneyspent, playedgames, created_at, updated_at, admin")
        if not row:
            raise ValueError("User not found")

        user_data = {
            "username": row[0],
            "balance": row[1],
            "moneyspent": row[2],
            "playedgames": row[3],
            "created_at": row[4].strftime("%Y-%m-%d %H:%M:%S") if row[4] else "",
            "updated_at": row[5].strftime("%Y-%m-%d %H:%M:%S") if row[5] else "",
            "admin": bool(row[6]),
        }
        return user_data

    def get_token_username(self, token: str) -> str | None:
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM usertable WHERE token = %s", (sanitize_input(token),))
        token = cursor.fetchone()
        return token[0] if token is not None else None

    def get_all_users_data(self):
        cursor = self.db_connection.cursor()
        cursor.execute("""
            SELECT id, balance, moneyspent, playedgames, created_at, admin
            FROM usertable 
            ORDER BY created_at DESC
            """)
        rows = cursor.fetchall()

        users_data = []
        for row in rows:
            user_data = {
                "username": row[0],
                "balance": row[1],
                "moneyspent": row[2],
                "playedgames": row[3],
                "created_at": row[4].strftime("%Y-%m-%d %H:%M:%S") if row[4] else "",
                "admin": bool(row[5]),
            }
            users_data.append(user_data)

        return users_data

    def create_user(self, username: str, password_hash: str, token: str):
        query = """
        INSERT INTO usertable (id, passwdhash, token)
        VALUES (%s, %s, %s)
        """
        values = (
            sanitize_input(username),
            sanitize_input(password_hash),
            sanitize_input(token),
        )
        self.db_connection.cursor().execute(query, values)
        self.db_connection.commit()

    def update_user_data(self, username: str, data: str, values: tuple = ()):
        # I know it is sql-injection prone, but data comes from 5 lines below
        query = f"UPDATE usertable SET {data} WHERE id = %s"  # noqa: S608
        values = (*values, sanitize_input(username))
        self.db_connection.cursor().execute(query, values)
        self.db_connection.commit()

    def update_user_balance(self, username: str, diff: int):
        if diff == 0:
            return
        self.update_user_data(username, "balance = balance + %s", (diff,))

    def update_user_spent(self, username: str, spent: int):
        self.update_user_data(username, "moneyspent = moneyspent + %s", (spent,))

    def update_played_games(self, username: str):
        self.update_user_data(username, "playedgames = playedgames + 1")

    def update_user_token(self, username: str, token: str):
        self.update_user_data(username, "token = %s", (sanitize_input(token),))

    def update_admin(self, username: str, status: bool):
        self.update_user_data(username, "admin = %s", (int(status),))


class User:
    @classmethod
    def register(cls, username: str, password: str) -> Self:
        db = DbConn()
        if db.user_exists(username):
            raise ValueError("User exists")
        token = get_hash(generate_random_string(255))
        db.create_user(username, get_hash(password), token)
        db.update_user_balance(username, 100)
        return cls(username, token)

    @classmethod
    def auth(cls, token: str) -> Self:
        db = DbConn()
        username = db.get_token_username(token)
        if username is None:
            raise ValueError("Invalid token")
        return cls(username, token)

    @classmethod
    def login(cls, username: str, password: str) -> Self:
        username = username.strip()
        password = password.strip()
        db = DbConn()
        if not db.user_exists(username):
            raise ValueError("Invalid username")
        if get_hash(password) != db.user_password_hash(username):
            logger.info((get_hash(password), db.user_password_hash(username)))
            raise ValueError("Invalid password")
        return cls(username)

    def __init__(self, username: str, token: str | None = None):
        self.db = DbConn()
        self.username = username
        self._token = token

    def view_info(self) -> str:
        return (
            f"ID : {self.username}\nToken : {self.token}\nPassword Hash : {self.db.user_password_hash(self.username)}"
        )

    @property
    def token(self):
        if self._token is None:
            self._token = self.db.user_token(self.username)
        return self._token

    @token.setter
    def token(self, value: str):
        self._token = value
        self.db.update_user_token(self.username, value)

    @property
    def balance(self) -> int:
        return self.db.user_balance(self.username)

    @property
    def admin(self) -> bool:
        return self.db.user_admin(self.username)

    @admin.setter
    def admin(self, value: bool):
        if value != self.admin:
            self.db.update_admin(self.username, value)

    def update_balance(self, balance_modifier: int):
        if balance_modifier < 0:
            if self.balance < abs(balance_modifier):
                raise ValueError("Too broke. lamo")
            self.db.update_user_spent(self.username, -balance_modifier)
        self.db.update_user_balance(self.username, balance_modifier)

    def update_played_games(self):
        self.db.update_played_games(self.username)


def get_hash(mystring: str) -> str:
    return hashlib.sha256(mystring.encode()).hexdigest()


def generate_random_string(length: int) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def get_all_users_data():
    """Fetch all users data for admin panel"""
    db = DbConn()
    cursor = db.db_connection.cursor()

    # Get all users with their stats
    query = """
    SELECT id, balance, moneyspent, playedgames, created_at, admin
    FROM usertable 
    ORDER BY created_at DESC
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    users_data = []
    for row in rows:
        user_data = {
            "username": row[0],
            "balance": row[1],
            "moneyspent": row[2],
            "playedgames": row[3],
            "created_at": row[4].strftime("%Y-%m-%d %H:%M:%S") if row[4] else "",
            "admin": bool(row[5]),
        }
        users_data.append(user_data)

    return {"users": users_data}
