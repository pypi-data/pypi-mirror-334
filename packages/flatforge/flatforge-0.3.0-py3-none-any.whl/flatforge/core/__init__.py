"""
Core module for FlatForge.

This module contains the core components of the FlatForge library.
"""

from flatforge.core.exceptions import (
    FlatForgeError, ConfigError, ParserError, ValidationError, 
    TransformationError, ProcessorError
)
from flatforge.core.models import (
    FileType, SectionType, Field, Record, Section, FileFormat,
    FieldValue, ParsedRecord, ProcessingResult
)

__all__ = [
    'FlatForgeError', 'ConfigError', 'ParserError', 'ValidationError',
    'TransformationError', 'ProcessorError', 'FileType', 'SectionType',
    'Field', 'Record', 'Section', 'FileFormat', 'FieldValue',
    'ParsedRecord', 'ProcessingResult'
]

# Add a from_yaml method to FileFormat
def from_yaml(file_path):
    """
    Create a FileFormat from a YAML file.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        A FileFormat object
        
    Raises:
        ConfigError: If the file cannot be parsed
    """
    from flatforge.parsers import ConfigParser
    parser = ConfigParser.from_file(file_path)
    return parser.parse()

# Attach the method to the FileFormat class
FileFormat.from_yaml = staticmethod(from_yaml) 