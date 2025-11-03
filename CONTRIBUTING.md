# Contributing to File Organizer

Thank you for your interest in contributing to File Organizer! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Abudi-seid10/File_manager/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version)
   - Screenshots if applicable

### Suggesting Enhancements

1. Check if the enhancement has already been suggested
2. Create a new issue with:
   - Clear description of the enhancement
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/File_manager.git
   cd File_manager
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```

3. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   pip install -r requirements-dev.txt
   ```

4. **Make Your Changes**
   - Write clear, readable code
   - Follow the existing code style
   - Add type hints where appropriate
   - Update docstrings for any modified functions

5. **Test Your Changes**
   ```bash
   # Run tests
   python -m unittest discover tests -v
   
   # Check syntax
   python -m py_compile main.py
   ```

6. **Format Your Code** (if tools are available)
   ```bash
   black main.py
   isort main.py
   flake8 main.py --max-line-length=120
   ```

7. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```
   
   Commit message guidelines:
   - Use present tense ("Add feature" not "Added feature")
   - Use imperative mood ("Move cursor to..." not "Moves cursor to...")
   - Limit first line to 72 characters
   - Reference issues and PRs when relevant

8. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   
   Then create a PR on GitHub with:
   - Clear title and description
   - Reference related issues
   - Description of changes made
   - Screenshots for UI changes

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Maximum line length: 120 characters
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Include type hints for function parameters and return values

### Documentation

- Update README.md if adding new features
- Add docstrings following Google style:
  ```python
  def function_name(param1: str, param2: int) -> bool:
      """
      Brief description of function.
      
      Args:
          param1: Description of param1.
          param2: Description of param2.
          
      Returns:
          bool: Description of return value.
          
      Raises:
          ValueError: When and why this error is raised.
      """
  ```

### Testing

- Add tests for new functionality
- Ensure existing tests pass
- Aim for high code coverage
- Test edge cases and error conditions

### Commit Standards

- Keep commits atomic (one logical change per commit)
- Write clear commit messages
- Reference issue numbers in commits

## Project Structure

```
File_manager/
├── main.py                 # Main application code
├── config.json             # User configuration
├── config.example.json     # Example configuration
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── setup.py               # Installation script
├── README.md              # User documentation
├── CONTRIBUTING.md        # This file
├── LICENSE                # MIT License
└── .github/
    └── workflows/
        └── ci.yml         # CI/CD configuration
```

## Getting Help

- Check the [README](README.md) for usage instructions
- Search existing [Issues](https://github.com/Abudi-seid10/File_manager/issues)
- Create a new issue if you need help

## Recognition

Contributors will be acknowledged in the project documentation.

Thank you for contributing to File Organizer!
