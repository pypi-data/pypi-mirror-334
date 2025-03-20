
## Installation

You can install FormMaster directly from PyPI:

```bash
pip install formmaster
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
python -m formfiller --path /path/to/student/documents --portal usyd
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