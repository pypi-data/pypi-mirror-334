import argparse
from test_gen_framework.cli.commands import generate, execute

def main():
    parser = argparse.ArgumentParser(
        prog="test-gen", description="Test Generation Framework CLI"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser(
        "generate", help="Generate test cases using AI model"
    )
    generate_parser.add_argument(
        "pr_number", type=int, help="The PR number to generate tests for"
    )
    generate_parser.set_defaults(func=generate.run)

    execute_parser = subparsers.add_parser(
        "execute", help="Execute tests with prioritization"
    )
    execute_parser.add_argument(
        "test_dir", type=str, help="The generated test directory to run"
    )
    execute_parser.add_argument(
        "pr_number", type=int, help="The PR number of generated tests"
    )
    execute_parser.set_defaults(func=execute.run)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
