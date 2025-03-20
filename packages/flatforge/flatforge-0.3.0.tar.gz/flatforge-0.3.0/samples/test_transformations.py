#!/usr/bin/env python
"""
Test script for FlatForge transformation rules.

This script tests all the transformation rules in FlatForge using the sample files.
"""
import os
import sys
import time

# Add the parent directory to the path so we can import flatforge
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flatforge.parsers import ConfigParser
from flatforge.processors import ValidationProcessor, ConversionProcessor

def test_delimited_transformations():
    """Test transformations on delimited files."""
    print("Testing delimited transformations...")
    
    # Parse the configuration
    config_path = os.path.join("samples", "config", "transformation_rules_test.yaml")
    config_parser = ConfigParser.from_file(config_path)
    file_format = config_parser.parse()
    
    # Create a processor
    processor = ValidationProcessor(file_format)
    
    # Process the file
    input_file = os.path.join("samples", "input", "transformation_test_input.csv")
    output_file = os.path.join("samples", "output", "transformation_test_output.csv")
    error_file = os.path.join("samples", "output", "transformation_test_errors.csv")
    
    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    result = processor.process(input_file, output_file, error_file)
    
    print(f"Processed {result.total_records} records with {result.error_count} errors.")
    print(f"Valid records: {result.valid_records}")
    print(f"Output written to: {output_file}")
    if result.error_count > 0:
        print(f"Errors written to: {error_file}")
    print()

def test_fixed_length_transformations():
    """Test transformations on fixed-length files."""
    print("Testing fixed-length transformations...")
    
    # Parse the configuration
    config_path = os.path.join("samples", "config", "transformation_rules_fixed_length.yaml")
    config_parser = ConfigParser.from_file(config_path)
    file_format = config_parser.parse()
    
    # Create a processor
    processor = ValidationProcessor(file_format)
    
    # Process the file
    input_file = os.path.join("samples", "input", "transformation_test_fixed_length.txt")
    output_file = os.path.join("samples", "output", "transformation_test_fixed_length_output.txt")
    error_file = os.path.join("samples", "output", "transformation_test_fixed_length_errors.txt")
    
    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    result = processor.process(input_file, output_file, error_file)
    
    print(f"Processed {result.total_records} records with {result.error_count} errors.")
    print(f"Valid records: {result.valid_records}")
    print(f"Output written to: {output_file}")
    if result.error_count > 0:
        print(f"Errors written to: {error_file}")
    print()

def test_format_conversion():
    """Test format conversion between delimited and fixed-length formats."""
    print("Testing format conversion...")
    
    # Parse the configurations
    delimited_config_path = os.path.join("samples", "config", "transformation_rules_test.yaml")
    fixed_length_config_path = os.path.join("samples", "config", "transformation_rules_fixed_length.yaml")
    
    delimited_config_parser = ConfigParser.from_file(delimited_config_path)
    delimited_format = delimited_config_parser.parse()
    
    fixed_length_config_parser = ConfigParser.from_file(fixed_length_config_path)
    fixed_length_format = fixed_length_config_parser.parse()
    
    # Test delimited to fixed-length conversion
    print("Testing delimited to fixed-length conversion...")
    
    # Create a processor
    processor = ConversionProcessor(delimited_format, fixed_length_format)
    
    # Process the file
    input_file = os.path.join("samples", "input", "transformation_test_input.csv")
    output_file = os.path.join("samples", "output", "delimited_to_fixed_length.txt")
    error_file = os.path.join("samples", "output", "delimited_to_fixed_length_errors.txt")
    
    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    result = processor.process(input_file, output_file, error_file)
    
    print(f"Processed {result.total_records} records with {result.error_count} errors.")
    print(f"Valid records: {result.valid_records}")
    print(f"Output written to: {output_file}")
    if result.error_count > 0:
        print(f"Errors written to: {error_file}")
    print()
    
    # Test fixed-length to delimited conversion
    print("Testing fixed-length to delimited conversion...")
    
    # Create a processor
    processor = ConversionProcessor(fixed_length_format, delimited_format)
    
    # Process the file
    input_file = os.path.join("samples", "input", "transformation_test_fixed_length.txt")
    output_file = os.path.join("samples", "output", "fixed_length_to_delimited.csv")
    error_file = os.path.join("samples", "output", "fixed_length_to_delimited_errors.csv")
    
    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    result = processor.process(input_file, output_file, error_file)
    
    print(f"Processed {result.total_records} records with {result.error_count} errors.")
    print(f"Valid records: {result.valid_records}")
    print(f"Output written to: {output_file}")
    if result.error_count > 0:
        print(f"Errors written to: {error_file}")
    print()

def main():
    """Run all transformation tests."""
    print("Running FlatForge transformation tests...\n")
    
    test_delimited_transformations()
    test_fixed_length_transformations()
    test_format_conversion()
    
    print("All tests completed.")

if __name__ == "__main__":
    main() 