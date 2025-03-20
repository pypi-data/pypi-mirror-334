import pytest
from Student import Student
from School import School

@pytest.mark.parametrize("student_name", [
    "John Doe",
    "Jane Smith",
    "Bob Johnson",
])
def test_add_student(capsys, student_name):
    # Initialize a new School instance for each test case
    school = School("Test School")
    
    # Create a new Student instance
    student = Student(student_name)
    
    # Add the student to the school
    school.add_student(student)
    
    # Assert that the student was added to the list
    assert len(school.students) == 1
    assert student in school.students
    
    # Capture and assert the printed message
    captured = capsys.readouterr()
    assert f"Student {student_name} has been added to Test School." in captured.out