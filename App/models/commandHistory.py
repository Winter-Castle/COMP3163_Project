from App.database import db
from datetime import datetime

class CommandHistory(db.Model):
    __tablename__ = 'command_history'
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.ID'), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, review_id):
        self.review_id = review_id

    def get_json(self):
        return {
            'id': self.id,
            'review_id': self.review_id,
            'time': self.time.isoformat(),
        }
