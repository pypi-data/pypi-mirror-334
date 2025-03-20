# DataValidityCheck - Data Validation Package

## Overview
**DataValidityCheck** is a Python package designed to validate personal data, including emails, phone numbers, dates, and URLs. It provides robust validation methods to ensure data accuracy and compliance with common formats.

## Table of Contents
- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
  - [Email Validation](#email-validation)
  - [Phone Number Validation](#phone-number-validation)
  - [Date Validation](#date-validation)
  - [URL Validation](#url-validation)
- [Contributing](#contributing)
- [License](#license)

## Installation
To install **DataValidityCheck**, use:
```bash
pip install DataValidityCheck
```

## Features
- **Email Validation**: Ensures a valid email format.
- **Phone Number Validation**: Supports Nigerian phone numbers in local and international formats.
- **Date Validation**: Validates dates in the `DD/MM/YYYY` format, including leap years.
- **URL Validation**: Checks for valid domain structures, including `http`, `https`, and `www` prefixes.

## Usage
First, import the `DataValidator` class:
```python
from DataValidityCheck import DataValidator

validator = DataValidator()
```

### Email Validation
```python
print(validator.validate_email("user@example.com"))  # True
print(validator.validate_email("invalid-email"))  # False
```

### Phone Number Validation
```python
print(validator.validate_phone("08123456789"))  # True
print(validator.validate_phone("+2348123456789"))  # True
print(validator.validate_phone("123456"))  # False
```

### Date Validation
```python
print(validator.validate_date("27/02/2024"))  # True 
print(validator.validate_date("31/04/2023"))  # False (April has 30 days)
```

### URL Validation
```python
print(validator.validate_url("https://www.google.com"))  # True
print(validator.validate_url("htp://invalid.com"))  # False
```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit your changes.
4. Submit a pull request.

Ensure you run tests before submitting:
```bash
pytest tests/
```

## Author
Olajide Oluwafemi Richard

## License
This package is open-source and available under the [MIT License](LICENSE).

