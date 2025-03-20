import json
import os


def load_test_data(metadata_file: str):
    absolute_path = os.path.abspath(metadata_file)

    if not os.path.exists(absolute_path):
        return {}
    try:
        with open(absolute_path, "r", encoding="utf-8") as file:
            return json.load(file) or {}
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading JSON file {absolute_path}: {e}")
        return {}


def save_test_data(test_data, metadata_file: str):
    """Save updated test data to the JSON file using an absolute path."""
    absolute_path = os.path.abspath(metadata_file)
    with open(absolute_path, "w") as file:
        json.dump(test_data, file, indent=4)


def update_test_result(file_name, outcome, execution_time, metadata_file, is_same_file):
    """Update test results after each test execution at the file level."""
    test_data = load_test_data(metadata_file)

    if file_name not in test_data:
        test_data[file_name] = {
            "failures": 0,
            "executions": 0,
            "total_execution_time": 0.0,
            "stability_score": 1.0,
        }

    file_info = test_data[file_name]

    if not is_same_file:
        file_info["executions"] += 1

    if outcome == "failed":
        file_info["failures"] += 1

    file_info["total_execution_time"] += execution_time

    file_info["avg_execution_time"] = (
        file_info["total_execution_time"] / file_info["executions"]
    )

    file_info["stability_score"] = 1 - (file_info["failures"] / file_info["executions"])

    save_test_data(test_data, metadata_file)


def update_test_results_from_json(results_file, metadata_file="test_metadata.json"):
    base_path = os.path.dirname(__file__)
    metadata_file = os.path.abspath(
        os.path.join(base_path, "./../storage", metadata_file)
    )

    if not os.path.exists(results_file):
        print(f"Warning: Results file '{results_file}' not found.")
        return
    try:
        with open(results_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        if "report" not in data or "tests" not in data["report"]:
            print(f"Error: Unexpected JSON structure in {results_file}")
            return
        results = data["report"]["tests"]
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading JSON file {results_file}: {e}")
        return

    last_file_name = None

    for test in results:
        test_name = test.get("name")
        outcome = test.get("outcome")
        execution_time = test.get("duration")

        if not test_name or outcome is None or execution_time is None:
            print(f"Warning: Skipping invalid test entry: {test}")
            continue

        file_name = test_name.split("::")[0]
        is_same_file = file_name == last_file_name

        update_test_result(
            file_name, outcome, execution_time, metadata_file, is_same_file
        )

        last_file_name = file_name
