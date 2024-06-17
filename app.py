from mysql_comands import *
import flask
app = flask.Flask(__name__)
database = mysql_comands()
#database.create_database("main")
database.set_database("main")
#database.create_table("users", {"id": "INT AUTO_INCREMENT PRIMARY KEY", "username": "VARCHAR(255)", "password": "VARCHAR(255)"})
database.insert_into_table("users", {"username": "admin", "password": "admin"})
if database.check_and_get_item("users", "username", "admin"):
  print(database.check_and_get_item("users", "username", "admin"))
  database.edit_item("users", "password", input("Enter new password: "), "username", "admin")