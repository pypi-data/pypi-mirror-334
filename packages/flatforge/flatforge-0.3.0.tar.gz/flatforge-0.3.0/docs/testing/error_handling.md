# Error Handling Tests

This document provides detailed information about the error handling tests in FlatForge, including the test files, sample error files, and how to run and extend the tests.

## Overview

Error handling is a critical aspect of FlatForge, as it ensures that the library correctly identifies and reports errors in input files. The error handling tests verify that FlatForge correctly handles various error conditions, such as:

- Date format errors
- Numeric value errors
- Required field errors
- String length errors
- Mixed errors (multiple error types in a single file)

## Test Files

The error handling tests are located in the `tests/unit/error_handling/` directory:

- `test_date_errors.py`: Tests for date format validation errors
- `test_numeric_errors.py`: Tests for numeric value validation errors
- `test_required_field_errors.py`: Tests for required field validation errors
- `test_string_length_errors.py`: Tests for string length validation errors
- `test_mixed_errors.py`: Tests for handling multiple types of errors in a single file
- `test_sample_files.py`: Tests that use the sample error files in the workspace

## Sample Error Files

FlatForge includes a set of sample files for testing error handling. These files are located in the `samples/input/errors/` directory:

- `date_format_errors.csv`: Contains records with date format errors
- `numeric_value_errors.csv`: Contains records with numeric value errors
- `required_field_errors.csv`: Contains records with missing required fields
- `string_length_errors.csv`: Contains records with string length errors
- `mixed_errors.csv`: Contains records with multiple types of errors
- `fixed_length_errors.txt`: Contains records with errors specific to fixed-length formats

### Date Format Errors

The `date_format_errors.csv` file contains the following records:

```
H,BATCH001,20230101120000
D,1001,John Smith,30-Feb-2023,US,75000.00,1000,Jane Doe
D,1002,Alice Johnson,2023/02/15,CA,80000.00,1000,Jane Doe
D,1003,Bob Williams,19900320,UK,65000.00,1001,John Smith
D,1004,Carol Brown,04-25-1995,AU,60000.00,1001,John Smith
D,1005,David Miller,31-11-1988,DE,70000.00,1002,Alice Johnson
D,1006,Eve Wilson,20231301,FR,72000.00,1002,Alice Johnson
F,422000.00,6
```

Error details:
- Record 2: Invalid date (February 30)
- Record 3: Wrong date format (using slashes)
- Record 5: Wrong date format (using dashes)
- Record 6: Invalid date (November 31)
- Record 7: Invalid date (month 13)

### Numeric Value Errors

The `numeric_value_errors.csv` file contains the following records:

```
H,BATCH001,20230101120000
D,ABC1,John Smith,19800101,US,75000.00,1000,Jane Doe
D,1002,Alice Johnson,19850215,CA,80K,1000,Jane Doe
D,1003,Bob Williams,19900320,UK,65,000.00,1001,John Smith
D,1004,Carol Brown,19950425,AU,-60000.00,1001,John Smith
D,1005,David Miller,19881130,DE,70000.00,MANAGER,Alice Johnson
F,350000.00,FIVE
```

Error details:
- Record 2: Non-numeric employee ID (`ABC1`)
- Record 3: Non-numeric salary (`80K`)
- Record 4: Incorrectly formatted number (`65,000.00`)
- Record 5: Negative salary (if not allowed)
- Record 6: Non-numeric manager ID (`MANAGER`)
- Record 7: Non-numeric employee count (`FIVE`)

### Required Field Errors

The `required_field_errors.csv` file contains the following records:

```
H,BATCH001,20230101120000
D,1001,,19800101,US,75000.00,1000,Jane Doe
D,,Alice Johnson,19850215,CA,80000.00,1000,Jane Doe
D,1003,Bob Williams,,UK,65000.00,1001,John Smith
D,1004,Carol Brown,19950425,,60000.00,1001,John Smith
D,1005,David Miller,19881130,DE,,1002,Alice Johnson
F,,5
```

Error details:
- Record 2: Missing employee name
- Record 3: Missing employee ID
- Record 4: Missing date of birth (not required)
- Record 5: Missing country code (not required)
- Record 6: Missing salary (not required)
- Record 7: Missing total salary

### String Length Errors

The `string_length_errors.csv` file contains the following records:

```
H,BATCH001TOOLONG,20230101120000
D,1001,John Smith with an extremely long name that exceeds the maximum length,19800101,US,75000.00,1000,Jane Doe
D,1002,Alice Johnson,19850215,USA,80000.00,1000,Jane Doe
D,1003,Bob Williams,19900320,U,65000.00,1001,John Smith
D,1004,Carol Brown,19950425,AUSTRALIA,60000.00,1001,John Smith
D,1005,David Miller,19881130,DE,70000.00,1002,Alice Johnson
F,350000.00,5
```

Error details:
- Record 1: Batch reference too long
- Record 2: Employee name too long
- Record 3: Country code too long (`USA` instead of 2 characters)
- Record 4: Country code too short (`U` instead of 2 characters)
- Record 5: Country code too long (`AUSTRALIA` instead of 2 characters)

### Mixed Errors

The `mixed_errors.csv` file contains the following records:

