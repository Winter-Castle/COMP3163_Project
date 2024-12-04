from App.models import Staff, Student
from App.database import db
from App.controllers.SentimentCommand import set_and_execute_sentiment_command

# Create a new staff member
def create_staff(username, firstname, lastname, email, password, faculty):
    new_staff = Staff(username=username, firstname=firstname, lastname=lastname,
                      email=email, password=password, faculty=faculty)
    db.session.add(new_staff)
 
    
    try:
        db.session.commit()
        return new_staff
    except Exception as e:
        print(f"[staff.create_staff] Error while creating staff: {str(e)}")
        db.session.rollback()
        return None

# Retrieve a staff member by ID
def get_staff_by_id(id):
    return Staff.query.filter_by(ID=id).first()

# Retrieve a staff member by email
def get_staff_by_email(email):
    return Staff.query.filter_by(email=email).first()

# Retrieve all staff members
def get_all_staff():
    return Staff.query.all()

# Update staff information
def update_staff_info(staff_id, username=None, firstname=None, lastname=None, email=None, password=None):
    staff = get_staff_by_id(staff_id)
    if not staff:
        print(f"[staff.update_staff_info] Staff with ID {staff_id} not found.")
        return False

    if username:
        staff.username = username
    if firstname:
        staff.firstname = firstname
    if lastname:
        staff.lastname = lastname
    if email:
        staff.email = email
    if password:
        staff.password = password

    try:
        db.session.commit()
        return True
    except Exception as e:
        print(f"[staff.update_staff_info] Error while updating staff: {str(e)}")
        db.session.rollback()
        return False

# Delete a staff member
def delete_staff(staff_id):
    staff = get_staff_by_id(staff_id)
    if not staff:
        print(f"[staff.delete_staff] Staff with ID {staff_id} not found.")
        return False

    db.session.delete(staff)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(f"[staff.delete_staff] Error while deleting staff: {str(e)}")
        db.session.rollback()
        return False

# Staff upvote
def staff_upvote(staff_id, student_id):
    """
    Allows a staff member to upvote a student.
    """
    response, _ = set_and_execute_sentiment_command(
        tagged_student_id=student_id,
        created_by_staff_id=staff_id,
        sentiment_type='upvote'
    )

    # Check if response contains a success message
    if response.get("message"):
        return response.get("message")  # Return the success message
    else:
        # Log error and return False if there is an error
        print(f"[staff.staff_upvote] Error: {response.get('error', 'Unknown error occurred.')}")
        return False

# Staff downvote
def staff_downvote(staff_id, student_id):
    """
    Allows a staff member to downvote a student.
    """
    response, _ = set_and_execute_sentiment_command(
        tagged_student_id=student_id,
        created_by_staff_id=staff_id,
        sentiment_type='downvote'
    )

    # Check if response contains a success message
    if response.get("message"):
        return response.get("message")  # Return the success message
    else:
        # Log error and return False if there is an error
        print(f"[staff.staff_downvote] Error: {response.get('error', 'Unknown error occurred.')}")
        return False
