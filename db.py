import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv("~/.c/.env")

dbcon = None

def initiateConnection():
    try:
        print(os.getenv("DB_HOST"))
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

print(initiateConnection())
closeConnection()
