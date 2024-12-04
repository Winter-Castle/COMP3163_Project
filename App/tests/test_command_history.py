import os
import tempfile
import pytest
import logging
import unittest

from datetime import datetime

from App.main import create_app
from App.database import db, create_db
from App.models import commandHistory
from App.controllers import (
    create_command_history,
    get_command_history_byID,
    get_all_command_history
)

'''
   Unit Tests
'''

class CommandHistoryUnitTests(unittest.TestCase):

    def test_new_command_history(self):
        new_command_history = commandHistory(review_id=1)
        assert new_command_history is not None
        assert new_command_history.review_id == 1
        assert isinstance(new_command_history.time, datetime)

    def test_command_history_to_json(self):
        new_command_history = commandHistory(review_id=1)
        new_command_history.id = 1
        command_history_json = new_command_history.get_json()
        self.assertDictEqual(command_history_json, {
            'id': 1,
            'command': new_command_history.history,
        })

'''
    Integration Tests
'''

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
        command_history = create_command_history(1)
        assert command_history is not None
        assert command_history.review_id == 1
        assert isinstance(command_history.time, datetime)

    def test_get_command_history_by_id(self):
        command_history = create_command_history(2)
        fetched_command_history = get_command_history_byID(command_history.id)
        assert fetched_command_history is not None
        assert fetched_command_history.review_id == 2

    def test_get_all_command_history(self):
        create_command_history(3)
        create_command_history(4)
        command_histories = get_all_command_history()
        assert len(command_histories) >= 2

    def test_update_command_history(self):
        command_history = create_command_history(5)
        command_history.review_id = 6
        db.session.commit()
        updated_command_history = get_command_history_byID(command_history.id)
        assert updated_command_history.review_id == 6

    def test_delete_command_history(self):
        command_history = create_command_history(7)
        db.session.delete(command_history)
        db.session.commit()
        deleted_command_history = get_command_history_byID(command_history.id)
        assert deleted_command_history is None
