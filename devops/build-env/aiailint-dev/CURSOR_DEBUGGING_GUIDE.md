# Cursor IDE Debugging Guide for aiailint

## Overview

This guide shows you how to set up breakpoints, debug aiailint, and use Cursor's IDE features effectively with the build environment.

## Setup Instructions

### 1. **Open the Build Environment in Cursor**

```bash
# Navigate to the build environment
cd /home/pt/aiai/devops/build-env

# Open in Cursor
cursor .
```

### 2. **Set Up the Environment**

```bash
# Run the setup script (if not already done)
./scripts/setup-env.sh

# Activate the virtual environment
source venv/bin/activate
```

### 3. **Verify Python Interpreter**

In Cursor:
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
2. Type "Python: Select Interpreter"
3. Choose: `./venv/bin/python`

## Debug Configurations

The `.vscode/launch.json` file provides several debug configurations:

### **1. Debug aiailint (Build Environment)**
- **Purpose**: Debug aiailint with the current file
- **Usage**: Set breakpoints in `aiailint.py`, then run this configuration
- **Args**: `validate ${file}`

### **2. Debug aiailint with custom args**
- **Purpose**: Debug with verbose and JSON output
- **Usage**: For detailed debugging with custom arguments
- **Args**: `validate --verbose --format json ${file}`

### **3. Debug aiailint package validation**
- **Purpose**: Debug package validation
- **Usage**: Test with the ubuntu-btrfs-aiai package
- **Args**: `validate --package ../../../packages/ubuntu-btrfs-aiai/`

### **4. Debug aiailint tests**
- **Purpose**: Debug test execution
- **Usage**: Set breakpoints in test files
- **Args**: Runs pytest with verbose output

## Setting Breakpoints

### **Step 1: Open aiailint Source**
```bash
# In Cursor, open the main aiailint file
open ../../../aiailint/src/aiailint.py
```

### **Step 2: Set Breakpoints**
1. **Click in the gutter** (left margin) next to line numbers
2. **Red dots** appear where you set breakpoints
3. **Common breakpoint locations**:
   - `main()` function entry point
   - `validate_file()` method
   - `_run_validation_pipeline()` method
   - Error handling sections

### **Step 3: Start Debugging**
1. **Press F5** or click the "Run and Debug" icon
2. **Select** "Debug aiailint (Build Environment)"
3. **Choose** a YAML file to validate
4. **Execution stops** at your breakpoints

## Debugging Workflow

### **1. Basic Debugging**
```bash
# 1. Set breakpoints in aiailint.py
# 2. Open a test YAML file
# 3. Press F5 and select "Debug aiailint (Build Environment)"
# 4. Step through code with F10 (step over) and F11 (step into)
```

### **2. Advanced Debugging**
```bash
# 1. Set breakpoints in specific validation methods
# 2. Use "Debug aiailint with custom args" for verbose output
# 3. Use "Debug aiailint package validation" for package testing
# 4. Use "Debug aiailint tests" for test debugging
```

## Debug Features

### **Variable Inspection**
- **Hover** over variables to see values
- **Watch** specific variables in the Debug panel
- **Locals** panel shows all local variables
- **Call Stack** shows execution path

