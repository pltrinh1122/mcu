# aiailint Source Code

## Overview

This directory contains the complete source code for the `aiailint` tool, organized into modular components for maintainability and extensibility.

## Directory Structure

```
src/
├── README.md                    # This file
├── aiailint.py                 # Main CLI tool entry point
├── aiai_schema.json            # Actual AIAI schema file
├── validators/                 # Validation modules
│   ├── syntax_validator.py    # YAML syntax validation
│   ├── schema_validator.py    # JSON Schema validation
│   ├── semantic_validator.py  # Shell command semantic analysis
│   ├── business_rules.py      # Business rule validation
│   └── cross_reference.py     # Cross-reference validation
├── analyzers/                  # Analysis modules
│   ├── bash_analyzer.py       # Bash command analysis
│   ├── destructive_detector.py # Destructive command detection
│   └── loop_detector.py       # Loop detection analysis
└── utils/                      # Utility modules
    ├── validation_result.py   # Data structures for validation results
    ├── output_formatter.py    # Text and JSON output formatting
    ├── error_formatter.py     # Error message formatting
    └── package_loader.py      # AIAI package loading and validation
```

## Architecture Overview

### Design Principles

1. **Modularity**: Each component has a single responsibility
2. **Extensibility**: Easy to add new validators and analyzers
3. **Testability**: All components are unit testable
4. **Safety First**: All validations prioritize operator safety
5. **Industry Standards**: Follows linting tool conventions

### Component Relationships

```
aiailint.py (Main CLI)
    ├── validators/ (Validation Pipeline)
    │   ├── syntax_validator.py
    │   ├── schema_validator.py
    │   ├── semantic_validator.py
    │   ├── business_rules.py
    │   └── cross_reference.py
    ├── analyzers/ (Analysis Engine)
    │   ├── bash_analyzer.py
    │   ├── destructive_detector.py
    │   └── loop_detector.py
    └── utils/ (Supporting Utilities)
        ├── validation_result.py
        ├── output_formatter.py
        ├── error_formatter.py
        └── package_loader.py
```

## Core Components

### 1. **Main Tool** (`aiailint.py`)
- **Purpose**: CLI interface and orchestration
- **Responsibilities**:
  - Parse command line arguments
  - Coordinate validation pipeline
  - Handle output formatting
  - Manage exit codes
  - Provide help and version information

### 2. **Validators** (`validators/`)
- **Purpose**: Perform specific types of validation
- **Common Interface**: All validators implement `validate(file_path)` method
- **Error Codes**: Each validator has specific error code ranges

#### Syntax Validator (`syntax_validator.py`)
- **Error Range**: E000-E099
- **Purpose**: YAML syntax and structure validation
- **Features**:
  - YAML parsing validation
  - File encoding checks
  - Basic structure validation
  - Unicode content handling

#### Schema Validator (`schema_validator.py`)
- **Error Range**: E100-E199
- **Purpose**: JSON Schema compliance validation
- **Features**:
  - Schema file loading
  - Required field validation
  - Data type checking
  - Constraint validation
  - Deprecated field detection

#### Semantic Validator (`semantic_validator.py`)
- **Error Range**: E200-E299
- **Purpose**: Shell command semantic analysis
- **Features**:
  - Command parsing and analysis
  - Security issue detection
  - Variable usage tracking
  - Command structure validation

#### Business Rules Validator (`business_rules.py`)
- **Error Range**: E300-E699
- **Purpose**: Business rule enforcement
- **Features**:
  - Destructive command validation
  - Logic check promotion suggestions
  - Safety rule enforcement
  - Best practice validation

#### Cross-Reference Validator (`cross_reference.py`)
- **Error Range**: E600-E699
- **Purpose**: Cross-reference and flow validation
- **Features**:
  - Circular reference detection
  - Unreachable code detection
  - Reference validation
  - Flow analysis

### 3. **Analyzers** (`analyzers/`)
- **Purpose**: Deep analysis of specific aspects
- **Common Interface**: All analyzers provide analysis methods

#### Bash Analyzer (`bash_analyzer.py`)
- **Purpose**: Shell command semantic analysis
- **Features**:
  - Command type classification
  - Destructive command detection
  - Logic check identification
  - Security issue detection
  - Variable extraction
  - Sudo usage detection
  - Redirection analysis

#### Destructive Detector (`destructive_detector.py`)
- **Purpose**: Identify destructive commands
- **Features**:
  - File system modification detection
  - System configuration changes
  - Network modifications
  - User account changes
  - Service modifications

#### Loop Detector (`loop_detector.py`)
- **Purpose**: Detect loops and circular references
- **Features**:
  - Infinite loop detection
  - Circular reference analysis
  - Script flow analysis
  - Dependency cycle detection

