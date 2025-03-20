"""
Unit tests for global rules.

This module contains unit tests for the global rules in FlatForge.
"""
import unittest
from typing import Dict, List, Any

from flatforge.core import (
    FileFormat, FileType, Section, SectionType, Record, Field, ParsedRecord, FieldValue
)
from flatforge.rules.global_rules import CountRule, SumRule, ChecksumRule, UniquenessRule
from flatforge.processors import ValidationProcessor


class TestGlobalRules(unittest.TestCase):
    """Test case for global rules."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a sample file format
        self.file_format = FileFormat(
            name="Test Format",
            type=FileType.DELIMITED,
            sections=[],
            delimiter=",",
            quote_char="\"",
            escape_char="\\",
            newline="\n",
            encoding="utf-8",
            skip_blank_lines=True,
            exit_on_first_error=False,
            abort_after_n_failed_records=-1
        )
        
        # Create a sample section
        self.section = Section(
            name="body",
            type=SectionType.BODY,
            record=Record(
                name="test_record",
                fields=[
                    Field(name="id", position=0),
                    Field(name="value", position=1)
                ]
            )
        )
        
        # Create sample records
        self.records = [
            self._create_record(1, {"id": "1", "value": "100"}),
            self._create_record(2, {"id": "2", "value": "200"}),
            self._create_record(3, {"id": "3", "value": "300"})
        ]
        
    def _create_record(self, record_number: int, values: Dict[str, str]) -> ParsedRecord:
        """Create a sample record."""
        field_values = {}
        for field_name, value in values.items():
            field = next((f for f in self.section.record.fields if f.name == field_name), None)
            if field:
                field_values[field_name] = FieldValue(field=field, value=value)
                
        raw_data = ",".join(values.values())
        return ParsedRecord(
            section=self.section,
            record_number=record_number,
            field_values=field_values,
            raw_data=raw_data
        )
        
    def test_count_rule(self):
        """Test the CountRule."""
        # Create a count rule
        rule = CountRule("test_count", {"section": "body"})
        
        # Process records
        for record in self.records:
            rule.process_record(record)
            
        # Check the count
        self.assertEqual(rule.state["count"], 3)
        
        # Check the calculated value
        self.assertEqual(rule.calculate_value(), 3)
        
        # Check that there are no errors
        errors = rule.finalize()
        self.assertEqual(len(errors), 0)
        
        # Test with expected count
        rule = CountRule("test_count", {"section": "body", "expected_count": 3})
        
        # Process records
        for record in self.records:
            rule.process_record(record)
            
        # Check that there are no errors
        errors = rule.finalize()
        self.assertEqual(len(errors), 0)
        
        # Test with wrong expected count
        rule = CountRule("test_count", {"section": "body", "expected_count": 4})
        
        # Process records
        for record in self.records:
            rule.process_record(record)
            
        # Check that there is an error
        errors = rule.finalize()
        self.assertEqual(len(errors), 1)
        self.assertIn("count mismatch", str(errors[0]).lower())
        
    def test_sum_rule(self):
        """Test the SumRule."""
        # Create a sum rule
        rule = SumRule("test_sum", {"section": "body", "field": "value"})
        
        # Process records
        for record in self.records:
            rule.process_record(record)
            
        # Check the sum
        self.assertEqual(rule.state["sum"], 600)
        
        # Check the calculated value
        self.assertEqual(rule.calculate_value(), 600)
        
        # Check that there are no errors
        errors = rule.finalize()
        self.assertEqual(len(errors), 0)
        
        # Test with expected sum
        rule = SumRule("test_sum", {"section": "body", "field": "value", "expected_sum": 600})
        
        # Process records
        for record in self.records:
            rule.process_record(record)
            
        # Check that there are no errors
        errors = rule.finalize()
        self.assertEqual(len(errors), 0)
        
        # Test with wrong expected sum
        rule = SumRule("test_sum", {"section": "body", "field": "value", "expected_sum": 700})
        
        # Process records
        for record in self.records:
            rule.process_record(record)
            
        # Check that there is an error
        errors = rule.finalize()
        self.assertEqual(len(errors), 1)
        self.assertIn("sum mismatch", str(errors[0]).lower())
        
    def test_checksum_rule(self):
        """Test the ChecksumRule."""
        # Create a checksum rule
        rule = ChecksumRule("test_checksum", {"section": "body", "field": "value", "type": "sum"})
        
        # Process records
        for record in self.records:
            rule.process_record(record)
            
        # Check the checksum
        expected_checksum = sum(ord(c) for c in "100") + sum(ord(c) for c in "200") + sum(ord(c) for c in "300")
        self.assertEqual(rule.state["checksum"], expected_checksum)
        
        # Check the calculated value
        self.assertEqual(rule.calculate_value(), expected_checksum)
        
        # Check that there are no errors
        errors = rule.finalize()
        self.assertEqual(len(errors), 0)
        
        # Test with expected checksum
        rule = ChecksumRule("test_checksum", {
            "section": "body", 
            "field": "value", 
            "type": "sum",
            "expected_checksum": expected_checksum
        })
        
        # Process records
        for record in self.records:
            rule.process_record(record)
            
        # Check that there are no errors
        errors = rule.finalize()
        self.assertEqual(len(errors), 0)
        
        # Test with wrong expected checksum
        rule = ChecksumRule("test_checksum", {
            "section": "body", 
            "field": "value", 
            "type": "sum",
            "expected_checksum": expected_checksum + 1
        })
        
        # Process records
        for record in self.records:
            rule.process_record(record)
            
        # Check that there is an error
        errors = rule.finalize()
        self.assertEqual(len(errors), 1)
        self.assertIn("checksum mismatch", str(errors[0]).lower())
        
    def test_uniqueness_rule_single_field(self):
        """Test the UniquenessRule with a single field."""
        # Create a uniqueness rule
        rule = UniquenessRule("test_uniqueness", {"section": "body", "fields": "id"})
        
        # Process records
        for record in self.records:
            rule.process_record(record)
            
        # Check that there are no errors
        errors = rule.finalize()
        self.assertEqual(len(errors), 0)
        
        # Add a duplicate record
        duplicate_record = self._create_record(4, {"id": "1", "value": "400"})
        rule.process_record(duplicate_record)
        
        # Check that there is an error
        errors = rule.finalize()
        self.assertEqual(len(errors), 1)
        self.assertIn("duplicate value", str(errors[0]).lower())
        
    def test_uniqueness_rule_composite_fields(self):
        """Test the UniquenessRule with composite fields."""
        # Create a uniqueness rule
        rule = UniquenessRule("test_uniqueness", {"section": "body", "fields": ["id", "value"]})
        
        # Process records
        for record in self.records:
            rule.process_record(record)
            
        # Check that there are no errors
        errors = rule.finalize()
        self.assertEqual(len(errors), 0)
        
        # Add a duplicate record
        duplicate_record = self._create_record(4, {"id": "1", "value": "100"})
        rule.process_record(duplicate_record)
        
        # Check that there is an error
        errors = rule.finalize()
        self.assertEqual(len(errors), 1)
        self.assertIn("duplicate composite value", str(errors[0]).lower())
        
        # Add a non-duplicate record
        non_duplicate_record = self._create_record(5, {"id": "1", "value": "500"})
        rule.process_record(non_duplicate_record)
        
        # Check that there is still only one error
        errors = rule.finalize()
        self.assertEqual(len(errors), 1)
        

if __name__ == '__main__':
    unittest.main() 