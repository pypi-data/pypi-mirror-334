# FlatForge Architecture

This document describes the architecture of FlatForge, a library for validating and transforming flat files.

## Overview

FlatForge is designed with a modular architecture that separates concerns and allows for easy extension. The library is composed of several modules, each with a specific responsibility:

- **Core**: Contains the core data models and exceptions
- **Parsers**: Contains the parsers for configuration files and flat files
- **Rules**: Contains the rules for validating and transforming field values
- **Processors**: Contains the processors for processing flat files
- **CLI**: Contains the command line interface

## Component Diagram

```
+----------------+     +----------------+     +----------------+
|      CLI       |---->|   Processors   |---->|    Parsers     |
+----------------+     +----------------+     +----------------+
                              |                      |
                              v                      v
                       +----------------+     +----------------+
                       |     Rules      |---->|     Core       |
                       +----------------+     +----------------+
```

## Module Descriptions

### Core

The Core module contains the fundamental data models and exceptions used throughout the library. It defines the structure of flat files, sections, records, and fields, as well as the exceptions that can be thrown during processing.

Key components:
- `FileFormat`: Represents the format of a flat file
- `Section`: Represents a section in a flat file
- `Record`: Represents a record format in a flat file
- `Field`: Represents a field in a flat file record
- `FieldValue`: Represents a field value in a parsed record
- `ParsedRecord`: Represents a parsed record from a flat file
- `ProcessingResult`: Represents the result of processing a flat file
- `ValidationError`: Exception raised for validation errors

### Parsers

The Parsers module contains the parsers for configuration files and flat files. It is responsible for parsing configuration files into `FileFormat` objects and parsing flat files into `ParsedRecord` objects.

Key components:
- `ConfigParser`: Abstract base class for config parsers
- `JsonConfigParser`: Config parser for JSON configuration files
- `YamlConfigParser`: Config parser for YAML configuration files
- `Parser`: Abstract base class for file parsers
- `FixedLengthParser`: Parser for fixed-length flat files
- `DelimitedParser`: Parser for delimited flat files

### Rules

The Rules module contains the rules for validating and transforming field values. It defines the abstract base classes for rules and provides concrete implementations of validation and transformation rules.

Key components:
- `Rule`: Abstract base class for all rules
- `ValidationRule`: Abstract base class for validation rules
- `TransformerRule`: Abstract base class for transformer rules
- `GlobalRule`: Abstract base class for global rules
- Concrete validation rules: `RequiredRule`, `NumericRule`, `StringLengthRule`, etc.
- Concrete transformation rules: `TrimRule`, `CaseRule`, `PadRule`, etc.
- Concrete global rules: `CountRule`, `SumRule`, `ChecksumRule`, etc.

### Processors

The Processors module contains the processors for processing flat files. It defines the abstract base class for processors and provides concrete implementations of processors for different use cases.

Key components:
- `Processor`: Abstract base class for processors
- `ValidationProcessor`: Processor that validates a file against a schema
- `ConversionProcessor`: Processor that converts a file from one format to another
- `CounterProcessor`: Processor that counts records in a file

### CLI

The CLI module contains the command line interface for FlatForge. It provides commands for validating, converting, and counting records in flat files.

Key components:
- `main`: Main CLI entry point
- `validate`: Command for validating a file against a schema
- `convert`: Command for converting a file from one format to another
- `count`: Command for counting records in a file

## Design Patterns

FlatForge uses several design patterns to achieve its goals:

### Factory Pattern

The Factory Pattern is used to create parsers and rules based on configuration. For example, the `Parser.create_parser` method creates a parser based on the file format type:

```python
@staticmethod
def create_parser(file_format: FileFormat) -> 'Parser':
    if file_format.type == FileType.FIXED_LENGTH:
        return FixedLengthParser(file_format)
    elif file_format.type == FileType.DELIMITED:
        return DelimitedParser(file_format)
    else:
        raise ParserError(f"Unsupported file type: {file_format.type}")
```

### Strategy Pattern

The Strategy Pattern is used to implement different validation and transformation strategies. For example, the `ValidationRule` and `TransformerRule` classes define the interface for validation and transformation strategies, and concrete implementations provide specific strategies:

```python
class ValidationRule(Rule):
    @abstractmethod
    def validate(self, field_value: FieldValue, record: ParsedRecord) -> None:
        pass
```

### Composite Pattern

The Composite Pattern is used to compose rules and apply them to field values. For example, a field can have multiple rules, and each rule is applied in sequence:

```python
def _apply_rules(self, field_value: FieldValue, record: ParsedRecord) -> None:
    rules = self._create_rules(field_value.field)
    
    for rule in rules:
        rule.apply(field_value, record)
```

### Observer Pattern

The Observer Pattern is used to notify global rules of record processing. For example, global rules observe the processing of records and update their state accordingly:

```python
def process(self, input_file: str, output_file: str, error_file: Optional[str] = None) -> ProcessingResult:
    # ...
    for record in parser.parse_file(input_file):
        # ...
        for rule in self.global_rules:
            rule.process_record(record)
        # ...
```

### Template Method Pattern

The Template Method Pattern is used to define the structure of processors and parsers. For example, the `Processor` class defines the structure of processors, and concrete implementations provide specific behavior:

```python
class Processor(ABC):
    def __init__(self, file_format: FileFormat):
        self.file_format = file_format
        self.global_rules: List[GlobalRule] = []
        
        # Create global rules
        self._create_global_rules()
    
    def _create_global_rules(self) -> None:
        # ...
    
    @abstractmethod
    def process(self, input_file: str, output_file: str, error_file: Optional[str] = None) -> ProcessingResult:
        pass
```

## Workflow

The typical workflow for using FlatForge is as follows:

1. Parse the configuration file to create a `FileFormat` object
2. Create a processor for the file format
3. Process the input file, applying rules to each field value
4. Write valid records to the output file and invalid records to the error file
5. Return a `ProcessingResult` object with the results of the processing

This workflow is encapsulated in the `process` method of the `Processor` class and its concrete implementations.

## Extension Points

FlatForge is designed to be extensible. The main extension points are:

- **Validation Rules**: Create custom validation rules by extending the `ValidationRule` class
- **Transformation Rules**: Create custom transformation rules by extending the `TransformerRule` class
- **Global Rules**: Create custom global rules by extending the `GlobalRule` class
- **Processors**: Create custom processors by extending the `Processor` class
- **Parsers**: Create custom parsers by extending the `Parser` class
- **Config Parsers**: Create custom config parsers by extending the `ConfigParser` class

By extending these classes, you can add custom functionality to FlatForge without modifying the core library. 