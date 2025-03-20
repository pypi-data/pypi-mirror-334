"""
Test script for the new global rule features in FlatForge.

This script tests the following features:
1. Global rules that calculate and insert values
2. Abort after N errors
3. Uniqueness validation for fields
"""
import os
import sys
import traceback
from flatforge.parsers import ConfigParser
from flatforge.processors import ValidationProcessor
from flatforge.file_format import FileFormat, FileType

def main():
    """Test the new global rule features."""
    try:
        # Parse the configuration
        config_path = 'samples/config/employee_csv_with_global_rules.yaml'
        input_path = 'samples/input/employee_data_with_duplicates.csv'
        output_path = 'samples/output/global_rules_valid.csv'
        error_path = 'samples/output/global_rules_errors.csv'
        
        print(f"Parsing configuration: {config_path}")
        config_parser = ConfigParser.from_file(config_path)
        file_format = config_parser.parse()
        
        print(f"Creating processor")
        processor = ValidationProcessor(file_format)
        
        print(f"Processing file: {input_path}")
        result = processor.process(input_path, output_path, error_path)
        
        print(f"Total records: {result.total_records}")
        print(f"Valid records: {result.valid_records}")
        print(f"Error count: {result.error_count}")
        
        print(f"Output written to: {output_path}")
        print(f"Errors written to: {error_path}")
        
        # Print the contents of the output file
        print("\nOutput file contents:")
        with open(output_path, 'r', encoding=file_format.encoding) as f:
            print(f.read())
            
        # Print the contents of the error file
        print("\nError file contents:")
        with open(error_path, 'r', encoding=file_format.encoding) as f:
            print(f.read())
            
        # Test abort after N errors
        print("\nTesting abort after N errors:")
        file_format.abort_after_n_failed_records = 1
        result = processor.process(input_path, output_path, error_path)
        print(f"Total records processed before abort: {result.total_records}")
        print(f"Error count: {result.error_count}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
    
if __name__ == '__main__':
    main() 