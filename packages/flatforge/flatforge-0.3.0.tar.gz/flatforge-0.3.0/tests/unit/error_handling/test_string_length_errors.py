"""
Unit tests for string length error handling.

This module contains unit tests for handling string length errors in FlatForge.
"""
import os
import unittest
from flatforge.core.models import FileFormat, FileType, Section, Record, Field, SectionType
from flatforge.processors.validation import ValidationProcessor


class TestStringLengthErrors(unittest.TestCase):
    """Test case for string length errors."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a test file format
        self._create_test_file_format()
        
        # Create a test file with string length errors
        self.test_input_file = "test_string_length_errors.csv"
        with open(self.test_input_file, "w") as f:
            f.write("H,BATCH001,20230101120000\n")
            f.write("D,1001,John Smith,19800101,USA,75000.00,1000,Jane Doe\n")  # Country code too long (3 chars)
            f.write("D,1002,Alice Johnson,19850215,C,80000.00,1000,Jane Doe\n")  # Country code too short (1 char)
            f.write("D,1003,Bob Williams,19900320,UK,65000.00,1001,J\n")  # Manager name too short
            f.write("D,1004,Carol Brown,19950425,AU,60000.00,1001,This manager name is way too long and exceeds the maximum length allowed for this field\n")  # Manager name too long
            f.write("D,1005,D,19881130,DE,70000.00,1002,Alice Johnson\n")  # Employee name too short
            f.write("F,350000.00,5\n")
        
        # Output files
        self.test_output_file = "test_string_length_valid.csv"
        self.test_error_file = "test_string_length_errors.txt"
        
    def tearDown(self):
        """Clean up after tests."""
        # Remove test files
        for file in [self.test_input_file, self.test_output_file, self.test_error_file]:
            if os.path.exists(file):
                os.remove(file)
                
    def _create_test_file_format(self):
        """Create a test file format for CSV files with string length validation."""
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
        
    def test_string_length_errors(self):
        """Test handling of string length errors."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.test_input_file, self.test_output_file, self.test_error_file)
        
        # Check the results
        self.assertEqual(result.total_records, 7)  # Header + 5 body records + footer
        self.assertEqual(result.valid_records, 2)  # Header and footer should be valid
        self.assertEqual(result.failed_records, 5)  # All body records have string length errors
        self.assertGreater(result.error_count, 0)  # Should have errors
        
        # Check that the error file exists and has content
        self.assertTrue(os.path.exists(self.test_error_file))
        with open(self.test_error_file, "r") as f:
            error_content = f.read()
            # Check for string length error indicators
            self.assertTrue(any(term in error_content.lower() for term in [
                "string_length", "length", "min", "max"
            ]))
            self.assertIn("USA", error_content)  # Should mention the invalid value
            self.assertIn("C", error_content)  # Should mention the invalid value
            self.assertIn("J", error_content)  # Should mention the invalid value
            
        # Check that the output file exists and has valid records
        self.assertTrue(os.path.exists(self.test_output_file))
        with open(self.test_output_file, "r") as f:
            output_content = f.read()
            self.assertIn("H,BATCH001,20230101120000", output_content)  # Header should be valid
            self.assertIn("F,350000.00,5", output_content)  # Footer should be valid
            
            # Invalid records should not be in the output
            self.assertNotIn("USA", output_content)
            self.assertNotIn(",C,", output_content)
            self.assertNotIn(",J\n", output_content)
            
    def test_error_details(self):
        """Test that error details are correctly captured."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.test_input_file, self.test_output_file, self.test_error_file)
        
        # Check that errors have detailed information
        string_length_errors = []
        for error in result.errors:
            error_str = str(error).lower()
            if any(term in error_str for term in ["string_length", "length", "min", "max"]):
                string_length_errors.append(error)
                
        self.assertGreater(len(string_length_errors), 0)  # Should have string length errors
        
        for error in string_length_errors:
            error_str = str(error).lower()
            # Check if the error message contains length-related terms
            self.assertTrue(any(term in error_str for term in ["length", "min", "max"]))
            
            # Check if the error message contains the field name and record number
            self.assertTrue(
                any(field in error_str for field in ["employee_name", "country_code", "manager_name"]) or
                "record" in error_str
            )


if __name__ == "__main__":
    unittest.main() 