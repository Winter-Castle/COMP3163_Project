from App.models import UpvoteCommand, DownvoteCommand, Review, Staff, Student
from App.models.StudentSentimentInvoker import SentimentInvoker
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
    student =  Student.query.filter_by(ID=tagged_student_id).first()
    staff = Staff.query.filter_by(ID=created_by_staff_id).first()
    
    try:
        # Create a new Review object
        review = Review(
            taggedStudentID=0,
            createdByStaffID=0,
            isPositive=False,  # Default to False, will be updated by the command
            details= ""
        )

        # Determine the sentiment command
        if sentiment_type.lower() == 'upvote':
            command = UpvoteCommand(review)
        elif sentiment_type.lower() == 'downvote':
            command = DownvoteCommand(review)
        else:
            raise Exception({"error": f"Invalid sentiment type: {sentiment_type}"}, 400)
        if  not student and not staff:
            raise Exception ("Student or staff not found", 404)

        
        # Create an invoker and set the command
        invoker = SentimentInvoker()
        invoker.setCommand(command)
        invoker.execute()

        #Update the review object
        review.taggedStudentID = student.ID
        review.createdByStaffID = staff.ID

        # Save the new review to the database
        db.session.add(review)
        db.session.commit()

        return {
            "message": f"Review {sentiment_type}d successfully",
            "review": review.to_json()  # Includes ID and dateCreated automatically
        }, 200

    except Exception as e:
        db.session.rollback()
        # raise Exception({"error": f"{str(e)}"}, 400)
        return {"error": f"Failed to apply sentiment: {str(e)}"}, 400
    
  
def set_and_execute_sentiment_command_obj(tagged_student_id, created_by_staff_id, sentiment_type):
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
    student =  Student.query.filter_by(ID=tagged_student_id).first()
    staff = Staff.query.filter_by(ID=created_by_staff_id).first()
    
    try:
        # Create a new Review object
        review = Review(
            taggedStudentID=0,
            createdByStaffID=0,
            isPositive=False,  # Default to False, will be updated by the command
            details= ""
        )

        # Determine the sentiment command
        if sentiment_type.lower() == 'upvote':
            command = UpvoteCommand(review)
        elif sentiment_type.lower() == 'downvote':
            command = DownvoteCommand(review)
        else:
            raise Exception({"error": f"Invalid sentiment type: {sentiment_type}"}, 400)
        if  not student and not staff:
            raise Exception ("Student or staff not found", 404)

        
        # Create an invoker and set the command
        invoker = SentimentInvoker()
        invoker.setCommand(command)
        invoker.execute()

        #Update the review object
        review.taggedStudentID = student.ID
        review.createdByStaffID = staff.ID

        # Save the new review to the database
        db.session.add(review)
        db.session.commit()

        return review

    except Exception as e:
        db.session.rollback()
        # raise Exception({"error": f"{str(e)}"}, 400)
        return None