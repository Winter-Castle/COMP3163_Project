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

#Get Student by ID
def get_student_by_id(studentID):
    student = Student.query.get(studentID)
    if student:
        return student.to_json()
    return None 

def get_studentOBJ_by_id(student_id):
    student = Student.query.get(student_id)
    return student  # Return the object directly, not its JSON representation

def get_student_by_full_name(full_name):
    """
    Retrieve a student by their full name and return their JSON representation.
    """
    student = Student.query.filter_by(fullName=full_name).first()
    if student:
        return student.to_json()
    return None


def get_student_reviews(student_id):
    """
    Retrieve all reviews for a given student and return their JSON representation.
    """
    student = get_studentOBJ_by_id(student_id)
    if not student:
        print(f"[student.get_student_reviews] Student with ID {student_id} not found.")
        return None

    # Assuming student.reviews is a list of review objects that have a method to_json()
    reviews_json = [review.to_json() for review in student.reviews]

    return reviews_json if reviews_json else None

# Retrieve all students
def get_all_students():
    """
    Retrieve all students from the database.
    """
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students = [student.to_json() for student in students]
    return students


def update_student(student_id, full_name=None, degree=None):
    """
    Update a student's full name and/or degree and save the changes to the database.
    """
    student = get_studentOBJ_by_id(student_id)
    if not student:
        print(f"[student.update_student] Student with ID {student_id} not found.")
        return None

    # Update only provided fields
    if full_name:
        student.fullName = full_name
    if degree:
        student.degree = degree

    try:
        db.session.commit()
        return student  # Return the updated student object
    except Exception as e:
        print(f"[student.update_student] Error while updating student: {str(e)}")
        db.session.rollback()
        return None


# Delete a student
def delete_student(student_id):
    """
    Delete a student from the database.
    """
    student = get_studentOBJ_by_id(student_id)
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
    student = get_studentOBJ_by_id(student_id)
    if not student:
        print(f"[student.get_student_reviews] Student with ID {student_id} not found.")
        return None
    return student.reviews
