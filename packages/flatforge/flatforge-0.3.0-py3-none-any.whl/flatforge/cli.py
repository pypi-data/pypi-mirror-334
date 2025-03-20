import click
import sys
import yaml
from tqdm import tqdm
from flatforge.core import FileFormat
from flatforge.processors import ValidationProcessor, ConversionProcessor, CounterProcessor

@click.group()
def cli():
    """FlatForge - A tool for working with flat files."""
    pass

@cli.command()
@click.option('--config', required=True, help='Path to the configuration file')
@click.option('--input', required=True, help='Path to the input file')
@click.option('--output', required=False, help='Path to the output file')
@click.option('--errors', required=False, help='Path to the error file')
@click.option('--chunk-size', required=False, type=int, default=0, 
              help='Process file in chunks of this size (for large files). Default is 0 (no chunking).')
@click.option('--show-progress', is_flag=True, help='Show progress bar when processing large files')
def validate(config, input, output, errors, chunk_size, show_progress):
    """Validate a file against a schema."""
    try:
        # Load the configuration
        file_format = FileFormat.from_yaml(config)
        
        # Create a processor
        processor = ValidationProcessor(file_format)
        
        # Process the file
        if chunk_size > 0:
            # Use chunked processing for large files
            with tqdm(total=100, disable=not show_progress) as progress_bar:
                def update_progress(processed, total):
                    if total > 0:
                        progress_bar.update(int(100 * processed / total) - progress_bar.n)
                    
                result = processor.process_chunked(input, output, errors, chunk_size, update_progress)
        else:
            # Use standard processing
            result = processor.process(input, output, errors)
            
        # Print the results
        click.echo(f"Total records: {result.total_records}")
        click.echo(f"Valid records: {result.valid_records}")
        click.echo(f"Error count: {result.error_count}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--input-config', required=True, help='Path to the input configuration file')
@click.option('--output-config', required=True, help='Path to the output configuration file')
@click.option('--mapping', required=False, help='Path to the mapping configuration file')
@click.option('--input', required=True, help='Path to the input file')
@click.option('--output', required=True, help='Path to the output file')
@click.option('--errors', required=False, help='Path to the error file')
@click.option('--chunk-size', required=False, type=int, default=0, 
              help='Process file in chunks of this size (for large files). Default is 0 (no chunking).')
@click.option('--show-progress', is_flag=True, help='Show progress bar when processing large files')
def convert(input_config, output_config, mapping, input, output, errors, chunk_size, show_progress):
    """Convert a file from one format to another."""
    try:
        # Load the configurations
        input_format = FileFormat.from_yaml(input_config)
        output_format = FileFormat.from_yaml(output_config)
        
        # Load the mapping if provided
        mapping_config = None
        if mapping:
            with open(mapping, 'r') as f:
                mapping_config = yaml.safe_load(f)
                
        # Create a processor
        processor = ConversionProcessor(input_format, output_format, mapping_config)
        
        # Process the file
        if chunk_size > 0:
            # Use chunked processing for large files
            with tqdm(total=100, disable=not show_progress) as progress_bar:
                def update_progress(processed, total):
                    if total > 0:
                        progress_bar.update(int(100 * processed / total) - progress_bar.n)
                    
                result = processor.process_chunked(input, output, errors, chunk_size, update_progress)
        else:
            # Use standard processing
            result = processor.process(input, output, errors)
            
        # Print the results
        click.echo(f"Total records: {result.total_records}")
        click.echo(f"Valid records: {result.valid_records}")
        click.echo(f"Error count: {result.error_count}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--config', required=True, help='Path to the configuration file')
@click.option('--input', required=True, help='Path to the input file')
@click.option('--output', required=False, help='Path to the output file')
@click.option('--chunk-size', required=False, type=int, default=0, 
              help='Process file in chunks of this size (for large files). Default is 0 (no chunking).')
@click.option('--show-progress', is_flag=True, help='Show progress bar when processing large files')
def count(config, input, output, chunk_size, show_progress):
    """Count records in a file."""
    try:
        # Load the configuration
        file_format = FileFormat.from_yaml(config)
        
        # Create a processor
        processor = CounterProcessor(file_format)
        
        # Process the file
        if chunk_size > 0:
            # Use chunked processing for large files
            with tqdm(total=100, disable=not show_progress) as progress_bar:
                def update_progress(processed, total):
                    if total > 0:
                        progress_bar.update(int(100 * processed / total) - progress_bar.n)
                    
                result = processor.process_chunked(input, output, None, chunk_size, update_progress)
        else:
            # Use standard processing
            result = processor.process(input, output)
            
        # Print the results
        click.echo(f"Total records: {result.total_records}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1) 