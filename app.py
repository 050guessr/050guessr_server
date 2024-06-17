from mysql_comands import *
import flask

app = flask.Flask(__name__)
pastalock = False
database = mysql_comands()

def new_database(naam):
    global pastalock
    if pastalock:
        print(pastalock)
        return "locked"
    database.create_database(naam)
    return "gemaakt"

def set_database(naam):
    global pastalock
    if pastalock:
        return "locked"
    database.set_database(naam)
    return "gezet"

def create_default_table(naam):
    global pastalock
    if pastalock:
        return "locked"
    database.create_table(
        naam,
        {
            "id": "INT AUTO_INCREMENT PRIMARY KEY",
            "username": "VARCHAR(255)",
            "password": "VARCHAR(255)",
        },
    )
    return "created"


app.run()
