# FlatForge Developer Guide

This guide explains how to use FlatForge programmatically and how to extend it with custom rules and processors.

## Using FlatForge Programmatically

### Validating a File

```python
from flatforge.parsers import ConfigParser
from flatforge.processors import ValidationProcessor

# Parse the configuration
config_parser = ConfigParser.from_file("schema.yaml")
file_format = config_parser.parse()

# Create a processor
processor = ValidationProcessor(file_format)

# Process the file
result = processor.process("data.csv", "valid.csv", "errors.csv")
print(f"Processed {result.total_records} records with {result.error_count} errors.")
print(f"Valid records: {result.valid_records}")
```

### Converting a File

```python
from flatforge.parsers import ConfigParser
from flatforge.processors import ConversionProcessor

# Parse the configurations
input_config_parser = ConfigParser.from_file("input_schema.yaml")
input_format = input_config_parser.parse()

output_config_parser = ConfigParser.from_file("output_schema.yaml")
output_format = output_config_parser.parse()

# Create a processor
processor = ConversionProcessor(input_format, output_format)

# Process the file
result = processor.process("data.csv", "converted.txt", "errors.csv")
print(f"Processed {result.total_records} records with {result.error_count} errors.")
print(f"Valid records: {result.valid_records}")
```

### Counting Records

```python
from flatforge.parsers import ConfigParser
from flatforge.processors import CounterProcessor

# Parse the configuration
config_parser = ConfigParser.from_file("schema.yaml")
file_format = config_parser.parse()

# Create a processor
processor = CounterProcessor(file_format)

# Process the file
result = processor.process("data.csv", "counts.txt")
print(f"Total records: {result.total_records}")
print(f"Valid records: {result.valid_records}")
print(f"Error count: {result.error_count}")
```

## Extending FlatForge

### Creating a Custom Validation Rule

To create a custom validation rule, extend the `ValidationRule` class and implement the `validate` method:

```python
from flatforge.core import ValidationError, FieldValue, ParsedRecord
from flatforge.rules.base import ValidationRule

class CustomValidationRule(ValidationRule):
    """A custom validation rule."""
    
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        """
        Validate a field value.
        
        Args:
            field_value: The field value to validate
            record: The record containing the field value
            
        Raises:
            ValidationError: If validation fails
        """
        value = field_value.value.strip()
        if not value and not self.params.get("required", False):
            return
            
        # Implement your custom validation logic here
        if not value.startswith(self.params.get("prefix", "")):
            raise ValidationError(
                f"Value must start with '{self.params.get('prefix', '')}'",
                field_name=field_value.field.name,
                rule_name=self.name,
                error_code="CUSTOM_VALIDATION",
                section_name=record.section.name,
                record_number=record.record_number,
                field_value=field_value.value
            )
```

### Creating a Custom Transformation Rule

To create a custom transformation rule, extend the `TransformerRule` class and implement the `transform` method:

```python
from flatforge.core import FieldValue, ParsedRecord
from flatforge.rules.base import TransformerRule

class CustomTransformerRule(TransformerRule):
    """A custom transformation rule."""
    
    def transform(self, field_value: FieldValue, record: ParsedRecord) -> str:
        """
        Transform a field value.
        
        Args:
            field_value: The field value to transform
            record: The record containing the field value
            
        Returns:
            The transformed value
        """
        value = field_value.value
        
        # Implement your custom transformation logic here
        prefix = self.params.get("prefix", "")
        suffix = self.params.get("suffix", "")
        
        return f"{prefix}{value}{suffix}"
```

### Creating a Custom Global Rule

To create a custom global rule, extend the `GlobalRule` class and implement the `process_record` and `finalize` methods:

