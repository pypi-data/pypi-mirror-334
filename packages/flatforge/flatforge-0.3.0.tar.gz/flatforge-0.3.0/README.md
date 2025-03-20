# FlatForge

A generic, modular, and extensible library to validate flat files of fixed length or delimited format.

## Features

- Validate flat files against predefined schemas
- Transform flat files from one format to another
- Support for fixed-length and delimited file formats
- Extensible rule system for validation and transformation
- Global rules for cross-record validation
- CLI interface for easy integration into workflows
- Support for multi-section files (header, body, footer)
- Comprehensive error reporting
- Efficient processing of large files (>1GB) with chunked processing and progress reporting

## Installation

```bash
pip install flatforge
```

## Quick Start

### Command Line Interface

```bash
# Validate a file against a schema
flatforge validate --config schema.yaml --input data.csv --output valid.csv --errors errors.csv

# Convert a file from one format to another
flatforge convert --config mapping.yaml --input data.csv --output converted.txt

# Process a large file with chunked processing and progress reporting
flatforge validate --config schema.yaml --input large_data.csv --output valid.csv --errors errors.csv --chunk-size 10000 --show-progress
```

### Programmatic Usage

```python
from flatforge.processors import ValidationProcessor
from flatforge.parsers import ConfigParser

# Parse the configuration
config_parser = ConfigParser.from_file("schema.yaml")
config = config_parser.parse()

# Create a processor
processor = ValidationProcessor(config)

# Process the file
result = processor.process("data.csv", "valid.csv", "errors.csv")
print(f"Processed {result.total_records} records with {result.error_count} errors")

# Process a large file in chunks with progress reporting
def update_progress(processed, total):
    print(f"Progress: {processed}/{total} records ({int(100 * processed / total)}%)")

result = processor.process_chunked(
    "large_data.csv", 
    "valid.csv", 
    "errors.csv", 
    chunk_size=10000, 
    progress_callback=update_progress
)
print(f"Processed {result.total_records} records with {result.error_count} errors")
```

## Documentation

For detailed documentation, please refer to:

- [User Guide](https://github.com/akram0zaki/flatforge/blob/master/docs/user_guide/README.md): How to use FlatForge
- [Developer Guide](https://github.com/akram0zaki/flatforge/blob/master/docs/developer_guide/README.md): How to extend FlatForge
- [Architecture](https://github.com/akram0zaki/flatforge/blob/master/docs/architecture/README.md): Design and architecture of FlatForge
- [Testing Guide](https://github.com/akram0zaki/flatforge/blob/master/docs/testing/README.md): How to test FlatForge and write new tests
- [Rules Guide](https://github.com/akram0zaki/flatforge/blob/master/docs/user_guide/rules_guide.md): Comprehensive guide to all validation rules

## Changelog

See the [CHANGELOG.md](https://github.com/akram0zaki/flatforge/blob/master/CHANGELOG.md) file for details on the changes made in each release.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](https://github.com/akram0zaki/flatforge/blob/master/CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## Author

- Akram Zaki (azpythonprojects@gmail.com)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/akram0zaki/flatforge/blob/master/LICENSE) file for details. 