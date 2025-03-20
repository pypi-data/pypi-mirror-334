"""
Transformation rules for FlatForge.

This module contains the transformation rules for transforming field values.
"""
import re
import datetime
from typing import Dict, List, Optional, Any

from flatforge.core import FieldValue, ParsedRecord
from flatforge.rules.base import TransformerRule


class TrimRule(TransformerRule):
    """Rule that trims whitespace from a field value."""
    
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Trim whitespace from a field value.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The trimmed value
        """
        value = field_value.value
        trim_type = self.params.get("type", "both")
        
        if trim_type == "left":
            return value.lstrip()
        elif trim_type == "right":
            return value.rstrip()
        else:  # both
            return value.strip()


class CaseRule(TransformerRule):
    """Rule that changes the case of a field value."""
    
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Change the case of a field value.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The transformed value
        """
        value = field_value.value
        case_type = self.params.get("type", "upper")
        
        if case_type == "upper":
            return value.upper()
        elif case_type == "lower":
            return value.lower()
        elif case_type == "title":
            return value.title()
        elif case_type == "camel":
            words = value.split()
            if not words:
                return ""
            result = words[0].lower()
            for word in words[1:]:
                if word:
                    result += word[0].upper() + word[1:].lower()
            return result
        else:
            return value


class PadRule(TransformerRule):
    """Rule that pads a field value to a specified length."""
    
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Pad a field value to a specified length.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The padded value
        """
        value = field_value.value
        length = self.params.get("length", field_value.field.length)
        if not length:
            raise ValueError("Pad rule requires a 'length' parameter or field length")
            
        pad_char = self.params.get("char", " ")
        pad_side = self.params.get("side", "left")
        
        if len(value) >= length:
            return value
            
        if pad_side == "left":
            return pad_char * (length - len(value)) + value
        else:  # right
            return value + pad_char * (length - len(value))


class DateFormatRule(TransformerRule):
    """Rule that formats a date field."""
    
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Format a date field.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The formatted date
        """
        value = field_value.value.strip()
        if not value:
            return value
            
        input_format = self.params.get("input_format", "%Y%m%d")
        output_format = self.params.get("output_format", "%Y-%m-%d")
        
        try:
            date = datetime.datetime.strptime(value, input_format)
            return date.strftime(output_format)
        except ValueError:
            # If the date can't be parsed, return the original value
            return value


class SubstringRule(TransformerRule):
    """Rule that extracts a substring from a field value."""
    
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Extract a substring from a field value.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The extracted substring
        """
        value = field_value.value
        start = self.params.get("start", 0)
        end = self.params.get("end", None)
        
        return value[start:end]


class ReplaceRule(TransformerRule):
    """Rule that replaces text in a field value."""
    
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Replace text in a field value.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The value with replacements
        """
        value = field_value.value
        old = self.params.get("old", "")
        new = self.params.get("new", "")
        
        if not old:
            return value
            
        return value.replace(old, new) 