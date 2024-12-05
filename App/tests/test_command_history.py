import pytest
import unittest
from datetime import datetime
from App.main import create_app  # Import create_app correctly
from App.models.commandHistory import CommandHistory  # Correctly import CommandHistory
from App.database import db, create_db
from App.controllers import (
    create_command_history,
    get_command_history_byID,
    get_all_command_history,
)


# Unit Tests for CommandHistory Model
class CommandHistoryUnitTests(unittest.TestCase):
    def test_create_command_history(self):
        # Create a CommandHistory instance
        review_id = 1
        new_command_history = CommandHistory(review_id=review_id)
        
        # Manually set the time to simulate database behavior
        new_command_history.time = datetime.utcnow()

        # Assert that the object is not None
        assert new_command_history is not None

        # Assert the review_id is correctly assigned
        assert new_command_history.review_id == review_id

        # Assert that the time is correctly set
        assert isinstance(new_command_history.time, datetime)

    def test_command_history_to_dict(self):
        # Create a CommandHistory instance
        review_id = 1
        new_command_history = CommandHistory(review_id=review_id)
        
        # Manually set the time
        new_command_history.time = datetime.utcnow()

        # Simulate saving to the database and ID generation
        new_command_history.id = 1

        # Get the dictionary representation of the command history
        command_history_dict = new_command_history.to_dict()

        # Assert the dictionary format
        self.assertDictEqual(command_history_dict, {
            'id': 1,
            'review_id': 1,
            'time': new_command_history.time.isoformat(),
        })


# Integration Tests for CommandHistory Controller
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


class CommandHistoryIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        self.app_context = self.app.app_context()
        self.app_context.push()
        create_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_command_history(self):
        # Create a command history entry
        review_id = 1
        command_history = create_command_history(review_id)

        # Assert that the command history was created
        assert command_history is not None
        assert command_history.review_id == review_id
        assert isinstance(command_history.time, datetime)

    def test_get_command_history_by_id(self):
        # Create a command history entry
        review_id = 2
        command_history = create_command_history(review_id)

        # Retrieve the command history by its ID
        fetched_command_history = get_command_history_byID(command_history.id)

        # Assert the fetched command history matches the created one
        assert fetched_command_history is not None
        assert fetched_command_history.id == command_history.id
        assert fetched_command_history.review_id == review_id

    def test_get_all_command_history(self):
        # Create multiple command history entries
        create_command_history(1)
        create_command_history(2)

        # Retrieve all command histories
        command_histories = get_all_command_history()

        # Assert that at least 2 command history records exist
        assert len(command_histories) >= 2
        assert all(isinstance(ch, CommandHistory) for ch in command_histories)
