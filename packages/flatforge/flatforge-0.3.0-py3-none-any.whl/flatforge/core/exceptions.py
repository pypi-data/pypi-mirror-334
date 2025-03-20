"""
Exceptions module for FlatForge.

This module contains all the custom exceptions used throughout the FlatForge library.
"""


class FlatForgeError(Exception):
    """Base exception for all FlatForge errors."""
    pass


class ConfigError(FlatForgeError):
    """Exception raised for configuration errors."""
    pass


class ParserError(FlatForgeError):
    """Exception raised for parsing errors."""
    pass


class ValidationError(FlatForgeError):
    """Exception raised for validation errors."""
    
    def __init__(self, message, field_name=None, value=None, rule_name=None, error_code=None, 
                 section_name=None, record_number=None, field_value=None):
        """
        Initialize a validation error.
        
        Args:
            message: The error message
            field_name: The name of the field that failed validation
            value: The value that failed validation
            rule_name: The name of the rule that failed
            error_code: A code identifying the type of error
            section_name: The name of the section containing the error
            record_number: The record number where the error occurred
            field_value: The field value that caused the error
        """
        self.field_name = field_name
        self.value = value
        self.rule_name = rule_name
        self.error_code = error_code
        self.section_name = section_name
        self.record_number = record_number
        self.field_value = field_value
        
        # Build a detailed error message
        detailed_message = message
        if field_name:
            detailed_message = f"Field '{field_name}': {detailed_message}"
        if value is not None:
            detailed_message = f"{detailed_message} (value: '{value}')"
        if rule_name:
            detailed_message = f"{detailed_message} [rule: {rule_name}]"
        if error_code:
            detailed_message = f"{detailed_message} <code: {error_code}>"
        if section_name:
            detailed_message = f"{detailed_message} in section '{section_name}'"
        if record_number is not None:
            detailed_message = f"{detailed_message} at record #{record_number}"
            
        super().__init__(detailed_message)


class TransformationError(FlatForgeError):
    """Exception raised for transformation errors."""
    pass


class ProcessorError(FlatForgeError):
    """Exception raised for processor errors."""
    pass 