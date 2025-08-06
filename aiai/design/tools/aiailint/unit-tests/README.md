# aiailint Unit Tests

## Overview

This directory contains comprehensive unit tests for the `aiailint` tool, covering all major components and functionality. The test suite is designed to guide the implementation of core validation logic through test-driven development.

## Test Structure

```
unit-tests/
├── test_data/                    # Test data files
│   ├── valid_scripts/           # Valid AIAI Scripts for testing
│   ├── invalid_scripts/         # Invalid AIAI Scripts for testing
│   └── test_packages/           # Test package structures
├── test_*.py                    # Individual test modules
├── run_tests.py                 # Test runner script
└── README.md                    # This file
```

## Test Categories

### 1. **Syntax Validator Tests** (`test_syntax_validator.py`)
- **Purpose**: Test YAML syntax validation
- **Status**: ✅ Framework Complete
- **Coverage**:
  - Valid YAML syntax
  - Invalid YAML syntax
  - Missing required fields
  - Unicode content handling
  - File validation
  - Error handling

### 2. **Schema Validator Tests** (`test_schema_validator.py`)
- **Purpose**: Test AIAI Script schema validation
- **Status**: ✅ Framework Complete
- **Coverage**:
  - Valid schema compliance
  - Missing required metadata
  - Invalid element types
  - Invalid field types
  - Validation elements
  - Script elements
  - File validation

### 3. **Bash Analyzer Tests** (`test_bash_analyzer.py`)
- **Purpose**: Test semantic analysis of shell commands
- **Status**: 🔄 Implementation In Progress
- **Coverage**:
  - Simple command analysis
  - Destructive command detection
  - Read-only command validation
  - Logic check detection
  - Sudo usage detection
  - Variable extraction
  - Redirection detection
  - Pipeline detection
  - Security issue detection
  - False positive prevention

### 4. **Business Rules Tests** (`test_business_rules.py`)
- **Purpose**: Test business rule validation
- **Status**: 🔄 Implementation In Progress
- **Coverage**:
  - Unmarked destructive commands
  - False destructive flags
  - Logic check promotion suggestions
  - Properly marked commands
  - Validation elements
  - Read-only commands
  - Mixed script validation

### 5. **Cross-Reference Tests** (`test_cross_reference.py`)
- **Purpose**: Test cross-reference and flow validation
- **Status**: 🔄 Implementation In Progress
- **Coverage**:
  - Valid references
  - Missing references
  - Circular reference detection
  - Unreachable elements
  - Self-references
  - Complex circular references
  - Scripts without references

### 6. **Package Loader Tests** (`test_package_loader.py`)
- **Purpose**: Test AIAI package loading and validation
- **Status**: ✅ Framework Complete
- **Coverage**:
  - Valid package structure
  - Missing required files
  - Invalid manifest format
  - Missing AIAI scripts
  - Empty scripts directory
  - Invalid script files
  - Package metadata extraction
  - File discovery

### 7. **Integration Tests** (`test_aiailint_integration.py`)
- **Purpose**: Test complete tool functionality
- **Status**: 🔄 Implementation In Progress
- **Coverage**:
  - Basic file validation
  - Invalid file handling
  - Destructive command validation
  - JSON output format
  - Package validation
  - Help output
  - Command line options
  - Error handling
  - Verbose output
  - Multiple validation issues
  - Circular reference detection
  - Logic check suggestions

## Test Data

### Valid Scripts (`test_data/valid_scripts/`)
- `basic_validation.yaml` - Basic valid AIAI Script
- `destructive_commands.yaml` - Script with properly marked destructive commands
- `logic_checks.yaml` - Script with logic checks for promotion testing
- `readonly_commands.yaml` - Script with read-only commands

### Invalid Scripts (`test_data/invalid_scripts/`)
- `syntax_error.yaml` - YAML syntax errors
- `unmarked_destructive.yaml` - Destructive commands not properly marked
- `false_destructive.yaml` - Commands incorrectly marked as destructive
- `circular_reference.yaml` - Scripts with circular references

### Test Packages (`test_data/test_packages/`)
- `valid_package/` - Complete valid AIAI package structure

## Running Tests

### Run All Tests
```bash
cd aiai/design/tools/aiailint/unit-tests
python3 run_tests.py
```

### Run Specific Test Module
```bash
python3 run_tests.py test_syntax_validator
```

### List Available Tests
```bash
python3 run_tests.py --list
```

### Run Individual Test File
```bash
python3 -m unittest test_syntax_validator.py -v
```

### Run with Coverage (if coverage.py is installed)
```bash
coverage run run_tests.py
coverage report
coverage html  # Generate HTML report
```

## Test Dependencies

### Required Python Packages
- `unittest` (built-in)
- `pathlib` (built-in)
- `tempfile` (built-in)
- `subprocess` (built-in)
- `json` (built-in)
- `yaml` - For YAML parsing
- `jsonschema` - For schema validation
- `bashlex` - For bash command parsing

### Optional Dependencies
- `coverage` - For code coverage analysis
- `pytest` - Alternative test runner

## Test Environment Setup

### 1. Install Dependencies
```bash
pip3 install pyyaml jsonschema bashlex
```