### 4. **Utilities** (`utils/`)
- **Purpose**: Supporting functionality and data structures

#### Validation Result (`validation_result.py`)
- **Purpose**: Data structures for validation results
- **Features**:
  - `ValidationResult` class
  - `LintIssue` class
  - Issue severity levels
  - Location tracking
  - Message formatting

#### Output Formatter (`output_formatter.py`)
- **Purpose**: Format validation results for output
- **Features**:
  - Text output formatting
  - JSON output formatting
  - Summary generation
  - Error categorization

#### Error Formatter (`error_formatter.py`)
- **Purpose**: Format error messages consistently
- **Features**:
  - Error code formatting
  - Location formatting
  - Message templating
  - Severity indicators

#### Package Loader (`package_loader.py`)
- **Purpose**: Load and validate AIAI packages
- **Features**:
  - Package structure validation
  - Manifest parsing
  - Script discovery
  - Metadata extraction

## Code Standards

### Python Standards
- **Python Version**: 3.8+
- **Style Guide**: PEP 8
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Comprehensive docstrings for all classes and methods
- **Error Handling**: Proper exception handling with meaningful messages

### Architecture Standards
- **Single Responsibility**: Each module has one clear purpose
- **Dependency Injection**: Minimize hard dependencies
- **Interface Consistency**: Common interfaces across similar components
- **Error Propagation**: Proper error handling and propagation
- **Logging**: Appropriate logging for debugging and monitoring

### Testing Standards
- **Unit Tests**: All components have unit tests
- **Test Coverage**: Aim for >90% code coverage
- **Test Data**: Comprehensive test data sets
- **Mocking**: Use mocks for external dependencies
- **Integration Tests**: End-to-end testing

## Development Workflow

### Adding New Components

#### 1. **Create Validator**
```python
# validators/new_validator.py
from typing import List
from pathlib import Path
from utils.validation_result import ValidationResult, LintIssue

class NewValidator:
    """New validation component"""
    
    def validate(self, file_path: Path) -> ValidationResult:
        """Validate the specified file"""
        result = ValidationResult()
        # Implementation here
        return result
```

#### 2. **Create Analyzer**
```python
# analyzers/new_analyzer.py
from typing import Any, Dict

class NewAnalyzer:
    """New analysis component"""
    
    def analyze(self, data: Any) -> Dict[str, Any]:
        """Analyze the provided data"""
        # Implementation here
        return {}
```

#### 3. **Update Main Tool**
```python
# aiailint.py
from validators.new_validator import NewValidator

# Add to validation pipeline
validators.append(NewValidator())
```

#### 4. **Add Tests**
```python
# unit-tests/test_new_validator.py
import unittest
from pathlib import Path
from validators.new_validator import NewValidator

class TestNewValidator(unittest.TestCase):
    def test_validation(self):
        # Test implementation
        pass
```

### Code Review Checklist
- [ ] Follows Python standards (PEP 8)
- [ ] Includes type hints
- [ ] Has comprehensive docstrings
- [ ] Includes unit tests
- [ ] Handles errors properly
- [ ] Uses consistent naming
- [ ] Follows architecture patterns
- [ ] Prioritizes safety

## Performance Considerations

### Optimization Strategies
1. **Lazy Loading**: Load resources only when needed
2. **Caching**: Cache expensive operations
3. **Parallel Processing**: Use multiprocessing for large files
4. **Memory Management**: Efficient data structures
5. **Early Exit**: Stop validation on critical errors

### Performance Targets
- **Small Files (< 1KB)**: < 100ms validation time
- **Medium Files (1-10KB)**: < 500ms validation time
- **Large Files (10-100KB)**: < 2s validation time
- **Memory Usage**: < 50MB for typical files

## Security Considerations

### Input Validation
- **File Paths**: Validate and sanitize file paths
- **YAML Content**: Safe YAML parsing
- **Command Analysis**: Secure command parsing
- **Package Validation**: Validate package integrity

### Output Sanitization
- **Error Messages**: Sanitize sensitive information
- **JSON Output**: Proper JSON escaping
- **File Operations**: Safe file handling

## Future Enhancements

### Planned Improvements
- **Plugin System**: Allow custom validators
- **Parallel Processing**: Multi-threaded validation
- **Caching**: Intelligent result caching
- **IDE Integration**: Language server support
- **Custom Rules**: User-defined validation rules

### Architecture Evolution
- **Microservices**: Split into separate services
- **API Interface**: REST API for integration
- **Database Backend**: Persistent result storage
- **Web Interface**: Browser-based validation

---

**Last Updated**: 2025-08-05  
**Code Status**: Framework Complete, Core Logic Implementation In Progress  
**Maintainer**: AIAI Core Developer Team 