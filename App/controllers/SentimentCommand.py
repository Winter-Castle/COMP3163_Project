from App.models import UpvoteCommand, DownvoteCommand, StudentSentimentInvoker, Review
from App.database import db


def set_and_execute_sentiment_command(tagged_student_id, created_by_staff_id, sentiment_type):
    """
    Create a new review object and apply sentiment using the command pattern.
    
    Args:
        tagged_student_id (int): The ID of the student being reviewed.
        created_by_staff_id (int): The ID of the staff creating the review.
        sentiment_type (str): The type of sentiment ('upvote' or 'downvote').
        details (str): Additional details for the review.
        
    Returns:
        dict: JSON response indicating success or failure.
    """
    try:
        # Create a new Review object
        review = Review(
            taggedStudentID=tagged_student_id,
            createdByStaffID=created_by_staff_id,
            isPositive=False,  # Default to False, will be updated by the command
            details= ""
        )
        
        # Determine the sentiment command
        if sentiment_type == 'upvote':
            command = UpvoteCommand(review)
        elif sentiment_type == 'downvote':
            command = DownvoteCommand(review)
        else:
            return {"error": "Invalid sentiment type"}, 400

        # Create an invoker and set the command
        invoker = StudentSentimentInvoker()
        invoker.setCommand(command)
        invoker.execute()

        # Save the new review to the database
        db.session.add(review)
        db.session.commit()

        return {
            "message": f"Review {sentiment_type}d successfully",
            "review": review.to_json()  # Includes ID and dateCreated automatically
        }, 200

    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to apply sentiment: {str(e)}"}, 500
    
  