### **Step Commands**
- **F5**: Continue execution
- **F10**: Step over (execute line, don't go into functions)
- **F11**: Step into (go into function calls)
- **Shift+F11**: Step out (exit current function)
- **F9**: Toggle breakpoint

### **Debug Console**
- **Evaluate expressions** in the debug console
- **Inspect variables** with `print(variable_name)`
- **Test code snippets** during debugging

## Example Debug Session

### **Step 1: Prepare Test File**
Create a test YAML file: `test_script.yaml`
```yaml
name: "Test Script"
version: "1.0"
body:
  - type: "command"
    id: "test-command"
    shellCommand: "echo 'Hello World'"
```

### **Step 2: Set Breakpoints**
1. Open `../../../aiailint/src/aiailint.py`
2. Set breakpoints at:
   - Line 456: `def main():`
   - Line 223: `def validate_file(self, file_path: Union[str, Path]) -> ValidationResult:`
   - Line 289: `def _load_yaml_data(self, file_path: Path) -> Optional[Dict[str, Any]]:`

### **Step 3: Start Debugging**
1. Open `test_script.yaml` in Cursor
2. Press `F5`
3. Select "Debug aiailint (Build Environment)"
4. Execution stops at your first breakpoint

### **Step 4: Step Through Code**
1. **F10** to step over lines
2. **F11** to step into function calls
3. **Hover** over variables to inspect values
4. **Watch** important variables like `file_path`, `data`, etc.

## Debugging Tips

### **1. Use Debug Prints**
Add temporary debug prints in your code:
```python
def validate_file(self, file_path: Union[str, Path]) -> ValidationResult:
    print(f"DEBUG: Validating file: {file_path}")  # Debug print
    # ... rest of the function
```

### **2. Conditional Breakpoints**
1. **Right-click** on a breakpoint
2. **Select** "Edit Breakpoint"
3. **Add condition** like: `file_path.endswith('.yaml')`

### **3. Logging Integration**
```python
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def validate_file(self, file_path: Union[str, Path]) -> ValidationResult:
    logger.debug(f"Starting validation of: {file_path}")
    # ... rest of the function
```

### **4. Exception Breakpoints**
1. **Debug panel** → **Breakpoints** → **+**
2. **Add exception breakpoint** for specific exceptions
3. **Catch all exceptions** to debug error handling

## Debugging Different Scenarios

### **1. Debugging Validation Errors**
```bash
# Create a file with validation errors
echo "invalid: yaml: content" > error_test.yaml

# Set breakpoints in error handling code
# Run debugger and watch error processing
```

### **2. Debugging Package Validation**
```bash
# Set breakpoints in package loading code
# Use "Debug aiailint package validation" configuration
# Step through package discovery and validation
```

### **3. Debugging Test Failures**
```bash
# Set breakpoints in test files
# Use "Debug aiailint tests" configuration
# Step through test execution
```

## Advanced Debugging

### **1. Remote Debugging**
If you need to debug on a remote system:
```python
import debugpy

# Add this to your code for remote debugging
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()
```

### **2. Performance Debugging**
```python
import time
import cProfile
import pstats

def profile_function(func):
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)
        return result
    return wrapper
```

### **3. Memory Debugging**
```python
import tracemalloc

# Start memory tracking
tracemalloc.start()

# Your code here

# Get memory snapshot
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
print("[ Top 10 memory users ]")
for stat in top_stats[:10]:
    print(stat)
```

## Troubleshooting

### **Common Issues**

#### **1. Python Interpreter Not Found**
```bash
# Solution: Make sure virtual environment is activated
source venv/bin/activate
# Then select the correct interpreter in Cursor
```

#### **2. Breakpoints Not Hit**
```bash
# Solution: Check that you're running the correct configuration
# Make sure the file path in launch.json is correct
# Verify PYTHONPATH is set correctly
```

#### **3. Import Errors**
```bash
# Solution: Check PYTHONPATH in launch.json
# Make sure aiailint source is in the path
# Verify virtual environment has all dependencies
```

#### **4. Debug Console Not Working**
```bash
# Solution: Make sure you're in a debug session
# Check that the debugger is attached
# Try restarting the debug session
```

## Keyboard Shortcuts

| Action | Windows/Linux | macOS |
|--------|---------------|-------|
| Start Debugging | F5 | F5 |
| Stop Debugging | Shift+F5 | Shift+F5 |
| Step Over | F10 | F10 |
| Step Into | F11 | F11 |
| Step Out | Shift+F11 | Shift+F11 |
| Continue | F5 | F5 |
| Toggle Breakpoint | F9 | F9 |
| Debug Console | Ctrl+Shift+Y | Cmd+Shift+Y |

## Best Practices

### **1. Use Meaningful Breakpoints**
- Set breakpoints at function entry points
- Set breakpoints before error-prone code
- Use conditional breakpoints for specific scenarios

### **2. Keep Debug Sessions Focused**
- Debug one issue at a time
- Use different debug configurations for different scenarios
- Clean up temporary debug prints

### **3. Use the Debug Console Effectively**
- Test expressions before adding them to code
- Inspect complex data structures
- Test function calls with different arguments

### **4. Document Debug Sessions**
- Take notes on what you discover
- Document common debugging patterns
- Share debugging tips with your team

---

## Summary

With this setup, you can:
✅ **Set breakpoints** in any aiailint source file  
✅ **Step through code** line by line  
✅ **Inspect variables** and data structures  
✅ **Debug different scenarios** with multiple configurations  
✅ **Use advanced debugging features** like conditional breakpoints  
✅ **Integrate with Cursor's IDE features** seamlessly  

The build environment provides a complete debugging experience that integrates perfectly with Cursor's powerful IDE capabilities.
