from abc import ABC, abstractmethod

class SentimentCommand(ABC):
    @abstractmethod
    def execute(self):
        """Execute the sentiment command."""
        pass
