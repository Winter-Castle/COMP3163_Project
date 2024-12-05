from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, make_response
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.database import db
from flask_login import login_required, current_user
from sqlalchemy import or_
from datetime import datetime

from App.models import Student, Staff, User
from App.controllers import (
    jwt_authenticate, get_student_by_id, 
    get_staff_by_id, create_review, get_reviews_by_staff,
    get_reviews_by_student, set_and_execute_sentiment_command
    )

staff_views = Blueprint('staff_views',
                        __name__,
                        template_folder='../templates')
'''
Page/Action Routes
'''



@staff_views.route('/Home', methods=['GET']) # This is the staff profile 
@login_required
def get_StaffHome_page():
  staff_id = current_user.get_id()
  staff = get_staff_by_id(staff_id)
  reviews = get_reviews_by_staff(staff_id)

  return render_template('Staff-Home.html', reviews =reviews, staff = staff)

@staff_views.route('/getStudentProfile/<string:uniID>', methods=['GET'])
@login_required
def getStudentProfile(uniID):
  student = get_student_by_id(uniID)
  reviews = get_reviews_by_student(uniID)
  return render_template('Student-Profile-forStaff.html',
                         student=student, reviews=reviews)



@staff_views.route('/studentSearch', methods=['GET'])
def student_search_page():

  return render_template('StudentSearch.html')

  
@staff_views.route('/createReview/<int:student_id>/<string:sentiment>', methods=['POST']) #upvotes or downvotes a post 
def createReview(sentiment, student_id):
  staff_id = current_user.get_id()

  data = request.form
  studentID = data['studentID']
  student = get_student_by_UniId(studentID)


  if student:
    set_and_execute_sentiment_command(student_id, staff_id, sentiment)
    return render_template('Stafflandingpage.html', message=message)
  else:
    message = f"Error creating review on Student: {student.fullName}"
    return render_template('Stafflandingpage.html', message=message)








