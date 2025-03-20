# FlatForge User Guide

This guide explains how to use FlatForge to validate and transform flat files.

## Installation

Install FlatForge using pip:

```bash
pip install flatforge
```

## Command Line Interface

FlatForge provides a command-line interface for validating, converting, and counting records in flat files.

### Validating a file

```bash
flatforge validate --config schema.yaml --input data.csv --output valid.csv --errors errors.csv
```

### Converting a file

```bash
flatforge convert --input-config input_schema.yaml --output-config output_schema.yaml --input data.csv --output converted.txt --errors errors.csv
```

### Counting records

```bash
flatforge count --config schema.yaml --input data.csv --output counts.txt
```

For more examples, see the [CLI examples](cli_examples.md) document.

## Processing Large Files

FlatForge supports efficient processing of large files (>1GB) through chunked processing. This feature allows you to process files in configurable chunks, which helps manage memory usage and provides progress reporting.

### Chunked Processing via CLI

All CLI commands support chunked processing with the following options:

- `--chunk-size`: Number of records to process in each chunk (default is 0, which means no chunking)
- `--show-progress`: Display a progress bar during processing

Example:

```bash
flatforge validate --config schema.yaml --input large_data.csv --output valid.csv --errors errors.csv --chunk-size 10000 --show-progress
```

### Chunked Processing via API

For programmatic use, all processor classes support chunked processing through the `process_chunked` method:

```python
from flatforge.file_format import FileFormat
from flatforge.processor import ValidationProcessor

# Load the configuration
file_format = FileFormat.from_yaml("schema.yaml")

# Create a processor
processor = ValidationProcessor(file_format)

# Define a progress callback function (optional)
def update_progress(processed_records, total_records):
    percent = int(100 * processed_records / total_records) if total_records > 0 else 0
    print(f"Progress: {percent}% ({processed_records}/{total_records})")

# Process the file in chunks
result = processor.process_chunked(
    input_file="large_data.csv",
    output_file="valid.csv",
    error_file="errors.csv",
    chunk_size=10000,  # Process 10,000 records at a time
    progress_callback=update_progress
)

print(f"Total records: {result.total_records}")
print(f"Valid records: {result.valid_records}")
print(f"Error count: {result.error_count}")
```

### Memory Considerations

When processing large files, consider the following:

1. **Chunk Size**: Choose a chunk size that balances memory usage and performance. Smaller chunks use less memory but may be slower due to increased I/O operations.

2. **Global Rules**: Be aware that global rules still accumulate data across all records. If you have complex global rules that store large amounts of data, consider optimizing them for memory efficiency.

3. **Error Handling**: When processing large files, errors are still collected in memory. If you expect many errors, consider processing the file in smaller chunks or implementing custom error handling.

## Configuration Files

FlatForge uses YAML or JSON configuration files to define the structure of flat files and the rules to apply to each field.

### File Format

A configuration file defines a file format with the following properties:

- `name`: The name of the file format
- `type`: The type of file (`fixed_length` or `delimited`)
- `sections`: A list of sections in the file
- `delimiter`: The delimiter character (for delimited files)
- `quote_char`: The quote character (for delimited files)
- `escape_char`: The escape character (for delimited files)
- `newline`: The newline character(s)
- `encoding`: The file encoding
- `skip_blank_lines`: Whether to skip blank lines
- `exit_on_first_error`: Whether to exit on the first error
- `description`: Optional description of the file format

### Sections

A section defines a part of the file with the following properties:

- `name`: The name of the section
- `type`: The type of section (`header`, `body`, `footer`, or `custom`)
- `record`: The record format for this section
- `min_records`: Minimum number of records in this section
- `max_records`: Maximum number of records in this section
- `identifier`: Optional identifier to recognize this section
- `description`: Optional description of the section

#### Section Identification

FlatForge supports two methods for identifying sections in a file:

1. **Using Record Type Identifiers**: You can specify an `identifier` for each section, which is used to determine which section a record belongs to. The identifier consists of a field name and an expected value.

   ```yaml
   identifier:
     field: record_type
     value: "H"  # For header section
   ```

2. **Using Positional Logic**: If no identifiers are provided, FlatForge will use positional logic to determine which section a record belongs to:
   - For 2-section files (header + body): The header is assumed to be 1 record, and the body is everything else.
   - For 3-section files (header + body + footer): The header is assumed to be 1 record, the footer is the last record, and the body is everything in between.

This allows you to process files that don't have explicit record type indicators.

### Records

A record defines the format of a record in a section with the following properties:

- `name`: The name of the record format
- `fields`: A list of fields in the record
- `description`: Optional description of the record

### Fields

A field defines a field in a record with the following properties:

- `name`: The name of the field
- `position`: The position of the field in the record (0-based)
- `length`: The length of the field (for fixed-length files)
- `rules`: A list of rules to apply to this field
- `description`: Optional description of the field

