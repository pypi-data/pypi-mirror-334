"""
Conversion processor module for FlatForge.

This module contains the conversion processor class.
"""
import csv
from typing import Dict, List, Optional, TextIO, Any

from flatforge.core import (
    FileFormat, ProcessingResult, ValidationError, ParsedRecord, ProcessorError,
    FileType
)
from flatforge.parsers import Parser
from flatforge.processors.base import Processor


class ConversionProcessor(Processor):
    """
    Processor that converts a file from one format to another.
    
    This processor converts an input file from one format to another based on
    a mapping configuration.
    """
    
    def __init__(self, input_format: FileFormat, output_format: FileFormat):
        """
        Initialize a conversion processor.
        
        Args:
            input_format: The input file format
            output_format: The output file format
        """
        super().__init__(input_format)
        self.input_format = input_format
        self.output_format = output_format
    
    def process(self, input_file: str, output_file: str, error_file: Optional[str] = None) -> ProcessingResult:
        """
        Process a file.
        
        Args:
            input_file: Path to the input file
            output_file: Path to the output file
            error_file: Optional path to the error file
            
        Returns:
            A ProcessingResult object
            
        Raises:
            ProcessorError: If the file cannot be processed
        """
        result = ProcessingResult()
        
        try:
            # Create a parser for the input format
            parser = Parser.create_parser(self.input_format)
            
            # Open the output and error files
            with open(output_file, 'w', encoding=self.output_format.encoding) as out_file:
                error_file_obj = None
                if error_file:
                    error_file_obj = open(error_file, 'w', encoding=self.input_format.encoding)
                    
                try:
                    # Process the file
                    for record in parser.parse_file(input_file):
                        result.total_records += 1
                        
                        # Apply global rules
                        for rule in self.global_rules:
                            rule.process_record(record)
                            
                        # Convert and write the record
                        if record.is_valid:
                            result.valid_records += 1
                            self._convert_and_write_record(out_file, record)
                        else:
                            result.error_count += len([e for fv in record.field_values.values() for e in fv.errors])
                            result.errors.extend([e for fv in record.field_values.values() for e in fv.errors])
                            
                            if error_file_obj:
                                self._write_error_record(error_file_obj, record)
                                
                            # Exit on first error if configured to do so
                            if self.input_format.exit_on_first_error:
                                break
                                
                    # Finalize global rules
                    for rule in self.global_rules:
                        errors = rule.finalize()
                        if errors:
                            result.error_count += len(errors)
                            result.errors.extend(errors)
                            
                finally:
                    if error_file_obj:
                        error_file_obj.close()
                        
        except Exception as e:
            raise ProcessorError(f"Error processing file: {str(e)}")
            
        return result
    
    def _process_record(self, record: ParsedRecord, out_file: Optional[TextIO], 
                       error_file_obj: Optional[TextIO], result: ProcessingResult) -> None:
        """
        Process a single record for chunked processing.
        
        Args:
            record: Record to process
            out_file: Output file object or None
            error_file_obj: Error file object or None
            result: ProcessingResult object to update
        """
        # Write the record to the appropriate file
        if record.is_valid:
            result.valid_records += 1
            if out_file:
                self._convert_and_write_record(out_file, record)
        else:
            result.error_count += len([e for fv in record.field_values.values() for e in fv.errors])
            result.errors.extend([e for fv in record.field_values.values() for e in fv.errors])
            
            if error_file_obj:
                self._write_error_record(error_file_obj, record)
    
    def _convert_and_write_record(self, file_obj: TextIO, record: ParsedRecord) -> None:
        """
        Convert and write a record to a file.
        
        Args:
            file_obj: File object to write to
            record: Record to convert and write
        """
        # Find the corresponding output section
        output_section = next(
            (s for s in self.output_format.sections if s.type == record.section.type),
            None
        )
        
        if not output_section:
            # If there's no corresponding section, skip this record
            return
            
        # Convert the record
        if self.output_format.type == FileType.FIXED_LENGTH:
            self._convert_to_fixed_length(file_obj, record, output_section)
        else:  # DELIMITED
            self._convert_to_delimited(file_obj, record, output_section)
    
    def _convert_to_fixed_length(self, file_obj: TextIO, record: ParsedRecord, output_section) -> None:
        """
        Convert a record to fixed-length format.
        
        Args:
            file_obj: File object to write to
            record: Record to convert
            output_section: Output section to convert to
        """
        output_line = ""
        
        # Build the output line
        for field in output_section.record.fields:
            # Find the corresponding input field
            input_field_name = self._get_mapping(output_section.name, field.name)
            
            if input_field_name and input_field_name in record.field_values:
                # Use the transformed value if available, otherwise use the raw value
                field_value = record.field_values[input_field_name]
                value = field_value.transformed_value if field_value.transformed_value is not None else field_value.value
            else:
                # If there's no corresponding input field, use an empty string
                value = ""
                
            # Pad the value to the field length
            if field.length:
                if len(value) > field.length:
                    # Truncate the value if it's too long
                    value = value[:field.length]
                else:
                    # Pad the value if it's too short
                    value = value.ljust(field.length)
                    
            output_line += value
            
        # Write the output line
        file_obj.write(output_line)
        file_obj.write(self.output_format.newline)
    
    def _convert_to_delimited(self, file_obj: TextIO, record: ParsedRecord, output_section) -> None:
        """
        Convert a record to delimited format.
        
        Args:
            file_obj: File object to write to
            record: Record to convert
            output_section: Output section to convert to
        """
        output_values = []
        
        # Build the output values
        for field in output_section.record.fields:
            # Find the corresponding input field
            input_field_name = self._get_mapping(output_section.name, field.name)
            
            if input_field_name and input_field_name in record.field_values:
                # Use the transformed value if available, otherwise use the raw value
                field_value = record.field_values[input_field_name]
                value = field_value.transformed_value if field_value.transformed_value is not None else field_value.value
            else:
                # If there's no corresponding input field, use an empty string
                value = ""
                
            output_values.append(value)
            
        # Write the output values
        delimiter = self.output_format.delimiter or ','
        output_line = delimiter.join(output_values)
        file_obj.write(output_line)
        file_obj.write(self.output_format.newline)
    
    def _get_mapping(self, section_name: str, field_name: str) -> Optional[str]:
        """
        Get the input field name for an output field.
        
        Args:
            section_name: Name of the output section
            field_name: Name of the output field
            
        Returns:
            The name of the corresponding input field, or None if there's no mapping
        """
        # Check if there's a mapping for this field
        mapping = getattr(self.output_format, 'mapping', {})
        
        # The mapping can be at the field level or the section level
        if section_name in mapping and field_name in mapping[section_name]:
            return mapping[section_name][field_name]
        elif field_name in mapping:
            return mapping[field_name]
            
        # If there's no mapping, use the same field name
        return field_name
    
    def _write_error_record(self, file_obj: TextIO, record: ParsedRecord) -> None:
        """
        Write an error record to a file.
        
        Args:
            file_obj: File object to write to
            record: Record to write
        """
        # Write the raw data and the errors
        file_obj.write(f"Record {record.record_number} in section {record.section.name}:{self.input_format.newline}")
        file_obj.write(f"Raw data: {record.raw_data}{self.input_format.newline}")
        
        # Write the errors
        for field_name, field_value in record.field_values.items():
            for error in field_value.errors:
                file_obj.write(f"Error: {str(error)}{self.input_format.newline}")
                
        file_obj.write(self.input_format.newline) 