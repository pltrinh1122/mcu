# Vibe Coding Guide for aiailint

## Overview

This guide explains how to use **strategic asserts** and **debug logs** for effective "vibe coding" without breakpoints. Perfect for collaborative development with AI assistants.

## Vibe Coding Philosophy

### **Why Strategic Asserts & Debug Logs?**

✅ **Collaborative**: Works great with AI assistants  
✅ **Reproducible**: Same output every time  
✅ **Non-interactive**: No IDE dependencies  
✅ **Structured**: Easy to parse and analyze  
✅ **Distributable**: Can share logs and results  

### **No More Breakpoints!**

Instead of setting breakpoints, we use:
- **Strategic asserts** to validate assumptions
- **Debug logs** to trace execution
- **Data inspection** to understand state
- **Performance tracking** to optimize code

## Quick Start

### **1. Set Up Vibe Environment**
```bash
cd /home/pt/aiai/devops/build-env
./scripts/setup-debugging.sh
```

### **2. Run Vibe Debug Session**
```bash
python vibe_debug_helper.py
```

### **3. Check Vibe Debug Log**
```bash
tail -f vibe_debug.log
```

## Strategic Asserts

### **Basic Asserts**
```python
from debug_utils import vibe_assert, vibe_assert_data_structure

# Validate conditions
vibe_assert(file_path.exists(), "File should exist")
vibe_assert(len(data) > 0, "Data should not be empty")

# Validate data types
vibe_assert_data_structure(yaml_data, dict, "YAML data should be dict")
vibe_assert_data_structure(validation_result, ValidationResult, "Result should be ValidationResult")
```

### **File Validation Asserts**
```python
from debug_utils import vibe_assert_file_exists, vibe_assert_yaml_valid

# Validate file exists
vibe_assert_file_exists(Path("script.yaml"), "Script file should exist")

# Validate YAML structure
vibe_assert_yaml_valid(yaml_data, "YAML should have required structure")
```

### **Custom Asserts**
```python
def vibe_assert_validation_pipeline(data, context=""):
    """Custom assert for validation pipeline"""
    vibe_assert(
        hasattr(data, 'success') and hasattr(data, 'errors'),
        "Validation result should have success and errors attributes",
        {"context": context, "data_type": type(data).__name__}
    )
```

## Debug Logging

### **Basic Logging**
```python
from debug_utils import vibe_log, vibe_error, vibe_success

# Log different levels
vibe_log("Starting validation process")
vibe_log("Processing file: script.yaml", "INFO")
vibe_success("Validation completed successfully")
vibe_error("Validation failed", exception)
```

### **Data Inspection**
```python
from debug_utils import vibe_inspect

# Inspect data structures
vibe_inspect(yaml_data, "YAML Data")
vibe_inspect(validation_result, "Validation Result")
vibe_inspect(complex_object, "Complex Object", max_depth=5)
```

### **Function Tracing**
```python
from debug_utils import vibe_trace_function

@vibe_trace_function
def validate_file(self, file_path):
    # Function calls will be automatically logged
    result = self._run_validation_pipeline(file_path)
    return result
```

## Performance Tracking

### **Performance Decorator**
```python
from debug_utils import vibe_performance_tracker

@vibe_performance_tracker
def expensive_validation_function(data):
    # Performance will be automatically tracked
    result = complex_validation_logic(data)
    return result
```

### **Manual Performance Tracking**
```python
import time
from debug_utils import vibe_log

def custom_performance_tracking():
    start_time = time.time()
    vibe_log("Starting expensive operation")
    
    # ... your code here ...
    
    duration = time.time() - start_time
    vibe_log(f"Operation completed in {duration:.4f}s")
```

## Debug State Management

### **Using Vibe State**
```python
from debug_utils import vibe_state

# Set debug state
vibe_state.set("current_file", "script.yaml")
vibe_state.set("validation_mode", "strict")
vibe_state.set("debug_level", "verbose")

# Get debug state
current_file = vibe_state.get("current_file")
validation_mode = vibe_state.get("validation_mode", "normal")

# Dump all state
vibe_state.dump()
```

## Vibe Coding Workflow

### **1. Start with Strategic Asserts**
```python
def validate_file(self, file_path):
    # Strategic assert: File should exist
    vibe_assert_file_exists(file_path, "File validation")
    
    # Strategic assert: File should be readable
    vibe_assert(file_path.is_file(), "Should be a file, not directory")
    
    # Continue with validation...
```

### **2. Add Debug Logging**
```python
def validate_file(self, file_path):
    vibe_log(f"Starting validation of: {file_path}")
    
    # Load and validate YAML
    yaml_data = self._load_yaml_data(file_path)
    vibe_inspect(yaml_data, "Loaded YAML Data")
    
    # Run validation pipeline
    result = self._run_validation_pipeline(file_path)
    vibe_inspect(result, "Validation Result")
    
    vibe_success(f"Validation completed for: {file_path}")
    return result
```

### **3. Use Performance Tracking**
```python
@vibe_performance_tracker
def _run_validation_pipeline(self, file_path):
    vibe_log("Running validation pipeline")
    
    # Your validation logic here
    # Performance will be automatically tracked
    
    return result
```

### **4. Manage Debug State**
```python
def validate_package(self, package_path):
    vibe_state.set("package_path", str(package_path))
    vibe_state.set("validation_start_time", time.time())
    
    # ... validation logic ...
    
    vibe_state.set("validation_end_time", time.time())
    vibe_state.dump()  # Log final state
```

