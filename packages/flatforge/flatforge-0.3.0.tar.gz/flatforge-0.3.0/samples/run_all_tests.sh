#!/bin/bash
# FlatForge Test Script for Unix-based systems
# This script runs all the sample tests for FlatForge

# Create output directory if it doesn't exist
mkdir -p samples/output

# Validation tests
echo "Running validation tests..."

# Employee data tests
echo "Testing employee data with record type identifiers (fixed-length)..."
flatforge validate --config samples/config/employee_fixed_length.yaml --input samples/input/employee_data.txt --output samples/output/employee_data_valid.txt --errors samples/output/employee_data_errors.txt

echo "Testing employee data without record type identifiers (fixed-length)..."
flatforge validate --config samples/config/employee_fixed_length_no_identifier.yaml --input samples/input/employee_data_no_identifier.txt --output samples/output/employee_data_no_identifier_valid.txt --errors samples/output/employee_data_no_identifier_errors.txt

echo "Testing employee data with record type identifiers (CSV)..."
flatforge validate --config samples/config/employee_csv.yaml --input samples/input/employee_data.csv --output samples/output/employee_data_valid.csv --errors samples/output/employee_data_errors.csv

echo "Testing employee data without record type identifiers (CSV)..."
flatforge validate --config samples/config/employee_csv_no_identifier.yaml --input samples/input/employee_data_no_identifier.csv --output samples/output/employee_data_no_identifier_valid.csv --errors samples/output/employee_data_no_identifier_errors.csv

# Transformation tests
echo "Testing transformation rules (fixed-length)..."
flatforge validate --config samples/config/transformation_rules_fixed_length.yaml --input samples/input/transformation_test_fixed_length.txt --output samples/output/transformation_test_fixed_length_valid.txt --errors samples/output/transformation_test_fixed_length_errors.txt

echo "Testing transformation rules (CSV)..."
flatforge validate --config samples/config/transformation_rules_test.yaml --input samples/input/transformation_test_input.csv --output samples/output/transformation_test_valid.csv --errors samples/output/transformation_test_errors.csv

# Conversion tests
echo "Running conversion tests..."

echo "Converting CSV to fixed-length (employee data)..."
flatforge convert --input-config samples/config/employee_csv.yaml --output-config samples/config/employee_fixed_length.yaml --input samples/input/employee_data.csv --output samples/output/employee_data_converted.txt --errors samples/output/employee_data_conversion_errors.txt

echo "Converting fixed-length to CSV (employee data)..."
flatforge convert --input-config samples/config/employee_fixed_length.yaml --output-config samples/config/employee_csv.yaml --input samples/input/employee_data.txt --output samples/output/employee_data_converted.csv --errors samples/output/employee_data_conversion_errors.csv

echo "Converting CSV to fixed-length (transformation test)..."
flatforge convert --input-config samples/config/transformation_rules_test.yaml --output-config samples/config/transformation_rules_fixed_length.yaml --input samples/input/transformation_test_input.csv --output samples/output/transformation_test_converted.txt --errors samples/output/transformation_test_conversion_errors.txt

echo "Converting fixed-length to CSV (transformation test)..."
flatforge convert --input-config samples/config/transformation_rules_fixed_length.yaml --output-config samples/config/transformation_rules_test.yaml --input samples/input/transformation_test_fixed_length.txt --output samples/output/transformation_test_converted.csv --errors samples/output/transformation_test_conversion_errors.txt

echo "Converting with mapping configuration..."
flatforge convert --input-config samples/config/transformation_rules_test.yaml --output-config samples/config/transformation_rules_fixed_length.yaml --mapping-config samples/config/conversion_test.yaml --input samples/input/transformation_test_input.csv --output samples/output/transformation_test_mapped.txt --errors samples/output/transformation_test_mapping_errors.txt

# Counting tests
echo "Running counting tests..."

echo "Counting employee records (fixed-length)..."
flatforge count --config samples/config/employee_fixed_length.yaml --input samples/input/employee_data.txt --output samples/output/employee_data_counts.txt

echo "Counting employee records (CSV)..."
flatforge count --config samples/config/employee_csv.yaml --input samples/input/employee_data.csv --output samples/output/employee_data_counts.txt

echo "Counting transformation test records (fixed-length)..."
flatforge count --config samples/config/transformation_rules_fixed_length.yaml --input samples/input/transformation_test_fixed_length.txt --output samples/output/transformation_test_fixed_length_counts.txt

echo "Counting transformation test records (CSV)..."
flatforge count --config samples/config/transformation_rules_test.yaml --input samples/input/transformation_test_input.csv --output samples/output/transformation_test_counts.txt

# Run the Python test script
echo "Running Python test script..."
python samples/test_transformations.py

echo "All tests completed." 