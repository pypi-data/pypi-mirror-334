# CLI Testing

This document provides guidance on testing the FlatForge Command Line Interface (CLI), including how to run CLI commands, test different functionality, and troubleshoot common issues.

## Overview

The FlatForge CLI provides a command-line interface for validating, transforming, and processing flat files. Testing the CLI ensures that it correctly handles various input files, configuration options, and error conditions.

## CLI Commands

FlatForge provides the following CLI commands:

- `validate`: Validates a file against a configuration
- `transform`: Transforms a file from one format to another
- `process`: Processes a file (validates and transforms)

### Validate Command

The `validate` command validates a file against a configuration:

```bash
flatforge validate --config <config_file> --input <input_file> --output <output_file> --error <error_file>
```

Parameters:
- `--config`: Path to the configuration file (YAML)
- `--input`: Path to the input file
- `--output`: Path to the output file (for valid records)
- `--error`: Path to the error file (for error details)

### Transform Command

The `transform` command transforms a file from one format to another:

```bash
flatforge transform --config <config_file> --input <input_file> --output <output_file> --error <error_file>
```

Parameters:
- `--config`: Path to the configuration file (YAML)
- `--input`: Path to the input file
- `--output`: Path to the output file (for transformed records)
- `--error`: Path to the error file (for error details)

### Process Command

The `process` command processes a file (validates and transforms):

```bash
flatforge process --config <config_file> --input <input_file> --output <output_file> --error <error_file>
```

Parameters:
- `--config`: Path to the configuration file (YAML)
- `--input`: Path to the input file
- `--output`: Path to the output file (for processed records)
- `--error`: Path to the error file (for error details)

## Testing the CLI

### Basic CLI Testing

To test the basic functionality of the CLI:

```bash
# Test validation
flatforge validate --config samples/config/employee_csv.yaml --input samples/input/employee_data.csv --output samples/output/valid.csv --error samples/output/errors.csv

# Test transformation
flatforge transform --config samples/config/csv_to_fixed_length.yaml --input samples/input/employee_data.csv --output samples/output/transformed.txt --error samples/output/errors.csv

# Test processing
flatforge process --config samples/config/employee_csv.yaml --input samples/input/employee_data.csv --output samples/output/processed.csv --error samples/output/errors.csv
```

### Testing with Sample Error Files

To test the CLI with sample error files:

```bash
# Test date format errors
flatforge validate --config samples/config/employee_csv.yaml --input samples/input/errors/date_format_errors.csv --output samples/output/errors/date_format_valid.csv --error samples/output/errors/date_format_errors.txt

# Test numeric value errors
flatforge validate --config samples/config/employee_csv.yaml --input samples/input/errors/numeric_value_errors.csv --output samples/output/errors/numeric_value_valid.csv --error samples/output/errors/numeric_value_errors.txt

# Test required field errors
flatforge validate --config samples/config/employee_csv.yaml --input samples/input/errors/required_field_errors.csv --output samples/output/errors/required_field_valid.csv --error samples/output/errors/required_field_errors.txt

# Test string length errors
flatforge validate --config samples/config/employee_csv.yaml --input samples/input/errors/string_length_errors.csv --output samples/output/errors/string_length_valid.csv --error samples/output/errors/string_length_errors.txt

# Test mixed errors
flatforge validate --config samples/config/employee_csv.yaml --input samples/input/errors/mixed_errors.csv --output samples/output/errors/mixed_valid.csv --error samples/output/errors/mixed_errors.txt

# Test fixed-length format errors
flatforge validate --config samples/config/employee_fixed_length.yaml --input samples/input/errors/fixed_length_errors.txt --output samples/output/errors/fixed_length_valid.txt --error samples/output/errors/fixed_length_errors.txt
```

### Testing with the Sample Script

The `samples/test_all_errors.py` script provides a convenient way to test the CLI with all sample error files:

```bash
python samples/test_all_errors.py
```

This script processes each sample error file and reports the results, providing a quick way to verify that the CLI correctly handles various error conditions.

## Automated CLI Testing

To automate CLI testing, you can create a script that runs various CLI commands and verifies the results:

```python
import os
import subprocess
import unittest

class TestCLI(unittest.TestCase):
    def setUp(self):
        # Set up test environment
        self.config_dir = "samples/config"
        self.input_dir = "samples/input"
        self.output_dir = "samples/output/cli_test"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def tearDown(self):
        # Clean up test environment
        for file in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, file))
            
    def test_validate_command(self):
        # Test validate command
        config_file = os.path.join(self.config_dir, "employee_csv.yaml")
        input_file = os.path.join(self.input_dir, "employee_data.csv")
        output_file = os.path.join(self.output_dir, "valid.csv")
        error_file = os.path.join(self.output_dir, "errors.csv")
        
        # Run the command
        result = subprocess.run([
            "flatforge", "validate",
            "--config", config_file,
            "--input", input_file,
            "--output", output_file,
            "--error", error_file
        ], capture_output=True, text=True)
        
        # Check the result
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(os.path.exists(error_file))
        
    # Add more test methods for other commands and scenarios
```

## Testing CLI Error Handling

To test how the CLI handles errors:

1. **Missing Parameters**: Test what happens when required parameters are missing
2. **Invalid Files**: Test what happens when input files don't exist or are invalid
3. **Invalid Configuration**: Test what happens when configuration files are invalid
4. **Permission Issues**: Test what happens when output files can't be written due to permission issues

Example:

```bash
# Test missing parameters
flatforge validate --config samples/config/employee_csv.yaml --input samples/input/employee_data.csv

# Test invalid input file
flatforge validate --config samples/config/employee_csv.yaml --input nonexistent_file.csv --output samples/output/valid.csv --error samples/output/errors.csv

# Test invalid configuration file
flatforge validate --config nonexistent_config.yaml --input samples/input/employee_data.csv --output samples/output/valid.csv --error samples/output/errors.csv
```

## Troubleshooting CLI Issues

If you encounter issues with the CLI:

1. **Check Command Syntax**: Ensure that the command syntax is correct
2. **Check File Paths**: Ensure that file paths are correct and accessible
3. **Check Configuration**: Ensure that the configuration file is valid
4. **Check Permissions**: Ensure that you have permission to read input files and write output files
5. **Check Error Output**: Check the error output for details about the issue
6. **Run with Verbose Output**: Use the `--verbose` flag to get more detailed output

## Best Practices for CLI Testing

1. **Test All Commands**: Test all CLI commands with various inputs
2. **Test Error Handling**: Test how the CLI handles various error conditions
3. **Test Edge Cases**: Test edge cases, such as large files or files with unusual formats
4. **Automate Testing**: Automate CLI testing to ensure consistent results
5. **Document Test Cases**: Document test cases and expected results
6. **Clean Up After Tests**: Clean up any files created during tests 