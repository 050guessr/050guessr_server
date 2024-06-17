from mysql_comands import *
import flask
import base64

app = flask.Flask(__name__)
pastalock = False
database = mysql_comands()


def encode_to_base64(input_string):
    return base64.b64encode(input_string.encode("utf-8"))


def decode_from_base64(input_string):
    return base64.b64decode(input_string).decode("utf-8")


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


@app.route("/maak_acount/<username>/<password>")
def maak_acount(username, password):
    if database.check_and_get_item("users", "username", username):
        return "gebruiker bestaat al"
    else:
        database.insert_into_table(
            "users", {"username": username, "password": password}
        )
        return "account aangemaakt"


@app.route("/login/<username>/<password>")
def login(username, password):
    if database.check_and_get_item("users", "username", username):
        if database.check_and_get_item("users", "password", password):
            return base64.b64encode(encode_to_base64(f"{username}And{password}"))
        else:
            return "verkeerd wachtwoord"
    else:
        return "gebruiker bestaat niet"


# new_database("main")
database.set_database("main")

app.run(debug=True)
