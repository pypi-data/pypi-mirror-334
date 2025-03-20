from test_gen_framework.services.Github_service import get_pr_diff, get_file_content
from test_gen_framework.generation.AI_Client import generate_test_cases
from test_gen_framework.execution.Test_execution import load_test_priorities
from test_gen_framework.prioritization.test_prioritizer import save_priorities
from test_gen_framework.config import read_config
import ast
import os

config = read_config()


def generate_tests(pr_number):
    code_diff_array = get_pr_diff(pr_number)

    if code_diff_array:
        priorities_path = config["TEST_LOC"] + "/test_priorities.json"
        priorities = load_test_priorities(priorities_path)
        for file_data in code_diff_array:
            if file_data["localfilepath"].endswith(".py") and not file_data[
                "localfilepath"
            ].startswith("tests"):
                print(f"Processing file: {file_data['localfilepath']}")
                file_content = get_file_content(file_data["filepathURL"])
                if file_content:
                    print(f"Full content fetched for {file_data['localfilepath']}")
                    full_function_code = extract_changed_function(
                        file_content, file_data["diff"]
                    )
                    if full_function_code:
                        for function_code in full_function_code:
                            test_script = generate_test_cases(
                                file_data["localfilepath"], function_code
                            )
                            print(extract_function_name(function_code)+'\n')
                            if test_script != "":
                                function_name = extract_function_name(function_code)
                                if function_name:
                                    base_filename = os.path.splitext(
                                        os.path.basename(file_data["localfilepath"])
                                    )[0]

                                    test_filename = (
                                        f"test_{function_name}_#{base_filename}.py"
                                    )
                                    test_file_path = os.path.join(
                                        config["TEST_LOC"], test_filename
                                    )

                                    try:
                                        with open(test_file_path, "w") as test_file:
                                            test_file.write(test_script)
                                        update_test_priorities(priorities, test_filename)
                                        print(f"Test file saved: {test_file_path}")
                                    except Exception as e:
                                        print(
                                            f"Failed to save test file for {file_data['localfilepath']}: {e}"
                                        )
                                else:
                                    print(
                                        f"Could not extract function name for {file_data['localfilepath']}"
                                    )
                            else:
                                print(
                                    f"Failed to generate test file for {file_data['localfilepath']}"
                                )
                        print('----------------------------------------------------------')
                    else:
                        print(
                            f"No valid function extracted for file {file_data['localfilepath']}"
                        )
                else:
                    print(
                        f"Failed to fetch file content for {file_data['localfilepath']}"
                    )
            else:
                print(f"Skipping non-Python file: {file_data['localfilepath']}")
        save_priorities(priorities, priorities_path)
    else:
        print(f"Error fetching PR diff for PR #{pr_number}")


def extract_changed_function(file_content, diff):
    changed_lines = parse_patch_lines(diff)
    return extract_full_function(file_content, changed_lines)


def parse_patch_lines(patch):
    lines = patch.split("\n")
    changed_lines = []

    for line in lines:
        if line.startswith("@@"):
            parts = line.split(" ")
            original_info = parts[1].split(",")
            modified_info = parts[2].split(",")
            original_start = int(original_info[0][1:])
            original_count = int(original_info[1]) if len(original_info) > 1 else 1
            modified_start = int(modified_info[0][1:])
            modified_count = int(modified_info[1]) if len(modified_info) > 1 else 1
            for i in range(modified_count):
                changed_lines.append(modified_start + i)

    return changed_lines


def extract_full_function(file_content, changed_lines) -> str:
    tree = ast.parse(file_content)
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if any(
                line in changed_lines
                for line in range(node.lineno, node.end_lineno + 1)
            ):
                function_code = extract_function_code(file_content, node)
                functions.append(function_code)

    return functions if functions else None


def extract_function_code(file_content, func_node) -> str:
    start_line = func_node.lineno - 1
    end_line = func_node.end_lineno

    lines = file_content.splitlines()
    function_code = "\n".join(lines[start_line:end_line])

    return function_code


def extract_function_name(function_code) -> str:
    import re

    match = re.match(r"\s*def (\w+)\(", function_code.strip())
    if match:
        return match.group(1)
    return None


def update_test_priorities(priorities, test_file_name):
    if test_file_name not in priorities:
        priorities[test_file_name] = 0