```python
from typing import List

from flatforge.core import ValidationError, ParsedRecord
from flatforge.rules.base import GlobalRule

class CustomGlobalRule(GlobalRule):
    """A custom global rule."""
    
    def __init__(self, name: str, params: dict = None):
        """
        Initialize a custom global rule.
        
        Args:
            name: The name of the rule
            params: Optional parameters for the rule
        """
        super().__init__(name, params)
        self.state = {"values": []}
    
    def process_record(self, record: ParsedRecord) -> None:
        """
        Process a record.
        
        Args:
            record: The record to process
        """
        # Only process records from the specified section
        section_name = self.params.get("section")
        if section_name and record.section.name != section_name:
            return
            
        # Get the field to process
        field_name = self.params.get("field")
        if not field_name:
            return
            
        # Get the field value
        field_value = record.field_values.get(field_name)
        if not field_value:
            return
            
        # Store the value for later processing
        self.state["values"].append(field_value.value)
    
    def finalize(self) -> List[ValidationError]:
        """
        Finalize the rule.
        
        Returns:
            A list of validation errors, if any
        """
        errors = []
        
        # Implement your custom finalization logic here
        expected_count = self.params.get("expected_count")
        if expected_count is not None:
            expected_count = int(expected_count)
            actual_count = len(self.state["values"])
            
            if actual_count != expected_count:
                errors.append(ValidationError(
                    f"Value count mismatch: expected {expected_count}, got {actual_count}",
                    rule_name=self.name,
                    error_code="CUSTOM_GLOBAL"
                ))
                
        return errors
```

### Registering Custom Rules

To make your custom rules available to FlatForge, register them in the rule registries:

```python
from flatforge.rules import VALIDATION_RULES, TRANSFORMER_RULES, GLOBAL_RULES

# Register custom validation rule
VALIDATION_RULES["custom_validation"] = CustomValidationRule

# Register custom transformation rule
TRANSFORMER_RULES["custom_transformer"] = CustomTransformerRule

# Register custom global rule
GLOBAL_RULES["custom_global"] = CustomGlobalRule
```

### Creating a Custom Processor

To create a custom processor, extend the `Processor` class and implement the `process` method:

```python
from typing import Optional

from flatforge.core import FileFormat, ProcessingResult, ProcessorError
from flatforge.parsers import Parser
from flatforge.processors.base import Processor

class CustomProcessor(Processor):
    """A custom processor."""
    
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
            
            # Open the output file
            with open(output_file, 'w', encoding=self.file_format.encoding) as out_file:
                # Process the file
                for record in parser.parse_file(input_file):
                    result.total_records += 1
                    
                    # Apply global rules
                    for rule in self.global_rules:
                        rule.process_record(record)
                        
                    # Implement your custom processing logic here
                    if record.is_valid:
                        result.valid_records += 1
                        # Write the record to the output file
                        out_file.write(f"Custom: {record.raw_data}\n")
                    else:
                        result.error_count += len([e for fv in record.field_values.values() for e in fv.errors])
                        result.errors.extend([e for fv in record.field_values.values() for e in fv.errors])
                        
                # Finalize global rules
                for rule in self.global_rules:
                    errors = rule.finalize()
                    if errors:
                        result.error_count += len(errors)
                        result.errors.extend(errors)
                        
        except Exception as e:
            raise ProcessorError(f"Error processing file: {str(e)}")
            
        return result
```

## Architecture

FlatForge is designed with a modular architecture that separates concerns and allows for easy extension.

### Core Components

- **Core**: Contains the core data models and exceptions
- **Parsers**: Contains the parsers for configuration files and flat files
- **Rules**: Contains the rules for validating and transforming field values
- **Processors**: Contains the processors for processing flat files
- **CLI**: Contains the command line interface

### Design Patterns

FlatForge uses several design patterns:

- **Factory Pattern**: Used to create parsers and rules based on configuration
- **Strategy Pattern**: Used to implement different validation and transformation strategies
- **Composite Pattern**: Used to compose rules and apply them to field values
- **Observer Pattern**: Used to notify global rules of record processing
- **Template Method Pattern**: Used to define the structure of processors and parsers

### Workflow

1. Parse the configuration file to create a `FileFormat` object
2. Create a processor for the file format
3. Process the input file, applying rules to each field value
4. Write valid records to the output file and invalid records to the error file
5. Return a `ProcessingResult` object with the results of the processing 