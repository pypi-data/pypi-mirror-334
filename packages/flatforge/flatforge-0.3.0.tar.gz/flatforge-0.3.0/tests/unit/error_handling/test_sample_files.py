"""
Unit tests for error handling using sample files.

This module contains unit tests that use the sample error files in the workspace.
"""
import os
import unittest
from flatforge.core.models import FileFormat, FileType, Section, Record, Field, SectionType
from flatforge.processors.validation import ValidationProcessor
from flatforge.parsers import ConfigParser


class TestSampleErrorFiles(unittest.TestCase):
    """Test case for sample error files."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Base paths
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
        self.config_dir = os.path.join(self.base_dir, "samples/config")
        self.input_dir = os.path.join(self.base_dir, "samples/input/errors")
        self.output_dir = os.path.join(self.base_dir, "samples/output/errors")
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Test files
        self.date_format_input = os.path.join(self.input_dir, "date_format_errors.csv")
        self.date_format_output = os.path.join(self.output_dir, "date_format_valid.csv")
        self.date_format_error = os.path.join(self.output_dir, "date_format_errors.txt")
        
        self.required_field_input = os.path.join(self.input_dir, "required_field_errors.csv")
        self.required_field_output = os.path.join(self.output_dir, "required_field_valid.csv")
        self.required_field_error = os.path.join(self.output_dir, "required_field_errors.txt")
        
        self.numeric_value_input = os.path.join(self.input_dir, "numeric_value_errors.csv")
        self.numeric_value_output = os.path.join(self.output_dir, "numeric_value_valid.csv")
        self.numeric_value_error = os.path.join(self.output_dir, "numeric_value_errors.txt")
        
        self.string_length_input = os.path.join(self.input_dir, "string_length_errors.csv")
        self.string_length_output = os.path.join(self.output_dir, "string_length_valid.csv")
        self.string_length_error = os.path.join(self.output_dir, "string_length_errors.txt")
        
        self.mixed_errors_input = os.path.join(self.input_dir, "mixed_errors.csv")
        self.mixed_errors_output = os.path.join(self.output_dir, "mixed_valid.csv")
        self.mixed_errors_error = os.path.join(self.output_dir, "mixed_errors.txt")
        
        # Parse the configuration
        config_path = os.path.join(self.config_dir, "employee_csv.yaml")
        print(f"Config path: {config_path}")
        print(f"Config exists: {os.path.exists(config_path)}")
        config_parser = ConfigParser.from_file(config_path)
        self.file_format = config_parser.parse()
        
    def tearDown(self):
        """Clean up after tests."""
        # Remove output files
        for file in [
            self.date_format_output, self.date_format_error,
            self.required_field_output, self.required_field_error,
            self.numeric_value_output, self.numeric_value_error,
            self.string_length_output, self.string_length_error,
            self.mixed_errors_output, self.mixed_errors_error
        ]:
            if os.path.exists(file):
                os.remove(file)
                
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
        
        # Check that the error file exists and has content
        self.assertTrue(os.path.exists(self.date_format_error))
        with open(self.date_format_error, "r") as f:
            error_content = f.read()
            self.assertTrue(any(term in error_content.lower() for term in ["date", "format"]))
            
        # Check that the output file exists and has valid records
        self.assertTrue(os.path.exists(self.date_format_output))
        
    def test_required_field_errors(self):
        """Test handling of required field errors using sample file."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.required_field_input, self.required_field_output, self.required_field_error)
        
        # Check the results
        self.assertGreater(result.total_records, 0)  # Should have some records
        self.assertGreater(result.valid_records, 0)  # Should have some valid records
        self.assertGreater(result.failed_records, 0)  # Should have some failed records
        self.assertGreater(result.error_count, 0)  # Should have errors
        
        # Check that the error file exists and has content
        self.assertTrue(os.path.exists(self.required_field_error))
        with open(self.required_field_error, "r") as f:
            error_content = f.read()
            self.assertTrue(any(term in error_content.lower() for term in ["required", "missing"]))
            
        # Check that the output file exists and has valid records
        self.assertTrue(os.path.exists(self.required_field_output))
        
    def test_numeric_value_errors(self):
        """Test handling of numeric value errors using sample file."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.numeric_value_input, self.numeric_value_output, self.numeric_value_error)
        
        # Check the results
        self.assertGreater(result.total_records, 0)  # Should have some records
        self.assertGreater(result.valid_records, 0)  # Should have some valid records
        self.assertGreater(result.failed_records, 0)  # Should have some failed records
        self.assertGreater(result.error_count, 0)  # Should have errors
        
        # Check that the error file exists and has content
        self.assertTrue(os.path.exists(self.numeric_value_error))
        with open(self.numeric_value_error, "r") as f:
            error_content = f.read()
            self.assertTrue(any(term in error_content.lower() for term in ["numeric", "number"]))
            
        # Check that the output file exists and has valid records
        self.assertTrue(os.path.exists(self.numeric_value_output))
        
    def test_string_length_errors(self):
        """Test handling of string length errors using sample file."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.string_length_input, self.string_length_output, self.string_length_error)
        
        # Check the results
        self.assertGreater(result.total_records, 0)  # Should have some records
        self.assertGreater(result.valid_records, 0)  # Should have some valid records
        self.assertGreater(result.failed_records, 0)  # Should have some failed records
        self.assertGreater(result.error_count, 0)  # Should have errors
        
        # Check that the error file exists and has content
        self.assertTrue(os.path.exists(self.string_length_error))
        with open(self.string_length_error, "r") as f:
            error_content = f.read()
            self.assertTrue(any(term in error_content.lower() for term in ["length", "min", "max"]))
            
        # Check that the output file exists and has valid records
        self.assertTrue(os.path.exists(self.string_length_output))
        
    def test_mixed_errors(self):
        """Test handling of mixed error types using sample file."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.mixed_errors_input, self.mixed_errors_output, self.mixed_errors_error)
        
        # Check the results
        self.assertGreater(result.total_records, 0)  # Should have some records
        self.assertGreater(result.valid_records, 0)  # Should have some valid records
        self.assertGreater(result.failed_records, 0)  # Should have some failed records
        self.assertGreater(result.error_count, 0)  # Should have errors
        
        # Check that the error file exists and has content
        self.assertTrue(os.path.exists(self.mixed_errors_error))
        
        # Check that the output file exists and has valid records
        self.assertTrue(os.path.exists(self.mixed_errors_output))
        
        # Check for different error types in the same file
        with open(self.mixed_errors_error, "r") as f:
            error_content = f.read()
            error_types = []
            if any(term in error_content.lower() for term in ["numeric", "number"]):
                error_types.append("numeric")
            if any(term in error_content.lower() for term in ["date", "format"]):
                error_types.append("date")
            if any(term in error_content.lower() for term in ["length", "min", "max"]):
                error_types.append("string_length")
            if any(term in error_content.lower() for term in ["required", "missing"]):
                error_types.append("required")
                
            # We should have at least 2 different types of errors
            self.assertGreaterEqual(len(error_types), 2, f"Expected at least 2 error types, got {error_types}")


if __name__ == "__main__":
    unittest.main() 