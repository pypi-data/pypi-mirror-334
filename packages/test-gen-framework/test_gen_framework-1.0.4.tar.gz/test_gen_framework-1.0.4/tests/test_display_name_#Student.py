import pytest

@pytest.mark.parametrize("name,expected_output", [
    ("John Doe", "Student Name: John Doe"),
    ("Jane Smith", "Student Name: Jane Smith"),
    ("Bob Johnson", "Student Name: Bob Johnson")
])
def test_display_name(name, expected_output, capsys):
    from Student import Student
    student = Student(name)
    student.display_name()
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output