# FlatForge Rules Guide

This guide provides detailed information about all the rules available in FlatForge, including their parameters and usage examples.

## Field-Level Rules

Field-level rules are applied to individual fields in a record. They can be used for validation or transformation of field values.

### Validation Rules

#### `required`

Validates that a field is not empty.

**Parameters:**
- None

**Example:**
```yaml
rules:
  - type: required
```

#### `numeric`

Validates that a field contains a numeric value.

**Parameters:**
- `min_value` (optional): Minimum allowed value
- `max_value` (optional): Maximum allowed value
- `decimal_precision` (optional): Number of decimal places
- `allow_negative` (optional): Whether to allow negative values (default: true)

**Example:**
```yaml
rules:
  - type: numeric
    params:
      min_value: 0
      max_value: 1000
      decimal_precision: 2
      allow_negative: false
```

#### `string_length`

Validates the length of a string field.

**Parameters:**
- `min_length` (optional): Minimum allowed length
- `max_length` (optional): Maximum allowed length
- `exact_length` (optional): Exact required length

**Example:**
```yaml
rules:
  - type: string_length
    params:
      min_length: 1
      max_length: 10
```

#### `regex`

Validates a field against a regular expression.

**Parameters:**
- `pattern`: Regular expression pattern
- `case_sensitive` (optional): Whether the match is case-sensitive (default: true)

**Example:**
```yaml
rules:
  - type: regex
    params:
      pattern: "^[A-Z]{2}\\d{4}$"
      case_sensitive: true
```

#### `date`

Validates that a field contains a valid date.

