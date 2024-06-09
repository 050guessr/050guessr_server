from flask import Flask

app = Flask(__name__)
score = 0
HI_score_setter = ""
@app.route('/sla_score_op/<spelernaam>/<score1>')
def write(spelernaam, score1):
    global HI_score_setter
    global score
    if int(score) < int(score1) and not int(score1) > 10000 :
        HI_score_setter = spelernaam
        score = score1
    return score

@app.route('/get_HI_score/')
def get_HI_score():
    global HI_score_setter
    global score
    return str(score) +" door "+ str(HI_score_setter)

if __name__ == '__main__':
    app.run(debug=True)

