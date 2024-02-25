from flask import Flask, render_template, session
from flask import request, jsonify
from boggle import Boggle

boggle_game = Boggle()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret843028'

ok_words = set()

@app.route('/')
def display_board():
    """Shows boggle game board."""
    board = boggle_game.make_board()
    letters = [ltr for row in board for ltr in row]
    session['board'] = board
    session['letters'] = letters
    return render_template('board.html')

@app.route('/verify', methods=['POST'])
def verify_guess():
    """Verifies if guess is in list of words. Returns result."""
    board = session['board']
    data = request.get_json()
    guess = data['guess']
    if guess not in ok_words or not ok_words:
        ok_words.add(guess)
        result = {"result": boggle_game.check_valid_word(board, guess)}
    else:
        result = {"result": "already-submitted-word"}
    return jsonify(result)

def update_stats(game_score):
    """Update game stats."""
    current_highest = session.get('highest_score')
    if not current_highest:
        session['highest_score'] = game_score
    elif game_score > current_highest :
        session['highest_score'] = game_score
    else:
        session['highest_score'] = current_highest    
    highest_score = {"highest_score": session['highest_score']}
    session['visited'] = 1 if not session.get('visited') else session['visited'] + 1 
    return highest_score


@app.route('/game-over', methods=['POST'])
def get_score():
    """Collect game stats when game-over. Return highest score."""
    data = request.get_json()
    game_score = data['score']
    highest_score = update_stats(game_score)
    return jsonify(highest_score)

