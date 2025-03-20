
# Test Generation Framework

The **Test Generation Framework** is a command-line interface (CLI) tool designed to generate and execute automated tests for pull requests (PRs) using AI models. It provides two main commands: `generate` for generating tests based on the PR number, and `execute` for running tests with prioritization.

## Features

- **Generate Test Cases**: Automatically generate test cases using an AI model based on the pull request.
- **Dynamic Tests prioritization**: Dynamically generate tests prioritization based on previous execution data.
- **Execute Tests**: Run generated tests with prioritization, making it easier to focus on the most important tests first.

## Installation

To install the framework, use the following command:

```bash
pip install test-gen-framework
```

## Usage

### Command-Line Interface

Once installed, you can use the `test-gen` command with the following syntax:

```bash
test-gen <command> <arguments>
```

### Available Commands

#### 1. `generate`

Generates test cases based on the provided pull request (PR) number.

**Usage:**

```bash
test-gen generate <pr_number>
```

**Arguments:**

- `pr_number`: The PR number for which to generate test cases.

**Example:**

```bash
test-gen generate 123
```

This will generate test cases for PR number 123.

#### 2. `execute`

Executes the generated tests with prioritization.

**Usage:**

```bash
test-gen execute <test_dir> <pr_number>
```

**Arguments:**

- `test_dir`: The directory where the generated test cases are located.
- `pr_number`: The PR number associated with the generated tests.

**Example:**

```bash
test-gen execute tests/pr_123 123
```

This will execute the tests located in the `tests/pr_123` directory, corresponding to PR number 123.

## How It Works

1. **Generate Command**: The `generate` command uses an AI model to generate automated tests for a given pull request. It leverages the PR number to gather relevant code and context.
2. **Execute Command**: The `execute` command runs the generated tests on a specified directory, prioritizing tests based on their importance and relevance.

## Contributing

If you'd like to contribute to the project, feel free to fork the repository and submit a pull request. Contributions are always welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
