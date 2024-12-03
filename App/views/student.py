from flask import Blueprint, render_template, jsonify, request
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, current_user
from App.models import Student, User
from App.controllers import get_student_by_id, get_student_reviews

student_views = Blueprint('student_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''

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

@student_views.route('/student-page', methods=['GET'])
@login_required
def student_page():
    """
    Render the student page with student details.
    """
    student = get_student_by_id(current_user.ID)
    if student:
        return render_template('StudentPage.html', student=student)
    return render_template('StudentPage.html', error="Student data not found.")

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