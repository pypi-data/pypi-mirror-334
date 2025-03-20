# FlatForge CLI Examples

This document provides examples of how to use the FlatForge command-line interface (CLI) to test all the sample configurations and input files included in the repository.

## Basic CLI Commands

FlatForge provides three main commands:

1. `validate`: Validate a file against a schema
2. `convert`: Convert a file from one format to another
3. `count`: Count records in a file

## Validation Examples

### Validating a Fixed-Length File

```bash
flatforge validate --config schemas/fixed_length.yaml --input data/fixed_length.txt --output output/valid.txt --errors output/errors.txt
```

### Validating a Delimited File

```bash
flatforge validate --config schemas/delimited.yaml --input data/delimited.csv --output output/valid.csv --errors output/errors.csv
```

### Validating with Record Type Identifiers

```bash
flatforge validate --config schemas/multi_section.yaml --input data/multi_section.txt --output output/valid.txt --errors output/errors.txt
```

## Conversion Examples

### Converting from Fixed-Length to Delimited

```bash
flatforge convert --input-config schemas/fixed_length.yaml --output-config schemas/delimited.yaml --input data/fixed_length.txt --output output/converted.csv --errors output/errors.csv
```

### Converting with Mapping Configuration

```bash
flatforge convert --input-config schemas/fixed_length.yaml --output-config schemas/delimited.yaml --mapping schemas/mapping.yaml --input data/fixed_length.txt --output output/converted.csv --errors output/errors.csv
```

### Converting with Transformation Rules

```bash
flatforge convert --input-config schemas/fixed_length_with_transformations.yaml --output-config schemas/delimited.yaml --input data/fixed_length.txt --output output/converted.csv --errors output/errors.csv
```

## Counting Examples

### Counting Records in a Fixed-Length File

```bash
flatforge count --config schemas/fixed_length.yaml --input data/fixed_length.txt --output output/counts.txt
```

### Counting Records in a Delimited File

```bash
flatforge count --config schemas/delimited.yaml --input data/delimited.csv --output output/counts.txt
```

### Counting Records with Record Type Identifiers

```bash
flatforge count --config schemas/multi_section.yaml --input data/multi_section.txt --output output/counts.txt
```

## Testing All Transformation Rules

To test all transformation rules at once, you can use the provided Python script:

```bash
python samples/test_transformations.py
```

This script will:
1. Test transformations on delimited files
2. Test transformations on fixed-length files
3. Test format conversion between delimited and fixed-length formats

## Batch Testing

You can create a shell script to run all the tests at once. Here's an example for Unix-based systems:

```bash
#!/bin/bash

# Create output directory if it doesn't exist
mkdir -p samples/output

# Validation tests
echo "Running validation tests..."

# Employee data tests
flatforge validate --config samples/config/employee_fixed_length.yaml --input samples/input/employee_data.txt --output samples/output/employee_data_valid.txt --errors samples/output/employee_data_errors.txt
flatforge validate --config samples/config/employee_fixed_length_no_identifier.yaml --input samples/input/employee_data_no_identifier.txt --output samples/output/employee_data_no_identifier_valid.txt --errors samples/output/employee_data_no_identifier_errors.txt
flatforge validate --config samples/config/employee_csv.yaml --input samples/input/employee_data.csv --output samples/output/employee_data_valid.csv --errors samples/output/employee_data_errors.csv
flatforge validate --config samples/config/employee_csv_no_identifier.yaml --input samples/input/employee_data_no_identifier.csv --output samples/output/employee_data_no_identifier_valid.csv --errors samples/output/employee_data_no_identifier_errors.csv

# Transformation tests
flatforge validate --config samples/config/transformation_rules_fixed_length.yaml --input samples/input/transformation_test_fixed_length.txt --output samples/output/transformation_test_fixed_length_valid.txt --errors samples/output/transformation_test_fixed_length_errors.txt
flatforge validate --config samples/config/transformation_rules_test.yaml --input samples/input/transformation_test_input.csv --output samples/output/transformation_test_valid.csv --errors samples/output/transformation_test_errors.csv

# Conversion tests
echo "Running conversion tests..."
flatforge convert --input-config samples/config/employee_csv.yaml --output-config samples/config/employee_fixed_length.yaml --input samples/input/employee_data.csv --output samples/output/employee_data_converted.txt --errors samples/output/employee_data_conversion_errors.txt
flatforge convert --input-config samples/config/employee_fixed_length.yaml --output-config samples/config/employee_csv.yaml --input samples/input/employee_data.txt --output samples/output/employee_data_converted.csv --errors samples/output/employee_data_conversion_errors.csv
flatforge convert --input-config samples/config/transformation_rules_test.yaml --output-config samples/config/transformation_rules_fixed_length.yaml --input samples/input/transformation_test_input.csv --output samples/output/transformation_test_converted.txt --errors samples/output/transformation_test_conversion_errors.txt
flatforge convert --input-config samples/config/transformation_rules_fixed_length.yaml --output-config samples/config/transformation_rules_test.yaml --input samples/input/transformation_test_fixed_length.txt --output samples/output/transformation_test_converted.csv --errors samples/output/transformation_test_conversion_errors.csv

# Counting tests
echo "Running counting tests..."
flatforge count --config samples/config/employee_fixed_length.yaml --input samples/input/employee_data.txt --output samples/output/employee_data_counts.txt
flatforge count --config samples/config/employee_csv.yaml --input samples/input/employee_data.csv --output samples/output/employee_data_counts.txt
flatforge count --config samples/config/transformation_rules_fixed_length.yaml --input samples/input/transformation_test_fixed_length.txt --output samples/output/transformation_test_fixed_length_counts.txt
flatforge count --config samples/config/transformation_rules_test.yaml --input samples/input/transformation_test_input.csv --output samples/output/transformation_test_counts.txt

# Run the Python test script
echo "Running Python test script..."
python samples/test_transformations.py

echo "All tests completed."
```

