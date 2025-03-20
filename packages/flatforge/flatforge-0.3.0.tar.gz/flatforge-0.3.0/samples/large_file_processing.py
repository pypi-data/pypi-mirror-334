#!/usr/bin/env python
"""
Example script demonstrating how to use FlatForge's chunked processing for large files.

This script shows how to:
1. Process a large file in chunks
2. Display progress during processing
3. Handle memory efficiently

Usage:
    python large_file_processing.py
"""
import os
import sys
import time
from tqdm import tqdm

# Add the parent directory to the path so we can import flatforge
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flatforge.core import FileFormat
from flatforge.parsers import ConfigParser
from flatforge.processors import ValidationProcessor, ConversionProcessor, CounterProcessor


def validate_large_file():
    """Example of validating a large file using chunked processing."""
    print("\n=== Validating a Large File ===")
    
    # Load the configuration
    config_parser = ConfigParser.from_file("samples/schemas/fixed_length.yaml")
    file_format = config_parser.parse()
    
    # Create a processor
    processor = ValidationProcessor(file_format)
    
    # Set up a progress bar
    with tqdm(total=100, desc="Validating") as progress_bar:
        def update_progress(processed, total):
            if total > 0:
                progress_bar.update(int(100 * processed / total) - progress_bar.n)
        
        # Process the file in chunks
        start_time = time.time()
        result = processor.process_chunked(
            input_file="samples/data/fixed_length.txt",
            output_file="samples/output/valid_chunked.txt",
            error_file="samples/output/errors_chunked.txt",
            chunk_size=1,  # Small chunk size for demonstration
            progress_callback=update_progress
        )
        elapsed_time = time.time() - start_time
    
    # Print the results
    print(f"Processed {result.total_records} records in {elapsed_time:.2f} seconds")
    print(f"Valid records: {result.valid_records}")
    print(f"Error count: {result.error_count}")


def convert_large_file():
    """Example of converting a large file using chunked processing."""
    print("\n=== Converting a Large File ===")
    
    # Load the configurations
    input_config_parser = ConfigParser.from_file("samples/schemas/fixed_length.yaml")
    input_format = input_config_parser.parse()
    
    output_config_parser = ConfigParser.from_file("samples/schemas/delimited.yaml")
    output_format = output_config_parser.parse()
    
    # Create a processor
    processor = ConversionProcessor(input_format, output_format)
    
    # Set up a progress bar
    with tqdm(total=100, desc="Converting") as progress_bar:
        def update_progress(processed, total):
            if total > 0:
                progress_bar.update(int(100 * processed / total) - progress_bar.n)
        
        # Process the file in chunks
        start_time = time.time()
        result = processor.process_chunked(
            input_file="samples/data/fixed_length.txt",
            output_file="samples/output/converted_chunked.csv",
            error_file="samples/output/conversion_errors_chunked.txt",
            chunk_size=1,  # Small chunk size for demonstration
            progress_callback=update_progress
        )
        elapsed_time = time.time() - start_time
    
    # Print the results
    print(f"Processed {result.total_records} records in {elapsed_time:.2f} seconds")
    print(f"Valid records: {result.valid_records}")
    print(f"Error count: {result.error_count}")


def count_large_file():
    """Example of counting records in a large file using chunked processing."""
    print("\n=== Counting Records in a Large File ===")
    
    # Load the configuration
    config_parser = ConfigParser.from_file("samples/schemas/fixed_length.yaml")
    file_format = config_parser.parse()
    
    # Create a processor
    processor = CounterProcessor(file_format)
    
    # Set up a progress bar
    with tqdm(total=100, desc="Counting") as progress_bar:
        def update_progress(processed, total):
            if total > 0:
                progress_bar.update(int(100 * processed / total) - progress_bar.n)
        
        # Process the file in chunks
        start_time = time.time()
        result = processor.process_chunked(
            input_file="samples/data/fixed_length.txt",
            output_file="samples/output/counts_chunked.txt",
            chunk_size=1,  # Small chunk size for demonstration
            progress_callback=update_progress
        )
        elapsed_time = time.time() - start_time
    
    # Print the results
    print(f"Counted {result.total_records} records in {elapsed_time:.2f} seconds")


def compare_processing_methods():
    """Compare standard processing vs. chunked processing."""
    print("\n=== Comparing Processing Methods ===")
    
    # Load the configuration
    config_parser = ConfigParser.from_file("samples/schemas/fixed_length.yaml")
    file_format = config_parser.parse()
    
    # Create a processor
    processor = ValidationProcessor(file_format)
    
    # Standard processing
    print("Standard processing:")
    start_time = time.time()
    result_standard = processor.process(
        input_file="samples/data/fixed_length.txt",
        output_file="samples/output/valid_standard.txt",
        error_file="samples/output/errors_standard.txt"
    )
    elapsed_time_standard = time.time() - start_time
    print(f"Processed {result_standard.total_records} records in {elapsed_time_standard:.2f} seconds")
    
    # Chunked processing
    print("\nChunked processing:")
    with tqdm(total=100, desc="Processing") as progress_bar:
        def update_progress(processed, total):
            if total > 0:
                progress_bar.update(int(100 * processed / total) - progress_bar.n)
        
        start_time = time.time()
        result_chunked = processor.process_chunked(
            input_file="samples/data/fixed_length.txt",
            output_file="samples/output/valid_chunked.txt",
            error_file="samples/output/errors_chunked.txt",
            chunk_size=1,  # Small chunk size for demonstration
            progress_callback=update_progress
        )
        elapsed_time_chunked = time.time() - start_time
    print(f"Processed {result_chunked.total_records} records in {elapsed_time_chunked:.2f} seconds")
    
    # Compare results
    print("\nComparison:")
    print(f"Standard processing time: {elapsed_time_standard:.2f} seconds")
    print(f"Chunked processing time: {elapsed_time_chunked:.2f} seconds")
    print(f"Difference: {(elapsed_time_chunked - elapsed_time_standard):.2f} seconds")
    print(f"Note: For small files, chunked processing may be slower due to overhead.")
    print(f"      For large files, chunked processing provides better memory efficiency.")


def main():
    """Run all examples."""
    # Create output directory if it doesn't exist
    os.makedirs("samples/output", exist_ok=True)
    
    # Run examples
    validate_large_file()
    convert_large_file()
    count_large_file()
    compare_processing_methods()


if __name__ == "__main__":
    main() 