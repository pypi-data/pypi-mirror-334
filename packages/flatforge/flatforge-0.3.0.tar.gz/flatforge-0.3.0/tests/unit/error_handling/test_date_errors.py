"""
Unit tests for date format error handling.

This module contains unit tests for handling date format errors in FlatForge.
"""
import os
import unittest
from flatforge.core.models import FileFormat, FileType, Section, Record, Field, SectionType
from flatforge.processors.validation import ValidationProcessor


class TestDateFormatErrors(unittest.TestCase):
    """Test case for date format errors."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a test file format
        self._create_test_file_format()
        
        # Create a test file with date format errors
        self.test_input_file = "test_date_errors.csv"
        with open(self.test_input_file, "w") as f:
            f.write("H,BATCH001,20230101120000\n")
            f.write("D,1001,John Smith,30-Feb-2023,US,75000.00,1000,Jane Doe\n")  # Invalid date (Feb 30)
            f.write("D,1002,Alice Johnson,2023/02/15,CA,80000.00,1000,Jane Doe\n")  # Wrong format
            f.write("D,1003,Bob Williams,19900320,UK,65000.00,1001,John Smith\n")  # Valid date
            f.write("D,1004,Carol Brown,04-25-1995,AU,60000.00,1001,John Smith\n")  # Wrong format
            f.write("D,1005,David Miller,31-11-1988,DE,70000.00,1002,Alice Johnson\n")  # Invalid date (Nov 31)
            f.write("D,1006,Eve Wilson,20231301,FR,72000.00,1002,Alice Johnson\n")  # Invalid date (month 13)
            f.write("F,422000.00,6\n")
        
        # Output files
        self.test_output_file = "test_date_valid.csv"
        self.test_error_file = "test_date_errors.txt"
        
    def tearDown(self):
        """Clean up after tests."""
        # Remove test files
        for file in [self.test_input_file, self.test_output_file, self.test_error_file]:
            if os.path.exists(file):
                os.remove(file)
                
    def _create_test_file_format(self):
        """Create a test file format for CSV files with date validation."""
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
            Field(name="employee_id", position=1, rules=[{"type": "required"}, {"type": "numeric"}]),
            Field(name="employee_name", position=2, rules=[{"type": "required"}]),
            Field(name="date_of_birth", position=3, rules=[
                {"type": "date", "params": {"format": "%Y%m%d"}}
            ]),
            Field(name="country_code", position=4, rules=[
                {"type": "string_length", "params": {"min_length": 2, "max_length": 2}}
            ]),
            Field(name="salary", position=5, rules=[{"type": "numeric"}]),
            Field(name="manager_id", position=6, rules=[{"type": "numeric"}]),
            Field(name="manager_name", position=7)
        ]
        
        # Create fields for the footer record
        footer_fields = [
            Field(name="record_type", position=0, rules=[{"type": "choice", "params": {"choices": ["F"]}}]),
            Field(name="total_salary", position=1, rules=[{"type": "required"}, {"type": "numeric"}]),
            Field(name="employee_count", position=2, rules=[{"type": "required"}, {"type": "numeric"}])
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
        
    def test_date_format_errors(self):
        """Test handling of date format errors."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.test_input_file, self.test_output_file, self.test_error_file)
        
        # Check the results
        self.assertEqual(result.total_records, 8)  # Header + 6 body records + footer
        self.assertEqual(result.valid_records, 3)  # Header, one valid body record, and footer
        self.assertEqual(result.failed_records, 5)  # 5 invalid body records
        self.assertGreater(result.error_count, 0)  # Should have errors
        
        # Check that the error file exists and has content
        self.assertTrue(os.path.exists(self.test_error_file))
        with open(self.test_error_file, "r") as f:
            error_content = f.read()
            self.assertIn("date_of_birth", error_content)  # Should mention the field name
            self.assertIn("30-Feb-2023", error_content)  # Should mention the invalid value
            
        # Check that the output file exists and has valid records
        self.assertTrue(os.path.exists(self.test_output_file))
        with open(self.test_output_file, "r") as f:
            output_content = f.read()
            self.assertIn("H,BATCH001,20230101120000", output_content)  # Header should be valid
            self.assertIn("D,1003,Bob Williams,19900320,UK,65000.00,1001,John Smith", output_content)  # Valid record
            self.assertIn("F,422000.00,6", output_content)  # Footer should be valid
            
            # Invalid records should not be in the output
            self.assertNotIn("30-Feb-2023", output_content)
            self.assertNotIn("2023/02/15", output_content)
            
    def test_error_details(self):
        """Test that error details are correctly captured."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.test_input_file, self.test_output_file, self.test_error_file)
        
        # Check that errors have detailed information
        for error in result.errors:
            error_str = str(error)
            self.assertIn("date", error_str.lower())  # Should mention it's a date error
            
            # Check if the error message contains the field name and record number
            self.assertTrue(
                "date_of_birth" in error_str or 
                "record" in error_str.lower()
            )


if __name__ == "__main__":
    unittest.main() 