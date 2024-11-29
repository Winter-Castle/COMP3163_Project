from App.database import db
from App.models import Review


def create_review(taggedStudentID, createdByStaffID, details, isPositive=False):
    """
    Create a new review entry.
    """
    new_review = Review(
        taggedStudentID=taggedStudentID,
        createdByStaffID=createdByStaffID,
        details=details,
        isPositive=isPositive
    )
    db.session.add(new_review)
    try:
        db.session.commit()
        return new_review
    except Exception as e:
        print("[ReviewController.create_review] Error:", str(e))
        db.session.rollback()
        return None


def delete_review(ID):
    """
    Delete a review by its ID.
    """
    review = Review.query.filter_by(ID=ID).first()
    if review:
        db.session.delete(review)
        try:
            db.session.commit()
            return True
        except Exception as e:
            print("[ReviewController.delete_review] Error:", str(e))
            db.session.rollback()
            return False
    return False


def update_review_sentiment(ID, isPositive):
    """
    Update the sentiment of a review.
    """
    review = Review.query.filter_by(ID=ID).first()
    if review:
        review.apply_sentiment(isPositive)
        try:
            db.session.commit()
            return review
        except Exception as e:
            print("[ReviewController.update_review_sentiment] Error:", str(e))
            db.session.rollback()
            return None
    return None


def get_review(ID):
    """
    Retrieve a review by its ID.
    """
    return Review.query.filter_by(ID=ID).first()


def get_reviews_by_student(taggedStudentID):
    """
    Retrieve all reviews for a specific student.
    """
    return Review.query.filter_by(taggedStudentID=taggedStudentID).all()


def get_reviews_by_staff(createdByStaffID):
    """
    Retrieve all reviews created by a specific staff member.
    """
    return Review.query.filter_by(createdByStaffID=createdByStaffID).all()


def calculate_average_sentiment(taggedStudentID):
    """
    Calculate the average sentiment for all reviews tagged to a specific student.
    """
    reviews = Review.query.filter_by(taggedStudentID=taggedStudentID).all()
    if not reviews:
        return 0  # No reviews, neutral sentiment
    total_sentiment = sum(1 if review.isPositive else -1 for review in reviews)
    return total_sentiment / len(reviews)


def get_review_statistics(taggedStudentID):
    """
    Get review statistics for a specific student.
    Returns the count of positive and negative reviews.
    """
    reviews = Review.query.filter_by(taggedStudentID=taggedStudentID).all()
    positive_count = sum(1 for review in reviews if review.isPositive)
    negative_count = len(reviews) - positive_count
    return {
        "total_reviews": len(reviews),
        "positive_reviews": positive_count,
        "negative_reviews": negative_count,
    }

