import keys
from mysql_comands import *
from flask_cors import CORS


database = mysql_comands(password=keys.db_password, user="root")
print("ingelogd op mysql")
try:
    database.create_database("main")
    print("database aangemaakt")
except:
    print("error: database bestaat al")

try:
    database.set_database("main")
    print("database ingesteld")
except:
    print("error: database bestaat niet")

try:
    database.create_table(
        "users",
        {
            "id": "INT AUTO_INCREMENT PRIMARY KEY",
            "username": "VARCHAR(255)",
            "password": "VARCHAR(255)",
            "email": "VARCHAR(255)",
            "user_score": "INT",
            "user_rank": "INT",
            "user_key": "VARCHAR(255)",
        },
    )
    print("tabel aangemaakt")
except:
    print("error: kon tabel niet aan maken")

print("setup klaar")