from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'A1B2C3D4E5F6'

boggle_game = Boggle()

@app.route("/")
def home():
  """show board game"""
  board = boggle_game.make_board()
  h_score = session.get("h_score", 0)
  num_plays = session.get("num_plays", 0)
  session['board'] = board
  

  return render_template("home.html", board = board,
                         num_plays = num_plays,
                         h_score = h_score)

@app.route("/check")
def check():
  """check dictionary for word"""

  word = request.args['word']
  board = session["board"]
  res = boggle_game.check_valid_word(board, word)

  return jsonify({'result': res})

@app.route("/submit-score", methods = ["POST"])
def submit_score():
  print("did the thing")
  """get the score of a play and update the number of plays and high score if needed"""

  score = request.json["score"]
  h_score = session.get("h_score", 0)
  num_plays = session.get("num_plays", 0)

  session["num_plays"] = num_plays + 1
  session["h_score"] = max(score, h_score)

  return jsonify(brokeRecord = score > h_score)