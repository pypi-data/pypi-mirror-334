# Transformation Rules

FlatForge provides a variety of transformation rules that can be applied to fields in a flat file. These rules allow you to modify field values before they are written to the output file.

## Available Transformation Rules

### Trim Rule

The `trim` rule removes whitespace from the edges of a field value.

**Parameters:**
- `type`: The type of trimming to perform. Options are:
  - `left`: Remove whitespace from the beginning of the value
  - `right`: Remove whitespace from the end of the value
  - `both`: Remove whitespace from both the beginning and end of the value (default)

**Example:**
```yaml
- type: trim
  params:
    type: both
```

**Input/Output Examples:**
- `"  hello  "` → `"hello"` (both)
- `"  hello  "` → `"hello  "` (left)
- `"  hello  "` → `"  hello"` (right)

### Case Rule

The `case` rule changes the case of letters in a field value.

**Parameters:**
- `type`: The type of case transformation to perform. Options are:
  - `upper`: Convert all letters to uppercase
  - `lower`: Convert all letters to lowercase
  - `title`: Convert the first letter of each word to uppercase
  - `camel`: Convert to camel case (first word lowercase, subsequent words capitalized with no spaces)

**Example:**
```yaml
- type: case
  params:
    type: upper
```

**Input/Output Examples:**
- `"hello world"` → `"HELLO WORLD"` (upper)
- `"Hello World"` → `"hello world"` (lower)
- `"hello world"` → `"Hello World"` (title)
- `"hello world"` → `"helloWorld"` (camel)

### Pad Rule

The `pad` rule pads a field value to a specified length.

**Parameters:**
- `length`: The desired length of the field (required if not specified in the field definition)
- `char`: The character to use for padding (default: space)
- `side`: The side to pad. Options are:
  - `left`: Pad on the left side
  - `right`: Pad on the right side (default)

**Example:**
```yaml
- type: pad
  params:
    length: 10
    char: "0"
    side: left
```

**Input/Output Examples:**
- `"123"` → `"0000000123"` (left padding with '0' to length 10)
- `"abc"` → `"abc       "` (right padding with spaces to length 10)

### Date Format Rule

The `date_format` rule formats a date field.

**Parameters:**
- `input_format`: The format of the input date (default: "%Y%m%d")
- `output_format`: The desired format of the output date (default: "%Y-%m-%d")

**Example:**
```yaml
- type: date_format
  params:
    input_format: "%Y%m%d"
    output_format: "%d-%m-%Y"
```

**Input/Output Examples:**
- `"20230415"` → `"15-04-2023"` (from YYYYMMDD to DD-MM-YYYY)

### Substring Rule

The `substring` rule extracts a substring from a field value.

**Parameters:**
- `start`: The starting index (0-based, inclusive)
- `end`: The ending index (exclusive, optional)

**Example:**
```yaml
- type: substring
  params:
    start: 2
    end: 6
```

**Input/Output Examples:**
- `"abcdefghij"` → `"cdef"` (characters at indices 2, 3, 4, and 5)

### Replace Rule

The `replace` rule replaces occurrences of a substring with another substring.

**Parameters:**
- `old`: The substring to replace
- `new`: The replacement substring

**Example:**
```yaml
- type: replace
  params:
    old: "abc"
    new: "XYZ"
```

**Input/Output Examples:**
- `"abc123abc"` → `"XYZ123XYZ"` (replace all occurrences of "abc" with "XYZ")

## Combining Transformation Rules

You can apply multiple transformation rules to a single field. The rules are applied in the order they are defined.

**Example:**
```yaml
- name: field_name
  position: 0
  rules:
    - type: trim
    - type: case
      params:
        type: upper
    - type: pad
      params:
        length: 15
        char: "-"
        side: right
```

This will:
1. Trim whitespace from both ends of the field value
2. Convert the value to uppercase
3. Pad the value to a length of 15 characters with "-" on the right side

## Sample Files

The FlatForge repository includes sample files to demonstrate the use of transformation rules:

- `samples/config/transformation_rules_test.yaml`: Configuration for testing transformation rules with delimited files
- `samples/config/transformation_rules_fixed_length.yaml`: Configuration for testing transformation rules with fixed-length files
- `samples/input/transformation_test_input.csv`: Sample delimited input file
- `samples/input/transformation_test_fixed_length.txt`: Sample fixed-length input file
- `samples/test_transformations.py`: Script to run transformation tests

You can run the test script to see the transformation rules in action:

```bash
python samples/test_transformations.py
``` 