from App.database import db
from App.models import Review

# Create a new review
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

# Delete a review
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

# Update a review (all fields)
def update_review(ID, taggedStudentID, createdByStaffID, details, isPositive):
    """
    Update all fields of a review.

    Args:
        ID (int): The ID of the review to update.
        taggedStudentID (int): The new student ID to tag.
        createdByStaffID (int): The new staff ID creating the review.
        details (str): The updated review details.
        isPositive (bool): The updated sentiment.

    Returns:
        Review: The updated review object, or None if an error occurred.
    """
    review = Review.query.filter_by(ID=ID).first()
    if review:
        review.taggedStudentID = taggedStudentID
        review.createdByStaffID = createdByStaffID
        review.details = details
        review.isPositive = isPositive
        try:
            db.session.commit()
            return review
        except Exception as e:
            print("[ReviewController.update_review] Error:", str(e))
            db.session.rollback()
            return None
    return None

# Update only the sentiment of a review
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

# Retrieve a review by its ID
def get_review(ID):
    """
    Retrieve a review by its ID.
    """
    return Review.query.filter_by(ID=ID).first()

# Retrieve all reviews for a specific student
def get_reviews_by_student(taggedStudentID):
    """
    Retrieve all reviews for a specific student.
    """
    return Review.query.filter_by(taggedStudentID=taggedStudentID).all()

# Retrieve all reviews created by a specific staff member
def get_reviews_by_staff(createdByStaffID):
    """
    Retrieve all reviews created by a specific staff member.
    """
    return Review.query.filter_by(createdByStaffID=createdByStaffID).all()

# Get review statistics for a student
def get_review_statistics(taggedStudentID):
    """
    Get review statistics for a specific student.
    Returns the total number of reviews, positive reviews, and negative reviews.

    Args:
        taggedStudentID (int): The ID of the student.

    Returns:
        dict: A dictionary containing:
            - total_reviews: Total number of reviews.
            - positive_reviews: Number of positive reviews (upvotes).
            - negative_reviews: Number of negative reviews (downvotes).
    """
    positive_count = get_upvotes_count(taggedStudentID)
    negative_count = get_downvotes_count(taggedStudentID)
    total_reviews = positive_count + negative_count

    return {
        "total_reviews": total_reviews,
        "positive_reviews": positive_count,
        "negative_reviews": negative_count,
    }

# Get the count of upvotes (positive reviews) for a student
def get_upvotes_count(taggedStudentID):
    """
    Get the total count of upvotes (positive reviews) for a specific student.

    Args:
        taggedStudentID (int): The ID of the student.

    Returns:
        int: The number of positive reviews for the student.
    """
    return Review.query.filter_by(taggedStudentID=taggedStudentID, isPositive=True).count()

# Get the count of downvotes (negative reviews) for a student
def get_downvotes_count(taggedStudentID):
    """
    Get the total count of downvotes (negative reviews) for a specific student.

    Args:
        taggedStudentID (int): The ID of the student.

    Returns:
        int: The number of negative reviews for the student.
    """
    return Review.query.filter_by(taggedStudentID=taggedStudentID, isPositive=False).count()
