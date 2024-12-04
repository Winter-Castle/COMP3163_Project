import pytest
import unittest
from datetime import datetime
from App.main import create_app
from App.database import db, create_db
from App.models import Review, UpvoteCommand, DownvoteCommand
from App.models.StudentSentimentInvoker import SentimentInvoker
from App.controllers import (set_and_execute_sentiment_command, create_review, create_staff, create_student,
    get_staff_by_id, delete_staff, delete_student # createInvoker,getInvoker

)

'''
   Unit Tests
'''
class SentimentCommandUnitTests(unittest.TestCase):

    def test_new_review(self):
        review = create_review(taggedStudentID=1, createdByStaffID=2, isPositive=False, details="")
        assert review is not None

    def test_review_to_json(self):
        review = create_review(taggedStudentID=1, createdByStaffID=2, isPositive=False, details="")
        review_json = review.to_json()
        assert review_json["reviewID"] == 2
        assert review_json["taggedStudentID"] == 1
        assert review_json["createdByStaffID"] == 2
        assert review_json["isPositive"] == False
        assert review_json["details"] == ""

    def test_upvote_command(self):
        review = Review(taggedStudentID=1, createdByStaffID=2, isPositive=False, details="")
        command = UpvoteCommand(review)
        command.execute()
        assert review.isPositive is True

    def test_downvote_command(self):
        review = Review(taggedStudentID=1, createdByStaffID=2, isPositive=True, details="")
        command = DownvoteCommand(review)
        command.execute()
        assert review.isPositive is False

    def test_sentiment_invoker(self):
        review = Review(taggedStudentID=1, createdByStaffID=2, isPositive=False, details="")
        command = UpvoteCommand(review)
        invoker = SentimentInvoker()
        invoker.setCommand(command)
        invoker.execute()
        assert review.isPositive is True
'''
   Integration Tests
'''

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    with app.app_context():
        create_db()
    yield app.test_client()
    with app.app_context():
        db.drop_all()

class SentimentCommandIntegrationTests(unittest.TestCase):

    def test_execute_upvote_command(self):
        staff = create_staff(username="testStaff", firstname="Test", lastname="Staff", email="testStaff@gmail.com", password="testStaffPassword", faculty="Test Faculty")  
        student = create_student(full_name="Test Student", degree="TestDegree")
        assert staff is not None
        assert student is not None
        response = set_and_execute_sentiment_command(student.ID, staff.ID, 'upvote')
        assert response[1] == 200  # HTTP Status code
        assert response[0]['message'] == "Review upvoted successfully"
        assert response[0]['review']['taggedStudentID'] == student.ID
        assert response[0]['review']['isPositive'] is True
       

    def test_execute_downvote_command(self):
        staff = create_staff(username="testStaff", firstname="Test", lastname="Staff", email="testStaff@gmail.com", password="testStaffPassword", faculty="Test Faculty")  
        student = create_student(full_name="Test Student", degree="TestDegree")
        assert staff is not None
        assert student is not None
        response = set_and_execute_sentiment_command(student.ID, staff.ID, 'downvote')
        assert response[1] == 200  # HTTP Status code
        assert response[0]['message'] == "Review downvoted successfully"
        assert response[0]['review']['taggedStudentID'] == student.ID
        assert response[0]['review']['isPositive'] is False
        

    def test_invalid_sentiment_type(self):
        response = set_and_execute_sentiment_command(1, 1, 'neutral')
        assert response[1] == 400  # HTTP Status code
        assert "Invalid sentiment type" in response[0]['error']

    def test_failed_sentiment_execution(self):
        response = set_and_execute_sentiment_command(None, None, 'upvote')  # Invalid input
        assert response[1] == 400  # HTTP Status code
        assert "Failed to apply sentiment" in response[0]['error']