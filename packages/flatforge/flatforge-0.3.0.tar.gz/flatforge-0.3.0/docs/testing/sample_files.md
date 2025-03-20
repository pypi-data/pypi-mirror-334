# Sample Test Files

This document provides detailed information about the sample test files included in FlatForge, including their structure, purpose, and how to use them for testing.

## Overview

FlatForge includes a set of sample files for testing various aspects of the library, including:

- Validation
- Transformation
- Error handling
- CLI functionality

These files are located in the `samples/` directory and are organized by purpose.

## Directory Structure

```
samples/
├── config/                # Configuration files
│   ├── employee_csv.yaml                    # CSV format configuration
│   ├── employee_fixed_length.yaml           # Fixed-length format configuration
│   ├── employee_csv_no_identifier.yaml      # CSV format without identifier
│   ├── employee_fixed_length_no_identifier.yaml # Fixed-length without identifier
│   ├── csv_to_fixed_length.yaml             # Transformation configuration
│   └── ...
├── input/                 # Input files
│   ├── employee_data.csv                    # Valid employee data (CSV)
│   ├── employee_data_no_identifier.csv      # Employee data without identifier
│   ├── errors/                              # Error test files
│   │   ├── date_format_errors.csv           # Date format errors
│   │   ├── numeric_value_errors.csv         # Numeric value errors
│   │   ├── required_field_errors.csv        # Required field errors
│   │   ├── string_length_errors.csv         # String length errors
│   │   ├── mixed_errors.csv                 # Mixed error types
│   │   └── fixed_length_errors.txt          # Fixed-length format errors
│   └── ...
├── output/                # Output directory for test results
│   ├── errors/                              # Output directory for error tests
│   └── ...
├── test_all_errors.py     # Script to test all error types
└── ...
```

## Configuration Files

### Employee CSV Configuration (`employee_csv.yaml`)

This configuration defines a CSV file format for employee data with the following fields:

- Record type (header, body, footer)
- Employee ID
- Employee name
- Date of birth
- Country code
- Salary
- Manager ID
- Manager name

It includes validation rules for each field, such as:

- Required fields
- Numeric values
- Date formats
- String lengths

### Employee Fixed-Length Configuration (`employee_fixed_length.yaml`)

This configuration defines a fixed-length file format for employee data with the same fields as the CSV format, but with fixed positions and lengths for each field.

### Transformation Configuration (`csv_to_fixed_length.yaml`)

This configuration defines a transformation from the CSV format to the fixed-length format, mapping fields from the source format to the target format.

## Input Files

### Valid Employee Data (`employee_data.csv`)

This file contains valid employee data in CSV format, with a header record, multiple body records, and a footer record.

### Error Test Files

#### Date Format Errors (`date_format_errors.csv`)

This file contains records with various date format errors:

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

#### Numeric Value Errors (`numeric_value_errors.csv`)

This file contains records with various numeric value errors:

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

#### Required Field Errors (`required_field_errors.csv`)

This file contains records with missing required fields:

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

#### String Length Errors (`string_length_errors.csv`)

This file contains records with string length errors:

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

#### Mixed Errors (`mixed_errors.csv`)

This file contains records with multiple types of errors:

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

#### Fixed-Length Format Errors (`fixed_length_errors.txt`)

This file contains records with errors specific to fixed-length formats:

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

## Sample Scripts

### Test All Errors Script (`test_all_errors.py`)

This script processes all sample error files and reports the results:

