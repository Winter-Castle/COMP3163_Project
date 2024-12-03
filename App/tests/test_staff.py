import pytest
import unittest
from App.main import create_app
from App.database import db, create_db
from App.models import Staff
from App.controllers.staff import (
    create_staff, get_staff_by_id, get_staff_by_email, get_all_staff,
    update_staff_info, delete_staff, staff_upvote, staff_downvote
)
from unittest.mock import patch

'''
   Unit Tests
'''
class StaffControllerUnitTests(unittest.TestCase):

    def test_new_staff(self):
        new_staff = Staff(username="jdoe", firstname="John", lastname="Doe", 
                          email="jdoe@example.com", password="secure123", faculty="Science")
        assert new_staff is not None

    def test_staff_to_json(self):
        new_staff = Staff(username="jdoe", firstname="John", lastname="Doe", 
                          email="jdoe@example.com", password="secure123", faculty="Science")
        new_staff_json = new_staff.to_json()
        self.assertDictEqual(new_staff_json, {
            "ID": None,
            "username": "jdoe",
            "firstname": "John",
            "lastname": "Doe",
            "email": "jdoe@example.com",
            "faculty": "Science"
        })

    @patch('App.controllers.staff_controller.set_and_execute_sentiment_command')
    def test_staff_upvote(self, mock_set_and_execute):
        mock_set_and_execute.return_value = ({"message": "Review upvoted successfully"}, 200)
        response = staff_upvote(1, 1)
        assert response == "Review upvoted successfully"

    @patch('App.controllers.staff_controller.set_and_execute_sentiment_command')
    def test_staff_downvote(self, mock_set_and_execute):
        mock_set_and_execute.return_value = ({"message": "Review downvoted successfully"}, 200)
        response = staff_downvote(1, 1)
        assert response == "Review downvoted successfully"

'''
   Integration Tests
'''

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    """
    Fixture to create an empty database for testing and clean it up afterward.
    """
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class StaffControllerIntegrationTests(unittest.TestCase):

    def test_create_staff(self):
        staff = create_staff("jdoe", "John", "Doe", "jdoe@example.com", "secure123", "Science")
        assert staff is not None

    def test_get_staff_by_id(self):
        staff = create_staff("jdoe", "John", "Doe", "jdoe@example.com", "secure123", "Science")
        retrieved_staff = get_staff_by_id(staff.ID)
        assert retrieved_staff.username == "jdoe"

    def test_get_all_staff(self):
        create_staff("jdoe", "John", "Doe", "jdoe@example.com", "secure123", "Science")
        staff_list = get_all_staff()
        assert len(staff_list) > 0

    def test_update_staff_info(self):
        staff = create_staff("jdoe", "John", "Doe", "jdoe@example.com", "secure123", "Science")
        updated = update_staff_info(staff.ID, firstname="Jane", lastname="Smith")
        assert updated is True
        updated_staff = get_staff_by_id(staff.ID)
        assert updated_staff.firstname == "Jane"

    def test_delete_staff(self):
        staff = create_staff("jdoe", "John", "Doe", "jdoe@example.com", "secure123", "Science")
        deleted = delete_staff(staff.ID)
        assert deleted is True
        assert get_staff_by_id(staff.ID) is None