### 2. Set Up Test Environment
```bash
cd aiai/design/tools/aiailint
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### 3. Verify Test Data
```bash
ls -la unit-tests/test_data/
```

## Current Test Status

### ✅ **Passing Tests (Framework Complete)**
- **Syntax Validator**: YAML parsing and basic structure validation
- **Schema Validator**: JSON Schema validation framework
- **Package Loader**: AIAI package loading and validation

### 🔄 **Failing Tests (Implementation In Progress)**
- **Bash Analyzer**: Core command analysis logic needs implementation
- **Business Rules**: Destructive command detection and logic check promotion
- **Cross-Reference**: Circular reference and unreachable code detection
- **Integration Tests**: End-to-end validation pipeline

### 📊 **Test Statistics**
- **Total Tests**: 70+ test cases
- **Framework Tests**: 25+ tests (passing)
- **Implementation Tests**: 45+ tests (failing - guiding development)
- **Coverage**: Comprehensive test scenarios defined

## Test Results Interpretation

### Exit Codes
- `0` - All tests passed
- `1` - One or more tests failed

### Output Format
```
test_name (test_module.TestClass) ... ok
test_name (test_module.TestClass) ... FAIL
test_name (test_module.TestClass) ... ERROR

================================================================================
TEST SUMMARY
================================================================================
Tests run: 45
Failures: 2
Errors: 1
Skipped: 0
```

### Common Test Issues

#### 1. **Import Errors**
- **Cause**: Missing dependencies or incorrect Python path
- **Solution**: Install required packages and set PYTHONPATH

#### 2. **File Not Found Errors**
- **Cause**: Test data files missing
- **Solution**: Ensure test_data directory structure is complete

#### 3. **Assertion Failures**
- **Cause**: Test expectations not met (expected during development)
- **Solution**: Implement missing functionality to make tests pass

## Implementation Guidance

### Test-Driven Development Approach

The failing tests serve as a specification for what needs to be implemented:

#### 1. **Bash Analyzer Implementation**
```python
# Tests expect these attributes in CommandAnalysis:
analysis.is_destructive      # Boolean flag
analysis.is_logic_check      # Boolean flag  
analysis.command_type        # String: 'simple', 'pipeline', 'list', 'conditional'
analysis.uses_sudo          # Boolean flag
analysis.variables          # List of variable names
analysis.has_redirections   # Boolean flag
analysis.has_security_issues # Boolean flag
```

#### 2. **Business Rules Implementation**
```python
# Tests expect validation of:
- Commands marked destructive but not actually destructive
- Commands not marked destructive but actually destructive
- Logic checks that should be promoted to validation elements
```

#### 3. **Cross-Reference Implementation**
```python
# Tests expect detection of:
- Circular references between scripts
- Unreachable script elements
- Missing script references
```

## Adding New Tests

### 1. Create Test File
```python
#!/usr/bin/env python3
"""
Unit tests for NewComponent
"""

import unittest
from pathlib import Path
import sys

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from validators.new_component import NewComponentValidator


class TestNewComponentValidator(unittest.TestCase):
    """Test cases for NewComponentValidator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = NewComponentValidator()
    
    def test_specific_functionality(self):
        """Test specific functionality"""
        # Test implementation
        pass


if __name__ == '__main__':
    unittest.main()
```

### 2. Add Test Data
Create appropriate test data files in `test_data/` directories.

### 3. Update Test Runner
The test runner automatically discovers tests with the pattern `test_*.py`.

## Continuous Integration

### GitHub Actions Example
```yaml
name: aiailint Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install pyyaml jsonschema bashlex
      - name: Run tests
        run: |
          cd aiai/design/tools/aiailint/unit-tests
          python3 run_tests.py
```

## Performance Considerations

### Test Execution Time
- **Unit Tests**: < 1 second per test
- **Integration Tests**: 1-5 seconds per test
- **Full Test Suite**: 30-60 seconds

### Memory Usage
- **Individual Tests**: < 10MB
- **Full Test Suite**: < 100MB

### Optimization Tips
1. Use `setUp()` and `tearDown()` for shared resources
2. Mock external dependencies
3. Use temporary files for file-based tests
4. Clean up resources in `tearDown()`

## Troubleshooting

### Common Issues

#### 1. **Module Import Errors**
```bash
# Solution: Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

#### 2. **Test Data Not Found**
```bash
# Solution: Check test data structure
ls -la unit-tests/test_data/
```

#### 3. **Permission Errors**
```bash
# Solution: Make test runner executable
chmod +x unit-tests/run_tests.py
```

### Debug Mode
```bash
# Run with verbose output
python3 -m unittest test_syntax_validator.py -v

# Run with debugger
python3 -m pdb run_tests.py
```

## Contributing

### Test Guidelines
1. **Naming**: Use descriptive test method names
2. **Isolation**: Each test should be independent
3. **Coverage**: Aim for >90% code coverage
4. **Documentation**: Document complex test scenarios
5. **Maintenance**: Keep tests up-to-date with code changes

### Test Review Checklist
- [ ] Tests cover all major functionality
- [ ] Edge cases are tested
- [ ] Error conditions are tested
- [ ] Test data is appropriate
- [ ] Tests are readable and maintainable
- [ ] Performance is acceptable
- [ ] Documentation is complete

### Implementation Priority
1. **High Priority**: Make failing tests pass by implementing core logic
2. **Medium Priority**: Add edge case tests for robustness
3. **Low Priority**: Performance optimization and advanced features

---

**Last Updated**: 2025-08-05  
**Test Coverage**: Comprehensive unit and integration tests  
**Implementation Status**: Framework Complete, Core Logic Implementation In Progress  
**Maintainer**: AIAI Core Developer Team 