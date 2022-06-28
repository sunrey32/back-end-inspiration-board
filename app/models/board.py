from app import db

class Board (db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board", lazy=True)

    def to_dict(self):
        if self.board_id is None:
            return {
                "title": self.title,
                "owner": self.owner
            }

        else:
            return {
                "board_id": self.board_id,
                "title": self.title,
                "owner": self.owner
            }