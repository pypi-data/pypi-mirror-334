"""
Validation rules for FlatForge.

This module contains the validation rules for validating field values.
"""
import re
import datetime
from typing import Dict, List, Optional, Any, Pattern

from flatforge.core import ValidationError, FieldValue, ParsedRecord
from flatforge.rules.base import ValidationRule


class RequiredRule(ValidationRule):
    """Rule that validates that a field is not empty."""
    
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate that a field is not empty.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If the field is empty
        """
        if not field_value.value or field_value.value.strip() == "":
            raise ValidationError(
                "Field is required",
                field_name=field_value.field.name,
                value=field_value.value,
                rule_name=self.name
            )


class NumericRule(ValidationRule):
    """Rule that validates that a field is numeric."""
    
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate that a field is numeric.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If the field is not numeric
        """
        value = field_value.value.strip()
        
        # Empty values are allowed (use RequiredRule to enforce non-empty)
        if not value:
            return
            
        # Check if the value is numeric
        try:
            # Handle decimal values
            if "." in value:
                float_value = float(value)
                
                # Check decimal precision if specified
                if "decimal_precision" in self.params:
                    decimal_precision = self.params["decimal_precision"]
                    decimal_part = value.split(".")[1]
                    if len(decimal_part) > decimal_precision:
                        raise ValidationError(
                            f"Value has more than {decimal_precision} decimal places",
                            field_name=field_value.field.name,
                            value=value,
                            rule_name=self.name
                        )
                        
                # Check min value if specified
                if "min_value" in self.params and float_value < float(self.params["min_value"]):
                    raise ValidationError(
                        f"Value is less than minimum value {self.params['min_value']}",
                        field_name=field_value.field.name,
                        value=value,
                        rule_name=self.name
                    )
                    
                # Check max value if specified
                if "max_value" in self.params and float_value > float(self.params["max_value"]):
                    raise ValidationError(
                        f"Value is greater than maximum value {self.params['max_value']}",
                        field_name=field_value.field.name,
                        value=value,
                        rule_name=self.name
                    )
            else:
                # Integer value
                int_value = int(value)
                
                # Check min value if specified
                if "min_value" in self.params and int_value < int(self.params["min_value"]):
                    raise ValidationError(
                        f"Value is less than minimum value {self.params['min_value']}",
                        field_name=field_value.field.name,
                        value=value,
                        rule_name=self.name
                    )
                    
                # Check max value if specified
                if "max_value" in self.params and int_value > int(self.params["max_value"]):
                    raise ValidationError(
                        f"Value is greater than maximum value {self.params['max_value']}",
                        field_name=field_value.field.name,
                        value=value,
                        rule_name=self.name
                    )
        except (ValueError, TypeError):
            raise ValidationError(
                "Value is not numeric",
                field_name=field_value.field.name,
                value=value,
                rule_name=self.name
            )


class StringLengthRule(ValidationRule):
    """Rule that validates the length of a string field."""
    
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate the length of a string field.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If the field length is invalid
        """
        value = field_value.value
        
        # Empty values are allowed (use RequiredRule to enforce non-empty)
        if not value:
            return
            
        # Check min length if specified
        if "min_length" in self.params and len(value) < self.params["min_length"]:
            raise ValidationError(
                f"Value length is less than minimum length {self.params['min_length']}",
                field_name=field_value.field.name,
                value=value,
                rule_name=self.name
            )
            
        # Check max length if specified
        if "max_length" in self.params and len(value) > self.params["max_length"]:
            raise ValidationError(
                f"Value length is greater than maximum length {self.params['max_length']}",
                field_name=field_value.field.name,
                value=value,
                rule_name=self.name
            )


class RegexRule(ValidationRule):
    """Rule that validates a field against a regular expression."""
    
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate a field against a regular expression.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If the field does not match the regular expression
        """
        value = field_value.value
        
        # Empty values are allowed (use RequiredRule to enforce non-empty)
        if not value:
            return
            
        # Get the pattern from the parameters
        pattern = self.params.get("pattern")
        if not pattern:
            raise ValidationError(
                "No pattern specified for regex rule",
                field_name=field_value.field.name,
                value=value,
                rule_name=self.name
            )
            
        # Compile the pattern
        try:
            regex = re.compile(pattern)
        except re.error:
            raise ValidationError(
                f"Invalid regular expression pattern: {pattern}",
                field_name=field_value.field.name,
                value=value,
                rule_name=self.name
            )
            
        # Check if the value matches the pattern
        if not regex.match(value):
            raise ValidationError(
                f"Value does not match pattern: {pattern}",
                field_name=field_value.field.name,
                value=value,
                rule_name=self.name
            )


class DateRule(ValidationRule):
    """Rule that validates a date field."""
    
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate a date field.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If the field is not a valid date
        """
        value = field_value.value
        
        # Empty values are allowed (use RequiredRule to enforce non-empty)
        if not value:
            return
            
        # Get the format from the parameters
        format_str = self.params.get("format", "%Y-%m-%d")
        
        # Parse the date
        try:
            date = datetime.datetime.strptime(value, format_str)
        except ValueError:
            raise ValidationError(
                f"Value is not a valid date in format {format_str}",
                field_name=field_value.field.name,
                value=value,
                rule_name=self.name
            )
            
        # Check min date if specified
        if "min_date" in self.params:
            min_date_str = self.params["min_date"]
            try:
                min_date = datetime.datetime.strptime(min_date_str, format_str)
                if date < min_date:
                    raise ValidationError(
                        f"Date is before minimum date {min_date_str}",
                        field_name=field_value.field.name,
                        value=value,
                        rule_name=self.name
                    )
            except ValueError:
                raise ValidationError(
                    f"Invalid minimum date format: {min_date_str}",
                    field_name=field_value.field.name,
                    value=value,
                    rule_name=self.name
                )
                
        # Check max date if specified
        if "max_date" in self.params:
            max_date_str = self.params["max_date"]
            try:
                max_date = datetime.datetime.strptime(max_date_str, format_str)
                if date > max_date:
                    raise ValidationError(
                        f"Date is after maximum date {max_date_str}",
                        field_name=field_value.field.name,
                        value=value,
                        rule_name=self.name
                    )
            except ValueError:
                raise ValidationError(
                    f"Invalid maximum date format: {max_date_str}",
                    field_name=field_value.field.name,
                    value=value,
                    rule_name=self.name
                )


class ChoiceRule(ValidationRule):
    """Rule that validates that a field value is one of a set of choices."""
    
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate that a field value is one of a set of choices.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If the field value is not one of the choices
        """
        value = field_value.value
        
        # Empty values are allowed (use RequiredRule to enforce non-empty)
        if not value:
            return
            
        # Get the choices from the parameters
        choices = self.params.get("choices", [])
        if not choices:
            raise ValidationError(
                "No choices specified for choice rule",
                field_name=field_value.field.name,
                value=value,
                rule_name=self.name
            )
            
        # Check if the value is one of the choices
        if value not in choices:
            raise ValidationError(
                f"Value is not one of the allowed choices: {', '.join(choices)}",
                field_name=field_value.field.name,
                value=value,
                rule_name=self.name
            ) 