**Parameters:**
- `format`: Date format string (using Python's strftime format)
- `min_date` (optional): Minimum allowed date (in the same format)
- `max_date` (optional): Maximum allowed date (in the same format)

**Example:**
```yaml
rules:
  - type: date
    params:
      format: "%Y%m%d"
      min_date: "20000101"
      max_date: "20301231"
```

#### `choice`

Validates that a field value is one of a set of choices.

**Parameters:**
- `choices`: List of allowed values
- `case_sensitive` (optional): Whether the comparison is case-sensitive (default: true)

**Example:**
```yaml
rules:
  - type: choice
    params:
      choices: ["A", "B", "C"]
      case_sensitive: false
```

### Transformation Rules

#### `trim`

Trims whitespace from a field value.

**Parameters:**
- `side` (optional): Which side to trim ("left", "right", or "both", default: "both")

**Example:**
```yaml
rules:
  - type: trim
    params:
      side: "both"
```

#### `case`

Changes the case of a field value.

**Parameters:**
- `type`: Type of case transformation ("upper", "lower", "title", or "sentence")

**Example:**
```yaml
rules:
  - type: case
    params:
      type: "upper"
```

#### `pad`

Pads a field value to a specified length.

**Parameters:**
- `length`: Target length
- `char`: Character to use for padding
- `side`: Which side to pad ("left" or "right")

**Example:**
```yaml
rules:
  - type: pad
    params:
      length: 10
      char: "0"
      side: "left"
```

#### `date_format`

Formats a date field.

**Parameters:**
- `input_format`: Input date format
- `output_format`: Output date format

**Example:**
```yaml
rules:
  - type: date_format
    params:
      input_format: "%Y%m%d"
      output_format: "%d/%m/%Y"
```

#### `substring`

Extracts a substring from a field value.

**Parameters:**
- `start`: Start index (0-based)
- `length` (optional): Length of substring to extract
- `end` (optional): End index (exclusive)

**Example:**
```yaml
rules:
  - type: substring
    params:
      start: 0
      length: 5
```

#### `replace`

Replaces text in a field value.

**Parameters:**
- `old`: Text to replace
- `new`: Replacement text
- `count` (optional): Maximum number of replacements (default: replace all)
- `regex` (optional): Whether to treat `old` as a regular expression (default: false)

**Example:**
```yaml
rules:
  - type: replace
    params:
      old: "-"
      new: ""
```

## Global Rules

Global rules are applied across all records in a file. They can be used for validation or calculation of aggregate values.

### `count`

Counts the number of records in a section.

**Parameters:**
- `section`: The section to count records in
- `count_field` (optional): Field to compare the count against (format: "section.field")
- `expected_count` (optional): Expected count value
- `include_invalid_records` (optional): Whether to include invalid records in the count (default: false)
- `insert_value` (optional): Whether to insert the calculated count into a target field (default: false)
- `target_field` (optional): Field to insert the count into (format: "section.field")

**Example:**
```yaml
global_rules:
  - type: count
    name: employee_count
    params:
      section: body
      count_field: footer.employee_count
      include_invalid_records: false
      insert_value: true
      target_field: footer.employee_count
```

### `sum`

Sums the values of a field across all records.

**Parameters:**
- `section`: The section containing the field to sum
- `field`: The field to sum
- `sum_field` (optional): Field to compare the sum against (format: "section.field")
- `expected_sum` (optional): Expected sum value
- `include_invalid_records` (optional): Whether to include invalid records in the sum (default: false)
- `insert_value` (optional): Whether to insert the calculated sum into a target field (default: false)
- `target_field` (optional): Field to insert the sum into (format: "section.field")

**Example:**
```yaml
global_rules:
  - type: sum
    name: salary_sum
    params:
      section: body
      field: salary
      sum_field: footer.total_salary
      include_invalid_records: false
      insert_value: true
      target_field: footer.total_salary
```

### `checksum`

Calculates a checksum of a field across all records.

**Parameters:**
- `section`: The section containing the field to calculate checksum for
- `field`: The field to calculate checksum for
- `type`: Type of checksum ("sum", "xor", "mod10", or "md5")
- `checksum_field` (optional): Field to compare the checksum against (format: "section.field")
- `expected_checksum` (optional): Expected checksum value
- `include_invalid_records` (optional): Whether to include invalid records in the checksum (default: false)
- `insert_value` (optional): Whether to insert the calculated checksum into a target field (default: false)
- `target_field` (optional): Field to insert the checksum into (format: "section.field")

**Example:**
```yaml
global_rules:
  - type: checksum
    name: data_checksum
    params:
      section: body
      field: data
      type: sum
      checksum_field: footer.checksum
      include_invalid_records: false
      insert_value: true
      target_field: footer.checksum
```

### `uniqueness`

Validates that a field or combination of fields has unique values across all records.

**Parameters:**
- `section`: The section containing the fields to check for uniqueness
- `fields`: The field or fields to check for uniqueness (string for single field, list for multiple fields)
- `include_invalid_records` (optional): Whether to include invalid records in the uniqueness check (default: false)

**Example for single field:**
```yaml
global_rules:
  - type: uniqueness
    name: unique_employee_id
    params:
      section: body
      fields: employee_id
      include_invalid_records: false
```

**Example for multiple fields (composite uniqueness):**
```yaml
global_rules:
  - type: uniqueness
    name: unique_employee_name_country
    params:
      section: body
      fields:
        - employee_name
        - country_code
      include_invalid_records: false
```

## Rule Execution Order

Rules are executed in the order they are defined in the configuration file. This is important to consider when using transformation rules, as the output of one rule becomes the input for the next rule.

For example, if you have a `trim` rule followed by a `string_length` rule, the length check will be applied to the trimmed value.

## Error Handling

When a rule fails, FlatForge generates a validation error with the following information:
- Error message
- Field name
- Record number
- Section name
- Error code (for programmatic handling)

You can control how errors are handled using the following options in the file format configuration:
- `exit_on_first_error`: Whether to stop processing on the first error
- `abort_after_n_failed_records`: Number of failed records after which to abort processing (-1 means process the whole file)

## Custom Rules

FlatForge supports custom rules through its extensible rule system. To create a custom rule, you need to:

1. Create a class that inherits from `Rule` or one of its subclasses
2. Implement the `validate` method for validation rules or the `transform` method for transformation rules
3. Register the rule with the rule registry

For more information on creating custom rules, see the [Developer Guide](../developer_guide/custom_rules.md). 