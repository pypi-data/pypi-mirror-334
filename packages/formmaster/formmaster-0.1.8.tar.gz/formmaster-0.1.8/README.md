# FormMaster

FormMaster is an automation tool designed to streamline the university application process for students applying to Australian universities. The system uses Selenium WebDriver to interact with university application portals and automatically fill in application forms based on student data.

## Features

- Extracts student information from Word documents (.docx) containing application details
- Supports multiple Australian universities:
  - USYD (Sydney University)
  - UNSW (New South Wales University)
- Provides a user-friendly interface for triggering form filling operations
- Handles repetitive form tasks while allowing manual intervention

## Installation

You can install FormMaster directly from PyPI:

```bash
pip install form-master
```

Or install from source:

```bash
git clone https://github.com/haroldmei/form-master.git
cd form-master
pip install -e .
```

## Usage

After installation, you can run FormMaster in two ways:

### Command Line

```bash
form-master --path /path/to/student/documents --portal usyd
```

### As Python Module

```python
from formmaster import FormFiller

filler = FormFiller(path="/path/to/student/documents", portal="usyd")
filler.run()
```

## Development

### Building the Package

To build the package locally:

1. Ensure you have the build tools installed:
   ```bash
   pip install build twine
   ```

2. Build the package:
   ```bash
   python -m build
   ```

This will create distribution files in the `dist/` directory:
- `formmaster-0.1.0-py3-none-any.whl` (Wheel package)
- `formmaster-0.1.0.tar.gz` (Source distribution)

### Publishing to PyPI

To upload the package to PyPI:

1. Test your package with TestPyPI first:
   ```bash
   python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   ```

2. Upload to the official PyPI:
   ```bash
   python -m twine upload dist/*
   ```

You will need to provide your PyPI credentials during upload. Alternatively, create a `.pypirc` file in your home directory:

## Documentation

For detailed documentation, please visit the [GitHub repository](https://github.com/haroldmei/form-master).

## License

This project is licensed under the MIT License - see the LICENSE file for details.