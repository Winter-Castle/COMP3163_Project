from App.database import db
from .user import User
from .student import Student
from .DownvoteCommand import DownvoteCommand
from .UpvoteCommand import UpvoteCommand

class Staff(User):
  __tablename__ = 'staff'
  ID = db.Column(db.Integer, db.ForeignKey('user.ID'), primary_key=True)
  

  __mapper_args__ = {"polymorphic_identity": "staff"}

  def __init__(self, username, firstname, lastname, email, password, faculty):
    super().__init__(username=username,
                     firstname=firstname,
                     lastname=lastname,
                     email=email,
                     password=password,
                     faculty=faculty)
  @property
  def is_active(self):
    return True
#return staff details on json format

  def to_json(self):
    return {
        "staffID":
        self.ID,
        "username":
        self.username,
        "firstname":
        self.firstname,
        "lastname":
        self.lastname,
        "email":
        self.email,
        "faculty":
        self.faculty
    }

  def __repr__(self):
    return f'<Admin {self.ID} :{self.email}>'
  
