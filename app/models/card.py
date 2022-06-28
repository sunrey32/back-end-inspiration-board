from app import db

class Card (db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"))
    board = db.relationship("Board", back_populates="cards", lazy=True)

    # def likes_count(self):
    #     return self.completed_at is not None

    def to_dict(self):

        if self.card_id is None:
            return {
                "message": self.message,
                "likes_count": self.likes_count,
                "board_id": self.board_id
        }
        else:
            return {
                "card_id": self.card_id,
                "message": self.message,
                "likes_count": self.likes_count,
                "board_id": self.board_id
            }