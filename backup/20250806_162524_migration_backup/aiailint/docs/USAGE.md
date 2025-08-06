# AIAI Script Linter Usage Guide

## Overview

The AIAI Script Linter (`aiailint`) provides comprehensive validation and linting functionality for AIAI Scripts.

## Features

- **Syntax Validation**: Validates AIAI Scripts against the specification
- **Best Practices**: Enforces coding standards and best practices
- **Error Detection**: Identifies common issues and provides helpful error messages
- **CI/CD Integration**: Designed for integration with CI/CD pipelines

## Installation

```bash
cd aiailint
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
# Validate a single script
python src/validator.py path/to/script.yaml

# Validate all scripts in a directory
python src/validator.py path/to/scripts/directory

# Validate with custom schema
python src/validator.py --schema custom-schema.json script.yaml
```

### Python API

```python
from aiailint.src.validator import AIAIScriptValidator

# Initialize validator
validator = AIAIScriptValidator()

# Validate a script
is_valid = validator.validate_script("path/to/script.yaml")

# Validate a directory
is_valid = validator.validate_directory("path/to/scripts/")
```

## Configuration

The linter can be configured through:

1. **Schema File**: Specify a custom schema file
2. **Rules File**: Define custom linting rules
3. **Ignore File**: Specify files to ignore during validation

## Integration

### GitHub Actions

```yaml
- name: Lint AIAI Scripts
  run: |
    cd aiailint
    python src/validator.py ../packages/*/src/*.yaml
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: aiai-lint
        name: AIAI Script Linter
        entry: python aiailint/src/validator.py
        language: python
        files: \.yaml$
```

## Error Codes

- `E001`: Missing metadata section
- `E002`: Missing steps section
- `E003`: Invalid YAML syntax
- `E004`: Schema validation failed
- `W001`: Deprecated feature usage

## Contributing

See the main repository documentation for contribution guidelines. 