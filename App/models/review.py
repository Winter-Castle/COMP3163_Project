from App.database import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'review'

    ID = db.Column(db.Integer, primary_key=True)
    taggedStudentID = db.Column(db.Integer, db.ForeignKey('student.ID'), nullable=False)
    createdByStaffID = db.Column(db.Integer, nullable=False)  # Assuming Staff ID comes from another model
    isPositive = db.Column(db.Boolean, nullable=False, default=False)  # Defaults to False
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.String(400), nullable=False)

    def __init__(self, taggedStudentID, createdByStaffID, details, isPositive=False):
        self.taggedStudentID = taggedStudentID
        self.createdByStaffID = createdByStaffID
        self.details = details
        self.isPositive = isPositive
        self.dateCreated = datetime.now()

    def apply_sentiment(self, is_positive: bool):
        """Update the review with new sentiment."""
        self.isPositive = is_positive
        db.session.commit()

    def get_id(self):
        return self.ID

    def to_json(self):
        return {
            "reviewID": self.ID,
            "taggedStudentID": self.taggedStudentID,
            "createdByStaffID": self.createdByStaffID,
            "dateCreated": self.dateCreated.strftime("%d-%m-%Y %H:%M"),
            "isPositive": self.isPositive,
            "details": self.details,
        }

    def __repr__(self):
        return f"<Review {self.ID}: {'Positive' if self.isPositive else 'Negative'}>"
