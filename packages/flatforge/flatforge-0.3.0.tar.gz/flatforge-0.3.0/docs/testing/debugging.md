# Debugging FlatForge

This document provides guidance on how to debug the FlatForge library in a local IDE, including explanations of the debug scripts provided in the workspace and best practices for effective debugging.

## Table of Contents

- [Overview](#overview)
- [Debug Scripts](#debug-scripts)
- [Setting Up Your IDE for Debugging](#setting-up-your-ide-for-debugging)
- [Debugging Techniques](#debugging-techniques)
- [Common Issues and Solutions](#common-issues-and-solutions)
- [Advanced Debugging](#advanced-debugging)

## Overview

Debugging is an essential part of the development process, allowing you to identify and fix issues in your code. FlatForge provides several debug scripts that make it easier to debug different aspects of the library in your IDE.

### Debugging a Library vs. a Python Script

Debugging a library like FlatForge differs from debugging a simple Python script in several important ways:

1. **Import Resolution**: When debugging a library, Python needs to know how to find and import the library modules. This is different from a standalone script where all code is typically in a single file or directory.

2. **Package Structure**: Libraries have a structured package hierarchy that must be maintained for imports to work correctly.

3. **Installation Requirements**: To properly debug a library, you typically need to install it in "development mode" so that changes to the source code are immediately reflected when the library is imported.

### Installing FlatForge in Development Mode

To debug FlatForge effectively, you should install it in development mode using pip:

```bash
# Navigate to the root directory of the FlatForge repository
cd path/to/flatforge-repo

# Install in development mode
pip install -e .
```

This creates a special link in your Python environment that points to your development directory, allowing you to:

- Import the library in your debug scripts as if it were installed normally
- Make changes to the source code and see them immediately without reinstalling
- Run tests against your development version

If you're using a virtual environment (recommended), make sure to activate it before installing:

```bash
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate

# Then install in development mode
pip install -e .
```

### Verifying the Installation

To verify that FlatForge is installed correctly in development mode, you can run:

```python
import flatforge
print(flatforge.__file__)  # Should point to your development directory
```

Now that you have FlatForge installed in development mode, you can use the debug scripts provided in the workspace to debug different aspects of the library.

## Debug Scripts

FlatForge includes several debug scripts in the root directory of the workspace, each designed for a specific debugging purpose:

### debug_main.py

This script allows you to debug the main processing functionality directly:

```python
"""
Debug script for the FlatForge CLI main module.

This script allows you to debug the main.py module directly in your IDE.
"""
from flatforge.cli.main import main

if __name__ == "__main__":
    # Call the main function with the arguments you want to test
    main(
        config="samples/config/employee_csv.yaml",
        input="samples/input/employee_data.csv",
        output="samples/output/debug_output.csv",
        errors="samples/output/debug_errors.csv",
        chunk_size=0,
        show_progress=False
    )
```

**Purpose**: Debug the core processing functionality without going through the CLI layer. This is useful for isolating issues in the main processing logic.

### debug_cli.py

This script allows you to debug the CLI interface by simulating command-line arguments:

```python
"""
Debug script for the FlatForge CLI.

This script allows you to debug the CLI in your IDE by directly calling the CLI function
with command-line arguments.
"""
import sys
from flatforge.cli import cli

if __name__ == "__main__":
    # Set up the arguments you want to pass to the CLI
    sys.argv = [
        "flatforge",  # Program name (can be anything)
        "validate",   # Command
        "--config", "samples/config/employee_fixed_length.yaml",
        "--input", "samples/input/employee_data.txt",
        "--output", "samples/output/debug_output.csv",
        "--errors", "samples/output/debug_errors.csv"
    ]
    
    # Call the CLI function
    cli()
```

**Purpose**: Debug the CLI interface by simulating command-line arguments. This is useful for testing how the CLI parses and processes arguments.

### debug_cli_chunked.py

This script allows you to debug the chunked processing functionality:

```python
"""
Debug script for the FlatForge CLI with chunked processing.

This script allows you to debug the CLI with chunked processing and progress reporting.
"""
import sys
from flatforge.cli import cli

if __name__ == "__main__":
    # Set up the arguments for chunked processing
    sys.argv = [
        "flatforge",
        "validate",
        "--config", "samples/config/employee_csv.yaml",
        "--input", "samples/input/employee_data.csv",
        "--output", "samples/output/debug_chunked_output.csv",
        "--errors", "samples/output/debug_chunked_errors.csv",
        "--chunk-size", "2",  # Process 2 records at a time
        "--show-progress"     # Show progress bar
    ]
    
    # Call the CLI function
    cli()
```

**Purpose**: Debug the chunked processing functionality, which processes files in smaller chunks to reduce memory usage and provide progress reporting. This is useful for testing performance and memory usage with large files.

### debug_cli_convert.py

This script allows you to debug the file format conversion functionality:

```python
"""
Debug script for the FlatForge CLI convert command.

This script allows you to debug the convert command in your IDE.
"""
import sys
from flatforge.cli import cli

if __name__ == "__main__":
    # Set up the arguments for the convert command
    sys.argv = [
        "flatforge",
        "convert",
        "--input-config", "samples/config/employee_csv.yaml",
        "--output-config", "samples/config/employee_fixed_length.yaml",
        "--input", "samples/input/employee_data.csv",
        "--output", "samples/output/debug_converted.txt",
        "--errors", "samples/output/debug_convert_errors.txt"
    ]
    
    # Call the CLI function
    cli()
```

**Purpose**: Debug the file format conversion functionality, which converts files from one format to another. This is useful for testing the transformation logic.

### debug_cli_click.py

This script allows you to debug the CLI using Click's test runner:

```python
"""
Debug script for the FlatForge CLI using Click's test runner.

This script allows you to debug the CLI in your IDE using Click's test runner,
which provides more detailed output and error handling.
"""
from click.testing import CliRunner
from flatforge.cli import cli

if __name__ == "__main__":
    runner = CliRunner()
    result = runner.invoke(cli, [
        "validate",
        "--config", "samples/config/employee_csv.yaml",
        "--input", "samples/input/employee_data.csv",
        "--output", "samples/output/debug_output.csv",
        "--errors", "samples/output/debug_errors.csv"
    ])
    
    # Print the result
    print(f"Exit code: {result.exit_code}")
    if result.exception:
        print(f"Exception: {result.exception}")
    print(f"Output:\n{result.output}")
```

**Purpose**: Debug the CLI using Click's test runner, which provides more detailed output and error handling. This is useful for testing the CLI in a controlled environment and capturing the output and exceptions.

## Setting Up Your IDE for Debugging

### Visual Studio Code

1. **Install the Python extension**: If you haven't already, install the Python extension for VS Code.

2. **Configure launch.json**: Create a `.vscode/launch.json` file with configurations for each debug script:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Main",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/debug_main.py",
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Debug CLI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/debug_cli.py",
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Debug CLI Chunked",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/debug_cli_chunked.py",
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Debug CLI Convert",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/debug_cli_convert.py",
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Debug CLI Click",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/debug_cli_click.py",
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

3. **Set breakpoints**: Set breakpoints in your code by clicking in the gutter next to the line numbers.

4. **Start debugging**: Press F5 or click the "Run and Debug" button in the sidebar, then select the configuration you want to run.

### PyCharm

1. **Configure run configurations**: Create run configurations for each debug script:
   - Click "Run" > "Edit Configurations"
   - Click the "+" button and select "Python"
   - Set the script path to the debug script you want to run
   - Set the working directory to the project root
   - Click "OK"

2. **Set breakpoints**: Set breakpoints in your code by clicking in the gutter next to the line numbers.

3. **Start debugging**: Press Shift+F9 or click the debug button next to the run configuration dropdown.

## Debugging Techniques

### Using Print Statements

While not the most sophisticated method, print statements can be a quick way to debug issues:

```python
print(f"Processing record: {record}")
print(f"Field value: {field.value}, Rules: {field.rules}")
```

### Using the Python Debugger (pdb)

You can use the Python debugger to interactively debug your code:

```python
import pdb

def process_record(record):
    pdb.set_trace()  # Debugger will stop here
    # Rest of the function
```

Common pdb commands:
- `n`: Execute the next line
- `s`: Step into a function call
- `c`: Continue execution until the next breakpoint
- `p expression`: Print the value of an expression
- `q`: Quit the debugger

### Using Logging

FlatForge uses Python's logging module for more structured debugging:

```python
import logging

logging.debug("Processing record: %s", record)
logging.info("Processed %d records", count)
logging.warning("Field %s has an invalid value: %s", field.name, field.value)
logging.error("Failed to process file: %s", str(e))
```

To enable debug logging, set the log level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Common Issues and Solutions

### Configuration Issues

**Issue**: The library can't find or parse the configuration file.

**Solution**: 
1. Check that the file path is correct and the file exists
2. Validate the YAML syntax using a YAML validator
3. Check that the configuration follows the expected schema

### Input File Issues

**Issue**: The library can't read or parse the input file.

**Solution**:
1. Check that the file path is correct and the file exists
2. Check that the file format matches the configuration
3. Check for encoding issues (try specifying the encoding explicitly)

### Validation Issues

**Issue**: Records are failing validation unexpectedly.

**Solution**:
1. Check the validation rules in the configuration
2. Check the error file for specific error messages
3. Debug the validation process to see which rules are failing

### Memory Issues

**Issue**: The library runs out of memory when processing large files.

**Solution**:
1. Use chunked processing with a smaller chunk size
2. Monitor memory usage during processing
3. Check for memory leaks (objects that aren't being garbage collected)

## Advanced Debugging

### Profiling

To identify performance bottlenecks, you can use Python's profiling tools:

```python
import cProfile
import pstats

# Profile the function
cProfile.run('process_file("input.csv", "output.csv", "errors.csv")', 'profile_stats')

# Analyze the results
p = pstats.Stats('profile_stats')
p.sort_stats('cumulative').print_stats(20)  # Show the 20 functions that took the most time
```

### Memory Profiling

To identify memory issues, you can use the `memory_profiler` package:

```python
from memory_profiler import profile

@profile
def process_file(input_file, output_file, error_file):
    # Function code
```

### Debugging Multithreaded Code

If you're using multithreading or multiprocessing, debugging can be more complex:

1. Use thread-safe logging
2. Use the `threading` module's debugging features
3. Consider using the `concurrent.futures` module, which provides a higher-level interface

## Conclusion

Effective debugging is essential for developing and maintaining the FlatForge library. By using the provided debug scripts and following the techniques outlined in this guide, you can quickly identify and fix issues in your code.

Remember that debugging is often an iterative process:
1. Reproduce the issue
2. Isolate the problem
3. Fix the issue
4. Verify the fix
5. Add tests to prevent regression

If you encounter persistent issues, don't hesitate to ask for help from the FlatForge community or consult the other documentation resources. 