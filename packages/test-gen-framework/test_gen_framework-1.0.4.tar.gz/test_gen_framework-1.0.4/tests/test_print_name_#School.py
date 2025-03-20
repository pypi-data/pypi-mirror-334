import pytest

@pytest.mark.parametrize("school_name,expected_output", [
    ("Central High", "School Name: Central High"),
    ("Eastside Elementary", "School Name: Eastside Elementary")
])
def test_print_name(school_name, expected_output, capsys):
    class School:
        def __init__(self, name):
            self.name = name
        
        def print_name(self):
            print(f"School Name: {self.name}")
    
    # Create instance and call method
    school = School(school_name)
    school.print_name()
    
    # Check output
    assert capsys.readouterr().out.strip() == expected_output