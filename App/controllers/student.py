from App.models import Student
from App.database import db

# Create a new student
def create_student(full_name, degree):
    """
    Create a new student and add them to the database.
    """
    new_student = Student(fullName=full_name, degree=degree)
    db.session.add(new_student)
    
    try:
        db.session.commit()
        return new_student
    except Exception as e:
        print(f"[student.create_student] Error while creating student: {str(e)}")
        db.session.rollback()
        return None

# Retrieve a student by ID
def get_student_by_id(student_id):
    """
    Retrieve a student by their ID.
    """
    return Student.query.filter_by(ID=student_id).first()

# Retrieve a student by name
def get_student_by_full_name(full_name):
    """
    Retrieve a student by their full name.
    """
    return Student.query.filter_by(fullName=full_name).first()

# Retrieve all students
def get_all_students():
    """
    Retrieve all students from the database.
    """
    return Student.query.all()

# Update a student's details
def update_student(student_id, full_name=None, degree=None):
    """
    Update a student's full name and/or degree.
    """
    student = get_student_by_id(student_id)
    if not student:
        print(f"[student.update_student] Student with ID {student_id} not found.")
        return False

    # Update only provided fields
    if full_name:
        student.fullName = full_name
    if degree:
        student.degree = degree

    try:
        db.session.commit()
        return True
    except Exception as e:
        print(f"[student.update_student] Error while updating student: {str(e)}")
        db.session.rollback()
        return False

# Delete a student
def delete_student(student_id):
    """
    Delete a student from the database.
    """
    student = get_student_by_id(student_id)
    if not student:
        print(f"[student.delete_student] Student with ID {student_id} not found.")
        return False

    db.session.delete(student)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print(f"[student.delete_student] Error while deleting student: {str(e)}")
        db.session.rollback()
        return False

# Get a student's reviews
def get_student_reviews(student_id):
    """
    Retrieve all reviews for a given student.
    """
    student = get_student_by_id(student_id)
    if not student:
        print(f"[student.get_student_reviews] Student with ID {student_id} not found.")
        return None
    return student.reviews
