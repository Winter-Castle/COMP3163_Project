from App.models.SentimentCommand import SentimentCommand
class UpvoteCommand(SentimentCommand):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        pass 

    def execute(self):
        print("Upvoting")

    def execute(self, review: Review, point_change: float):
        review.apply_sentiment(is_positive=True, point_change=point_change)