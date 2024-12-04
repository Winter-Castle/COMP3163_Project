import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from App.database import db, get_migrate
from App.main import create_app
from App.models import Student
from App.controllers import (
    create_student, create_staff,
    create_review, 
     get_staff_by_id,set_and_execute_sentiment_command
  )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()

  create_student(username="billy",
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 password="billypass",
                 faculty="FST",
                 admittedTerm="",
                 UniId='816031160',
                 degree="",
                 gpa="")

  create_student(username="shivum",
                 firstname="Shivum",
                 lastname="Praboocharan",
                 email="shivum.praboocharan@my.uwi.edu",
                 password="shivumpass",
                 faculty="FST",
                 admittedTerm="2019/2021",
                 UniId='816016480',
                 degree="Bachelor of Computer Science with Management",
                 gpa='')

  create_student(username="jovani",
                 firstname="Jovani",
                 lastname="Highley",
                 email="jovani.highley@my.uwi.edu",
                 password="jovanipass",
                 faculty="FST",
                 admittedTerm="2021/2022",
                 UniId='816026834',
                 degree="Bachelor of Computer Science with Management",
                 gpa='')

  create_student(username="kasim",
                 firstname="Kasim",
                 lastname="Taylor",
                 email="kasim.taylor@my.uwi.edu",
                 password="kasimpass",
                 faculty="FST",
                 admittedTerm="2019/2021",
                 UniId='816030847',
                 degree="Bachelor of Computer Science (General",
                 gpa='')

  create_student(username="brian",
                 firstname="Brian",
                 lastname="Cheruiyot",
                 email="brian.cheruiyot@my.uwi.edu",
                 password="brianpass",
                 faculty="FST",
                 admittedTerm="2021/2022",
                 UniId='816031609',
                 degree="Bachelor of Computer Science (General)",
                 gpa="")

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


  staff = get_staff_by_id(7)
  student1 = get_student_by_UniId(816031609)
  create_review(staff, student1, True, 5, "Behaves very well in class!")

  student2 = get_student_by_UniId(816016480)
  create_review(staff, student2, True, 5, "Behaves very well in class!")
  student3 = get_student_by_UniId(816026834)
  create_review(staff, student3, True, 5, "Behaves very well in class!")
  student4 = get_student_by_UniId(816030847)
  create_review(staff, student4, True, 5, "Behaves very well in class!")

  students = Student.query.all()

  for student in students:
    
    if student:
      print(student.ID)
      create_karma(student.ID)
      student.karmaID = get_karma(student.ID).karmaID
      print(get_karma(student.ID).karmaID)
      db.session.commit()


# '''
# User Commands
# '''

# # Commands can be organized using groups

# # create a group, it would be the first argument of the comand
# # eg : flask user <command>
# # user_cli = AppGroup('user', help='User object commands')

# # # Then define the command and any parameters and annotate it with the group (@)
# @user_cli.command("create", help="Creates a user")
# @click.argument("username", default="rob")
# @click.argument("password", default="robpass")
# def create_user_command(id, username, firstname,lastname , password, email, faculty):
#     create_user(id, username, firstname,lastname , password, email, faculty)
#     print(f'{username} created!')

# # this command will be : flask user create bob bobpass

# @user_cli.command("list", help="Lists users in the database")
# @click.argument("format", default="string")
# def list_user_command(format):
#     if format == 'string':
#         print(get_all_users())
#     else:
#         print(get_all_users_json())

# app.cli.add_command(user_cli) # add the group to the cli
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

