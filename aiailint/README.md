# aiailint

## Overview

aiailint is a comprehensive validation and linting tool for AIAI (AI Augmented Installation) Scripts and packages. It provides syntax validation, schema compliance checking, semantic analysis, and business rule enforcement to ensure AIAI Scripts are safe, correct, and follow best practices.

## Features

- **Safety First**: Detects destructive commands and prevents unsafe operations
- **Comprehensive Validation**: YAML syntax, JSON Schema compliance, and semantic analysis
- **Business Rule Enforcement**: Validates destructive command marking and logic check patterns
- **Loop Detection**: Identifies infinite loops and circular references
- **Industry Standards**: CLI patterns, exit codes, and output formats following linting tool conventions
- **Multiple Output Formats**: Human-readable text and machine-readable JSON
- **Schema Synchronization**: Uses actual schema file for consistency

## Installation

### Prerequisites

```bash
# Required dependencies
pip install pyyaml jsonschema

# Bash parser (choose one)
pip install bashlex           # Recommended - most mature
pip install bashparser        # Alternative with enhanced features
pip install libbash          # Alternative with direct bash integration
```

### Install aiailint

```bash
# From the aiai/design/tools/aiailint directory
chmod +x src/aiailint.py

# Add to PATH or create symlink
ln -s /path/to/aiai/design/tools/aiailint/src/aiailint.py /usr/local/bin/aiailint
```

## Usage

### Basic Validation

```bash
# Validate a single AIAI Script file
aiailint validate script.yaml
aiailint script.yaml  # Backward compatible

# Verbose output
aiailint validate script.yaml --verbose

# Strict mode (warnings as errors)
aiailint validate script.yaml --strict

# JSON output for CI/CD
aiailint validate script.yaml --format json
```

### Package Validation

```bash
# Validate entire AIAI package
aiailint validate --package /path/to/aiai-package/
aiailint --package /path/to/aiai-package/  # Shorthand

# Package validation with JSON output
aiailint validate --package ubuntu-btrfs-aiai/ --format json
```

### Specialized Validation

```bash
# Business rules only
aiailint validate script.yaml --business-rules-only

# Skip semantic analysis (faster)
aiailint validate script.yaml --no-semantic

# Combine options
aiailint validate --package pkg/ --strict --format json --verbose
```

## Validation Types

### 1. Syntax Validation (E000-E099)
- YAML parsing and structure validation
- File encoding and basic properties
- Structural depth and complexity checks

### 2. Schema Validation (E100-E199)  
- JSON Schema compliance against aiai_schema.json
- Required field validation
- Data type and constraint checking
- Deprecated field detection

### 3. Semantic Validation (E200-E299)
- Shell command parsing using bash parsers
- Command structure and safety analysis
- Security issue detection
- Variable usage tracking

### 4. Business Rules (E300-E699)
- **BR001**: Destructive command validation (E301-E399)
- **BR002**: Logic check promotion suggestions (W401-W499)
- **BR003**: Loop detection (E501-E599)
- **BR004**: Cross-reference validation (E601-E699)

## Examples

### Destructive Command Detection

```yaml
# ❌ Will trigger E301 error
- type: "command"
  id: "cleanup-temp"
  shellCommand: "rm -rf /tmp/installation-backup"
  destructive: false  # Should be true!

# ✅ Correctly marked
- type: "command"
  id: "cleanup-temp"
  shellCommand: "rm -rf /tmp/installation-backup"
  destructive: true
```

### Logic Check Promotion

```yaml
# ⚠ Will trigger W401 warning
- type: "command"
  id: "check-sudo"
  shellCommand: "[ -n \"$SUDO_USER\" ] && echo 'sudo_active' || echo 'no_sudo'"

# ✅ Better as validation element
- type: "validation"
  id: "check-sudo"
  command: "[ -n \"$SUDO_USER\" ] && echo 'sudo_active' || echo 'no_sudo'"
  expected_output: "sudo_active"
```

## Output Formats

### Text Format (Human-readable)

```
=== Validating AIAI Script: script.yaml ===

✗ Validation failed with 1 error(s)

ERRORS:
  ✗ E301: Destructive command not marked as destructive: cleanup-temp (File removal) at body[0].body[1]
    Command: rm -rf /tmp/installation-backup
    Fix: Add 'destructive: true' to this command

SUMMARY:
  Files Processed: 1
  Errors: 1
  Warnings: 0

Validation FAILED due to errors.
```

### JSON Format (Machine-readable)

