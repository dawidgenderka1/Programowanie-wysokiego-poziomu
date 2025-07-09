import random
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GameResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    rounds = db.Column(db.Integer)


class MemoryGame:
    def __init__(self, size=4):
        self.size = size
        self.cards = self._generate_cards()
        self.revealed = [[False]*size for _ in range(size)]
        self.rounds = 0
        self.matched_pairs = 0

    def _generate_cards(self):
        emoji_list = ['🐶', '🐱', '🐭', '🦊', '🐻', '🐼', '🐨', '🐸', 
                  '🐵', '🐧', '🐦', '🐤', '🦄', '🐝', '🐙', '🦕']
    
        num_pairs = (self.size * self.size) // 2
        selected = random.sample(emoji_list, num_pairs)
        card_values = selected * 2
        random.shuffle(card_values)
        return [card_values[i * self.size:(i + 1) * self.size] for i in range(self.size)]


    def reveal(self, x1, y1, x2, y2):
        if self.revealed[x1][y1] or self.revealed[x2][y2]:
            return False
        self.rounds += 1
        if self.cards[x1][y1] == self.cards[x2][y2]:
            self.revealed[x1][y1] = True
            self.revealed[x2][y2] = True
            self.matched_pairs += 1
            return True
        return False

    def is_game_over(self):
        return self.matched_pairs == (self.size * self.size) // 2
