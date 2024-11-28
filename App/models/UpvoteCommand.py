from App.models.sentimentCommand import SentimentCommand
from App.models.review import Review

class UpvoteCommand(SentimentCommand):

    def __init__(self, review: Review):
        self.review = review
        pass 

    def execute(self, review: Review, point_change: float):
        self.review.apply_sentiment(is_positive=True)
        #have to place review logic here 