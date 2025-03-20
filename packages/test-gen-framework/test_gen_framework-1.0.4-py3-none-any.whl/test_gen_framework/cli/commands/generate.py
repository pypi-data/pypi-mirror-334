from test_gen_framework.generation.Test_generation import generate_tests

def run(args):
    pr_number = args.pr_number
    print(f"Generating tests for PR #{pr_number}...")
    generate_tests(pr_number)
