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
        {
            "config": os.path.join(config_dir, "employee_csv.yaml"),
            "input": os.path.join(input_dir, "required_field_errors.csv"),
            "output": os.path.join(output_dir, "required_field_valid.csv"),
            "error": os.path.join(output_dir, "required_field_errors.txt"),
            "description": "Required Field Errors"
        },
        {
            "config": os.path.join(config_dir, "employee_csv.yaml"),
            "input": os.path.join(input_dir, "numeric_value_errors.csv"),
            "output": os.path.join(output_dir, "numeric_value_valid.csv"),
            "error": os.path.join(output_dir, "numeric_value_errors.txt"),
            "description": "Numeric Value Errors"
        },
        {
            "config": os.path.join(config_dir, "employee_csv.yaml"),
            "input": os.path.join(input_dir, "string_length_errors.csv"),
            "output": os.path.join(output_dir, "string_length_valid.csv"),
            "error": os.path.join(output_dir, "string_length_errors.txt"),
            "description": "String Length Errors"
        },
        {
            "config": os.path.join(config_dir, "employee_csv.yaml"),
            "input": os.path.join(input_dir, "mixed_errors.csv"),
            "output": os.path.join(output_dir, "mixed_valid.csv"),
            "error": os.path.join(output_dir, "mixed_errors.txt"),
            "description": "Mixed Errors"
        },
        {
            "config": os.path.join(config_dir, "employee_fixed_length.yaml"),
            "input": os.path.join(input_dir, "fixed_length_errors.txt"),
            "output": os.path.join(output_dir, "fixed_length_valid.txt"),
            "error": os.path.join(output_dir, "fixed_length_errors.log"),
            "description": "Fixed-Length Format Errors"
        }
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