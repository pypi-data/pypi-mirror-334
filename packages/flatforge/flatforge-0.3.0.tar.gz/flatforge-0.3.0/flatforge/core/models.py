"""
Core data models for FlatForge.

This module contains the data models used throughout the FlatForge library.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Union


class FileType(Enum):
    """Enum representing the type of flat file."""
    FIXED_LENGTH = "fixed_length"
    DELIMITED = "delimited"


class SectionType(Enum):
    """Enum representing the type of section in a flat file."""
    HEADER = "header"
    BODY = "body"
    FOOTER = "footer"
    CUSTOM = "custom"


@dataclass
class Field:
    """
    Represents a field in a flat file record.
    
    Attributes:
        name: The name of the field
        position: The position of the field in the record (0-based)
        length: The length of the field (for fixed-length files)
        rules: List of rules to apply to this field
        description: Optional description of the field
    """
    name: str
    position: int
    length: Optional[int] = None
    rules: List[Dict[str, Any]] = field(default_factory=list)
    description: Optional[str] = None


@dataclass
class Record:
    """
    Represents a record format in a flat file.
    
    Attributes:
        name: The name of the record format
        fields: List of fields in the record
        description: Optional description of the record
    """
    name: str
    fields: List[Field]
    description: Optional[str] = None


@dataclass
class Section:
    """
    Represents a section in a flat file.
    
    Attributes:
        name: The name of the section
        type: The type of section
        record: The record format for this section
        min_records: Minimum number of records in this section
        max_records: Maximum number of records in this section
        identifier: Optional identifier to recognize this section
        description: Optional description of the section
    """
    name: str
    type: SectionType
    record: Record
    min_records: int = 1
    max_records: Optional[int] = None
    identifier: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


@dataclass
class FileFormat:
    """
    Represents the format of a flat file.
    
    Attributes:
        name: The name of the file format
        type: The type of file (fixed-length or delimited)
        sections: List of sections in the file
        delimiter: The delimiter character (for delimited files)
        quote_char: The quote character (for delimited files)
        escape_char: The escape character (for delimited files)
        newline: The newline character(s)
        encoding: The file encoding
        skip_blank_lines: Whether to skip blank lines
        exit_on_first_error: Whether to exit on the first error
        abort_after_n_failed_records: Number of failed records after which to abort processing (-1 means process the whole file)
        description: Optional description of the file format
    """
    name: str
    type: FileType
    sections: List[Section]
    delimiter: Optional[str] = None
    quote_char: Optional[str] = None
    escape_char: Optional[str] = None
    newline: str = "\n"
    encoding: str = "utf-8"
    skip_blank_lines: bool = True
    exit_on_first_error: bool = False
    abort_after_n_failed_records: int = -1
    description: Optional[str] = None


@dataclass
class FieldValue:
    """
    Represents a field value in a parsed record.
    
    Attributes:
        field: The field definition
        value: The raw value of the field
        transformed_value: The transformed value of the field
        errors: List of validation errors for this field
    """
    field: Field
    value: str
    transformed_value: Optional[Any] = None
    errors: List[Any] = field(default_factory=list)


@dataclass
class ParsedRecord:
    """
    Represents a parsed record from a flat file.
    
    Attributes:
        section: The section this record belongs to
        record_number: The record number in the file
        field_values: Dictionary of field values by field name
        raw_data: The raw data for this record
        is_valid: Whether the record is valid
    """
    section: Section
    record_number: int
    field_values: Dict[str, FieldValue]
    raw_data: str
    is_valid: bool = True


@dataclass
class ProcessingResult:
    """
    Represents the result of processing a flat file.
    
    Attributes:
        total_records: Total number of records processed
        valid_records: Number of valid records
        failed_records: Number of failed records
        error_count: Number of errors encountered
        errors: List of validation errors
    """
    total_records: int = 0
    valid_records: int = 0
    failed_records: int = 0
    error_count: int = 0
    errors: List[Any] = field(default_factory=list) 