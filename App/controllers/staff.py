from App.models import Staff, Student, UpvoteCommand, DownvoteCommand
from App.database import db

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
    staff_member = get_staff_by_id(staff_id)
    student = Student.query.filter_by(ID=student_id).first()

    if staff_member and student:
        upvote = UpvoteCommand(staff_member, student)
        try:
            upvote.execute()  # Execute the upvote command
            return True
        except Exception as e:
            print(f"[staff.staff_upvote] Error while upvoting: {str(e)}")
            return False
    print("[staff.staff_upvote] Staff or Student not found.")
    return False

# Staff downvote
def staff_downvote(staff_id, student_id):
    """
    Allows a staff member to downvote a student.
    """
    staff_member = get_staff_by_id(staff_id)
    student = Student.query.filter_by(ID=student_id).first()

    if staff_member and student:
        downvote = DownvoteCommand(staff_member, student)
        try:
            downvote.execute()  # Execute the downvote command
            return True
        except Exception as e:
            print(f"[staff.staff_downvote] Error while downvoting: {str(e)}")
            return False
    print("[staff.staff_downvote] Staff or Student not found.")
    return False




