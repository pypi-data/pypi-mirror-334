import pytest

@pytest.mark.parametrize("name", [
    "Alice",
    "Bob",
    "Charlie",
    ""
])
def test_student_init(name):
    from Student import Student
    student = Student(name)
    assert student.name == name