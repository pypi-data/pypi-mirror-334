import json
from test_gen_framework.services.LLM_service import call_llm_model


def generate_test_cases(filename: str, function: str) -> str:
    prompt = f"""
    Write a pytest unit test for the following function:

    File Name: {filename}
    Function:

    {function}

    Instructions:
    - Use pytest `@pytest.mark.parametrize` to test multiple cases efficiently.
    - Write simple test cases; do not complicate them with custom logic inside the tests.
    - If the function being tested calls methods from external classes or objects, **do not mock those methods**. Instead, focus on testing the actual behavior of the function being tested.
    - IMPORTANT, if there are external classes used within the test make sure to import them, you can assume all the classes are their within the project and the follow the naming conventions for python classes.
    - Directly assert the expected behavior.
    - If the function prints output capture that output using `capsys` and assert the printed message.
    - The test function should follow pytest naming conventions.
    - Do not use any third-party packages beyond what is already used in the original code.
    - Use assertions directly to validate expected outputs, such as checking the length of the `students` list and the properties of the added student.
    - Structure the test file properly to ensure smooth execution with `pytest`.

    Generate only the test code.
    """

    print("calling the model")
    response = call_llm_model(prompt)
    test_code = response.get("output", "")

    return test_code
