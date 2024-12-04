from App.database import db
from App.models.sentimentCommand import SentimentCommand 

class SentimentInvoker(SentimentCommand):
# class StudentSentimentInvoker():
    id = db.Column(db.Integer, primary_key=True)
    
    def __init__(self):
        self.command = None 

    def setCommand(self, command: SentimentCommand):
        self.command = command

    def execute(self):
        if self.command is not None:
            self.command.execute()
        else:
            print("No command set")
