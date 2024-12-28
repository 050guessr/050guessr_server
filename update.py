import keys
from mysql_comands import *
from flask_cors import CORS


database = mysql_comands(password=keys.db_password, user="root")
print("ingelogd op mysql")

try:
    database.set_database("main")
    print("database ingesteld")
except:
    print("error: database bestaat niet")

try:
    database.add_column("users","user_score_moeilijk" ,"INT")
except:
    print("error: iets is misgegaan")

print("update klaar")