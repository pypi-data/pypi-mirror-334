"""
File parser module for FlatForge.

This module contains the classes for parsing flat files.
"""
import csv
import io
from abc import ABC, abstractmethod
from typing import Dict, Iterator, List, Optional, Tuple, Union

from flatforge.core import (
    FileFormat, FileType, Section, SectionType, Field, ParsedRecord, FieldValue, ParserError
)
from flatforge.rules import Rule, ValidationRule, TransformerRule, VALIDATION_RULES, TRANSFORMER_RULES


class Parser(ABC):
    """
    Abstract base class for file parsers.
    
    A parser parses an input file according to a provided file format.
    """
    
    @staticmethod
    def create_parser(file_format: FileFormat) -> 'Parser':
        """
        Create a parser for a file format.
        
        Args:
            file_format: The file format to create a parser for
            
        Returns:
            A parser instance
            
        Raises:
            ParserError: If the file format is not supported
        """
        if file_format.type == FileType.FIXED_LENGTH:
            return FixedLengthParser(file_format)
        elif file_format.type == FileType.DELIMITED:
            return DelimitedParser(file_format)
        else:
            raise ParserError(f"Unsupported file type: {file_format.type}")
    
    def __init__(self, file_format: FileFormat):
        """
        Initialize a parser.
        
        Args:
            file_format: The file format to parse
        """
        self.file_format = file_format
        self.current_section: Optional[Section] = None
        self.section_record_count: Dict[str, int] = {}
        self.rules_cache: Dict[str, List[Rule]] = {}
    
    def parse_file(self, file_path: str) -> Iterator[ParsedRecord]:
        """
        Parse a file.
        
        Args:
            file_path: Path to the file to parse
            
        Yields:
            ParsedRecord objects for each record in the file
            
        Raises:
            ParserError: If the file cannot be parsed
        """
        try:
            with open(file_path, 'r', encoding=self.file_format.encoding) as f:
                yield from self.parse(f)
        except Exception as e:
            raise ParserError(f"Error parsing file: {str(e)}")
    
    @abstractmethod
    def parse(self, file_obj: io.TextIOBase) -> Iterator[ParsedRecord]:
        """
        Parse a file object.
        
        Args:
            file_obj: File object to parse
            
        Yields:
            ParsedRecord objects for each record in the file
            
        Raises:
            ParserError: If the file cannot be parsed
        """
        pass
    
    def _detect_last_record(self, file_obj: io.TextIOBase) -> Optional[int]:
        """
        Detect the total number of records in a file.
        
        This is used to identify the last record when no explicit identifier is provided
        for the footer section.
        
        Args:
            file_obj: File object to parse
            
        Returns:
            The total number of records, or None if the file cannot be read
        """
        try:
            # Save the current position
            current_pos = file_obj.tell()
            
            # Count the records
            record_count = 0
            for line in file_obj:
                if self.file_format.skip_blank_lines and not line.strip():
                    continue
                record_count += 1
                
            # Reset the file position
            file_obj.seek(current_pos)
            
            return record_count
        except Exception:
            # If we can't determine the record count, return None
            return None
    
    def _get_section_for_record(self, raw_data: str, record_number: int, total_records: Optional[int] = None) -> Section:
        """
        Determine which section a record belongs to.
        
        Args:
            raw_data: Raw record data
            record_number: Record number in the file
            total_records: Optional total number of records in the file
            
        Returns:
            The section the record belongs to
            
        Raises:
            ParserError: If the section cannot be determined
        """
        # If we're already in a section, check if we need to switch
        if self.current_section:
            # Check if we've reached the maximum number of records for this section
            if (self.current_section.max_records and 
                self.section_record_count.get(self.current_section.name, 0) >= self.current_section.max_records):
                # Find the next section
                current_index = next(
                    (i for i, s in enumerate(self.file_format.sections) if s.name == self.current_section.name),
                    -1
                )
                if current_index < len(self.file_format.sections) - 1:
                    self.current_section = self.file_format.sections[current_index + 1]
                    self.section_record_count[self.current_section.name] = 0
                else:
                    raise ParserError(f"Unexpected record after last section: {record_number}")
            
            # Check if the record matches an identifier for a different section
            for section in self.file_format.sections:
                if section.identifier and self._matches_identifier(raw_data, section):
                    self.current_section = section
                    self.section_record_count[section.name] = 0
                    break
            
            # If no identifier matched but we have a positional section structure, try to determine section by position
            if not any(s.identifier for s in self.file_format.sections) and len(self.file_format.sections) > 1:
                # Apply positional section detection logic
                self._apply_positional_section_detection(record_number, total_records)
        
        # If we don't have a current section, start with the first one
        if not self.current_section:
            self.current_section = self.file_format.sections[0]
            self.section_record_count[self.current_section.name] = 0
        
        # Increment the record count for this section
        self.section_record_count[self.current_section.name] = self.section_record_count.get(self.current_section.name, 0) + 1
        
        return self.current_section
    
    def _apply_positional_section_detection(self, record_number: int, total_records: Optional[int] = None) -> None:
        """
        Apply positional section detection logic when record type is not specified.
        
        This method implements the logic that:
        - If file has 2 sections, section 1 length is 1 record
        - If file has 3 sections, section 1 length is 1 record and section 3 length is also 1 record
        
        Args:
            record_number: Current record number
            total_records: Optional total number of records in the file
        """
        total_sections = len(self.file_format.sections)
        
        # For 2-section files (header + body)
        if total_sections == 2:
            header_section = next((s for s in self.file_format.sections if s.type == SectionType.HEADER), None)
            body_section = next((s for s in self.file_format.sections if s.type == SectionType.BODY), None)
            
            if header_section and body_section:
                # If we're in the header and have processed 1 record, move to body
                if (self.current_section.type == SectionType.HEADER and 
                    self.section_record_count.get(self.current_section.name, 0) >= 1):
                    self.current_section = body_section
                    self.section_record_count[body_section.name] = 0
        
        # For 3-section files (header + body + footer)
        elif total_sections == 3:
            header_section = next((s for s in self.file_format.sections if s.type == SectionType.HEADER), None)
            body_section = next((s for s in self.file_format.sections if s.type == SectionType.BODY), None)
            footer_section = next((s for s in self.file_format.sections if s.type == SectionType.FOOTER), None)
            
            if header_section and body_section and footer_section:
                # If we're in the header and have processed 1 record, move to body
                if (self.current_section.type == SectionType.HEADER and 
                    self.section_record_count.get(self.current_section.name, 0) >= 1):
                    self.current_section = body_section
                    self.section_record_count[body_section.name] = 0
                
                # If this is the last record and we know the total, move to footer
                if total_records and record_number == total_records and self.current_section.type == SectionType.BODY:
                    self.current_section = footer_section
                    self.section_record_count[footer_section.name] = 0
                    return
                
                # If max_records is specified for body, use it to determine when to switch to footer
                if body_section.max_records:
                    total_expected_body_records = body_section.max_records
                    if (self.current_section.type == SectionType.BODY and 
                        self.section_record_count.get(self.current_section.name, 0) >= total_expected_body_records):
                        self.current_section = footer_section
                        self.section_record_count[footer_section.name] = 0
    
    def _matches_identifier(self, raw_data: str, section: Section) -> bool:
        """
        Check if a record matches a section identifier.
        
        Args:
            raw_data: Raw record data
            section: Section to check
            
        Returns:
            True if the record matches the section identifier, False otherwise
        """
        if not section.identifier:
            return False
            
        # The identifier can be a field value or a regex pattern
        if 'field' in section.identifier and 'value' in section.identifier:
            field_name = section.identifier['field']
            expected_value = section.identifier['value']
            
            # Parse the record to get the field value
            field = next((f for f in section.record.fields if f.name == field_name), None)
            if not field:
                return False
                
            # Extract the field value based on the parser type
            if self.file_format.type == FileType.FIXED_LENGTH:
                start_pos = 0
                for f in section.record.fields:
                    if f.position < field.position:
                        start_pos += f.length or 0
                field_value = raw_data[start_pos:start_pos + (field.length or 0)].strip()
            else:  # DELIMITED
                delimiter = self.file_format.delimiter or ','
                values = raw_data.split(delimiter)
                if field.position < len(values):
                    field_value = values[field.position].strip()
                else:
                    return False
                    
            return field_value == expected_value
        
        # TODO: Add support for regex patterns
        
        return False
    
    def _create_rules(self, field: Field) -> List[Rule]:
        """
        Create rules for a field.
        
        Args:
            field: The field to create rules for
            
        Returns:
            A list of Rule objects
            
        Raises:
            ParserError: If a rule cannot be created
        """
        # Check if we've already created rules for this field
        cache_key = f"{field.name}_{id(field)}"
        if cache_key in self.rules_cache:
            return self.rules_cache[cache_key]
            
        rules = []
        
        for rule_config in field.rules:
            if 'type' not in rule_config:
                raise ParserError(f"Rule for field {field.name} must have a type")
                
            rule_type = rule_config['type']
            rule_name = rule_config.get('name', rule_type)
            rule_params = rule_config.get('params', {})
            
            # Create the rule
            if rule_type in VALIDATION_RULES:
                rule_class = VALIDATION_RULES[rule_type]
                rules.append(rule_class(rule_name, rule_params))
            elif rule_type in TRANSFORMER_RULES:
                rule_class = TRANSFORMER_RULES[rule_type]
                rules.append(rule_class(rule_name, rule_params))
            else:
                raise ParserError(f"Unknown rule type: {rule_type}")
                
        # Cache the rules for this field
        self.rules_cache[cache_key] = rules
        
        return rules
    
    def _apply_rules(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Apply rules to a field value.
        
        Args:
            field_value: The field value to apply rules to
            record: The record containing the field value
        """
        rules = self._create_rules(field_value.field)
        
        for rule in rules:
            rule.apply(field_value, record)


class FixedLengthParser(Parser):
    """Parser for fixed-length flat files."""
    
    def parse(self, file_obj: io.TextIOBase) -> Iterator[ParsedRecord]:
        """
        Parse a fixed-length file.
        
        Args:
            file_obj: File object to parse
            
        Yields:
            ParsedRecord objects for each record in the file
            
        Raises:
            ParserError: If the file cannot be parsed
        """
        record_number = 0
        
        # If no section has an identifier, try to detect the total number of records
        total_records = None
        if not any(s.identifier for s in self.file_format.sections) and len(self.file_format.sections) > 1:
            total_records = self._detect_last_record(file_obj)
        
        for line_number, line in enumerate(file_obj, 1):
            # Skip blank lines if configured to do so
            if self.file_format.skip_blank_lines and not line.strip():
                continue
                
            record_number += 1
            
            # Determine which section this record belongs to
            section = self._get_section_for_record(line, record_number, total_records)
            
            # Parse the record
            try:
                parsed_record = self._parse_record(line, section, record_number)
                yield parsed_record
            except Exception as e:
                raise ParserError(f"Error parsing record {record_number} at line {line_number}: {str(e)}")
    
    def _parse_record(self, line: str, section: Section, record_number: int) -> ParsedRecord:
        """
        Parse a fixed-length record.
        
        Args:
            line: Raw record data
            section: Section the record belongs to
            record_number: Record number in the file
            
        Returns:
            A ParsedRecord object
            
        Raises:
            ParserError: If the record cannot be parsed
        """
        field_values = {}
        start_pos = 0
        
        for field in section.record.fields:
            if field.length is None:
                raise ParserError(f"Field {field.name} in section {section.name} must have a length")
                
            # Extract the field value
            end_pos = start_pos + field.length
            if end_pos > len(line):
                # If the line is shorter than expected, pad with spaces
                value = line[start_pos:].ljust(field.length)
            else:
                value = line[start_pos:end_pos]
                
            # Create a field value
            field_value = FieldValue(field=field, value=value)
            field_values[field.name] = field_value
            
            start_pos = end_pos
        
        # Create a parsed record
        parsed_record = ParsedRecord(
            section=section,
            record_number=record_number,
            field_values=field_values,
            raw_data=line
        )
        
        # Apply rules to each field value
        for field_value in field_values.values():
            self._apply_rules(field_value, parsed_record)
            
        return parsed_record


class DelimitedParser(Parser):
    """Parser for delimited flat files."""
    
    def parse(self, file_obj: io.TextIOBase) -> Iterator[ParsedRecord]:
        """
        Parse a delimited file.
        
        Args:
            file_obj: File object to parse
            
        Yields:
            ParsedRecord objects for each record in the file
            
        Raises:
            ParserError: If the file cannot be parsed
        """
        record_number = 0
        
        # If no section has an identifier, try to detect the total number of records
        total_records = None
        if not any(s.identifier for s in self.file_format.sections) and len(self.file_format.sections) > 1:
            total_records = self._detect_last_record(file_obj)
        
        # Create a CSV reader
        delimiter = self.file_format.delimiter or ','
        quote_char = self.file_format.quote_char or '"'
        
        # Handle escape characters
        if self.file_format.escape_char:
            # Convert escaped characters to their actual values
            escape_map = {
                '\\t': '\t',
                '\\n': '\n',
                '\\r': '\r',
                '\\\\': '\\',
                '\\\'': '\'',
                '\\"': '"'
            }
            if self.file_format.escape_char in escape_map:
                escape_char = escape_map[self.file_format.escape_char]
            else:
                escape_char = self.file_format.escape_char
        else:
            escape_char = None
            
        reader = csv.reader(
            file_obj,
            delimiter=delimiter,
            quotechar=quote_char,
            escapechar=escape_char
        )
        
        for line_number, row in enumerate(reader, 1):
            # Skip blank lines if configured to do so
            if self.file_format.skip_blank_lines and not any(row):
                continue
                
            record_number += 1
            
            # Convert the row back to a delimited string for section detection
            raw_data = delimiter.join(row)
            
            # Determine which section this record belongs to
            section = self._get_section_for_record(raw_data, record_number, total_records)
            
            # Parse the record
            try:
                parsed_record = self._parse_record(row, raw_data, section, record_number)
                yield parsed_record
            except Exception as e:
                raise ParserError(f"Error parsing record {record_number} at line {line_number}: {str(e)}")
    
    def _parse_record(self, row: List[str], raw_data: str, section: Section, record_number: int) -> ParsedRecord:
        """
        Parse a delimited record.
        
        Args:
            row: List of field values
            raw_data: Raw record data
            section: Section the record belongs to
            record_number: Record number in the file
            
        Returns:
            A ParsedRecord object
            
        Raises:
            ParserError: If the record cannot be parsed
        """
        field_values = {}
        
        for field in section.record.fields:
            # Extract the field value
            if field.position < len(row):
                value = row[field.position]
            else:
                # If the row is shorter than expected, use an empty string
                value = ""
                
            # Create a field value
            field_value = FieldValue(field=field, value=value)
            field_values[field.name] = field_value
        
        # Create a parsed record
        parsed_record = ParsedRecord(
            section=section,
            record_number=record_number,
            field_values=field_values,
            raw_data=raw_data
        )
        
        # Apply rules to each field value
        for field_value in field_values.values():
            self._apply_rules(field_value, parsed_record)
            
        return parsed_record 