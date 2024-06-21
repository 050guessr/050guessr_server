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
            "user_score": "INT",
            "user_rank": "INT",
            "user_key": "VARCHAR(255)",
        },
    )
    print(f"Table '{naam}' created successfully!")
    return "created"


@app.route("/maak_acount/<username>/<password>")
def maak_acount(username, password):
    if database.get_item("users", "username", username):
        return "gebruiker bestaat al"
    else:
        database.insert_into_table(
            "users",
            {
                "username": username,
                "password": password,
                "user_score": 0,
                "user_rank": 0,
                "user_key": encode_to_base64(f"{username}And{password}"),
            },
        )
        return "account aangemaakt"


@app.route("/login/<username>/<password>")
def login(username, password):
    if database.get_item("users", "username", username):
        if database.get_item("users", "password", password):
            return base64.b64encode(encode_to_base64(f"{username}And{password}"))
        else:
            return "verkeerd wachtwoord"
    else:
        return "gebruiker bestaat niet"


@app.route("/set_score/<key>/<score>")
def set_score(key, score):
    database.edit_item("users", "user_score", score, "user_key", key)

database.set_database("main")
app.run(debug=True)
