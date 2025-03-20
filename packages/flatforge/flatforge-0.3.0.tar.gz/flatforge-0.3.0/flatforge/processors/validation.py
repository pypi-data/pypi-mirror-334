"""
Validation processor module for FlatForge.

This module contains the validation processor class.
"""
import csv
from typing import Dict, List, Optional, TextIO, Any

from flatforge.core import (
    FileFormat, ProcessingResult, ValidationError, ParsedRecord, ProcessorError, FieldValue
)
from flatforge.parsers import Parser
from flatforge.processors.base import Processor


class ValidationProcessor(Processor):
    """
    Processor that validates a file against a schema.
    
    This processor validates an input file against a schema and writes valid
    records to an output file and invalid records to an error file.
    """
    
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
            # Create a parser
            parser = Parser.create_parser(self.file_format)
            
            # Store records for post-processing (needed for inserting calculated values)
            records_by_section = {}
            
            # Open the output and error files
            with open(output_file, 'w', encoding=self.file_format.encoding) as out_file:
                error_file_obj = None
                if error_file:
                    error_file_obj = open(error_file, 'w', encoding=self.file_format.encoding)
                    
                try:
                    # Process the file
                    for record in parser.parse_file(input_file):
                        result.total_records += 1
                        
                        # Store the record for post-processing
                        section_name = record.section.name
                        if section_name not in records_by_section:
                            records_by_section[section_name] = []
                        records_by_section[section_name].append(record)
                        
                        # Apply field-level rules first
                        # Global rules will be applied after field-level rules
                        
                        # Write the record to the appropriate file
                        if record.is_valid:
                            # Apply global rules
                            for rule in self.global_rules:
                                rule.process_record(record)
                                
                            result.valid_records += 1
                        else:
                            # Increment failed records counter
                            result.failed_records += 1
                            
                            error_count = len([e for fv in record.field_values.values() for e in fv.errors])
                            result.error_count += error_count
                            result.errors.extend([e for fv in record.field_values.values() for e in fv.errors])
                            
                            # Apply global rules if configured to include invalid records
                            for rule in self.global_rules:
                                if rule.params.get("include_invalid_records", False):
                                    rule.process_record(record)
                            
                            if error_file_obj:
                                self._write_error_record(error_file_obj, record)
                                
                            # Exit on first error if configured to do so
                            if self.file_format.exit_on_first_error:
                                break
                                
                            # Abort after N failed records if configured
                            if (self.file_format.abort_after_n_failed_records > 0 and 
                                result.failed_records >= self.file_format.abort_after_n_failed_records):
                                break
                    
                    # Finalize global rules and insert calculated values
                    global_rule_errors = []
                    calculated_values = {}
                    
                    for rule in self.global_rules:
                        # Get any validation errors from the rule
                        errors = rule.finalize()
                        if errors:
                            global_rule_errors.extend(errors)
                            result.error_count += len(errors)
                            result.errors.extend(errors)
                        
                        # Check if this rule should insert its calculated value
                        if rule.should_insert_value():
                            target_field = rule.get_target_field()
                            if target_field:
                                section_name, field_name = target_field.split(".")
                                calculated_values[(section_name, field_name)] = rule.calculate_value()
                    
                    # Write global rule errors to error file
                    if error_file_obj and global_rule_errors:
                        for error in global_rule_errors:
                            error_file_obj.write(f"Global rule error: {str(error)}{self.file_format.newline}")
                        error_file_obj.write(self.file_format.newline)
                    
                    # Insert calculated values and write records to output file
                    for section_name, records in records_by_section.items():
                        for record in records:
                            # Skip invalid records
                            if not record.is_valid:
                                continue
                                
                            # Insert calculated values
                            for (target_section, target_field), value in calculated_values.items():
                                if target_section == section_name and target_field in record.field_values:
                                    field_value = record.field_values[target_field]
                                    # Convert the value to string if needed
                                    if not isinstance(value, str):
                                        value = str(value)
                                    field_value.value = value
                                    field_value.transformed_value = value
                            
                            # Write the record to the output file
                            self._write_record(out_file, record)
                            
                finally:
                    if error_file_obj:
                        error_file_obj.close()
                        
        except Exception as e:
            raise ProcessorError(f"Error processing file: {str(e)}")
            
        return result
    
    def _process_record(self, record: ParsedRecord, out_file: Optional[TextIO], 
                       error_file_obj: Optional[TextIO], result: ProcessingResult) -> bool:
        """
        Process a single record for chunked processing.
        
        Args:
            record: Record to process
            out_file: Output file object or None
            error_file_obj: Error file object or None
            result: ProcessingResult object to update
            
        Returns:
            True if processing should continue, False if it should stop
        """
        # Write the record to the appropriate file
        if record.is_valid:
            # Apply global rules
            for rule in self.global_rules:
                rule.process_record(record)
                
            result.valid_records += 1
            if out_file:
                self._write_record(out_file, record)
            return True
        else:
            # Increment failed records counter
            result.failed_records += 1
            
            error_count = len([e for fv in record.field_values.values() for e in fv.errors])
            result.error_count += error_count
            result.errors.extend([e for fv in record.field_values.values() for e in fv.errors])
            
            # Apply global rules if configured to include invalid records
            for rule in self.global_rules:
                if rule.params.get("include_invalid_records", False):
                    rule.process_record(record)
            
            if error_file_obj:
                self._write_error_record(error_file_obj, record)
            
            # Check if we should abort due to too many errors
            if (self.file_format.abort_after_n_failed_records > 0 and 
                result.failed_records >= self.file_format.abort_after_n_failed_records):
                return False
                
            # Check if we should exit on first error
            if self.file_format.exit_on_first_error:
                return False
                
            return True
    
    def _write_record(self, file_obj: TextIO, record: ParsedRecord) -> None:
        """
        Write a record to a file.
        
        Args:
            file_obj: File object to write to
            record: Record to write
        """
        # Write the raw data without adding an extra newline
        raw_data = record.raw_data.rstrip(self.file_format.newline)
        file_obj.write(raw_data + self.file_format.newline)
    
    def _write_error_record(self, file_obj: TextIO, record: ParsedRecord) -> None:
        """
        Write an error record to a file.
        
        Args:
            file_obj: File object to write to
            record: Record to write
        """
        # Write the raw data and the errors
        file_obj.write(f"Record {record.record_number} in section {record.section.name}:{self.file_format.newline}")
        file_obj.write(f"Raw data: {record.raw_data}{self.file_format.newline}")
        
        # Write the errors
        for field_name, field_value in record.field_values.items():
            for error in field_value.errors:
                file_obj.write(f"Error: {str(error)}{self.file_format.newline}")
                
        file_obj.write(self.file_format.newline) 