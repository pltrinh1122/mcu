# viscriptlint Output Format Comparison with Industry Standards

## Current viscriptlint Output Format

### Example 1: Clean File (Warnings Only)
```
=== Validating viScript: viscriptlint/unit-tests/test_clean_viscript.json ===

[WARNING] ajv not available, skipping JSON Schema validation
[INFO] JSON syntax is valid
[INFO] Install ajv with: npm install -g ajv-cli
[INFO] All required fields present
[INFO] All checks have required fields
[INFO] All severity fields valid
[INFO] All validation types valid
[INFO] No deprecated fields found
[INFO] No unsupported attributes found

=== VALIDATION SUMMARY ===
File: viscriptlint/unit-tests/test_clean_viscript.json
Errors: 0
Warnings: 1
[WARNING] Status: PASSED WITH WARNINGS

Consider addressing the warnings above for better viScript quality.
```

### Example 2: File with Errors
```
=== Validating viScript: viscriptlint/unit-tests/unit_test_viscript_schema.json ===

[ERROR] Found unsupported attributes: conditional, test_mode
[ERROR] empty_command_test: empty command
[WARNING] ajv not available, skipping JSON Schema validation
[WARNING] These attributes are documented but not actually supported by verified_installer.py
[WARNING] Remove these attributes for cleaner code and proper functionality
[WARNING] Found removed top-level fields: mount_points, services, filesystems, test_operations, dependencies, post_verification
[INFO] JSON syntax is valid
[INFO] Install ajv with: npm install -g ajv-cli
[INFO] All required fields present
[INFO] All checks have required fields
[INFO] All severity fields valid
[INFO] All validation types valid
[INFO] No deprecated fields found
[INFO] These fields were removed from the schema and will be ignored
[INFO] Consider removing them from your viScript for cleaner code

=== VALIDATION SUMMARY ===
File: viscriptlint/unit-tests/unit_test_viscript_schema.json
Errors: 2
Warnings: 4
[ERROR] Status: FAILED

Please fix the errors above before using this viScript.

Consider addressing the warnings above for better viScript quality.
```

## Industry Standard Lint Tool Output Formats

### 1. ESLint (JavaScript)
```
/path/to/file.js
  1:1  error  'console' is not defined  no-undef
  2:5  error  Missing semicolon         semi

✖ 2 problems (2 errors, 0 warnings)
```

### 2. Pylint (Python)
```
************* Module test_file
test_file.py:1:0: C0114: Missing module docstring (missing-docstring)
test_file.py:3:4: C0103: Invalid function name "testFunc" (invalid-name)
test_file.py:5:0: C0116: Missing function or method docstring (missing-docstring)

------------------------------------------------------------------
Your code has been rated at 6.67/10 (previous run: 6.67/10, +0.00)
```

### 3. Flake8 (Python)
```
test_file.py:1:1: E302 expected 2 blank lines, found 1
test_file.py:3:1: E303 too many blank lines (3)
test_file.py:5:1: F401 'os' imported but unused
```

### 4. Black (Python Code Formatter)
```
would reformat /path/to/file.py
All done! ✨ 🍰 ✨
1 file would be reformatted.
```

### 5. MyPy (Python Type Checker)
```
test_file.py:5: error: Incompatible types in assignment (expression has type "str", variable has type "int")
test_file.py:8: error: Argument 1 to "len" has incompatible type "int"; expected "Sized"
Found 2 errors in 1 file (checked 1 source file)
```

### 6. ShellCheck (Bash)
```
In test.sh line 1:
echo "test"
^-- SC2001: See if you can use ${variable//search/replace} instead of sed.

In test.sh line 3:
rm -rf /tmp/*
^-- SC2115: Use "${var:?}" to ensure this never expands to / .
```

## Key Differences and Recommendations

### 1. **File Location and Line Numbers**
**Industry Standard**: `file.js:1:1` or `file.py:5:10`
**viscriptlint**: No line numbers, only file-level issues

**Recommendation**: Add line numbers for specific field issues
```
viscriptlint/unit-tests/unit_test_viscript_schema.json:45:5  error  Found unsupported attribute "test_mode"
```

### 2. **Error Code Format**
**Industry Standard**: `E302`, `C0114`, `SC2001`
**viscriptlint**: No error codes

**Recommendation**: Add error codes for better tooling integration
```
VIS001: Found unsupported attribute
VIS002: Missing required field
VIS003: Invalid severity value
```

### 3. **Concise Output**
**Industry Standard**: Brief, focused messages
**viscriptlint**: Verbose with explanations

**Recommendation**: Add `--quiet` flag for concise output
```
file.json:45:5  error  VIS001: Found unsupported attribute "test_mode"
file.json:67:3  error  VIS002: Missing required field "validation_type"
```

### 4. **Machine-Readable Output**
**Industry Standard**: JSON/XML output for CI/CD
**viscriptlint**: Human-readable only

**Recommendation**: Add `--format json` option
```json
{
  "file": "test.json",
  "errors": [
    {
      "line": 45,
      "column": 5,
      "code": "VIS001",
      "message": "Found unsupported attribute",
      "severity": "error"
    }
  ],
  "warnings": [],
  "summary": {
    "errors": 1,
    "warnings": 0
  }
}
```

### 5. **Exit Codes**
**Industry Standard**: 0=success, 1=errors, 2=warnings
**viscriptlint**: ✅ Aligned correctly

### 6. **Color Coding**
**Industry Standard**: Red for errors, yellow for warnings
**viscriptlint**: ✅ Uses colors correctly

## Proposed Improvements

### 1. **Add Line Numbers**
```python
def get_field_location(data, field_path):
    """Get approximate line number for field in JSON"""
    # Implementation to find line numbers
    pass
```

### 2. **Add Error Codes**
```python
class ErrorCodes:
    UNSUPPORTED_ATTRIBUTE = "VIS001"
    MISSING_REQUIRED_FIELD = "VIS002"
    INVALID_SEVERITY = "VIS003"
    INVALID_VALIDATION_TYPE = "VIS004"
    DEPRECATED_FIELD = "VIS005"
    EMPTY_COMMAND = "VIS006"
```

### 3. **Add Machine-Readable Output**
```python
def generate_json_output(result):
    """Generate JSON output for CI/CD integration"""
    return {
        "file": str(file_path),
        "errors": [{"line": e.line, "column": e.column, "code": e.code, "message": e.message} for e in result.errors],
        "warnings": [{"line": w.line, "column": w.column, "code": w.code, "message": w.message} for w in result.warnings],
        "summary": {"errors": len(result.errors), "warnings": len(result.warnings)}
    }
```

### 4. **Add Quiet Mode**
```python
def generate_concise_output(result):
    """Generate concise output similar to industry standards"""
    for error in result.errors:
        print(f"{file_path}:{error.line}:{error.column}  error  {error.code}: {error.message}")
```

## Implementation Priority

1. **High Priority**: Add error codes and line numbers
2. **Medium Priority**: Add JSON output format
3. **Low Priority**: Add quiet mode for concise output

## Benefits of Alignment

- **CI/CD Integration**: Machine-readable output for automation
- **IDE Integration**: Error codes for quick fixes
- **Developer Experience**: Familiar format for users
- **Tool Integration**: Compatible with existing lint toolchains 