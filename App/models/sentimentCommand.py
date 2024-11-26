from App.database import db

class SentimentCommand(db.Model):
    __tablename__ = 'sentiment_command'
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(50))


    def __init__(self, command):
        self.id = id
        self.command = command

    def get_json(self):
        return{
            'id': self.id,
            'command': self.command,
        }
    