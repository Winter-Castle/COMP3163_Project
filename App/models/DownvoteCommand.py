class DownvoteCommand(SentimentCommand):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        pass 

    def execute(self):
        print("Downvoting")