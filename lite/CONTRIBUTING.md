# Contributing to Lite

Thank you for your interest in contributing to Lite! We welcome all contributions, from bug reports and documentation improvements to new features and refactors.

## Getting Started

### Prerequisites
- Python 3.9 or higher
- [ruff](https://github.com/astral-sh/ruff) (for linting)
- [pytest](https://docs.pytest.org/) (for testing)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/csv610/lite.git
   cd lite
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -e ".[test]"
   ```

## Development Workflow

1. **Create a Branch**: Always create a new branch for your work.
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Coding Standards**: We use `ruff` for linting and formatting. Please run it before committing:
   ```bash
   ruff check .
   ruff format .
   ```

3. **Writing Tests**: If you add a new feature or fix a bug, please include tests in the `tests/` directory.

4. **Running Tests**: Ensure all tests pass before submitting a Pull Request:
   ```bash
   pytest
   ```

## Pull Request Process

1. Ensure your code follows the existing style and all tests pass.
2. Update the `README.md` if your changes introduce new user-facing features.
3. Submit a Pull Request targeting the `main` branch.
4. Provide a clear description of the changes and the problem they solve.

## Code of Conduct

Please be respectful and professional in all interactions within this project.
