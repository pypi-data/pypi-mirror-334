"""
Unit tests for mixed error handling.

This module contains unit tests for handling multiple types of errors in a single file in FlatForge.
"""
import os
import unittest
from flatforge.core.models import FileFormat, FileType, Section, Record, Field, SectionType
from flatforge.processors.validation import ValidationProcessor


class TestMixedErrors(unittest.TestCase):
    """Test case for mixed error types."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a test file format
        self._create_test_file_format()
        
        # Create a test file with mixed errors
        self.test_input_file = "test_mixed_errors.csv"
        with open(self.test_input_file, "w") as f:
            f.write("H,BATCH001,20230101120000\n")
            f.write("D,ABC1,John Smith,19800101,US,75000.00,1000,Jane Doe\n")  # Non-numeric employee_id
            f.write("D,1002,Alice Johnson,19851315,CA,80000.00,1000,Jane Doe\n")  # Invalid date (month 13)
            f.write("D,1003,Bob Williams,19900320,U,65000.00,1001,J\n")  # Country code too short, manager name too short
            f.write("D,1004,,19950425,AU,60000.00,1001,John Smith\n")  # Missing required employee_name
            f.write("D,1005,David Miller,19881130,DE,70000.00,MANAGER,Alice Johnson\n")  # Non-numeric manager_id
            f.write("F,350000.00,FIVE\n")  # Non-numeric employee_count
        
        # Output files
        self.test_output_file = "test_mixed_valid.csv"
        self.test_error_file = "test_mixed_errors.txt"
        
    def tearDown(self):
        """Clean up after tests."""
        # Remove test files
        for file in [self.test_input_file, self.test_output_file, self.test_error_file]:
            if os.path.exists(file):
                os.remove(file)
                
    def _create_test_file_format(self):
        """Create a test file format for CSV files with multiple validation rules."""
        # Create fields for the header record
        header_fields = [
            Field(name="record_type", position=0, rules=[{"type": "choice", "params": {"choices": ["H"]}}]),
            Field(name="batch_reference", position=1, rules=[{"type": "required"}]),
            Field(name="batch_timestamp", position=2, rules=[
                {"type": "required"},
                {"type": "date", "params": {"format": "%Y%m%d%H%M%S"}}
            ])
        ]
        
        # Create fields for the body record
        body_fields = [
            Field(name="record_type", position=0, rules=[{"type": "choice", "params": {"choices": ["D"]}}]),
            Field(name="employee_id", position=1, rules=[
                {"type": "required"}, 
                {"type": "numeric"}
            ]),
            Field(name="employee_name", position=2, rules=[
                {"type": "required"},
                {"type": "string_length", "params": {"min_length": 2, "max_length": 50}}
            ]),
            Field(name="date_of_birth", position=3, rules=[
                {"type": "date", "params": {"format": "%Y%m%d"}}
            ]),
            Field(name="country_code", position=4, rules=[
                {"type": "string_length", "params": {"min_length": 2, "max_length": 2}}
            ]),
            Field(name="salary", position=5, rules=[
                {"type": "numeric", "params": {"min_value": 0, "decimal_precision": 2}}
            ]),
            Field(name="manager_id", position=6, rules=[{"type": "numeric"}]),
            Field(name="manager_name", position=7, rules=[
                {"type": "string_length", "params": {"min_length": 2, "max_length": 50}}
            ])
        ]
        
        # Create fields for the footer record
        footer_fields = [
            Field(name="record_type", position=0, rules=[{"type": "choice", "params": {"choices": ["F"]}}]),
            Field(name="total_salary", position=1, rules=[
                {"type": "required"}, 
                {"type": "numeric", "params": {"min_value": 0, "decimal_precision": 2}}
            ]),
            Field(name="employee_count", position=2, rules=[
                {"type": "required"}, 
                {"type": "numeric", "params": {"min_value": 0}}
            ])
        ]
        
        # Create records
        header_record = Record(name="header_record", fields=header_fields)
        body_record = Record(name="body_record", fields=body_fields)
        footer_record = Record(name="footer_record", fields=footer_fields)
        
        # Create sections
        header_section = Section(
            name="header",
            type=SectionType.HEADER,
            record=header_record,
            min_records=1,
            max_records=1
        )
        
        body_section = Section(
            name="body",
            type=SectionType.BODY,
            record=body_record
        )
        
        footer_section = Section(
            name="footer",
            type=SectionType.FOOTER,
            record=footer_record,
            min_records=1,
            max_records=1
        )
        
        # Create file format
        self.file_format = FileFormat(
            name="Test CSV Format",
            type=FileType.DELIMITED,
            sections=[header_section, body_section, footer_section],
            delimiter=",",
            quote_char='"',
            escape_char=None,
            newline="\n",
            encoding="utf-8",
            skip_blank_lines=True,
            exit_on_first_error=False,
            abort_after_n_failed_records=-1
        )
        
    def test_mixed_errors(self):
        """Test handling of mixed error types."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.test_input_file, self.test_output_file, self.test_error_file)
        
        # Check the results
        self.assertEqual(result.total_records, 7)  # Header + 5 body records + footer
        self.assertEqual(result.valid_records, 1)  # Only the header should be valid
        self.assertEqual(result.failed_records, 6)  # All body records and footer have errors
        self.assertGreater(result.error_count, 0)  # Should have errors
        
        # Check that the error file exists and has content
        self.assertTrue(os.path.exists(self.test_error_file))
        with open(self.test_error_file, "r") as f:
            error_content = f.read()
            
            # Check for different error types
            self.assertTrue(any(error_type in error_content.lower() for error_type in [
                "numeric", "date", "string length", "required"
            ]))
            
            # Check for specific error values
            self.assertIn("ABC1", error_content)  # Non-numeric employee_id
            self.assertIn("19851315", error_content)  # Invalid date
            self.assertIn("U", error_content)  # Country code too short
            self.assertIn("J", error_content)  # Manager name too short
            self.assertIn("MANAGER", error_content)  # Non-numeric manager_id
            self.assertIn("FIVE", error_content)  # Non-numeric employee_count
            
        # Check that the output file exists and has valid records
        self.assertTrue(os.path.exists(self.test_output_file))
        with open(self.test_output_file, "r") as f:
            output_content = f.read()
            self.assertIn("H,BATCH001,20230101120000", output_content)  # Header should be valid
            
            # Invalid records should not be in the output
            self.assertNotIn("ABC1", output_content)
            self.assertNotIn("19851315", output_content)
            self.assertNotIn(",U,", output_content)
            self.assertNotIn("MANAGER", output_content)
            self.assertNotIn("FIVE", output_content)
            
    def test_error_counts_by_type(self):
        """Test that error counts by type are correctly tracked."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.test_input_file, self.test_output_file, self.test_error_file)
        
        # Check that we have different types of errors
        error_types = set()
        for error in result.errors:
            error_str = str(error).lower()
            if "numeric" in error_str:
                error_types.add("numeric")
            elif "date" in error_str:
                error_types.add("date")
            elif "string length" in error_str:
                error_types.add("string_length")
            elif "required" in error_str:
                error_types.add("required")
                
        # We should have at least 3 different types of errors
        self.assertGreaterEqual(len(error_types), 3)
        
    def test_multiple_errors_per_record(self):
        """Test that multiple errors per record are correctly captured."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.test_input_file, self.test_output_file, self.test_error_file)
        
        # Check that we have errors
        self.assertGreater(len(result.errors), 0, "No errors were captured")
        
        # Check that the error file exists and has content
        self.assertTrue(os.path.exists(self.test_error_file))
        with open(self.test_error_file, "r") as f:
            error_content = f.read()
            
            # Check for different error types in the same file
            error_types = []
            if any(term in error_content.lower() for term in ["numeric", "number"]):
                error_types.append("numeric")
            if any(term in error_content.lower() for term in ["date", "format"]):
                error_types.append("date")
            if any(term in error_content.lower() for term in ["string_length", "length", "min", "max"]):
                error_types.append("string_length")
            if any(term in error_content.lower() for term in ["required", "missing"]):
                error_types.append("required")
                
            # We should have at least 2 different types of errors
            self.assertGreaterEqual(len(error_types), 2, f"Expected at least 2 error types, got {error_types}")


if __name__ == "__main__":
    unittest.main() 