import os
import tempfile
import logging
import pytest
import unittest

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_user_by_username,
    get_user,
    get_all_users,
    get_all_users_json,
    update_user_username,
    update_username,
    update_name,
    update_email,
    update_password,
    update_faculty,
    delete_user
)

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        new_user = create_user(
            username="testuser",
            firstname="Test",
            lastname="User",
            password="securepassword",
            email="test@example.com",
            faculty="Engineering"
        )
        assert new_user.username == "testuser"

    def test_user_to_json(self):
        new_user = create_user(
            username="testuser",
            firstname="Test",
            lastname="User",
            password="securepassword",
            email="test@example.com",
            faculty="Engineering"
        )
        user_json = new_user.get_json()
        self.assertDictEqual(user_json, {
            "id": 2,
            "username": "testuser",
            "firstname": "Test",
            "lastname": "User",
            "email": "test@example.com",
            "faculty": "Engineering"
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

class UserIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("testuser", "Test", "User", "securepassword", "test@example.com", "Engineering")
        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"

    def test_get_user_by_username(self):
        create_user("uniqueuser", "Unique", "User", "password", "unique@example.com", "Science")
        user = get_user_by_username("uniqueuser")
        assert user is not None
        assert user.email == "unique@example.com"

    def test_get_user(self):
        user = create_user("anotheruser", "Another", "User", "password123", "another@example.com", "Arts")
        fetched_user = get_user(user.ID)
        assert fetched_user is not None
        assert fetched_user.firstname == "Another"

    def test_get_all_users(self):
        create_user("user1", "First", "User", "pass", "user1@example.com", "Business")
        create_user("user2", "Second", "User", "pass", "user2@example.com", "Law")
        users = get_all_users()
        assert len(users) >= 2

    def test_update_user_username(self):
        user = create_user("oldusername", "User", "Name", "password", "user@example.com", "Education")
        success = update_user_username(user.ID, "newusername")
        assert success
        updated_user = get_user(user.ID)
        assert updated_user.username == "newusername"

    def test_update_username(self):
        user = create_user("tempuser", "Temp", "Name", "password", "temp@example.com", "Physics")
        success = update_username(user.ID, "permanentuser")
        assert success
        updated_user = get_user(user.ID)
        assert updated_user.username == "permanentuser"

    def test_update_name(self):
        user = create_user("renameuser", "Old", "Name", "password", "rename@example.com", "Chemistry")
        success = update_name(user.ID, "New", "Name")
        assert success
        updated_user = get_user(user.ID)
        assert updated_user.firstname == "New"
        assert updated_user.lastname == "Name"

    def test_update_email(self):
        user = create_user("emailupdate", "Email", "User", "password", "old@example.com", "Biology")
        success = update_email(user.ID, "new@example.com")
        assert success
        updated_user = get_user(user.ID)
        assert updated_user.email == "new@example.com"

    def test_update_password(self):
        user = create_user("passworduser", "Pass", "Word", "oldpassword", "password@example.com", "IT")
        success = update_password(user.ID, "newpassword")
        assert success
        updated_user = get_user(user.ID)
        assert updated_user.check_password("newpassword")

    def test_update_faculty(self):
        user = create_user("facultyuser", "Faculty", "User", "password", "faculty@example.com", "Medicine")
        success = update_faculty(user.ID, "Nursing")
        assert success
        updated_user = get_user(user.ID)
        assert updated_user.faculty == "Nursing"

    def test_delete_user(self):
        user = create_user("deletethis", "Delete", "User", "password", "delete@example.com", "Fine Arts")
        success = delete_user(user.ID)
        deleted_user = get_user(user.ID)
        assert deleted_user is None
