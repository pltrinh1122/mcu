# viscriptlint

## Overview

viscriptlint is a comprehensive validation and linting tool for viScript files used by the VI framework. It provides JSON syntax validation, schema compliance checking, and best practices enforcement.

## Module Structure

```
viscriptlint/
├── docs/                    # Documentation
│   └── VISCRIPT_SCHEMA.md  # Schema documentation
├── src/                     # Source files
│   ├── viscriptlint.py     # Main tool with subcommands (Python)
│   ├── viscript_schema.json # JSON Schema definition
│   └── fix_viscripts.py    # Consolidated fix script (helper)
└── unit-tests/             # Unit tests
    ├── test_viscriptlint.py           # Python unit tests for viscriptlint.py
    ├── test_fix_viscripts.py         # Python unit tests for fix_viscripts.py
    ├── test_clean_viscript.json      # Clean test data for unit tests
    ├── test_viscriptlint_integration.sh
    ├── validate_test_viscript.sh
    └── unit_test_viscript_schema.json
```

## Key Features

- **Python Implementation**: Robust JSON parsing and error handling
- **Industry-Standard Subcommands**: `validate`, `fix` commands
- **JSON Syntax Validation**: Ensures valid JSON structure
- **Schema Compliance**: Validates against formal JSON Schema
- **Best Practices**: Enforces coding standards and conventions
- **Exit Code Integration**: Standard exit codes for CI/CD pipelines
- **Comprehensive Reporting**: Detailed error and warning messages
- **Python-First**: All tools use Python for consistency and reliability

## Usage

### Basic Validation

```bash
# Validate a viScript file (default command)
./src/viscriptlint.py validate system_validation_viScript.json
./src/viscriptlint.py system_validation_viScript.json  # Backward compatible

# Verbose validation with detailed output
./src/viscriptlint.py validate btrfs_root_viScript.json --verbose

# Strict validation (treats warnings as errors)
./src/viscriptlint.py validate ../ubuntu-btrfs-vi/src/docker_viScript.json --strict
```

### Fix Schema Issues

```bash
# Fix schema issues automatically
./src/viscriptlint.py fix old_schema_viscript.json

# Fix with verbose output
./src/viscriptlint.py fix legacy_viscript.json --verbose
```

### Exit Codes

- `0`: Success (no errors, no warnings)
- `1`: Error (validation failed, invalid arguments, missing dependencies)
- `2`: Warning (validation passed with warnings)

### Script Integration

```bash
./src/viscriptlint.py validate file.json
case $? in
    0) echo "Validation passed" ;;
    1) echo "Validation failed" ;;
    2) echo "Validation passed with warnings" ;;
esac
```

## Schema Validation

The tool validates against the formal JSON Schema defined in `src/viscript_schema.json`:

- Required fields: `installation_type`, `version`, `phases`
- Check requirements: `name`, `description`, `command`, `validation_type`, `severity`
- Validation types: `return_value`, `output_pattern`, `both`, `none`
- Severity levels: `critical`, `informational`

## Helper Scripts

### Direct Script Usage

```bash
# Fix schema issues using Python
python3 ./src/fix_viscripts.py

# Fix specific file
python3 ./src/fix_viscripts.py my_viscript.json
```

## Testing

### Python Unit Tests

```bash
# Run all unit tests
cd unit-tests
python3 test_viscriptlint.py
python3 test_fix_viscripts.py

# Run specific test file
python3 -m unittest test_viscriptlint.TestViscriptLinter.test_validate_json_syntax_valid
python3 -m unittest test_fix_viscripts.TestFixViscripts.test_fix_viscript_file_with_critical_field
```

### Bash Integration Tests

```bash
# Run integration tests
./unit-tests/test_viscriptlint_integration.sh
```

## Dependencies

- `jq`: JSON processing (required)
- `ajv`: JSON Schema validation (optional, for formal schema validation)

## Documentation

See `docs/VISCRIPT_SCHEMA.md` for comprehensive schema documentation and examples. 