## Example: Complete Vibe Coding Session

### **Step 1: Set Up Environment**
```python
from debug_utils import (
    setup_vibe_logging, vibe_assert, vibe_log, 
    vibe_inspect, vibe_state, vibe_performance_tracker
)

# Set up vibe logging
vibe_logger = setup_vibe_logging("DEBUG", "vibe_debug.log")
vibe_log("Starting vibe coding session")
```

### **Step 2: Strategic Asserts**
```python
def vibe_validate_script(script_path):
    # Strategic asserts
    vibe_assert(Path(script_path).exists(), "Script file must exist")
    vibe_assert(script_path.endswith('.yaml'), "Script must be YAML file")
    
    # Load and validate data
    with open(script_path) as f:
        data = yaml.safe_load(f)
    
    vibe_assert_yaml_valid(data, "Script validation")
    vibe_inspect(data, "Script Data")
    
    return data
```

### **Step 3: Debug Logging**
```python
@vibe_performance_tracker
def vibe_process_script(script_path):
    vibe_log(f"Processing script: {script_path}")
    
    # Load script
    script_data = vibe_validate_script(script_path)
    vibe_success("Script loaded successfully")
    
    # Process each command
    for i, command in enumerate(script_data.get('body', [])):
        vibe_log(f"Processing command {i+1}: {command.get('id', 'unknown')}")
        vibe_inspect(command, f"Command {i+1}")
        
        # Process command...
        vibe_success(f"Command {i+1} processed")
    
    vibe_success("All commands processed")
```

### **Step 4: State Management**
```python
def vibe_debug_session():
    vibe_state.set("session_id", "vibe_session_001")
    vibe_state.set("start_time", time.time())
    
    # Process multiple scripts
    scripts = ["script1.yaml", "script2.yaml", "script3.yaml"]
    
    for script in scripts:
        vibe_state.set("current_script", script)
        vibe_process_script(script)
    
    vibe_state.set("end_time", time.time())
    vibe_state.dump()
```

## Vibe Coding Best Practices

### **1. Use Descriptive Assert Messages**
```python
# Good
vibe_assert(len(data) > 0, "Data should contain at least one element")

# Better
vibe_assert(len(data) > 0, "Script should have at least one command in body")
```

### **2. Log Important State Changes**
```python
vibe_log("Starting validation phase")
vibe_log("Entering destructive command detection")
vibe_log("Completed semantic analysis")
```

### **3. Inspect Complex Data Structures**
```python
# Always inspect loaded data
yaml_data = yaml.safe_load(file_content)
vibe_inspect(yaml_data, "Loaded YAML")

# Inspect validation results
result = validate_script(yaml_data)
vibe_inspect(result, "Validation Result")
```

### **4. Track Performance for Expensive Operations**
```python
@vibe_performance_tracker
def expensive_validation_function(data):
    # This will automatically log performance
    return complex_validation_logic(data)
```

### **5. Use State Management for Complex Sessions**
```python
vibe_state.set("validation_mode", "strict")
vibe_state.set("current_file", file_path)
vibe_state.set("debug_level", "verbose")
```

## Troubleshooting Vibe Coding

### **Common Issues**

#### **1. Assert Failures**
```bash
# Check vibe debug log for detailed error messages
tail -f vibe_debug.log | grep "VIBE ASSERT"
```

#### **2. Performance Issues**
```bash
# Look for performance logs
tail -f vibe_debug.log | grep "VIBE PERFORMANCE"
```

#### **3. State Issues**
```bash
# Check current debug state
python -c "from debug_utils import vibe_state; vibe_state.dump()"
```

### **Debug Helper Commands**
```bash
# Run vibe debug session
python vibe_debug_helper.py

# Check vibe debug log
tail -f vibe_debug.log

# Filter specific log levels
tail -f vibe_debug.log | grep "VIBE SUCCESS"
tail -f vibe_debug.log | grep "VIBE ERROR"
```

## Integration with aiailint

### **Adding Vibe Debugging to aiailint**

```python
# In aiailint.py, add vibe debugging
from debug_utils import vibe_log, vibe_assert, vibe_inspect

class AiaiLinter:
    def __init__(self, verbose=False, strict=False):
        vibe_log(f"Initializing AiaiLinter: verbose={verbose}, strict={strict}")
        # ... rest of initialization
    
    def validate_file(self, file_path):
        vibe_log(f"Starting validation of: {file_path}")
        
        # Strategic assert
        vibe_assert(Path(file_path).exists(), "File must exist")
        
        # Load and inspect YAML
        yaml_data = self._load_yaml_data(file_path)
        vibe_inspect(yaml_data, "Loaded YAML Data")
        
        # Run validation
        result = self._run_validation_pipeline(file_path)
        vibe_inspect(result, "Validation Result")
        
        vibe_success(f"Validation completed for: {file_path}")
        return result
```

## Summary

Vibe coding with strategic asserts and debug logs provides:

✅ **Collaborative debugging** that works with AI assistants  
✅ **Reproducible results** every time  
✅ **Structured logging** for easy analysis  
✅ **Performance tracking** for optimization  
✅ **State management** for complex sessions  
✅ **No IDE dependencies** - works anywhere  

This approach is perfect for "vibe coding" where you want to understand what's happening without the overhead of setting breakpoints and stepping through code manually.
