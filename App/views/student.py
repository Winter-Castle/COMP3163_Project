from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, current_user
from App.models import Student, User
from App.controllers import get_student_by_id, get_student_reviews, update_student, delete_student, get_all_students, get_all_students_json, create_student, get_student_by_full_name

student_views = Blueprint('student_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''
#changes I made for postman
@student_views.route('/api/student', methods=['POST'])
def create_student_endpoint():
    data = request.json
    
    # Check if required fields are in the request
    if not data or 'full_name' not in data or 'degree' not in data:
        return jsonify({'message': 'Missing required fields: full_name or degree'}), 400
    
    # Call the function to create the student if data is valid
    create_student(data['full_name'], data['degree'])
    
    return jsonify({'message': f"student {data['full_name']} created"}), 201


@student_views.route('/api/student/all', methods=['GET'])
def get_users_action():
    users = get_all_students_json()
    return jsonify(users)

# Get a student by ID
@student_views.route('/api/student/<int:studentID>', methods=['GET'])
#@jwt_required()
def get_student_action(studentID):
    student = get_student_by_id(studentID)
    if student:
        return jsonify(student), 200
    return jsonify({'Error': 'Student not found'}), 404

# Get a student by full name
@student_views.route('/api/student/name/<string:full_name>', methods=['GET'])
# @jwt_required()  # Uncomment if authentication is required
def get_student_by_full_name_action(full_name):
    student = get_student_by_full_name(full_name)
    if student:
        return jsonify(student), 200
    return jsonify({'Error': 'Student not found'}), 404

# Update a student's details
@student_views.route('/api/student/<int:student_id>', methods=['PUT'])
# @jwt_required()  # Uncomment if authentication is required
def update_student_action(student_id):
    data = request.get_json()
    full_name = data.get('full_name')
    degree = data.get('degree')

    if update_student(student_id, full_name=full_name, degree=degree):
        return jsonify({'Message': 'Student updated successfully'}), 200
    return jsonify({'Error': 'Failed to update student. Student not found or error occurred.'}), 400

@student_views.route('/api/student/<int:student_id>', methods=['DELETE'])
def delete_student_action(student_id):
    """
    Handle deleting a student by their ID.
    """
    deleted = delete_student(student_id)  # Call the delete_student function from the controller

    if deleted:
        return jsonify({'Message': 'Student deleted successfully'}), 200
    return jsonify({'Error': 'Failed to delete student. Student not found or error occurred.'}), 400


# Get a student's reviews
@student_views.route('/api/student/<int:student_id>/reviews', methods=['GET'])
def get_student_reviews_action(student_id):
    reviews = get_student_reviews(student_id)
    if reviews is not None:
        return jsonify(reviews), 200
    return jsonify({'Error': 'Student not found or no reviews available'}), 404


######

@student_views.route('/StudentHome', methods=['GET'])
@login_required
def student_home_page():
    """
    Render the student home page.
    """
    student = get_student_by_id(current_user.ID)
    if student:
        return render_template('Student-Home.html', student=student)
    return render_template('Student-Home.html', error="Student not found.")

@student_views.route('/student_dashboard', methods=['GET'])
@login_required
def student_dashboard_page():
    """
    Render the student dashboard page.
    """
    return render_template('StudentPage.html')

@student_views.route('/view-all-reviews', methods=['GET'])
@login_required
def view_all_reviews():
    """
    Render the view-all-reviews page for the current student.
    """
    student = get_student_by_id(current_user.ID)
    if student:
        reviews = get_student_reviews(student.ID)
        if reviews is not None:
            return render_template('AllStudentReviews.html', student=student, reviews=reviews)
        return render_template('AllStudentReviews.html', error="No reviews found.")
    return render_template('AllStudentReviews.html', error="Student not found.")

@student_views.route('/api/view-all-reviews', methods=['GET'])
@jwt_required()
def view_all_reviews_api():
    """
    API to retrieve all reviews for the current student.
    """
    student = get_student_by_id(jwt_current_user.ID)
    if student:
        reviews = get_student_reviews(student.ID)
        if reviews is not None:
            reviews_json = [review.to_json() for review in reviews]
            return jsonify({'reviews': reviews_json}), 200
        return jsonify({'error': 'No reviews found.'}), 404
    return jsonify({'error': 'Student not found.'}), 404

#@student_views.route('/student-page/<int:studentID>', methods=['GET'])
#@jwt_required()
#def student_page(studentID):
#    """
#    Render the student page with details of the student identified by studentID.
#    """
#    student = get_student_by_id(studentID)  # Fetch the student using the studentID from the URL
#    if student:
#        return render_template('StudentPage.html', student=student)  # Pass the student object to the template
#    return render_template('StudentPage.html', error="Student data not found.")  # Render error if no student found


@student_views.route('/api/student-page', methods=['GET'])
@jwt_required()
def student_page_api():
    """
    API to retrieve details of the current student.
    """
    student = get_student_by_id(jwt_current_user.ID)
    if student:
        return jsonify(student.to_json()), 200
    return jsonify({'error': 'Student data not found.'}), 404

@student_views.route('/view-all-students', methods=['GET'])
def view_all_students_page():
    """
    Render a page showing all students.
    """
    try:
        students = Student.query.all()  # Fetch all students from the database
        if students:
            return render_template('Student-Home.html', students=students)
        return render_template('Student-Home.html', error="No students found.")
    except Exception as e:
        print(f"[student_views.view_all_students_page] Error: {str(e)}")
        return render_template('Student-Home.html', error="Failed to retrieve students.")