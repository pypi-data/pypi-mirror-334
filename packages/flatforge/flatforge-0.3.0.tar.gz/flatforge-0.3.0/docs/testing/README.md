# Testing FlatForge

This documentation provides comprehensive guidance on testing the FlatForge library, including unit tests, error handling tests, and CLI testing. It's designed to help developers understand the testing infrastructure and extend it as needed.

## Table of Contents

- [Overview](#overview)
- [Test Directory Structure](#test-directory-structure)
- [Unit Tests](#unit-tests)
- [Error Handling Tests](#error-handling-tests)
- [CLI Testing](#cli-testing)
- [Sample Test Files](#sample-test-files)
- [Debugging](#debugging)
- [Best Practices](#best-practices)
- [Extending the Tests](#extending-the-tests)

## Overview

FlatForge includes a comprehensive test suite that verifies the functionality of the library, including:

- Core functionality tests
- Error handling tests
- CLI functionality tests
- Integration tests

The tests are designed to be run using Python's built-in `unittest` framework, and can be executed individually or as a complete suite.

## Test Directory Structure

```
flatforge-repo/
├── tests/
│   ├── unit/                  # Unit tests
│   │   ├── error_handling/    # Error handling tests
│   │   │   ├── test_date_errors.py
│   │   │   ├── test_numeric_errors.py
│   │   │   ├── test_required_field_errors.py
│   │   │   ├── test_string_length_errors.py
│   │   │   ├── test_mixed_errors.py
│   │   │   └── test_sample_files.py
│   │   └── ...
│   └── integration/           # Integration tests
├── samples/
│   ├── input/
│   │   ├── errors/            # Sample error files
│   │   │   ├── date_format_errors.csv
│   │   │   ├── numeric_value_errors.csv
│   │   │   ├── required_field_errors.csv
│   │   │   ├── string_length_errors.csv
│   │   │   ├── mixed_errors.csv
│   │   │   └── fixed_length_errors.txt
│   │   └── ...
│   ├── output/                # Output directory for test results
│   │   ├── errors/            # Output directory for error tests
│   │   └── ...
│   ├── config/                # Configuration files
│   └── test_all_errors.py     # Script to test all error types
└── ...
```

## Unit Tests

Unit tests verify the functionality of individual components of the library. They are located in the `tests/unit/` directory.

### Running Unit Tests

To run all unit tests:

```bash
python -m unittest discover
```

To run a specific test file:

```bash
python -m unittest tests/unit/path/to/test_file.py
```

To run a specific test case:

```bash
python -m unittest tests.unit.path.to.test_module.TestClass.test_method
```

For more detailed information about unit testing, see [Unit Testing](unit_testing.md).

## Error Handling Tests

Error handling tests verify that the library correctly handles various error conditions, such as:

- Date format errors
- Numeric value errors
- Required field errors
- String length errors
- Mixed errors (multiple error types in a single file)

These tests are located in the `tests/unit/error_handling/` directory.

### Running Error Handling Tests

To run all error handling tests:

```bash
cd tests/unit/error_handling
python -m unittest discover
```

### Error Handling Test Files

Each error handling test file focuses on a specific type of error:

- `test_date_errors.py`: Tests for date format validation errors
- `test_numeric_errors.py`: Tests for numeric value validation errors
- `test_required_field_errors.py`: Tests for required field validation errors
- `test_string_length_errors.py`: Tests for string length validation errors
- `test_mixed_errors.py`: Tests for handling multiple types of errors in a single file
- `test_sample_files.py`: Tests that use the sample error files in the workspace

For more detailed information about error handling tests, see [Error Handling Tests](error_handling.md).

## CLI Testing

The CLI functionality can be tested using the sample scripts in the `samples/` directory.

### Running CLI Tests

To test the CLI with a specific configuration and input file:

```bash
flatforge validate --config samples/config/employee_csv.yaml --input samples/input/employee_data.csv --output samples/output/valid.csv --error samples/output/errors.csv
```

For more detailed information about CLI testing, see [CLI Testing](cli_testing.md).

## Sample Test Files

FlatForge includes a set of sample files for testing error handling. These files are located in the `samples/input/errors/` directory.

For more detailed information about sample test files, see [Sample Test Files](sample_files.md).

## Debugging

FlatForge provides several debug scripts to help you debug the library in your local IDE. These scripts are located in the root directory of the workspace and are designed to make it easier to debug different aspects of the library.

### Debug Scripts

- `debug_main.py`: Debug the core processing functionality
- `debug_cli.py`: Debug the CLI interface
- `debug_cli_chunked.py`: Debug the chunked processing functionality
- `debug_cli_convert.py`: Debug the file format conversion functionality
- `debug_cli_click.py`: Debug the CLI using Click's test runner

For more detailed information about debugging, see [Debugging](debugging.md).

## Best Practices

When testing FlatForge, follow these best practices:

1. **Test Coverage**: Ensure that tests cover all functionality, including edge cases and error conditions.
2. **Isolation**: Each test should be independent and not rely on the state of other tests.
3. **Cleanup**: Clean up any files created during tests to avoid affecting subsequent test runs.
4. **Descriptive Names**: Use descriptive names for test methods to clearly indicate what they're testing.
5. **Assertions**: Use specific assertions to verify expected behavior.
6. **Error Messages**: Include informative error messages in assertions to help diagnose failures.

## Extending the Tests

When extending FlatForge with new functionality, follow these guidelines for adding tests:

1. **Create Unit Tests**: Add unit tests for new functionality in the appropriate directory.
2. **Error Handling**: Add error handling tests for any new validation rules or error conditions.
3. **Sample Files**: Create sample files that demonstrate the new functionality and error conditions.
4. **Documentation**: Update this documentation to include information about the new tests.

### Adding a New Error Type Test

To add a test for a new error type:

1. Create a new test file in `tests/unit/error_handling/` (e.g., `test_new_error_type.py`).
2. Create a sample error file in `samples/input/errors/` (e.g., `new_error_type.csv`).
3. Add a test case in `test_sample_files.py` for the new error type.
4. Add the new error type to the `test_all_errors.py` script.

Example test structure:

```python
import os
import unittest
from flatforge.core.models import FileFormat, FileType, Section, Record, Field, SectionType
from flatforge.processors.validation import ValidationProcessor

class TestNewErrorType(unittest.TestCase):
    def setUp(self):
        # Set up test fixtures
        self._create_test_file_format()
        self._create_test_input_file()
        
    def tearDown(self):
        # Clean up after tests
        pass
        
    def _create_test_file_format(self):
        # Create a test file format with the new validation rule
        pass
        
    def _create_test_input_file(self):
        # Create a test file with the new error type
        pass
        
    def test_new_error_type(self):
        # Test handling of the new error type
        pass
        
    def test_error_details(self):
        # Test that error details are correctly captured
        pass
```

### Testing with the Sample Script

The `samples/test_all_errors.py` script can be used to test all error types, including any new ones you add:

```bash
python samples/test_all_errors.py
```

This script processes each error file and reports the results, providing a quick way to verify that error handling is working correctly. 