import os
import tempfile
import pytest
import logging
import unittest

from App.main import create_app
from App.database import db, create_db
from App.models import Student
from App.controllers import (
    create_student,
    get_student_by_id,
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
        new_student = Student(fullName="John Doe", degree="Computer Science")
        # Simulate saving to the database and ID generation
        new_student.ID = 1
        student_json = new_student.to_json()
        self.assertDictEqual(student_json, {
            "studentID": 1,
            "fullName": "John Doe",
            "degree": "Computer Science",
            "reviews": []
        })

'''
    Integration Tests
'''

class StudentIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        self.app_context = self.app.app_context()
        self.app_context.push()
        create_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_student(self):
        student = create_student("John Doe", "Computer Science")
        assert student is not None
        assert student.fullName == "John Doe"
        assert student.degree == "Computer Science"

    def test_get_student_by_id(self):
        student = create_student("Jane Smith", "Mathematics")
        fetched_student = get_student_by_id(student.ID)
        assert fetched_student is not None
        # Handle the possibility of a dictionary response
        if isinstance(fetched_student, dict):
            assert fetched_student["fullName"] == "Jane Smith"
            assert fetched_student["degree"] == "Mathematics"
        else:
            assert fetched_student.fullName == "Jane Smith"
            assert fetched_student.degree == "Mathematics"

    def test_get_student_by_full_name(self):
        create_student("Alice Johnson", "Physics")
        fetched_student = get_student_by_full_name("Alice Johnson")
        assert fetched_student is not None
        # Handle the possibility of a dictionary response
        if isinstance(fetched_student, dict):
            assert fetched_student["degree"] == "Physics"
        else:
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
        assert updated_student is not None
        # Handle the possibility of a dictionary response
        if isinstance(updated_student, dict):
            assert updated_student["fullName"] == "Updated Name"
            assert updated_student["degree"] == "Updated Degree"
        else:
            assert updated_student.fullName == "Updated Name"
            assert updated_student.degree == "Updated Degree"

    def test_delete_student(self):
        student = create_student("To Delete", "To Delete Degree")
        success = delete_student(student.ID)
        assert success
        deleted_student = get_student_by_id(student.ID)
        assert deleted_student is None
