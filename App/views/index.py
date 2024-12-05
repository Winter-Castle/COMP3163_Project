from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db, Student
import random
from App.controllers import (
    create_user,
    create_student,
    create_staff,
    get_staff_by_id,
    create_review,
    create_command_history
)
from flask_login import login_required, login_user, current_user, logout_user

index_views = Blueprint('index_views',
                        __name__,
                        template_folder='../templates')


@index_views.route('/', methods=['GET'])
def index_page():
  return render_template('login.html')


@index_views.route('/hello')
def hello_world():
  return 'Hello, World!'


@index_views.route('/init', methods=['GET'])
def init():
  db.drop_all()
  db.create_all()


  # Creating students
  create_student(full_name="Billy John", degree="Comp Sci")
  create_student(full_name="Jane Doe", degree="Comp Sci")
  create_student(full_name="Alice Smith", degree="Mathematics")
  create_student(full_name="Bob Brown", degree="Physics")
  create_student(full_name="Cathy Green", degree="Chemistry")
  create_student(full_name="David White", degree="Biology")
  create_student(full_name="Eva Black", degree="History")
  create_student(full_name="Frank Yellow", degree="Geography")
  create_student(full_name="Georgia Red", degree="Philosophy")
  create_student(full_name="Henry Blue", degree="Economics")
  create_student(full_name="Ivy Purple", degree="Political Science")
  create_student(full_name="Jack Orange", degree="Psychology")
  create_student(full_name="Karen Pink", degree="Sociology")
  create_student(full_name="Leo Cyan", degree="Engineering")
  create_student(full_name="Mona Magenta", degree="Business")
  create_student(full_name="Nina Lime", degree="Finance")
  create_student(full_name="Oscar Olive", degree="Art")
  create_student(full_name="Paul Teal", degree="Music")
  create_student(full_name="Quinn Violet", degree="Theater")

  #Creating staff
  create_staff(username="tim",
               firstname="Tim",
               lastname="Long",
               email="",
               password="timpass",
               faculty="")

  create_staff(username="vijay",
               firstname="Vijayanandh",
               lastname="Rajamanickam",
               email="Vijayanandh.Rajamanickam@sta.uwi.edu",
               password="vijaypass",
               faculty="FST")

  create_staff(username="permanand",
               firstname="Permanand",
               lastname="Mohan",
               email="Permanand.Mohan@sta.uwi.edu",
               password="password",
               faculty="FST")

  create_staff(username="john",
               firstname="John",
               lastname="Deo",
               email="John.Deo@sta.uwi.edu",
               password="password",
               faculty="FST")

  create_staff(username="james",
               firstname="James",
               lastname="Thomas",
               email="James.Thomas@sta.uwi.edu",
               password="password",
               faculty="FST")

  create_staff(username="richard",
               firstname="Richard",
               lastname="Rajkumar",
               email="Richard.Rajkumar@sta.uwi.edu",
               password="password",
               faculty="FST")



  review_messages = ["Excellent participation!", "Needs improvement in assignments.", "Great teamwork!", "Outstanding performance in projects!", "Regularly submits assignments late.", "Shows leadership in group activities.", "Needs to focus more on lectures.", "Always on time!", "Frequently absent.", "Positive attitude towards learning."]

  for student_id in range(1, 15):
      staff_id = random.randint(1, 3)
      message = random.choice(review_messages)
      is_positive = random.choice([True, False])
      review = create_review(staff_id, student_id, message, is_positive)
      create_command_history(review.ID)

  return jsonify(message='db initialized!')


@index_views.route('/health', methods=['GET'])
def health_check():
  return jsonify({'status': 'healthy'})


@index_views.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
  return send_from_directory('/workspaces/Info3604_Project/images', filename)
