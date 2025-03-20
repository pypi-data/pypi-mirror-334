# Publishing zen-completions to PyPI

This document outlines the process for building and publishing the zen-completions package to PyPI.

## Prerequisites

1. Ensure you have the necessary tools installed:
   ```bash
   pip install build twine
   ```

2. Create accounts on PyPI (https://pypi.org) and TestPyPI (https://test.pypi.org) if you don't already have them.

3. Generate API tokens for both services in your account settings.

4. Create or update your `~/.pypirc` file with the tokens:
   ```
   [distutils]
   index-servers=
       pypi
       testpypi

   [pypi]
   repository = https://upload.pypi.org/legacy/
   username = __token__
   password = pypi-YOUR_TOKEN_HERE

   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-YOUR_TOKEN_HERE
   ```

## Release Process

1. Update the version number in both `pyproject.toml` and `zen_completions/__init__.py`.

2. Build the distribution packages:
   ```bash
   python -m build
   ```

3. Upload to TestPyPI first to verify everything works:
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

4. Test the installation from TestPyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --no-deps zen-completions
   ```

5. Upload to the real PyPI:
   ```bash
   python -m twine upload dist/*
   ```

## Updating Dependencies

In the consuming projects, update the pyproject.toml or requirements.txt to use the PyPI version instead of the Git repository:

```toml
# Before
zen-completions = {git = "https://github.com/zenafide/zen-completions.git"}

# After
zen-completions = "^0.1.0"  # Or whatever version you've published
``` 