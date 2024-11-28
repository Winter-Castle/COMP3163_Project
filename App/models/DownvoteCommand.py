from App.models.sentimentCommand import SentimentCommand
from App.models.review import Review

class DownvoteCommand(SentimentCommand):
    
    def __init__(self, review: Review):
        self.review = review
        pass 

    def execute(self):
        self.review.apply_sentiment(is_positive=False)
        
