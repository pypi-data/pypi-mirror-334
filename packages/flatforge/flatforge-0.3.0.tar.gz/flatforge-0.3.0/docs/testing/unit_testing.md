# Unit Testing in FlatForge

This document provides detailed information about unit testing in FlatForge, including the test structure, how to run tests, and best practices for writing new tests.

## Overview

FlatForge uses Python's built-in `unittest` framework for unit testing. The unit tests are designed to verify that individual components of the library work correctly in isolation. The test suite covers:

- Core functionality
- Validation
- Transformation
- Error handling
- CLI functionality

## Test Directory Structure

```
tests/
├── unit/                   # Unit tests
│   ├── core/               # Tests for core functionality
│   │   ├── test_models.py  # Tests for core models
│   │   ├── test_validators.py # Tests for validators
│   │   └── ...
│   ├── parsers/            # Tests for parsers
│   │   ├── test_config_parser.py # Tests for config parser
│   │   └── ...
│   ├── processors/         # Tests for processors
│   │   ├── test_validation_processor.py # Tests for validation processor
│   │   ├── test_transformation_processor.py # Tests for transformation processor
│   │   └── ...
│   ├── error_handling/     # Tests for error handling
│   │   ├── test_date_errors.py # Tests for date format errors
│   │   ├── test_numeric_errors.py # Tests for numeric value errors
│   │   ├── test_required_field_errors.py # Tests for required field errors
│   │   ├── test_string_length_errors.py # Tests for string length errors
│   │   ├── test_mixed_errors.py # Tests for mixed error types
│   │   ├── test_sample_files.py # Tests using sample error files
│   │   └── ...
│   └── cli/                # Tests for CLI functionality
│       ├── test_cli.py     # Tests for CLI commands
│       └── ...
└── integration/            # Integration tests
    └── ...
```

## Running Unit Tests

### Running All Tests

To run all unit tests:

```bash
python -m unittest discover
```

This will discover and run all tests in the `tests` directory.

### Running Tests in a Specific Directory

To run tests in a specific directory:

```bash
python -m unittest discover -s tests/unit/core
```

This will run all tests in the `tests/unit/core` directory.

### Running a Specific Test File

To run a specific test file:

```bash
python -m unittest tests/unit/core/test_models.py
```

This will run all tests in the `test_models.py` file.

### Running a Specific Test Case

To run a specific test case:

```bash
python -m unittest tests.unit.core.test_models.TestRecord
```

This will run all tests in the `TestRecord` class in the `test_models.py` file.

### Running a Specific Test Method

To run a specific test method:

```bash
python -m unittest tests.unit.core.test_models.TestRecord.test_record_creation
```

This will run only the `test_record_creation` method in the `TestRecord` class.

## Test Structure

### Test Case Structure

Each test case follows a similar structure:

```python
import unittest
import os
import tempfile
from flatforge.core.models import Record

class TestRecord(unittest.TestCase):
    """Test case for the Record class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create test fixtures
        self.record_data = {
            "employee_id": "1001",
            "employee_name": "John Smith",
            "date_of_birth": "19800101",
            "country_code": "US",
            "salary": "75000.00",
            "manager_id": "1000",
            "manager_name": "Jane Doe"
        }
        
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up test fixtures
        pass
        
    def test_record_creation(self):
        """Test record creation."""
        # Create a record
        record = Record("D", self.record_data)
        
        # Check the record type
        self.assertEqual(record.record_type, "D")
        
        # Check the record data
        self.assertEqual(record.data["employee_id"], "1001")
        self.assertEqual(record.data["employee_name"], "John Smith")
        # ... more assertions ...
        
    def test_record_validation(self):
        """Test record validation."""
        # Create a record
        record = Record("D", self.record_data)
        
        # Validate the record
        validation_result = record.validate()
        
        # Check the validation result
        self.assertTrue(validation_result.is_valid)
        self.assertEqual(len(validation_result.errors), 0)
        
    # ... more test methods ...
```

### Test Fixtures

Test fixtures are set up in the `setUp` method and torn down in the `tearDown` method. Common test fixtures include:

- Test data
- Temporary files
- Mock objects

### Assertions

The `unittest` framework provides a variety of assertions for testing:

