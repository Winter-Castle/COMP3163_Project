class UpvoteCommand(SentimentCommand):

    _instance = None

    @classmethod
    def __init__(self, review_id, user_id):
        self.review_id = review_id
        self.user_id = user_id