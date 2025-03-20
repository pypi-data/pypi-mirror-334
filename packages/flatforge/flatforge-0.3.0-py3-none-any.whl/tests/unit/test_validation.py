"""
Unit tests for the validation processor.
"""
import os
import tempfile
import unittest

from flatforge.core import FileFormat, FileType, SectionType
from flatforge.parsers import ConfigParser
from flatforge.processors import ValidationProcessor


class TestValidation(unittest.TestCase):
    """Test case for the validation processor."""
    
    def setUp(self):
        """Set up the test case."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create a sample configuration
        self.config_path = os.path.join(self.temp_dir.name, 'config.yaml')
        with open(self.config_path, 'w') as f:
            f.write("""
name: Test Format
type: delimited
description: A test format
delimiter: ","
newline: "\n"
encoding: utf-8
skip_blank_lines: true
exit_on_first_error: false

sections:
  - name: body
    type: body
    min_records: 1
    record:
      name: test_record
      fields:
        - name: field1
          position: 0
          rules:
            - type: required
        - name: field2
          position: 1
          rules:
            - type: numeric
              params:
                min_value: 0
            """)
            
        # Create a sample input file
        self.input_path = os.path.join(self.temp_dir.name, 'input.csv')
        with open(self.input_path, 'w') as f:
            f.write("value1,10\n")
            f.write("value2,20\n")
            
        # Create output and error file paths
        self.output_path = os.path.join(self.temp_dir.name, 'output.csv')
        self.error_path = os.path.join(self.temp_dir.name, 'error.csv')
    
    def tearDown(self):
        """Clean up after the test case."""
        self.temp_dir.cleanup()
    
    def test_validation(self):
        """Test the validation processor."""
        # Parse the configuration
        config_parser = ConfigParser.from_file(self.config_path)
        file_format = config_parser.parse()
        
        # Create a processor
        processor = ValidationProcessor(file_format)
        
        # Process the file
        result = processor.process(self.input_path, self.output_path, self.error_path)
        
        # Check the result
        self.assertEqual(result.total_records, 2)
        self.assertEqual(result.valid_records, 2)
        self.assertEqual(result.error_count, 0)
        
        # Check the output file
        with open(self.output_path, 'r') as f:
            content = f.read()
            self.assertIn("value1,10", content)
            self.assertIn("value2,20", content)
    
    def test_chunked_validation(self):
        """Test the chunked validation processor."""
        # Parse the configuration
        config_parser = ConfigParser.from_file(self.config_path)
        file_format = config_parser.parse()
        
        # Create a processor
        processor = ValidationProcessor(file_format)
        
        # Process the file in chunks
        chunked_output_path = os.path.join(self.temp_dir.name, 'chunked_output.csv')
        chunked_error_path = os.path.join(self.temp_dir.name, 'chunked_errors.csv')
        
        # Define a progress callback
        progress_updates = []
        def update_progress(processed, total):
            progress_updates.append((processed, total))
        
        result = processor.process_chunked(
            self.input_path, 
            chunked_output_path, 
            chunked_error_path, 
            chunk_size=1,  # Process one record at a time
            progress_callback=update_progress
        )
        
        # Check the result
        self.assertEqual(result.total_records, 2)
        self.assertEqual(result.valid_records, 2)
        self.assertEqual(result.error_count, 0)
        
        # Check the output file
        with open(chunked_output_path, 'r') as f:
            content = f.read()
            self.assertIn("value1,10", content)
            self.assertIn("value2,20", content)
        
        # Check that progress was reported
        self.assertGreater(len(progress_updates), 0)
        self.assertEqual(progress_updates[-1][0], 2)  # Final processed count
    
    def test_validation_with_errors(self):
        """Test the validation processor with errors."""
        # Create a sample input file with errors
        error_input_path = os.path.join(self.temp_dir.name, 'error_input.csv')
        with open(error_input_path, 'w') as f:
            f.write("value1,10\n")
            f.write(",20\n")  # Missing required field
            f.write("value3,-30\n")  # Negative number
            
        # Parse the configuration
        config_parser = ConfigParser.from_file(self.config_path)
        file_format = config_parser.parse()
        
        # Create a processor
        processor = ValidationProcessor(file_format)
        
        # Process the file
        result = processor.process(error_input_path, self.output_path, self.error_path)
        
        # Check the result
        self.assertEqual(result.total_records, 3)
        self.assertEqual(result.valid_records, 1)
        self.assertEqual(result.error_count, 2)
        
        # Check the output file
        with open(self.output_path, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0].strip(), "value1,10")
            
        # Check the error file
        self.assertTrue(os.path.exists(self.error_path))
        with open(self.error_path, 'r') as f:
            content = f.read()
            self.assertIn("Field is required", content)
            self.assertIn("Value is less than minimum value", content)


if __name__ == '__main__':
    unittest.main() 