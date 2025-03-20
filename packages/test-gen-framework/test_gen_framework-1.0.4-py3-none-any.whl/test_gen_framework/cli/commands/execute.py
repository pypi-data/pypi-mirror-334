from test_gen_framework.execution.Test_execution import execute_tests

def run(args):
    test_dir = args.test_dir
    pr_number = args.pr_number
    print(f"Running tests in {test_dir}...")
    execute_tests(test_dir, pr_number)
