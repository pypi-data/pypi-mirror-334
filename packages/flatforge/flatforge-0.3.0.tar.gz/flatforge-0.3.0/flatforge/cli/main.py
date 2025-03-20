"""
CLI main module for FlatForge.

This module contains the main CLI entry point for FlatForge.
"""
import sys
from typing import Optional

import click

from flatforge.core import ConfigError, ProcessorError
from flatforge.parsers import ConfigParser
from flatforge.processors import ValidationProcessor, ConversionProcessor, CounterProcessor


@click.group()
@click.version_option()
def main():
    """FlatForge - A library for validating and transforming flat files."""
    pass


@main.command()
@click.option('--config', '-c', required=True, help='Path to the configuration file.')
@click.option('--input', '-i', required=True, help='Path to the input file.')
@click.option('--output', '-o', required=True, help='Path to the output file.')
@click.option('--errors', '-e', help='Path to the error file.')
def validate(config: str, input: str, output: str, errors: Optional[str] = None):
    """Validate a file against a schema."""
    try:
        # Parse the configuration
        config_parser = ConfigParser.from_file(config)
        file_format = config_parser.parse()
        
        # Create a processor
        processor = ValidationProcessor(file_format)
        
        # Process the file
        result = processor.process(input, output, errors)
        
        # Print the result
        click.echo(f"Processed {result.total_records} records with {result.error_count} errors.")
        click.echo(f"Valid records: {result.valid_records}")
        
        # Return a non-zero exit code if there were errors
        if result.error_count > 0:
            sys.exit(1)
            
    except (ConfigError, ProcessorError) as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option('--input-config', '-ic', required=True, help='Path to the input configuration file.')
@click.option('--output-config', '-oc', required=True, help='Path to the output configuration file.')
@click.option('--input', '-i', required=True, help='Path to the input file.')
@click.option('--output', '-o', required=True, help='Path to the output file.')
@click.option('--errors', '-e', help='Path to the error file.')
def convert(input_config: str, output_config: str, input: str, output: str, errors: Optional[str] = None):
    """Convert a file from one format to another."""
    try:
        # Parse the configurations
        input_config_parser = ConfigParser.from_file(input_config)
        input_format = input_config_parser.parse()
        
        output_config_parser = ConfigParser.from_file(output_config)
        output_format = output_config_parser.parse()
        
        # Create a processor
        processor = ConversionProcessor(input_format, output_format)
        
        # Process the file
        result = processor.process(input, output, errors)
        
        # Print the result
        click.echo(f"Processed {result.total_records} records with {result.error_count} errors.")
        click.echo(f"Valid records: {result.valid_records}")
        
        # Return a non-zero exit code if there were errors
        if result.error_count > 0:
            sys.exit(1)
            
    except (ConfigError, ProcessorError) as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option('--config', '-c', required=True, help='Path to the configuration file.')
@click.option('--input', '-i', required=True, help='Path to the input file.')
@click.option('--output', '-o', help='Path to the output file.')
def count(config: str, input: str, output: Optional[str] = None):
    """Count records in a file."""
    try:
        # Parse the configuration
        config_parser = ConfigParser.from_file(config)
        file_format = config_parser.parse()
        
        # Create a processor
        processor = CounterProcessor(file_format)
        
        # Process the file
        result = processor.process(input, output)
        
        # Print the result
        click.echo(f"Total records: {result.total_records}")
        click.echo(f"Valid records: {result.valid_records}")
        click.echo(f"Error count: {result.error_count}")
        
    except (ConfigError, ProcessorError) as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main() 