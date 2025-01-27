# Contributing to PDF Statement Reader

Thank you for your interest in contributing to PDF Statement Reader! This document provides guidelines and information about contributing to this project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone git@github.com:your-username/pdf_statement_reader.git
```
3. Set up your development environment:
```bash
uv sync
```

## Development Process

1. Create a new branch for your feature or bugfix:
```bash
git checkout -b feature-name
```

2. Make your changes, following our coding standards
3. Write or update tests as needed
4. Run the test suite to ensure everything passes
5. Commit your changes with a clear commit message following conventional commits format
6. Push to your fork and submit a pull request

## Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages. Each commit message should be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types include:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

Examples:
```
feat(parser): add ability to parse HSBC statements
fix(config): correct column mapping for Absa statements
docs: update configuration guide
test(validation): add tests for balance validation
```

## Adding New Statement Configurations

One of the most valuable ways to contribute is by adding support for new bank statement formats:

1. Create a new configuration file in the appropriate location:
   ```
   config > [country code] > [bank] > [statement type].json
   ```

2. Follow the configuration format as described in the README.md
3. Test your configuration with sample statements
4. Include documentation about the new format in your pull request

## Pull Request Guidelines

- Include a clear description of the changes
- Add/update tests for any new functionality
- Ensure all tests pass
- Update documentation as needed
- Follow existing code style and conventions

## Running Tests

Before submitting a pull request, make sure all tests pass:

```bash
# Run the test suite
pytest

# Check code coverage
pytest --cov=pdf_statement_reader
```

## Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Comment complex logic as needed

## Reporting Issues

When reporting issues, please include:

- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Version information (Python version, package version)
- Any relevant error messages or logs

## License

By contributing to PDF Statement Reader, you agree that your contributions will be licensed under the same license as the project.

## Questions?

If you have questions about contributing, feel free to open an issue for discussion.

Thank you for contributing to PDF Statement Reader! 