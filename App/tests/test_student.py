import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Student
from App.controllers import (
    create_student,
    get_student,
    get_student_by_full_name,
    get_all_students,
    update_student,
    delete_student
)

'''
   Unit Tests
'''

class StudentUnitTests(unittest.TestCase):

    def test_new_student(self):
        new_student = Student(fullName="John Doe", degree="Computer Science")
        assert new_student is not None

    def test_student_to_json(self):
        new_student = Student(ID=1, fullName="John Doe", degree="Computer Science")
        student_json = new_student.to_json()
        self.assertDictEqual(student_json, {
            "ID": 1,
            "fullName": "John Doe",
            "degree": "Computer Science"
        })


'''
    Integration Tests
'''

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class StudentIntegrationTests(unittest.TestCase):

    def test_create_student(self):
        student = create_student("John Doe", "Computer Science")
        assert student is not None
        assert student.fullName == "John Doe"
        assert student.degree == "Computer Science"

    def test_get_student_by_id(self):
        student = create_student("Jane Smith", "Mathematics")
        fetched_student = get_student_by_id(student.ID)
        assert fetched_student is not None
        assert fetched_student.fullName == "Jane Smith"
        assert fetched_student.degree == "Mathematics"

    def test_get_student_by_full_name(self):
        create_student("Alice Johnson", "Physics")
        fetched_student = get_student_by_full_name("Alice Johnson")
        assert fetched_student is not None
        assert fetched_student.degree == "Physics"

    def test_get_all_students(self):
        create_student("Student One", "Engineering")
        create_student("Student Two", "Biology")
        students = get_all_students()
        assert len(students) >= 2

    def test_update_student(self):
        student = create_student("Temp Name", "Temp Degree")
        success = update_student(student.ID, full_name="Updated Name", degree="Updated Degree")
        assert success
        updated_student = get_student_by_id(student.ID)
        assert updated_student.fullName == "Updated Name"
        assert updated_student.degree == "Updated Degree"

    def test_delete_student(self):
        student = create_student("To Delete", "To Delete Degree")
        success = delete_student(student.ID)
        assert success
        deleted_student = get_student_by_id(student.ID)
        assert deleted_student is None