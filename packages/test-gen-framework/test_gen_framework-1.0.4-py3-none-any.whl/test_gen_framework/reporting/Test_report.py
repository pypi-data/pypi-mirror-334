import json
import os
from collections import defaultdict
from test_gen_framework.config import read_config
from test_gen_framework.services.Dashboard_service import sync_dashboard_view

config = read_config()


def report_test_results(results_file, coverage):
    """Update test data from a JSON results file"""
    with open(results_file, "r") as file:
        results = json.load(file)["report"]["tests"]

    grouped_tests = defaultdict(
        lambda: {
            "file_name": "",
            "Project": config["PROJECT_NAME"],
            "Outcome": "passed",
            "Unit tests": [],
        }
    )

    for test in results:
        test_name = test["name"]
        outcome = test["outcome"]
        execution_time = test["duration"]

        file_path = test_name.split("::")[0]
        file_name = file_path.split("/")[-1]

        function_name = test_name.split("::")[-1]

        unit_test_entry = {
            "unit_test": function_name,
            "Outcome": outcome,
            "duration": execution_time,
            "file_name": file_name,
        }

        grouped_tests[file_name]["file_name"] = file_name
        grouped_tests[file_name]["Unit tests"].append(unit_test_entry)
        if outcome != "passed":
            grouped_tests[file_name]["Outcome"] = "failed"

    final_json = {
        "tests": list(grouped_tests.values()),  
        "coverage": coverage,  
        "token": config["CLOUD_TOKEN"], 
        "project": config["PROJECT_NAME"],  
    }

    status = sync_dashboard_view(final_json)
    return status