- `assertEqual(a, b)`: Check that `a` equals `b`
- `assertNotEqual(a, b)`: Check that `a` does not equal `b`
- `assertTrue(x)`: Check that `x` is `True`
- `assertFalse(x)`: Check that `x` is `False`
- `assertIs(a, b)`: Check that `a` is `b`
- `assertIsNot(a, b)`: Check that `a` is not `b`
- `assertIsNone(x)`: Check that `x` is `None`
- `assertIsNotNone(x)`: Check that `x` is not `None`
- `assertIn(a, b)`: Check that `a` is in `b`
- `assertNotIn(a, b)`: Check that `a` is not in `b`
- `assertIsInstance(a, b)`: Check that `a` is an instance of `b`
- `assertNotIsInstance(a, b)`: Check that `a` is not an instance of `b`
- `assertRaises(exc, fun, *args, **kwds)`: Check that `fun(*args, **kwds)` raises `exc`
- `assertRaisesRegex(exc, r, fun, *args, **kwds)`: Check that `fun(*args, **kwds)` raises `exc` and the message matches regex `r`
- `assertWarns(warn, fun, *args, **kwds)`: Check that `fun(*args, **kwds)` raises `warn`
- `assertWarnsRegex(warn, r, fun, *args, **kwds)`: Check that `fun(*args, **kwds)` raises `warn` and the message matches regex `r`
- `assertLogs(logger, level)`: Check that the code logs on `logger` with minimum level `level`
- `assertAlmostEqual(a, b)`: Check that `a` is approximately equal to `b`
- `assertNotAlmostEqual(a, b)`: Check that `a` is not approximately equal to `b`
- `assertGreater(a, b)`: Check that `a` is greater than `b`
- `assertGreaterEqual(a, b)`: Check that `a` is greater than or equal to `b`
- `assertLess(a, b)`: Check that `a` is less than `b`
- `assertLessEqual(a, b)`: Check that `a` is less than or equal to `b`
- `assertRegex(s, r)`: Check that `s` matches regex `r`
- `assertNotRegex(s, r)`: Check that `s` does not match regex `r`
- `assertCountEqual(a, b)`: Check that `a` and `b` have the same elements in the same number, regardless of order

## Core Unit Tests

### Core Models Tests

The core models tests verify that the core models work correctly:

- `Record`: Tests for record creation, validation, and transformation
- `Field`: Tests for field creation, validation, and transformation
- `ValidationResult`: Tests for validation result creation and manipulation
- `ProcessingResult`: Tests for processing result creation and manipulation

Example:

```python
def test_record_validation(self):
    """Test record validation with a valid record."""
    # Create a record
    record = Record("D", self.record_data)
    
    # Create a validator
    validator = RecordValidator(self.file_format)
    
    # Validate the record
    validation_result = validator.validate(record)
    
    # Check the validation result
    self.assertTrue(validation_result.is_valid)
    self.assertEqual(len(validation_result.errors), 0)
```

### Validators Tests

The validators tests verify that the validators work correctly:

- `FieldValidator`: Tests for field validation
- `RecordValidator`: Tests for record validation
- `FileValidator`: Tests for file validation

Example:

```python
def test_required_field_validation(self):
    """Test required field validation."""
    # Create a field with a required value
    field = Field("employee_id", "1001", {"required": True})
    
    # Create a validator
    validator = FieldValidator()
    
    # Validate the field
    validation_result = validator.validate(field)
    
    # Check the validation result
    self.assertTrue(validation_result.is_valid)
    self.assertEqual(len(validation_result.errors), 0)
    
    # Create a field with a missing required value
    field = Field("employee_id", "", {"required": True})
    
    # Validate the field
    validation_result = validator.validate(field)
    
    # Check the validation result
    self.assertFalse(validation_result.is_valid)
    self.assertEqual(len(validation_result.errors), 1)
    self.assertEqual(validation_result.errors[0].error_type, "REQUIRED_FIELD")
```

## Error Handling Tests

The error handling tests verify that the library correctly handles various error conditions:

- Date format errors
- Numeric value errors
- Required field errors
- String length errors
- Mixed errors

Example:

```python
def test_date_format_errors(self):
    """Test handling of date format errors."""
    # Create a processor
    processor = ValidationProcessor(self.file_format)
    
    # Process the file
    result = processor.process(self.input_file, self.output_file, self.error_file)
    
    # Check the results
    self.assertEqual(result.total_records, 8)  # Header + 6 body records + footer
    self.assertEqual(result.valid_records, 3)  # Header + 1 body record + footer
    self.assertEqual(result.failed_records, 5)  # 5 body records with errors
    self.assertEqual(result.error_count, 5)  # 5 errors
    
    # Check the error file
    with open(self.error_file, "r") as f:
        error_content = f.read()
        
    # Check that the error file contains the expected errors
    self.assertIn("Invalid date format", error_content)
    self.assertIn("30-Feb-2023", error_content)
    self.assertIn("2023/02/15", error_content)
    self.assertIn("04-25-1995", error_content)
    self.assertIn("31-11-1988", error_content)
    self.assertIn("20231301", error_content)
```

## CLI Tests

The CLI tests verify that the CLI functionality works correctly:

- Command execution
- Parameter handling
- Error handling

Example:

```python
def test_validate_command(self):
    """Test the validate command."""
    # Create a runner
    runner = CliRunner()
    
    # Run the command
    result = runner.invoke(cli, [
        "validate",
        "--config", self.config_file,
        "--input", self.input_file,
        "--output", self.output_file,
        "--error", self.error_file
    ])
    
    # Check the result
    self.assertEqual(result.exit_code, 0)
    self.assertIn("Processed 8 records", result.output)
    self.assertIn("Valid records: 3", result.output)
    self.assertIn("Failed records: 5", result.output)
    self.assertIn("Errors: 5", result.output)
```

