import sys
import mail
import keys
import flask
import base64
import string
import random
import beveiliging
import password_module
import json, os, signal
from mysql_comands import *
import time
from flask_cors import CORS


app = flask.Flask(__name__)
CORS(app)

pastalock = False
database = sqlite_commands(database_name="main.db")

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
            "user_score_moeilijk": "INT",
            "bage": "INT",
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
                "user_key": str(random.randint(1000, 9999)*int(time.time())/50 ),
            },
        )
        return "account aangemaakt"

@app.route("/login/<username>/<password>")
def login(username, password):
    if database.get_item("users", "username", username):
        if password_module.PasswordUtils.verify_password(
            password, database.get_item("users", "username", username)[2]
        ):
            return str(database.get_item("users", "username", username)[6])
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


@app.route("/leaderboardMoeilijk")
def get_leaderboard_moeilijk():
    """
    Retrieves the leaderboard sorted by user scores in descending order,
    excluding the user_key and password fields.

    Returns:
        json: A JSON response containing the sorted leaderboard without user_key and password fields.
    """
    leaderboard = database.get_all_items_sorted("users", "user_score_moeilijk", descending=True)

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

def set_score(key, score, pasta, waar):
    try:score = int(score)
    except ValueError:return "Ongeldige score, moet een getal zijn.", 400  # Bad Request
    if score > 10000:return "ik ben zoo boos ike ga aleen naar de speeltuin", 400
    if not beveiliging.ontsleutel_en_vergelijken(pasta, str(score)):return "ik ben zoo boos ike ga aleen naar de speeltuin", 400
    oude_score = database.get_item("users", "user_key", key)[4]
    database.edit_item("users", waar, score, "user_key", key)
    return str(oude_score)

@app.route("/set_score/<key>/<score>/<pasta>")
def set_score_eenvoudig(key, score, pasta):
    return set_score(key, score, pasta, "user_score")

@app.route("/set_score_moeilijk/<key>/<score>/<pasta>")
def set_score_moeilijk(key, score, pasta):
    return set_score(key, score, pasta, "user_score_moeilijk")


def verban(key):
    # check if new score is higher
    # UPDATE ER ZIJN PROBLEEMEN MET DE AUTO VERBANNING
    # UIT GEZET OP 22 december 2024
    # WARN: WERKT MOGELIJK NIET
    # TODO: kijk of dit aan mag
    if keys.auto_ban:
        database.edit_item("users", "user_score", 0, "user_key", str(key))
        database.edit_item("users", "password", "verbanen", "user_key", str(key))
        database.edit_item("users", "user_key", "verbannen", "user_key", str(key)) 
    if keys.auto_flag:
        database.edit_item("users", "user_rank", 1, "user_key", str(key))

    return "key {} is verbannen".format(key)


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
    
@app.route("/set_bage/<key>/<bage_num>")
def set_bage(key, bage_num):
    database.edit_item(
        "users",
        "bage",
        bage_num,
        "user_key",
        key,
    )
    return "bage updated"

@app.route("/ADMIN/<admin_key>/update/<user_key>/<type>/<new_value>")
def admin_update(admin_key, user_key, type, new_value):
    if admin_key == keys.admin_key:
        database.edit_item(
            "users",
            type,
            new_value,
            "user_key",
            user_key,
        )
        return "updated"
    else:
        return "incorecte ADMIN key"
    
@app.route("/ADMIN/<admin_key>/delete/<user_key>")
def admin_delete(admin_key, user_key):
    if admin_key == keys.admin_key:
        database.edit_item("users", "user_score", 0, "user_key", str(user_key))
        database.edit_item("users", "password", "verbanen", "user_key", str(user_key))
        database.edit_item("users", "user_key", "verbannen", "user_key", str(user_key))
        return "deleted"
    else:
        return "incorecte ADMIN key"

@app.route("/ADMIN/<admin_key>/unfilterd_list")
def admin_unfilterd_list(admin_key):
    if admin_key == keys.admin_key:
        return database.get_all_items_sorted("users", "user_score", descending=True)
    else:
        return "incorecte ADMIN key"

@app.errorhandler(500)
def internal_error(error):
    # Log the error (optional)
    app.logger.error(f"Server Error: {error}")
    
    # Optionally, trigger an external command to restart the app
    os.system('pm2 restart app')  # Restarts using pm2

    return "Internal Server Error", 500


print()
try:
    get_leaderboard()
except:
    create_default_table("users")

from waitress import serve
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)

