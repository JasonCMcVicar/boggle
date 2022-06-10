from flask import Flask, request, render_template, jsonify
from uuid import uuid4
import json

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}

@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return json.dumps({"gameId": game_id, "board": game.board})

@app.post("/api/score-word")
def score_word():
    """ Accessed the gameId and word from the json request. 
        If the word isn't on the board, return json with result:'not-on-board'.
        If not word, return json with result:'not-word'.
        If word is on board and a valid word, return json with result:'ok'. 
    """
    data = request.json
    game_id = data["gameId"]
    word = data["word"]
    game = games[game_id]

    if not game.check_word_on_board(word):
        return jsonify({"result":"not-on-board"})
    elif not game.is_word_in_word_list(word):
        return jsonify({"result":"not-word"})
    else:
        return jsonify({"result":"ok"})
