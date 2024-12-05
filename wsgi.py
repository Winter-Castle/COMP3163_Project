import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from App.database import db, get_migrate
from App.main import create_app
from App.models import Student
import random
from App.controllers import (
    create_student, create_staff,
    create_review, get_student_by_id,
     get_staff_by_id,set_and_execute_sentiment_command, create_command_history
  )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
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
    #create_command_history(review.ID)

print("Database initialized")



'''
Test Commands
'''

test = AppGroup('test', help='Testing commands')

@test.command("final", help="Runs ALL tests")
@click.argument("type", default="all")
def final_tests_command(type):
  if type == "all":
    sys.exit(pytest.main(["App/tests"]))

@test.command("user", help="Run User tests!!")
@click.argument("type", default="all")
def user_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "UserUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "User"]))


@test.command("student", help="Run Student tests")
@click.argument("type", default="all")
def student_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "StudentUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "Student"]))


@test.command("staff", help="Run Staff tests")
@click.argument("type", default="all")
def staff_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "StaffUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "StaffIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "Staff"]))


@test.command("review", help="Run Review tests")
@click.argument("type", default="all")
def review_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "ReviewUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "ReviewIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "Review"]))

@app.cli.command("apply_sentiment", help="Apply a sentiment (upvote/downvote) to a student review")
@click.argument("tagged_student_id", type=int)
@click.argument("created_by_staff_id", type=int)
@click.argument("sentiment_type", type=str)
def apply_sentiment(tagged_student_id, created_by_staff_id, sentiment_type):
    """
    CLI command to apply sentiment using the set_and_execute_sentiment_command function.

    Args:
        tagged_student_id (int): ID of the tagged student.
        created_by_staff_id (int): ID of the staff creating the review.
        sentiment_type (str): Sentiment type ('upvote' or 'downvote').
    """
    response, status = set_and_execute_sentiment_command(tagged_student_id, created_by_staff_id, sentiment_type)
    if status == 200:
        print(f"Success: {response['message']}")
        print(f"Review Details: {response['review']}")
    elif status == 400:
        print(f"Error: {response['error']}")
    elif status == 500:
        print(f"Error: {response['error']}")


@test.command("sentiment", help="Run sentiment tests")
@click.argument("type", default="all")
def sentiment_tests_command(type):
    """
    CLI command to run sentiment-related tests.
    
    Args:
        type (str): Test type ('unit', 'int', or 'all').
    """
    if type == "unit":
        sys.exit(pytest.main(["-k", "SentimentCommandUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "SentimentCommandIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "SentimentCommand"]))


app.cli.add_command(test)



@test.command("commandHistory", help="Run Command History tests")
@click.argument("type", default="all")
def history_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "CommandHistoryUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "CommandHistoryIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "CommandHistory"]))

