import os
import unittest
from flatforge.core.models import FileFormat, FileType, Section, Record, Field, SectionType
from flatforge.processors.validation import ValidationProcessor


class TestValidationProcessor(unittest.TestCase):

    def _create_test_file_format(self):
        """Create a test file format for CSV files."""
        # Create a field for the record
        id_field = Field(name="id", position=0)
        name_field = Field(name="name", position=1)
        age_field = Field(name="age", position=2, rules=[{"type": "regex", "pattern": "^\\d+$"}])
        
        # Create a record
        record = Record(name="employee", fields=[id_field, name_field, age_field])
        
        # Create a section
        section = Section(name="body", type=SectionType.BODY, record=record)
        
        # Create a file format
        file_format = FileFormat(
            name="Employee CSV",
            type=FileType.DELIMITED,
            sections=[section],
            delimiter=",",
            quote_char='"',
            escape_char=None,
            newline="\n",
            encoding="utf-8",
            skip_blank_lines=True,
            exit_on_first_error=False,
            abort_after_n_failed_records=-1
        )
        
        return file_format

    def test_abort_after_n_failed_records(self):
        """Test that the processor aborts after N failed records."""
        # Create a file format with abort_after_n_failed_records=2
        file_format = self._create_test_file_format()
        file_format.abort_after_n_failed_records = 2
        
        # Create a processor
        processor = ValidationProcessor(file_format=file_format)
        
        # Create a test file with 5 records, 3 of which are invalid
        with open("test_input.csv", "w") as f:
            f.write("1,John,30\n")    # Valid
            f.write("2,Jane,invalid\n")  # Invalid - age is not a number
            f.write("3,Bob,invalid\n")   # Invalid - age is not a number
            f.write("4,Alice,40\n")   # Valid but should not be processed
            f.write("5,Mike,invalid\n")  # Invalid but should not be processed
        
        # Process the file
        result = processor.process("test_input.csv", "test_output.csv", "test_error.csv")
        
        # Check that processing stopped after 2 failed records
        self.assertEqual(result.total_records, 2)
        self.assertEqual(result.valid_records, 0)
        self.assertEqual(result.failed_records, 2)
        
        # Clean up
        os.remove("test_input.csv")
        os.remove("test_output.csv")
        os.remove("test_error.csv") 