from mysql_comands import *
import flask
import base64
from flask_cors import CORS



app = flask.Flask(__name__)
CORS(app)

pastalock = False
database = mysql_comands(password="siemsiem")

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
            return encode_to_base64(f"{username}And{password}") #mysql_comands.get_item("users","key","username",username)
        else:
            return "verkeerd wachtwoord"
    else:
        return "gebruiker bestaat niet"

@app.route("/get_score/<username>")
def get_score(username):
    return str(database.get_item("users", "username", username)[3])

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
        {key: value for key, value in user.items() if key not in ["user_key", "password"]}
        for user in leaderboard
    ]
    
    return flask.jsonify(filtered_leaderboard)


@app.route("/set_score/<key>/<score>")
def set_score(key, score):
    database.edit_item("users","user_score",int(score),"user_key",str(key))
    return str(database.get_item("users", "user_key", key)[3])
database.set_database("main")
app.run(debug=True)
