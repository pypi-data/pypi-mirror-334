import pytest
from School import School

@pytest.fixture(
    params=[
        ("Central High", "Central High"),
        ("Green Valley Middle School!", "Green Valley Middle School!"),
        ("", ""),
    ]
)
def init_school(request):
    return School(request.param[0]), request.param[1]

def test_initSchool(init_school):
    school, expected_name = init_school
    assert school.name == expected_name
    assert len(school.students) == 0