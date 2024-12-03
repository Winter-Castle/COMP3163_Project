import pytest
import unittest
from datetime import datetime
from App.main import create_app
from App.database import db, create_db
from App.models import Review
from App.controllers import (
    create_review,
    delete_review,
    update_review,
    update_review_sentiment,
    get_review,
    get_reviews_by_student,
    get_reviews_by_staff,
    get_review_statistics,
    get_upvotes_count,
    get_downvotes_count
)

'''
    Unit Tests
'''
class ReviewUnitTests(unittest.TestCase):

    def test_new_review(self):
        newReview = Review(
            taggedStudentID=1,
            createdByStaffID=101,
            details="Great work!",
            isPositive=True
        )
        assert newReview is not None

    def test_review_to_json(self):
        # Create a new Review instance
        newReview = Review(
            taggedStudentID=1,
            createdByStaffID=101,
            details="Great work!",
            isPositive=True
        )
        # Mock the dateCreated field
        newReview.dateCreated = datetime.now()  # Assign current time for consistency

        # Generate JSON and expected output
        newReview_json = newReview.to_json()
        expected_date_created = newReview.dateCreated.strftime("%d-%m-%Y %H:%M")

        # Test the JSON structure
        self.assertDictEqual(newReview_json, {
            "reviewID": None,  # Match the to_json key
            "taggedStudentID": 1,
            "createdByStaffID": 101,
            "dateCreated": expected_date_created,  # Dynamically match date formatting
            "isPositive": True,
            "details": "Great work!"
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

class ReviewIntegrationTests(unittest.TestCase):

    def test_create_review(self):
        review = create_review(1, 101, "Great work!", True)
        assert review is not None
        assert review.taggedStudentID == 1
        assert review.createdByStaffID == 101
        assert review.details == "Great work!"
        assert review.isPositive is True

    def test_get_review(self):
        review = create_review(1, 102, "Needs improvement.", False)
        retrieved_review = get_review(review.ID)
        assert retrieved_review is not None
        assert retrieved_review.ID == review.ID
        assert retrieved_review.details == "Needs improvement."
    
    def test_delete_review(self):
        review = create_review(2, 103, "Good performance.", True)
        result = delete_review(review.ID)
        assert result is True
        deleted_review = get_review(review.ID)
        assert deleted_review is None

    def test_update_review(self):
        review = create_review(3, 104, "Average performance.", False)
        updated_review = update_review(review.ID, 3, 104, "Improved performance.", True)
        assert updated_review is not None
        assert updated_review.details == "Improved performance."
        assert updated_review.isPositive is True

    def test_update_review_sentiment(self):
        review = create_review(4, 105, "Needs significant improvement.", False)
        updated_review = update_review_sentiment(review.ID, True)
        assert updated_review is not None
        assert updated_review.isPositive is True

    def test_get_reviews_by_student(self):
        create_review(5, 106, "Excellent progress.", True)
        reviews = get_reviews_by_student(5)
        assert len(reviews) > 0

    def test_get_reviews_by_staff(self):
        create_review(6, 107, "Average work.", False)
        reviews = get_reviews_by_staff(107)
        assert len(reviews) > 0

    def test_review_statistics(self):
        create_review(7, 108, "Great job!", True)
        create_review(7, 109, "Needs work.", False)
        stats = get_review_statistics(7)
        assert stats["total_reviews"] == 2
        assert stats["positive_reviews"] == 1
        assert stats["negative_reviews"] == 1

    def test_upvote_count(self):
        create_review(8, 110, "Amazing!", True)
        assert get_upvotes_count(8) == 1

    def test_downvote_count(self):
        create_review(9, 111, "Poor performance.", False)
        assert get_downvotes_count(9) == 1
