from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("src/requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="formmaster",
    version="0.1.1",
    author="Form-Master Team",
    author_email="maintainer@example.com",
    description="Form automation tool for Australian university application processes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haroldmei/form-master",
    project_urls={
        "Bug Tracker": "https://github.com/haroldmei/form-master/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Office/Business :: Office Suites",
    ],
    package_dir={"": "src"},
    py_modules=["formfiller", "etl"],  # Use py_modules for individual Python files
    python_requires=">=3.11,<3.12",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "formmaster=formfiller:run",  # Direct reference to formfiller.py
        ],
    },
    include_package_data=True,
)