### Rules

A rule defines a validation or transformation to apply to a field with the following properties:

- `type`: The type of rule
- `name`: Optional name of the rule (defaults to the type)
- `params`: Optional parameters for the rule

### Global Rules

- `count`: Counts the number of records in a section
- `sum`: Sums the values of a field across all records
- `checksum`: Calculates a checksum of a field across all records
- `uniqueness`: Validates that a field or combination of fields has unique values across all records

For detailed information about global rules, see [Global Rules](global_rules.md).

## Example Configuration

Here's an example configuration for a fixed-length file format:

```yaml
name: Employee File Format
type: fixed_length
description: A fixed-length file format for employee data
newline: "\n"
encoding: utf-8
skip_blank_lines: true
exit_on_first_error: false

sections:
  - name: header
    type: header
    min_records: 1
    max_records: 1
    description: Header section containing batch information
    record:
      name: header_record
      description: Header record format
      fields:
        - name: record_type
          position: 0
          length: 1
          description: Record type indicator (H for header)
          rules:
            - type: choice
              params:
                choices: ["H"]
        - name: batch_reference
          position: 1
          length: 10
          description: Batch reference number
          rules:
            - type: required
            - type: string_length
              params:
                min_length: 1
                max_length: 10
        - name: batch_timestamp
          position: 2
          length: 14
          description: Batch timestamp (YYYYMMDDHHmmss)
          rules:
            - type: required
            - type: date
              params:
                format: "%Y%m%d%H%M%S"

  - name: body
    type: body
    min_records: 0
    description: Body section containing employee records
    identifier:
      field: record_type
      value: "D"
    record:
      name: employee_record
      description: Employee record format
      fields:
        - name: record_type
          position: 0
          length: 1
          description: Record type indicator (D for data)
          rules:
            - type: choice
              params:
                choices: ["D"]
        - name: employee_id
          position: 1
          length: 10
          description: Employee ID
          rules:
            - type: required
            - type: numeric
        - name: employee_name
          position: 2
          length: 35
          description: Employee name
          rules:
            - type: required
            - type: string_length
              params:
                max_length: 35
        - name: date_of_birth
          position: 3
          length: 8
          description: Date of birth (YYYYMMDD)
          rules:
            - type: date
              params:
                format: "%Y%m%d"
        - name: country_code
          position: 4
          length: 2
          description: Country code (2 letters)
          rules:
            - type: string_length
              params:
                min_length: 2
                max_length: 2
            - type: case
              params:
                type: upper
        - name: salary
          position: 5
          length: 10
          description: Salary (with 2 decimal places)
          rules:
            - type: numeric
              params:
                min_value: 0
                decimal_precision: 2
            - type: trim
        - name: manager_id
          position: 6
          length: 10
          description: Manager ID
          rules:
            - type: numeric
        - name: manager_name
          position: 7
          length: 35
          description: Manager name
          rules:
            - type: string_length
              params:
                max_length: 35

  - name: footer
    type: footer
    min_records: 1
    max_records: 1
    description: Footer section containing summary information
    identifier:
      field: record_type
      value: "F"
    record:
      name: footer_record
      description: Footer record format
      fields:
        - name: record_type
          position: 0
          length: 1
          description: Record type indicator (F for footer)
          rules:
            - type: choice
              params:
                choices: ["F"]
        - name: total_salary
          position: 1
          length: 15
          description: Sum of all employee salaries
          rules:
            - type: required
            - type: numeric
              params:
                min_value: 0
                decimal_precision: 2
        - name: employee_count
          position: 2
          length: 10
          description: Count of all employees in the body section
          rules:
            - type: required
            - type: numeric
              params:
                min_value: 0

global_rules:
  - type: sum
    name: salary_sum
    params:
      section: body
      field: salary
      sum_field: footer.total_salary
  - type: count
    name: employee_count
    params:
      section: body
      count_field: footer.employee_count
```

## Available Rules

FlatForge provides a wide range of rules for validating and transforming data. Here's a brief overview:

### Validation Rules

- `required`: Validates that a field is not empty
- `numeric`: Validates that a field is numeric
- `string_length`: Validates the length of a string field
- `regex`: Validates a field against a regular expression
- `date`: Validates a date field
- `choice`: Validates that a field value is one of a set of choices

### Transformation Rules

- `trim`: Trims whitespace from a field value
- `case`: Changes the case of a field value
- `pad`: Pads a field value to a specified length
- `date_format`: Formats a date field
- `substring`: Extracts a substring from a field value
- `replace`: Replaces text in a field value

### Global Rules

- `count`: Counts the number of records in a section
- `sum`: Sums the values of a field across all records
- `checksum`: Calculates a checksum of a field across all records
- `uniqueness`: Validates that a field or combination of fields has unique values across all records

For detailed information about all rules and their parameters, see the [Rules Guide](rules_guide.md). 