"""
Unit tests for required field error handling.

This module contains unit tests for handling required field errors in FlatForge.
"""
import os
import unittest
from flatforge.core.models import FileFormat, FileType, Section, Record, Field, SectionType
from flatforge.processors.validation import ValidationProcessor


class TestRequiredFieldErrors(unittest.TestCase):
    """Test case for required field errors."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a test file format
        self._create_test_file_format()
        
        # Create a test file with required field errors
        self.test_input_file = "test_required_field_errors.csv"
        with open(self.test_input_file, "w") as f:
            f.write("H,BATCH001,20230101120000\n")
            f.write("D,1001,,19800101,US,75000.00,1000,Jane Doe\n")  # Missing employee_name
            f.write("D,,Alice Johnson,19850215,CA,80000.00,1000,Jane Doe\n")  # Missing employee_id
            f.write("D,1003,Bob Williams,,UK,65000.00,1001,John Smith\n")  # Missing date_of_birth (not required)
            f.write("D,1004,Carol Brown,19950425,,60000.00,1001,John Smith\n")  # Missing country_code (not required)
            f.write("D,1005,David Miller,19881130,DE,,1002,Alice Johnson\n")  # Missing salary (not required)
            f.write("F,,5\n")  # Missing total_salary
        
        # Output files
        self.test_output_file = "test_required_field_valid.csv"
        self.test_error_file = "test_required_field_errors.txt"
        
    def tearDown(self):
        """Clean up after tests."""
        # Remove test files
        for file in [self.test_input_file, self.test_output_file, self.test_error_file]:
            if os.path.exists(file):
                os.remove(file)
                
    def _create_test_file_format(self):
        """Create a test file format for CSV files with required field validation."""
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
        
    def test_required_field_errors(self):
        """Test handling of required field errors."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.test_input_file, self.test_output_file, self.test_error_file)
        
        # Check the results
        self.assertEqual(result.total_records, 7)  # Header + 5 body records + footer
        self.assertEqual(result.valid_records, 4)  # Header + 3 body records (with non-required fields missing)
        self.assertEqual(result.failed_records, 3)  # 2 invalid body records + footer
        self.assertGreater(result.error_count, 0)  # Should have errors
        
        # Check that the error file exists and has content
        self.assertTrue(os.path.exists(self.test_error_file))
        with open(self.test_error_file, "r") as f:
            error_content = f.read()
            self.assertTrue(any(term in error_content.lower() for term in ["required", "missing"]))
            self.assertIn("employee_name", error_content)  # Should mention the missing field
            self.assertIn("employee_id", error_content)  # Should mention the missing field
            
        # Check that the output file exists and has valid records
        self.assertTrue(os.path.exists(self.test_output_file))
        with open(self.test_output_file, "r") as f:
            output_content = f.read()
            self.assertIn("H,BATCH001,20230101120000", output_content)  # Header should be valid
            
            # Records with non-required fields missing should be in the output
            self.assertIn("D,1003,Bob Williams", output_content)  # Missing date_of_birth (not required)
            self.assertIn("D,1004,Carol Brown", output_content)  # Missing country_code (not required)
            self.assertIn("D,1005,David Miller", output_content)  # Missing salary (not required)
            
            # Records with required fields missing should not be in the output
            self.assertNotIn("D,1001,,19800101", output_content)  # Missing employee_name
            self.assertNotIn("D,,Alice Johnson", output_content)  # Missing employee_id
            
    def test_error_details(self):
        """Test that error details are correctly captured."""
        # Create a processor
        processor = ValidationProcessor(self.file_format)
        
        # Process the file
        result = processor.process(self.test_input_file, self.test_output_file, self.test_error_file)
        
        # Check that errors have detailed information
        required_errors = [e for e in result.errors if "required" in str(e).lower()]
        self.assertGreater(len(required_errors), 0)  # Should have required field errors
        
        for error in required_errors:
            error_str = str(error)
            self.assertIn("required", error_str.lower())  # Should mention it's a required field error
            
            # Check if the error message contains the field name and record number
            self.assertTrue(
                any(field in error_str for field in ["employee_name", "employee_id", "total_salary"]) or
                "record" in error_str.lower()
            )


if __name__ == "__main__":
    unittest.main() 