```
H,BATCH001,20230101120000
D,ABC1,,30-Feb-2023,USA,75K,1000,Jane Doe
D,1002,Alice Johnson with an extremely long name that exceeds the maximum length,19850215,CA,80000.00,MANAGER,Jane Doe
D,1003,Bob Williams,19900320,UK,65000.00,1001,
D,,Carol Brown,04-25-1995,AU,-60000.00,1001,John Smith
D,1005,David Miller,31-11-1988,D,70000.00,1002,Alice Johnson
F,NOT_A_NUMBER,FIVE
```

Error details:
- Record 2: Non-numeric employee ID, missing employee name, invalid date, country code too long, non-numeric salary
- Record 3: Employee name too long, non-numeric manager ID
- Record 4: Missing manager name
- Record 5: Missing employee ID, wrong date format, negative salary
- Record 6: Invalid date, country code too short
- Record 7: Non-numeric total salary, non-numeric employee count

### Fixed-Length Format Errors

The `fixed_length_errors.txt` file contains records with errors specific to fixed-length formats:

```
H BATCH001  20230101120000
D 1001      John Smith                         30-Feb-2023US       75000.00  1000      Jane Doe                          
D 1002      Alice Johnson                      19850215   CAL      80K       1000      Jane Doe                          
D 1003      Bob Williams                       19900320   UK       65000.00  1001      John Smith                        
D 1004      Carol Brown                        19950425   AU       -60000.00 1001      John Smith                        
D 1005      David Miller                       19881130   DE       70000.00  MANAGER   Alice Johnson                     
F 350000.00 FIVE      
```

Error details:
- Record 2: Invalid date
- Record 3: Country code too long, non-numeric salary
- Record 5: Negative salary
- Record 6: Non-numeric manager ID
- Record 7: Non-numeric employee count

## Running the Tests

### Running Individual Test Files

To run a specific error handling test file:

```bash
cd tests/unit/error_handling
python -m unittest test_date_errors.py
```

### Running All Error Handling Tests

To run all error handling tests:

```bash
cd tests/unit/error_handling
python -m unittest discover
```

### Running Tests with Sample Files

The `test_sample_files.py` file contains tests that use the sample error files in the workspace. To run these tests:

```bash
cd tests/unit/error_handling
python -m unittest test_sample_files.py
```

### Running the Sample Script

The `samples/test_all_errors.py` script processes all sample error files and reports the results:

```bash
python samples/test_all_errors.py
```

## Test Structure

Each error handling test file follows a similar structure:

1. **Setup**: Creates a test file format and test input file with specific errors
2. **Teardown**: Cleans up any files created during the test
3. **Test Methods**: Verify that errors are correctly identified and reported

Example test method:

```python
def test_date_format_errors(self):
    """Test handling of date format errors."""
    # Create a processor
    processor = ValidationProcessor(self.file_format)
    
    # Process the file
    result = processor.process(self.test_input_file, self.test_output_file, self.test_error_file)
    
    # Check the results
    self.assertEqual(result.total_records, 8)  # Header + 6 body records + footer
    self.assertEqual(result.valid_records, 3)  # Header, one valid body record, and footer
    self.assertEqual(result.failed_records, 5)  # 5 invalid body records
    self.assertGreater(result.error_count, 0)  # Should have errors
    
    # Check that the error file exists and has content
    self.assertTrue(os.path.exists(self.test_error_file))
    with open(self.test_error_file, "r") as f:
        error_content = f.read()
        self.assertIn("date_of_birth", error_content)  # Should mention the field name
        self.assertIn("30-Feb-2023", error_content)  # Should mention the invalid value
```

## Extending the Tests

### Adding a New Error Type

To add a test for a new error type:

1. Create a new test file in `tests/unit/error_handling/` (e.g., `test_new_error_type.py`)
2. Create a sample error file in `samples/input/errors/` (e.g., `new_error_type.csv`)
3. Add a test case in `test_sample_files.py` for the new error type
4. Add the new error type to the `test_all_errors.py` script

### Adding a New Validation Rule

To add a test for a new validation rule:

1. Add the validation rule to the appropriate test file format
2. Add test cases that verify the rule is correctly applied
3. Add sample records that violate the rule to the appropriate sample error file

Example validation rule:

```python
Field(name="email", position=8, rules=[
    {"type": "email", "params": {"allow_empty": True}}
])
```

## Best Practices

When writing error handling tests, follow these best practices:

1. **Test Both Valid and Invalid Cases**: Include both valid and invalid records in test files
2. **Test Edge Cases**: Include edge cases, such as boundary values
3. **Verify Error Details**: Check that error messages include specific details about the error
4. **Clean Up After Tests**: Remove any files created during tests
5. **Use Descriptive Names**: Use descriptive names for test methods and variables
6. **Document Test Files**: Include comments in test files explaining the purpose of each test case

## Troubleshooting

If you encounter issues with the error handling tests:

1. **Check File Paths**: Ensure that file paths are correct and use absolute paths when necessary
2. **Check File Format**: Ensure that the file format matches the expected format
3. **Check Validation Rules**: Ensure that validation rules are correctly defined
4. **Check Error Messages**: Check that error messages are correctly formatted
5. **Run with Verbose Output**: Use the `-v` flag to get more detailed output: `python -m unittest discover -v` 