For Windows systems, you can create a similar batch file:

```batch
@echo off
REM Create output directory if it doesn't exist
mkdir samples\output 2>nul

REM Validation tests
echo Running validation tests...

REM Employee data tests
flatforge validate --config samples\config\employee_fixed_length.yaml --input samples\input\employee_data.txt --output samples\output\employee_data_valid.txt --errors samples\output\employee_data_errors.txt
flatforge validate --config samples\config\employee_fixed_length_no_identifier.yaml --input samples\input\employee_data_no_identifier.txt --output samples\output\employee_data_no_identifier_valid.txt --errors samples\output\employee_data_no_identifier_errors.txt
flatforge validate --config samples\config\employee_csv.yaml --input samples\input\employee_data.csv --output samples\output\employee_data_valid.csv --errors samples\output\employee_data_errors.csv
flatforge validate --config samples\config\employee_csv_no_identifier.yaml --input samples\input\employee_data_no_identifier.csv --output samples\output\employee_data_no_identifier_valid.csv --errors samples\output\employee_data_no_identifier_errors.csv

REM Transformation tests
flatforge validate --config samples\config\transformation_rules_fixed_length.yaml --input samples\input\transformation_test_fixed_length.txt --output samples\output\transformation_test_fixed_length_valid.txt --errors samples\output\transformation_test_fixed_length_errors.txt
flatforge validate --config samples\config\transformation_rules_test.yaml --input samples\input\transformation_test_input.csv --output samples\output\transformation_test_valid.csv --errors samples\output\transformation_test_errors.csv

REM Conversion tests
echo Running conversion tests...
flatforge convert --input-config samples\config\employee_csv.yaml --output-config samples\config\employee_fixed_length.yaml --input samples\input\employee_data.csv --output samples\output\employee_data_converted.txt --errors samples\output\employee_data_conversion_errors.txt
flatforge convert --input-config samples\config\employee_fixed_length.yaml --output-config samples\config\employee_csv.yaml --input samples\input\employee_data.txt --output samples\output\employee_data_converted.csv --errors samples\output\employee_data_conversion_errors.csv
flatforge convert --input-config samples\config\transformation_rules_test.yaml --output-config samples\config\transformation_rules_fixed_length.yaml --input samples\input\transformation_test_input.csv --output samples\output\transformation_test_converted.txt --errors samples\output\transformation_test_conversion_errors.txt
flatforge convert --input-config samples\config\transformation_rules_fixed_length.yaml --output-config samples\config\transformation_rules_test.yaml --input samples\input\transformation_test_fixed_length.txt --output samples\output\transformation_test_converted.csv --errors samples\output\transformation_test_conversion_errors.csv

REM Counting tests
echo Running counting tests...
flatforge count --config samples\config\employee_fixed_length.yaml --input samples\input\employee_data.txt --output samples\output\employee_data_counts.txt
flatforge count --config samples\config\employee_csv.yaml --input samples\input\employee_data.csv --output samples\output\employee_data_counts.txt
flatforge count --config samples\config\transformation_rules_fixed_length.yaml --input samples\input\transformation_test_fixed_length.txt --output samples\output\transformation_test_fixed_length_counts.txt
flatforge count --config samples\config\transformation_rules_test.yaml --input samples\input\transformation_test_input.csv --output samples\output\transformation_test_counts.txt

REM Run the Python test script
echo Running Python test script...
python samples\test_transformations.py

echo All tests completed.
```

## Expected Results

When running these tests, you should expect the following:

1. **Validation Tests**: All records should be validated according to the rules defined in the configuration files. Any validation errors will be written to the error files.

2. **Conversion Tests**: Records should be converted from one format to another according to the mapping defined in the configuration files.

3. **Counting Tests**: The number of records in each section should be counted and written to the output files.

4. **Transformation Tests**: All transformation rules should be applied to the fields as defined in the configuration files.

## Troubleshooting

If you encounter any issues when running these tests, check the following:

1. Make sure all the required files exist in the correct locations.
2. Check that the flatforge library is installed correctly.
3. Verify that the configuration files are valid YAML or JSON.
4. Check the error files for specific validation or conversion errors.

For more detailed information about the flatforge CLI, refer to the [User Guide](README.md). 