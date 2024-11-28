from App.database import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'review'

    ID = db.Column(db.Integer, primary_key=True)
    taggedStudentID = db.Column(db.Integer, db.ForeignKey('student.ID'), nullable=False)
    createdByStaffID = db.Column(db.Integer, nullable=False)  # Assuming Staff ID comes from another model
    isPositive = db.Column(db.Boolean, nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    points = db.Column(db.Float, nullable=False)
    details = db.Column(db.String(400), nullable=False)

    def __init__(self, taggedStudentID, createdByStaffID, isPositive, points, details):
        self.taggedStudentID = taggedStudentID
        self.createdByStaffID = createdByStaffID
        self.isPositive = isPositive
        self.points = points
        self.details = details
        self.dateCreated = datetime.now()

    def get_id(self):
        return self.ID

    def to_json(self):
        return {
            "reviewID": self.ID,
            "taggedStudentID": self.taggedStudentID,
            "createdByStaffID": self.createdByStaffID,
            "dateCreated": self.dateCreated.strftime("%d-%m-%Y %H:%M"),
            "isPositive": self.isPositive,
            "points": self.points,
            "details": self.details,
            "studentSeen": self.studentSeen
        }
