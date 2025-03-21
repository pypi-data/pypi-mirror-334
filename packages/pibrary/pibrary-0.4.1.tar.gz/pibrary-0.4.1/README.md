# Pibrary

<p align="center">
    <em>Pibrary framework: A package of reusable code for ML projects</em>
</p>
<p align="center">
    <a href="https://github.com/connectwithprakash/pibrary/actions?query=workflow%3ATest+event%3Apush+branch%3Amain" target="_blank">
        <img src="https://github.com/connectwithprakash/pibrary/workflows/Test/badge.svg?event=push&branch=main" alt="Test">
    </a>
    <a href='https://pibrary.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/pibrary/badge/?version=latest' alt='Documentation Status' />
    </a>
    <a href="https://pypi.org/project/pibrary" target="_blank">
        <img src="https://img.shields.io/pypi/v/pibrary?color=%2334D058&label=pypi%20package" alt="Package version">
    </a>
    <a href="https://pypi.org/project/pibrary" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/pibrary.svg?color=%2334D058" alt="Supported Python versions">
    </a>
    <a href="https://opensource.org/licenses/MIT" target="_blank">
        <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
    </a>
</p>

## Installation

```bash
pip install pibrary
```

## Features
- File Class: Read and write files in csv, json, and pickle formats.
- String Class: String manipulation functions.
- LoguruPro Class: Loguru logger with additional features.
    - Timeit Decorator: Decorator to measure the execution time of a function.
    - Log Table Method: Print a table in the log.

## Usage
```python
from pibrary.file import File
from pibrary.loguru import logger
from pibrary.string import String

# File Class
dataframe = File(file_path).read().csv()
File(file_path).write(dataframe).csv()

json_data = File(file_path).read().json()
File(file_path).write(json_data).csv()

pickle_data = File(file_path).read().pickle()
File(file_path).write(pickle_data).csv()

# Logger
@logger.timeit
def some_function(...):
    ...

data = [
    ["Item 1", "Value 1", "Description 1", "Extra 1"],
    ["Item 2", "Value 2", "Description 2", "Extra 2"],
    ["Item 3", "Value 3", "Description 3", "Extra 3"],
    ["Item 4", "Value 4", "Description 4", "Extra 4"],
]
# Log the timing data as a table
logger.log_table(data)

# String Class
new_text = String(text).lower().remove_digits().remove_punctuation().strip()
```

## Documentation

The full documentation of Pibrary is available at https://pibrary.readthedocs.io/en/latest/.

## Contributing
Contributions are welcome! Please read [CONTRIBUTING](CONTRIBUTING) for details on how to contribute to this project.


# License
This project is licensed under the terms of the [MIT license](LICENSE).
