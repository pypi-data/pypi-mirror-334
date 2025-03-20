"""
Counter processor module for FlatForge.

This module contains the counter processor class.
"""
from typing import Dict, Optional, TextIO, Callable

from flatforge.core import FileFormat, ProcessingResult, ProcessorError, SectionType, ParsedRecord
from flatforge.parsers import Parser
from flatforge.processors.base import Processor


class CounterProcessor(Processor):
    """
    Processor that counts records in a file.
    
    This processor counts the number of records in each section of a file.
    """
    
    def process(self, input_file: str, output_file: Optional[str] = None, error_file: Optional[str] = None) -> ProcessingResult:
        """
        Process a file.
        
        Args:
            input_file: Path to the input file
            output_file: Optional path to the output file
            error_file: Optional path to the error file
            
        Returns:
            A ProcessingResult object
            
        Raises:
            ProcessorError: If the file cannot be processed
        """
        result = ProcessingResult()
        section_counts: Dict[str, int] = {}
        
        try:
            # Create a parser
            parser = Parser.create_parser(self.file_format)
            
            # Process the file
            for record in parser.parse_file(input_file):
                result.total_records += 1
                
                # Count records by section
                section_name = record.section.name
                section_counts[section_name] = section_counts.get(section_name, 0) + 1
                
                # Apply global rules
                for rule in self.global_rules:
                    rule.process_record(record)
                    
                # Count valid records
                if record.is_valid:
                    result.valid_records += 1
                else:
                    result.error_count += len([e for fv in record.field_values.values() for e in fv.errors])
                    result.errors.extend([e for fv in record.field_values.values() for e in fv.errors])
                    
            # Finalize global rules
            for rule in self.global_rules:
                errors = rule.finalize()
                if errors:
                    result.error_count += len(errors)
                    result.errors.extend(errors)
                    
            # Write the counts to the output file if provided
            if output_file:
                with open(output_file, 'w', encoding=self.file_format.encoding) as f:
                    f.write(f"Total records: {result.total_records}\n")
                    f.write(f"Valid records: {result.valid_records}\n")
                    f.write(f"Error count: {result.error_count}\n\n")
                    
                    f.write("Section counts:\n")
                    for section_name, count in section_counts.items():
                        f.write(f"{section_name}: {count}\n")
                        
        except Exception as e:
            raise ProcessorError(f"Error processing file: {str(e)}")
            
        return result
    
    def _process_record(self, record: ParsedRecord, out_file: Optional[TextIO], 
                       error_file_obj: Optional[TextIO], result: ProcessingResult) -> None:
        """
        Process a single record for chunked processing.
        
        Args:
            record: Record to process
            out_file: Output file object (may be None for CounterProcessor)
            error_file_obj: Error file object or None
            result: ProcessingResult object to update
        """
        # Store section counts in the result object's custom data
        if not hasattr(result, 'section_counts'):
            result.section_counts = {}
            
        # Count records by section
        section_name = record.section.name
        result.section_counts[section_name] = result.section_counts.get(section_name, 0) + 1
        
        # Count valid records
        if record.is_valid:
            result.valid_records += 1
        else:
            result.error_count += len([e for fv in record.field_values.values() for e in fv.errors])
            result.errors.extend([e for fv in record.field_values.values() for e in fv.errors])
    
    def process_chunked(self, input_file: str, output_file: Optional[str] = None, error_file: Optional[str] = None,
                       chunk_size: int = 10000, progress_callback: Optional[Callable[[int, int], None]] = None) -> ProcessingResult:
        """
        Process a file in chunks for better memory efficiency with large files.
        
        This method overrides the base implementation to handle the special case of CounterProcessor,
        which doesn't write records to the output file during processing but only at the end.
        
        Args:
            input_file: Path to the input file
            output_file: Optional path to the output file
            error_file: Optional path to the error file
            chunk_size: Number of records to process in each chunk
            progress_callback: Optional callback function that receives (processed_records, total_records)
            
        Returns:
            A ProcessingResult object
            
        Raises:
            ProcessorError: If the file cannot be processed
        """
        # Use the base implementation to process the file in chunks
        result = super().process_chunked(input_file, None, error_file, chunk_size, progress_callback)
        
        # Write the counts to the output file if provided
        if output_file and hasattr(result, 'section_counts'):
            try:
                with open(output_file, 'w', encoding=self.file_format.encoding) as f:
                    f.write(f"Total records: {result.total_records}\n")
                    f.write(f"Valid records: {result.valid_records}\n")
                    f.write(f"Error count: {result.error_count}\n\n")
                    
                    f.write("Section counts:\n")
                    for section_name, count in result.section_counts.items():
                        f.write(f"{section_name}: {count}\n")
            except Exception as e:
                raise ProcessorError(f"Error writing output file: {str(e)}")
                
        return result 