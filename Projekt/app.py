from flask import Flask, render_template, request, session, jsonify
from models import MemoryGame, db, GameResult

app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memory.db'
db.init_app(app)

with app.app_context():
    db.create_all()


def load_game():
    game_data = session.get('game')
    if not game_data:
        return MemoryGame()
    game = MemoryGame()
    game.__dict__.update(game_data)
    return game

@app.route('/')
def index():
    game = MemoryGame()
    session['game'] = game.__dict__
    return render_template('index.html', size=game.size)

@app.route('/play', methods=['POST'])
def play():
    data = request.json
    x1, y1 = data['x1'], data['y1']
    x2, y2 = data['x2'], data['y2']
    game = load_game()
    matched = game.reveal(x1, y1, x2, y2)
    over = game.is_game_over()
    session['game'] = game.__dict__
    
    return jsonify({
        'matched': matched,
        'game_over': over,
        'rounds': game.rounds,
        'revealed': game.revealed
    })

@app.route('/get_cards')
def get_cards():
    game = load_game()
    return jsonify({
        'cards': game.cards,
        'revealed': game.revealed
    })

@app.route('/results')
def results():
    results = GameResult.query.order_by(GameResult.rounds.asc()).all()
    return render_template('results.html', results=results)


@app.route('/save_result', methods=['POST'])
def save_result():
    data = request.get_json()
    username = data.get('username')
    rounds = data.get('rounds')

    if username and rounds is not None:
        result = GameResult(username=username, rounds=rounds)
        db.session.add(result)
        db.session.commit()
        return jsonify({'message': 'Result saved'})
    return jsonify({'message': 'Invalid data'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

