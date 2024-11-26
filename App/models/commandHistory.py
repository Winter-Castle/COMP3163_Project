from App.database import db

class CommandHistory(db.Model):
    __tablename__ = 'command_history'
    id = db.Column(db.Integer, primary_key=True)
    history = db.relationship('SentimentCommand', backref='command_history', lazy=True)



    def __init__(self, history):
        self.id = id
        self.history = history

    def get_json(self):
        return{
            'id': self.id,
            'command': self.history,
        }
    