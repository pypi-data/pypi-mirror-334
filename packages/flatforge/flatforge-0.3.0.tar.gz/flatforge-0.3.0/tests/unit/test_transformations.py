"""
Unit tests for the transformation rules.
"""
import unittest

from flatforge.core import FieldValue, ParsedRecord, Field, Section, SectionType, Record
from flatforge.rules import TransformerRule, TRANSFORMER_RULES
from flatforge.rules.transformation import (
    TrimRule, CaseRule, PadRule, DateFormatRule, SubstringRule, ReplaceRule
)


class TestTransformationRules(unittest.TestCase):
    """Test case for the transformation rules."""
    
    def setUp(self):
        """Set up the test case."""
        # Create a field
        self.field = Field(name="test_field", position=0)
        
        # Create a record
        self.record = Record(name="test_record", fields=[self.field])
        
        # Create a section
        self.section = Section(name="test_section", type=SectionType.BODY, record=self.record)
        
        # Create a parsed record
        self.parsed_record = ParsedRecord(
            section=self.section,
            record_number=1,
            field_values={},
            raw_data="test data"
        )
    
    def test_trim_rule(self):
        """Test the trim rule."""
        # Test both trim
        field_value = FieldValue(field=self.field, value="  test  ")
        rule = TrimRule("trim", {"type": "both"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "test")
        
        # Test left trim
        field_value = FieldValue(field=self.field, value="  test  ")
        rule = TrimRule("trim", {"type": "left"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "test  ")
        
        # Test right trim
        field_value = FieldValue(field=self.field, value="  test  ")
        rule = TrimRule("trim", {"type": "right"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "  test")
        
        # Test default (both)
        field_value = FieldValue(field=self.field, value="  test  ")
        rule = TrimRule("trim")
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "test")
    
    def test_case_rule(self):
        """Test the case rule."""
        # Test upper case
        field_value = FieldValue(field=self.field, value="test")
        rule = CaseRule("case", {"type": "upper"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "TEST")
        
        # Test lower case
        field_value = FieldValue(field=self.field, value="TEST")
        rule = CaseRule("case", {"type": "lower"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "test")
        
        # Test title case
        field_value = FieldValue(field=self.field, value="test case")
        rule = CaseRule("case", {"type": "title"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "Test Case")
        
        # Test camel case
        field_value = FieldValue(field=self.field, value="test case")
        rule = CaseRule("case", {"type": "camel"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "testCase")
        
        # Test default (upper)
        field_value = FieldValue(field=self.field, value="test")
        rule = CaseRule("case")
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "TEST")
    
    def test_pad_rule(self):
        """Test the pad rule."""
        # Test left padding
        field_value = FieldValue(field=self.field, value="123")
        rule = PadRule("pad", {"length": 5, "char": "0", "side": "left"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "00123")
        
        # Test right padding
        field_value = FieldValue(field=self.field, value="abc")
        rule = PadRule("pad", {"length": 5, "char": "*", "side": "right"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "abc**")
        
        # Test no padding needed
        field_value = FieldValue(field=self.field, value="12345")
        rule = PadRule("pad", {"length": 5, "char": "0", "side": "left"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "12345")
        
        # Test default (left padding with space)
        field = Field(name="test_field", position=0, length=5)
        field_value = FieldValue(field=field, value="abc")
        rule = PadRule("pad")
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "  abc")
    
    def test_date_format_rule(self):
        """Test the date format rule."""
        # Test date formatting
        field_value = FieldValue(field=self.field, value="20230415")
        rule = DateFormatRule("date_format", {"input_format": "%Y%m%d", "output_format": "%d-%m-%Y"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "15-04-2023")
        
        # Test invalid date
        field_value = FieldValue(field=self.field, value="invalid")
        rule = DateFormatRule("date_format", {"input_format": "%Y%m%d", "output_format": "%d-%m-%Y"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "invalid")  # Should return the original value
        
        # Test empty value
        field_value = FieldValue(field=self.field, value="")
        rule = DateFormatRule("date_format", {"input_format": "%Y%m%d", "output_format": "%d-%m-%Y"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "")  # Should return the original value
    
    def test_substring_rule(self):
        """Test the substring rule."""
        # Test substring extraction
        field_value = FieldValue(field=self.field, value="abcdefghij")
        rule = SubstringRule("substring", {"start": 2, "end": 6})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "cdef")
        
        # Test substring without end
        field_value = FieldValue(field=self.field, value="abcdefghij")
        rule = SubstringRule("substring", {"start": 5})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "fghij")
        
        # Test substring with start beyond length
        field_value = FieldValue(field=self.field, value="abc")
        rule = SubstringRule("substring", {"start": 5})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "")
    
    def test_replace_rule(self):
        """Test the replace rule."""
        # Test single replacement
        field_value = FieldValue(field=self.field, value="abc123")
        rule = ReplaceRule("replace", {"old": "abc", "new": "XYZ"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "XYZ123")
        
        # Test multiple replacements
        field_value = FieldValue(field=self.field, value="abc123abc")
        rule = ReplaceRule("replace", {"old": "abc", "new": "XYZ"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "XYZ123XYZ")
        
        # Test no replacement
        field_value = FieldValue(field=self.field, value="123")
        rule = ReplaceRule("replace", {"old": "abc", "new": "XYZ"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "123")
        
        # Test empty old value
        field_value = FieldValue(field=self.field, value="abc123")
        rule = ReplaceRule("replace", {"old": "", "new": "XYZ"})
        result = rule.transform(field_value, self.parsed_record)
        self.assertEqual(result, "abc123")  # Should return the original value


if __name__ == '__main__':
    unittest.main() 