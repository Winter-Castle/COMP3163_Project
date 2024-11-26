from App.database import db
from App.models.sentimentCommand import SentimentCommand

from datetime import datetime


class CommandHistory(db.Model):
    __tablename__ = 'command_history'
    id = db.Column(db.Integer, primary_key=True)
    history = db.relationship('SentimentCommand', backref='command_history', lazy=True)
    time = db.Column(db.DateTime, nullable=False)


    def __init__(self, history: SentimentCommand):
        self.history = history
        self.time = datetime.now()

    def get_json(self):
        return{
            'id': self.id,
            'command': self.history,
        }
    