```json
{
  "aiailint_version": "1.0.0",
  "timestamp": "2025-08-05T10:30:00Z",
  "target": {
    "path": "script.yaml",
    "type": "file"
  },
  "validation": {
    "status": "failed",
    "errors": 1,
    "warnings": 0
  },
  "issues": [
    {
      "severity": "error",
      "code": "E301",
      "message": "Destructive command not marked as destructive",
      "location": "body[0].body[1]"
    }
  ],
  "exit_code": 1
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: AIAI Script Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Install dependencies
      run: pip install pyyaml jsonschema bashlex
    - name: Validate AIAI Scripts
      run: |
        aiailint validate src/aiaiScript/ --format json --strict
```

## Error Codes

- **E000-E099**: Critical syntax errors
- **E100-E199**: Schema validation errors  
- **E200-E299**: Semantic validation errors
- **E300-E399**: Destructive command violations
- **W400-W499**: Logic check warnings
- **E500-E599**: Loop detection errors
- **E600-E699**: Cross-reference errors

## Exit Codes

- `0`: Success (no errors, no warnings)
- `1`: Error (validation failed)
- `2`: Warning (validation passed with warnings)

## Development

### Architecture

```
aiailint/
├── src/
│   ├── aiailint.py              # Main tool
│   ├── aiai_schema.json         # Actual schema file
│   ├── validators/              # Validation modules
│   │   ├── syntax_validator.py
│   │   ├── schema_validator.py
│   │   ├── semantic_validator.py
│   │   ├── business_rules.py
│   │   └── cross_reference.py
│   ├── analyzers/               # Analysis modules
│   │   ├── bash_analyzer.py
│   │   ├── destructive_detector.py
│   │   └── loop_detector.py
│   └── utils/                   # Utility modules
│       ├── validation_result.py
│       ├── output_formatter.py
│       ├── error_formatter.py
│       └── package_loader.py
├── unit-tests/                  # Test suite
│   ├── test_data/              # Test data files
│   ├── test_*.py              # Test modules
│   └── run_tests.py           # Test runner
└── docs/                       # Documentation
```

### Schema Synchronization

The tool uses the actual AIAI schema file to ensure consistency:

```bash
# Schema file is an actual file
ls -la src/aiai_schema.json
# -rw-rw-r-- 1 user user 23900 Aug  6 16:28 aiai_schema.json
```

This ensures that:
- **Single Source of Truth**: Schema file is maintained in the tool
- **Direct Access**: No dependency on external soft links
- **Prevents Schema Drift**: Schema is version controlled with the tool

### Running Tests

```bash
cd aiai/design/tools/aiailint
python3 unit-tests/run_tests.py
```

### Current Implementation Status

#### ✅ **Completed Components:**
- **Framework Architecture**: Complete module structure and CLI interface
- **Syntax Validator**: YAML syntax validation with error handling
- **Schema Validator**: JSON Schema validation framework
- **Bash Analyzer**: Shell command parsing and analysis framework
- **Business Rules**: Framework for destructive command and logic check validation
- **Cross-Reference**: Framework for circular reference detection
- **Package Loader**: AIAI package loading and validation
- **Output Formatters**: Text and JSON output formatting
- **Test Framework**: Comprehensive test suite with 70+ test cases

#### 🔄 **In Progress:**
- **Core Validation Logic**: Implementation of actual validation algorithms
- **Destructive Command Detection**: Command analysis and classification
- **Logic Check Promotion**: Identification and suggestion logic
- **Cross-Reference Validation**: Circular reference detection algorithms

#### 📋 **Planned Features:**
- **Enhanced Security Analysis**: Advanced security issue detection
- **Performance Optimization**: Faster validation for large scripts
- **IDE Integration**: Editor plugins and language server support
- **Custom Rule Engine**: User-defined validation rules

## Contributing

### Development Guidelines

1. **Test-Driven Development**: Write tests before implementing features
2. **Safety First**: All business rules prioritize operator safety
3. **Schema Compliance**: Maintain compatibility with AIAI schema
4. **Documentation**: Update docs for new features
5. **Code Style**: Follow existing patterns and conventions

### Adding New Validators

1. **Create Validator Module**: Add to `src/validators/`
2. **Add Tests**: Create comprehensive test suite
3. **Update Main Tool**: Integrate with validation pipeline
4. **Update Documentation**: Document new validation types

### Testing

```bash
# Run all tests
python3 unit-tests/run_tests.py

# Run specific test module
python3 unit-tests/run_tests.py test_syntax_validator

# Run with coverage
coverage run unit-tests/run_tests.py
coverage report
```

## License

This project follows the same license as the AIAI framework.

---

**Last Updated**: 2025-08-05  
**Version**: 1.0.0  
**Status**: Framework Complete, Core Logic Implementation In Progress