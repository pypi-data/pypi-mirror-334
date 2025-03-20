import json
import os
from test_gen_framework.services.Github_service import get_pr_diff


def load_test_data(priority_file: str):
    try:
        if not os.path.exists(priority_file):
            with open(priority_file, "w") as file:
                json.dump({}, file)

        with open(priority_file, "r") as file:
            priorities = json.load(file)
        return priorities
    except Exception as e:
        print(f"Error reading the priorities file: {e}")
        with open(priority_file, "w") as file:
            json.dump({}, file)

        return {}


def calculate_priority(test_file, test_info, changed_file):
    failures = test_info["failures"]
    avg_execution_time = test_info["avg_execution_time"]
    stability_score = test_info["stability_score"]

    weight_failures = 5
    weight_exec_time = 2
    weight_stability = 3

    priority = (
        (weight_failures * failures)
        + (weight_exec_time * avg_execution_time)
        + (weight_stability * (1 - stability_score))
        + (100 if test_file.split("#")[1] in changed_file else 0)
    )

    return round(priority)


def prioritize_tests(output_file, pr_number):
    base_path = os.path.dirname(__file__)
    metadata_file = os.path.join(base_path, "./../storage", "test_metadata.json")
    test_data = load_test_data(metadata_file)
    code_diff_array = get_pr_diff(pr_number)
    file_names = [item["localfilepath"] for item in code_diff_array]

    priorities = {}
    for test_file, test_info in test_data.items():
        file_name = test_file.split("/")[-1]
        priority = calculate_priority(file_name, test_info, file_names)
        priorities[file_name] = priority

    sorted_priorities = dict(
        sorted(priorities.items(), key=lambda item: item[1], reverse=True)
    )

    save_priorities(sorted_priorities, output_file)
    return sorted_priorities


def save_priorities(priorities, output_file):
    absolute_path = os.path.abspath(output_file)
    try:
        if not os.path.exists(absolute_path):
            with open(absolute_path, "w", encoding="utf-8") as file:
                json.dump({}, file)

        with open(absolute_path, "r", encoding="utf-8") as file:
            try:
                existing_priorities = json.load(file)
                if not isinstance(existing_priorities, dict):
                    existing_priorities = {}
            except json.JSONDecodeError:
                print(
                    f"Warning: Corrupt JSON detected in {output_file}. Resetting file."
                )
                existing_priorities = {}

        existing_priorities.update(priorities)

        with open(absolute_path, "w", encoding="utf-8") as file:
            json.dump(existing_priorities, file, indent=4)

    except (IOError, OSError) as e:
        print(f"Error saving priorities to {output_file}: {e}")
