from App.database import db

class Student(db.Model):
    __tablename__ = 'student'

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    degree = db.Column(db.String(100), nullable=False)
    fullName = db.Column(db.String(200), nullable=False)
    
    # One-to-Many relationship with Review
    reviews = db.relationship('Review', backref='student', lazy=True)

    def __init__(self, fullName, degree):
        self.fullName = fullName
        self.degree = degree

    def get_id(self):
        return self.ID

    def to_json(self):
        return {
            "studentID": self.ID,
            "fullName": self.fullName,
            "degree": self.degree,
            "reviews": [review.to_json() for review in self.reviews]
        }
