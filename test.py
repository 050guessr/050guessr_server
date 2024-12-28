import keys
from mysql_comands import *

database = mysql_comands(password=keys.db_password, user="root")
database.set_database("main")
print("ingelogd op mysql")
print(database.get_all_items_sorted("users", "user_score_moeilijk", descending=True))