## Writing New Unit Tests

### Creating a New Test File

To create a new test file:

1. Create a new file in the appropriate directory with a name starting with `test_`
2. Import the `unittest` module and the modules you want to test
3. Create a test case class that inherits from `unittest.TestCase`
4. Add test methods to the class with names starting with `test_`
5. Add a `setUp` method to set up test fixtures
6. Add a `tearDown` method to clean up test fixtures

Example:

```python
import unittest
import os
import tempfile
from flatforge.core.models import Record

class TestNewFeature(unittest.TestCase):
    """Test case for a new feature."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create test fixtures
        pass
        
    def tearDown(self):
        """Tear down test fixtures."""
        # Clean up test fixtures
        pass
        
    def test_new_feature(self):
        """Test the new feature."""
        # Test the new feature
        pass
```

### Adding Test Methods

To add a new test method:

1. Add a method to the test case class with a name starting with `test_`
2. Add a docstring to describe the test
3. Add code to test the functionality
4. Add assertions to verify the results

Example:

```python
def test_new_feature(self):
    """Test the new feature."""
    # Test the new feature
    result = new_feature()
    
    # Verify the results
    self.assertEqual(result, expected_result)
```

### Testing Error Conditions

To test error conditions:

1. Use the `assertRaises` method to check that the code raises the expected exception
2. Use the `assertRaisesRegex` method to check that the exception message matches the expected pattern

Example:

```python
def test_error_condition(self):
    """Test an error condition."""
    # Test that the code raises the expected exception
    with self.assertRaises(ValueError):
        # Code that should raise a ValueError
        new_feature(invalid_input)
        
    # Test that the exception message matches the expected pattern
    with self.assertRaisesRegex(ValueError, "Invalid input"):
        # Code that should raise a ValueError with a specific message
        new_feature(invalid_input)
```

### Testing with Temporary Files

To test with temporary files:

1. Use the `tempfile` module to create temporary files
2. Use the `setUp` method to create the temporary files
3. Use the `tearDown` method to clean up the temporary files

Example:

```python
def setUp(self):
    """Set up test fixtures."""
    # Create temporary files
    self.temp_dir = tempfile.TemporaryDirectory()
    self.input_file = os.path.join(self.temp_dir.name, "input.csv")
    self.output_file = os.path.join(self.temp_dir.name, "output.csv")
    self.error_file = os.path.join(self.temp_dir.name, "error.txt")
    
    # Create the input file
    with open(self.input_file, "w") as f:
        f.write("H,BATCH001,20230101120000\n")
        f.write("D,1001,John Smith,19800101,US,75000.00,1000,Jane Doe\n")
        f.write("F,75000.00,1\n")
        
def tearDown(self):
    """Tear down test fixtures."""
    # Clean up temporary files
    self.temp_dir.cleanup()
```

## Best Practices

### Test Coverage

- Aim for high test coverage (80% or higher)
- Test all public methods and functions
- Test both normal and error conditions
- Test edge cases and boundary conditions

### Test Isolation

- Each test should be independent of other tests
- Tests should not depend on the order in which they are run
- Tests should not depend on external resources (e.g., databases, web services)
- Use test fixtures to set up and tear down test environments

### Test Cleanup

- Clean up all resources created during tests
- Use the `tearDown` method to clean up test fixtures
- Use context managers (`with` statements) to ensure resources are cleaned up

### Descriptive Names

- Use descriptive names for test methods
- Include the method being tested and the scenario being tested
- Use the `test_` prefix for test methods

### Assertions

- Use the most specific assertion for the condition being tested
- Include descriptive messages in assertions
- Test one condition per assertion

### Documentation

- Include docstrings for all test methods
- Describe what the test is testing and why
- Include examples of expected inputs and outputs

### Continuous Integration

- Run tests automatically on code changes
- Use a continuous integration service (e.g., GitHub Actions, Travis CI)
- Fail the build if tests fail

## Troubleshooting

### Common Issues

- **Test not running**: Check that the test method name starts with `test_`
- **Test failing**: Check the assertion message for details
- **Test hanging**: Check for infinite loops or blocking calls
- **Test crashing**: Check for exceptions in the test code

### Debugging Tests

- Use the `-v` flag to run tests with verbose output
- Use the `pdb` module to debug tests
- Use the `print` function to print debug information

Example:

```bash
python -m unittest -v tests/unit/core/test_models.py
```

### Test Failures

If a test fails, the error message will include:

- The test method that failed
- The assertion that failed
- The expected and actual values
- The line number where the failure occurred

Example:

```
FAIL: test_record_validation (tests.unit.core.test_models.TestRecord)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "tests/unit/core/test_models.py", line 42, in test_record_validation
    self.assertTrue(validation_result.is_valid)
AssertionError: False is not true
```

## Conclusion

Unit testing is an essential part of the FlatForge development process. By following the guidelines in this document, you can write effective unit tests that help ensure the library works correctly and reliably. 