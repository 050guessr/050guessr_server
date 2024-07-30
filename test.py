from mysql_comands import *
import mysql_comands
database = mysql_comands.mysql_comands(password="siemsiem")
database.set_database("main")
print(database.get_all_items_sorted("users","score",True))