```python
"""
Test script for running all error handling tests in FlatForge.

This script runs tests for all error types using the sample error files.
"""
import os
import sys
import traceback
from flatforge.parsers import ConfigParser
from flatforge.processors import ValidationProcessor
from flatforge.core.models import ProcessingResult

def process_file(config_path, input_path, output_path, error_path, description):
    """Process a file and handle errors."""
    try:
        print(f"\n=== Testing {description} ===")
        print(f"Config: {config_path}")
        print(f"Input: {input_path}")
        print(f"Output: {output_path}")
        print(f"Error: {error_path}")
        
        # Parse the configuration
        config_parser = ConfigParser.from_file(config_path)
        file_format = config_parser.parse()
        
        # Create a processor
        processor = ValidationProcessor(file_format)
        
        # Process the file
        result = processor.process(input_path, output_path, error_path)
        
        # Print the results
        print(f"Total records: {result.total_records}")
        print(f"Valid records: {result.valid_records}")
        print(f"Failed records: {result.failed_records}")
        print(f"Error count: {result.error_count}")
        
        # Print the first few errors
        if result.errors:
            print("\nSample errors:")
            for i, error in enumerate(result.errors[:3]):
                print(f"  {i+1}. {error}")
            if len(result.errors) > 3:
                print(f"  ... and {len(result.errors) - 3} more errors")
        
        return result
        
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return None

def main():
    """Run all error handling tests."""
    # Base paths
    base_dir = os.path.abspath(os.path.dirname(__file__))
    config_dir = os.path.join(base_dir, "config")
    input_dir = os.path.join(base_dir, "input/errors")
    output_dir = os.path.join(base_dir, "output/errors")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Test cases
    test_cases = [
        {
            "config": os.path.join(config_dir, "employee_csv.yaml"),
            "input": os.path.join(input_dir, "date_format_errors.csv"),
            "output": os.path.join(output_dir, "date_format_valid.csv"),
            "error": os.path.join(output_dir, "date_format_errors.txt"),
            "description": "Date Format Errors"
        },
        # ... other test cases ...
    ]
    
    # Run the tests
    results = []
    for test_case in test_cases:
        result = process_file(
            test_case["config"],
            test_case["input"],
            test_case["output"],
            test_case["error"],
            test_case["description"]
        )
        results.append((test_case["description"], result))
    
    # Print summary
    print("\n=== Summary ===")
    for description, result in results:
        if result:
            print(f"{description}: {result.valid_records}/{result.total_records} valid, {result.error_count} errors")
        else:
            print(f"{description}: Failed to process")

if __name__ == "__main__":
    main()
```

To run this script:

```bash
python samples/test_all_errors.py
```

## Using Sample Files for Testing

### Manual Testing

You can use the sample files for manual testing:

1. **Validation Testing**: Use the sample error files to test validation functionality
2. **Transformation Testing**: Use the valid employee data to test transformation functionality
3. **CLI Testing**: Use the sample files to test CLI functionality

Example:

```bash
# Test validation with date format errors
flatforge validate --config samples/config/employee_csv.yaml --input samples/input/errors/date_format_errors.csv --output samples/output/errors/date_format_valid.csv --error samples/output/errors/date_format_errors.txt
```

### Automated Testing

You can use the sample files for automated testing:

1. **Unit Tests**: Use the sample files in unit tests to verify functionality
2. **Integration Tests**: Use the sample files in integration tests to verify end-to-end functionality
3. **CLI Tests**: Use the sample files in CLI tests to verify CLI functionality

Example unit test:

```python
def test_date_format_errors(self):
    """Test handling of date format errors using sample file."""
    # Create a processor
    processor = ValidationProcessor(self.file_format)
    
    # Process the file
    result = processor.process(self.date_format_input, self.date_format_output, self.date_format_error)
    
    # Check the results
    self.assertEqual(result.total_records, 8)  # Header + 6 body records + footer
    self.assertGreater(result.valid_records, 0)  # Should have some valid records
    self.assertGreater(result.failed_records, 0)  # Should have some failed records
    self.assertGreater(result.error_count, 0)  # Should have errors
```

## Creating New Sample Files

To create new sample files:

1. **Identify the Test Case**: Determine what aspect of the library you want to test
2. **Create the Sample File**: Create a file with appropriate content for the test case
3. **Add to the Test Suite**: Add the file to the appropriate test suite
4. **Document the File**: Document the file's purpose and structure

Example:

```python
# Create a new sample file for email validation errors
with open("samples/input/errors/email_validation_errors.csv", "w") as f:
    f.write("H,BATCH001,20230101120000\n")
    f.write("D,1001,John Smith,19800101,US,75000.00,1000,Jane Doe,john.smith@example\n")  # Missing TLD
    f.write("D,1002,Alice Johnson,19850215,CA,80000.00,1000,Jane Doe,alice.johnson@\n")  # Missing domain
    f.write("D,1003,Bob Williams,19900320,UK,65000.00,1001,John Smith,@example.com\n")  # Missing username
    f.write("D,1004,Carol Brown,19950425,AU,60000.00,1001,John Smith,carol.brown@example.com\n")  # Valid email
    f.write("F,280000.00,4\n")
```

## Best Practices

1. **Use Realistic Data**: Use realistic data in sample files to ensure tests are representative of real-world scenarios
2. **Include Edge Cases**: Include edge cases in sample files to test boundary conditions
3. **Document Error Cases**: Document the specific errors in each sample file to make it clear what's being tested
4. **Keep Files Small**: Keep sample files small to make them easy to understand and debug
5. **Use Consistent Formats**: Use consistent formats across sample files to make them easier to work with
6. **Version Control**: Keep sample files under version control to track changes over time 