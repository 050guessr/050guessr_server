import sys
import mail
import keys
import flask
import base64
import string
import random
import password_module
import json, os, signal
from mysql_comands import *
from flask_cors import CORS


app = flask.Flask(__name__)
CORS(app)

pastalock = False
database = mysql_comands(password=keys.db_password, user="root")


def encode_to_base64(input_string):
    return base64.b64encode(input_string.encode("utf-8"))

def decode_from_base64(input_string):
    return base64.b64decode(input_string).decode("utf-8")

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
            "email": "VARCHAR(255)",
            "user_score": "INT",
            "user_rank": "INT",
            "user_key": "VARCHAR(255)",
        },
    )
    print(f"Table '{naam}' created successfully!")
    return "created"

@app.route("/maak_acount_V2/<username>/<password>/<email>")
def maak_acount_V2(username, password, email):

    if database.get_item("users", "username", username):
        return "gebruiker bestaat al"
    elif database.get_item("users", "email", email):
        return "email al in gebruik"
    else:
        password = password_module.PasswordUtils.hash_password(password)
        database.insert_into_table(
            "users",
            {
                "username": username,
                "password": password,
                "email": email,
                "user_score": 0,
                "user_rank": 0,
                "user_key": encode_to_base64(f"{username}q{password}"),
            },
        )
        return "account aangemaakt"

@app.route("/maak_acount/<username>/<password>")
def maak_acount(username, password):

    if database.get_item("users", "username", username):
        return "gebruiker bestaat al"
    else:

        database.insert_into_table(
            "users",
            {
                "username": username,
                "password": password_module.PasswordUtils.hash_password(password),
                "email": "NO-MAIL",
                "user_score": 0,
                "user_rank": 0,
                "user_key": encode_to_base64(
                    f"{username}And{password_module.PasswordUtils.hash_password(password)}"
                ),
            },
        )
        return "account aangemaakt"

@app.route("/login/<username>/<password>")
def login(username, password):
    if database.get_item("users", "username", username):
        if password_module.PasswordUtils.verify_password(
            password, database.get_item("users", "username", username)[2]
        ):
            return database.get_item("users", "username", username)[6]
        else:
            return "verkeerd wachtwoord"
    else:
        return "gebruiker bestaat niet"

@app.route("/get_score/<username>")
def get_score(username):
    return str(database.get_item("users", "username", username)[4])

@app.route("/leaderboard")
def get_leaderboard():
    """
    Retrieves the leaderboard sorted by user scores in descending order,
    excluding the user_key and password fields.

    Returns:
        json: A JSON response containing the sorted leaderboard without user_key and password fields.
    """
    leaderboard = database.get_all_items_sorted("users", "user_score", descending=True)

    # Exclude 'user_key' and 'password' fields from the leaderboard data
    filtered_leaderboard = [
        {
            key: value
            for key, value in user.items()
            if key not in ["user_key", "password", "email"]
        }
        for user in leaderboard
    ]

    return flask.jsonify(filtered_leaderboard)

@app.route("/set_score/<key>/<score>")
def set_score(key, score):
    # check if new score is higher
    if (score > 10000):
        return "ik ben zoo boos ike ga aleen naar de speeltuin"
    if database.get_item("users", "user_key", key)[4] < int(score):
        database.edit_item("users", "user_score", int(score), "user_key", str(key))
    
    return str(database.get_item("users", "user_key", key)[4])


@app.route("/verban/<key>")
def verban(key):
    # check if new score is higher
    database.edit_item("users", "user_score", 0, "user_key", str(key))
    database.edit_item("users", "password", "verbanen", "user_key", str(key))
    database.edit_item("users", "user_score", "verbannen", "user_key", str(key))

    return "doei doei"

@app.route("/get_item/<column_name>/<search_value>/<row>")
def get_item(column_name, search_value, row):
    print(row)
    if row == "2" or row == "6" or row == "3":
        return "ik ben zoo boos ike ga aleen naar de speeltuin"
    return str(database.get_item("users", column_name, search_value)[int(row)])

@app.route("/restore_acount/<email>")
def restore_acount(email):
    length = 50
    data = database.get_item("users", "email", email)
    if data:
        letters = string.ascii_letters + string.digits  # No punctuation, just letters and digits
        random_string = ''.join(random.choice(letters) for i in range(length))
        database.edit_item(
            "users",
            "password",
            password_module.PasswordUtils.hash_password(random_string),
            "email",
            email,
        )

        mail.send_mail(email, random_string)
    return email

@app.route("/set_password/<old_password>/<new_password>/<key>")
def set_password(old_password, new_password, key):
    if password_module.PasswordUtils.verify_password(
        old_password, database.get_item("users", "key", key)[2]
    ):
        database.edit_item(
            "users",
            "password",
            password_module.PasswordUtils.hash_password(new_password),
            "key3",
            key,
        )
        return "password updated"
    else:
        return "wrong password"

@app.route("/stop", methods=["GET"])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return json.jsonify({"success": True, "message": "Server is shutting down..."})

@app.errorhandler(500)
def internal_error(error):
    # Log the error (optional)
    app.logger.error(f"Server Error: {error}")
    
    # Optionally, trigger an external command to restart the app
    os.system('pm2 restart app')  # Restarts using pm2

    return "Internal Server Error", 500

print()
database.set_database("main")

app.run(debug=False, port="5000")
