# aiailint Specification
Version: 1.0  
Date: 2025-08-05

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Validation Types](#3-validation-types)
4. [Business Rules](#4-business-rules)
5. [Command Line Interface](#5-command-line-interface)
6. [Output Formats](#6-output-formats)
7. [Error Codes](#7-error-codes)
8. [Dependencies](#8-dependencies)
9. [Implementation Guidelines](#9-implementation-guidelines)
10. [Integration](#10-integration)
11. [Future Requirements](#11-future-requirements)

---

## 1. Overview

### 1.1 Purpose

aiailint is a comprehensive validation and linting tool for AIAI (AI Augmented Installation) Scripts and packages. It provides syntax validation, schema compliance checking, semantic analysis, and business rule enforcement to ensure AIAI Scripts are safe, correct, and follow best practices.

### 1.2 Goals

**Primary Goals:**
- **Safety First**: Prevent destructive outcomes by identifying potentially dangerous commands
- **Schema Compliance**: Validate AIAI Scripts against the formal schema definition
- **Business Rule Enforcement**: Ensure scripts follow AIAI best practices and conventions
- **Loop Prevention**: Detect infinite loops and circular references that could cause system issues
- **Command Classification**: Automatically identify and validate command types and attributes

**Secondary Goals:**
- **Package Validation**: Support validation of complete AIAI packages with MANIFEST files
- **Industry Standards**: Follow linting tool conventions for output, exit codes, and CLI patterns
- **CI/CD Integration**: Provide machine-readable output for automated workflows
- **Developer Experience**: Clear, actionable error messages with precise location information

### 1.3 Scope

**In Scope:**
- Individual AIAI Script file validation (`.yaml` files)
- Complete AIAI Package validation (directory with MANIFEST)
- Syntax validation (YAML parsing)
- Schema validation (JSON Schema compliance)
- Semantic analysis of shell commands using bash parser
- Business rule validation (destructive commands, loops, classification)
- Cross-reference validation (script and command ID resolution)
- Output in both human-readable (text) and machine-readable (JSON) formats

**Out of Scope:**
- Runtime execution of commands or scripts
- Dynamic analysis requiring system state
- Performance optimization of scripts
- Alternative output formats beyond text and JSON
- Automatic fixing of validation errors (separate tool)

---

## 2. Architecture

### 2.1 Design Principles

**Single-Pass Validation Pipeline:**
Following the proven viscriptlint architecture, aiailint uses a single-pass validation algorithm with parallel validation phases for optimal performance and maintainability.

**Modular Validation System:**
Each validation type operates independently on the same parsed data structure, enabling:
- Independent development and testing of validation rules
- Parallel execution of validation phases
- Easy addition of new validation types
- Clear separation of concerns

**Fail-Fast Safety Model:**
Critical validation errors immediately abort processing to prevent unsafe operations, while warnings and informational messages allow continued validation for comprehensive reporting.

### 2.2 Core Components

```
aiailint/
├── src/
│   ├── aiailint.py           # Main tool with subcommand architecture
│   ├── aiai_schema.json      # AIAI Schema definition (from core/)
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── syntax_validator.py      # YAML syntax validation
│   │   ├── schema_validator.py      # JSON Schema compliance
│   │   ├── semantic_validator.py    # Shell command analysis
│   │   ├── business_rules.py        # Business rule enforcement
│   │   └── cross_reference.py       # ID resolution and loop detection
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── bash_analyzer.py         # Shell command semantic analysis
│   │   ├── destructive_detector.py  # Destructive command detection
│   │   └── loop_detector.py         # Loop and circular reference detection
│   └── utils/
│       ├── __init__.py
│       ├── package_loader.py        # AIAI Package loading and validation
│       ├── error_formatter.py       # Error message formatting
│       └── output_formatter.py      # Text and JSON output formatting
├── docs/
│   ├── AIAILINT_SPECIFICATION.md    # This specification
│   └── SCHEMA_VALIDATION_RULES.md   # Detailed validation rules
└── unit-tests/
    ├── test_aiailint.py
    ├── test_validators/
    ├── test_analyzers/
    └── test_data/
        ├── valid_scripts/
        ├── invalid_scripts/
        └── test_packages/
```

### 2.3 Validation Pipeline

**Stage 1: Input Processing**
```
File/Package → Parse Type → Load Components → Basic Validation
```

**Stage 2: Parallel Validation Phases**
```
Parsed Data → [Syntax, Schema, Semantic, Business Rules, Cross-Reference] → Results
```

**Stage 3: Result Aggregation**
```
Validation Results → Severity Classification → Output Formatting → Exit Code
```

---

## 3. Validation Types

### 3.1 Syntax Validation

**Purpose**: Ensure AIAI Scripts are valid YAML files that can be parsed.

**Implementation**:
- Use Python's `yaml.safe_load()` for parsing
- Capture and report YAML syntax errors with line/column information
- Validate file encoding and basic file system properties

**Error Conditions**:
- Invalid YAML syntax
- File not found or unreadable
- Empty files
- Encoding issues

**Error Codes**: `E000-E099` (Critical syntax errors)

### 3.2 Schema Validation

**Purpose**: Validate AIAI Scripts against the formal JSON Schema definition.

**Implementation**:
- Convert parsed YAML to JSON-compatible structure
- Validate against `aiai_schema.json` using `jsonschema` library
- Report schema violations with precise JSON path information
- Validate required fields, data types, and constraints

**Error Conditions**:
- Missing required fields
- Invalid data types
- Constraint violations
- Unknown or deprecated fields

**Error Codes**: `E100-E199` (Schema validation errors)

### 3.3 Semantic Validation

**Purpose**: Analyze shell commands for semantic correctness and safety.

**Implementation**:
- Use `bashlex` library for parsing shell commands into AST
- Analyze command structure, arguments, and control flow
- Detect command types (assignments, conditionals, pipes, etc.)
- Validate command semantics and potential issues

**Dependencies**:
- `bashlex` (primary) - Python port of GNU bash parser
- `bashparser` (fallback) - Enhanced bash parsing with semantic analysis
- `libbash` (alternative) - Python bindings to bash AST

**Error Conditions**:
- Unparseable shell commands
- Invalid command syntax
- Potentially unsafe command patterns
- Unrecognized command structures

**Error Codes**: `E200-E299` (Semantic validation errors)

---

## 4. Business Rules

### 4.1 Destructive Command Validation (Priority 1)

**Rule BR001**: Commands that perform destructive operations MUST be marked with `destructive: true`.

**Detection Criteria**:
```python
DESTRUCTIVE_PATTERNS = {
    # File system operations
    'rm', 'rmdir', 'unlink', 'shred',
    'dd', 'fdisk', 'parted', 'mkfs', 'format',
    'mv', 'cp -f', 'rsync --delete',
    
    # System modifications
    'sudo', 'su', 'passwd', 'chown', 'chmod',
    'mount', 'umount', 'swapon', 'swapoff',
    'systemctl stop', 'systemctl disable', 'systemctl mask',
    'service stop', 'service disable',
    
    # Package management
    'apt remove', 'apt purge', 'apt autoremove',
    'yum remove', 'dnf remove', 'pacman -R',
    'snap remove', 'flatpak uninstall',
    
    # Process management
    'kill', 'killall', 'pkill', 'xkill',
    
    # Network operations
    'iptables -D', 'iptables -F', 'ufw delete',
    'ifconfig down', 'ip link delete'
}

DESTRUCTIVE_COMMAND_PATTERNS = [
    r'rm\s+.*-[rf]',     # rm with recursive or force flags
    r'dd\s+.*of=',       # dd with output file
    r'>\s*/dev/',        # Redirecting to device files
    r'mkfs\.',           # Any mkfs command
    r'parted.*rm',       # Parted partition removal
    r'systemctl.*stop|disable|mask',  # Service stopping
]
```

**Validation Logic**:
1. Parse shell command using bash parser
2. Extract command name and arguments from AST
3. Check command against destructive patterns
4. If destructive operation detected but `destructive: false` or unset → Error
5. If `destructive: true` but no destructive operation detected → Warning

**Error Codes**:
- `E301`: Destructive command not marked as destructive
- `W301`: Command marked destructive but appears safe
- `E302`: Cannot analyze command for destructive operations

### 4.2 Logic Check Promotion (Priority 1)

**Rule BR002**: Commands containing logic checks SHOULD be promoted to validation elements.

**Detection Criteria**:
```python
LOGIC_CHECK_PATTERNS = [
    # Test command patterns
    r'\[\s+.*\s+\]',              # [ condition ]
    r'\[\[\s+.*\s+\]\]',          # [[ condition ]]
    r'test\s+',                   # test command
    
    # Conditional operators
    r'&&||\|\|',                  # && or ||
    r'if\s+.*;.*then',            # if-then constructs
    r'case\s+.*in',               # case statements
    
    # File/directory tests
    r'-[a-z]\s+\$?\w+',          # -f, -d, -e, etc.
    r'\$\?\s*[!=]=',             # Exit code checks
    
    # Variable checks
    r'\[\s*-[nz]\s+\$',          # -n or -z variable tests
    r'\$\{.*:-.*\}',             # Parameter expansion with defaults
]
```

**Validation Logic**:
1. Parse command into AST using bash parser
2. Analyze AST for conditional constructs and logical operators
3. Detect file tests, variable checks, and exit code evaluations
4. If logic check detected → Suggest promotion to validation element
5. Check if equivalent validation element exists

**Error Codes**:
- `W401`: Command contains logic check, consider validation element
- `I401`: Logic check pattern detected in command

### 4.3 Loop Detection (Priority 1)

**Rule BR003**: Scripts MUST NOT contain infinite loops or circular references.

**Detection Scope**:
- **Intra-Script Loops**: Commands referencing each other within a script
- **Inter-Script Loops**: Circular references between scripts in BR paths
- **Self-References**: Scripts or commands referencing themselves

**Detection Algorithm**:
```python
def detect_loops(aiai_script):
    # Build dependency graph
    graph = build_dependency_graph(aiai_script)
    
    # Detect cycles using DFS
    visited = set()
    rec_stack = set()
    
    for node in graph:
        if detect_cycle_dfs(node, visited, rec_stack, graph):
            return True
    return False

def build_dependency_graph(script):
    """Build directed graph of dependencies"""
    graph = {}
    
    # Add command references in conditionals
    for conditional in find_conditionals(script):
        source = conditional['condition']['source']
        if source in graph:
            graph[source].extend(get_conditional_targets(conditional))
    
    # Add script references in BR paths
    for br_path in find_br_paths(script):
        for i, script_id in enumerate(br_path):
            if i + 1 < len(br_path):
                if script_id not in graph:
                    graph[script_id] = []
                graph[script_id].append(br_path[i + 1])
    
    return graph
```

**Error Conditions**:
- Circular references in BR paths
- Commands referencing each other in conditionals
- Self-referential scripts or commands
- Unreachable commands due to malformed flow

**Error Codes**:
- `E501`: Circular reference detected in BR paths
- `E502`: Infinite loop in command references
- `E503`: Self-referential script or command
- `W501`: Potentially unreachable command detected

### 4.4 Cross-Reference Validation

**Rule BR004**: All script and command references MUST be resolvable.

**Validation Logic**:
1. Collect all script and command IDs from the AIAI Script
2. Collect all references in conditionals and BR paths
3. Verify each reference resolves to an existing ID
4. Check for duplicate IDs
5. Validate reference context (commands in conditionals, scripts in BR paths)

**Error Codes**:
- `E601`: Unresolved script reference in BR path
- `E602`: Unresolved command reference in conditional
- `E603`: Duplicate script or command ID
- `W601`: Unused script or command definition

---

## 5. Command Line Interface

### 5.1 Subcommand Architecture

Following viscriptlint patterns for consistency:

```bash
# File validation (default mode)
aiailint validate script.yaml
aiailint script.yaml  # Backward compatible

# Package validation
aiailint validate --package /path/to/aiai-package/
aiailint --package /path/to/aiai-package/  # Shorthand

# Verbose output
aiailint validate script.yaml --verbose

# Strict mode (warnings as errors)
aiailint validate script.yaml --strict

# JSON output for CI/CD
aiailint validate script.yaml --format json

# Help
aiailint help
aiailint help validate
aiailint --help
```

### 5.2 Options and Flags

**Global Options:**
- `--verbose, -v`: Detailed validation output with explanations
- `--strict`: Treat warnings as errors (changes exit code)
- `--format FORMAT`: Output format (`text` or `json`)
- `--help, -h`: Show help information

**Validation Options:**
- `--package, -p`: Validate entire AIAI package instead of single file
- `--schema PATH`: Use custom schema file for validation
- `--no-semantic`: Skip semantic analysis (syntax and schema only)
- `--business-rules-only`: Run only business rule validation
- `--config FILE`: Load configuration from file

**Examples:**
```bash
# Basic validation
aiailint validate btrfs_system_validation_aiaiScript.yaml

# Package validation with JSON output
aiailint validate --package ubuntu-btrfs-aiai/ --format json

# Strict validation for CI/CD
aiailint validate scripts/ --strict --format json

# Skip semantic analysis for faster validation
aiailint validate script.yaml --no-semantic

# Verbose business rules check
aiailint validate script.yaml --business-rules-only --verbose
```

---

## 6. Output Formats

### 6.1 Text Format (Default)

**Human-readable output** with colors, formatting, and detailed explanations:

```
=== Validating AIAI Script: btrfs_system_validation_aiaiScript.yaml ===

✓ YAML Syntax: Valid
✓ Schema Validation: Passed
⚠ Semantic Analysis: 2 warnings
✗ Business Rules: 1 error

ERRORS:
  E301 [Line 59]: Destructive command not marked as destructive
    Command: "rm -rf /tmp/installation-backup"
    Location: body[0].body[1].shellCommand
    Fix: Add 'destructive: true' to this command
    
WARNINGS:
  W401 [Line 43]: Command contains logic check, consider validation element
    Command: "[ -n \"$SUDO_USER\" ] && echo 'sudo_active' || echo 'no_sudo'"
    Location: body[0].body[0].shellCommand
    Suggestion: Convert to validation element with expected_output
    
  W501 [Line 78]: Potentially unreachable command detected
    Command ID: "disk-model-info"
    Reason: No conditional path leads to this command
    
SUMMARY:
  Files Processed: 1
  Errors: 1
  Warnings: 2
  Info: 0
  
Validation FAILED due to errors. Use --strict to treat warnings as errors.
```

### 6.2 JSON Format

**Machine-readable output** for CI/CD integration:

```json
{
  "aiailint_version": "1.0.0",
  "timestamp": "2025-08-05T10:30:00Z",
  "files": [
    {
      "path": "btrfs_system_validation_aiaiScript.yaml",
      "status": "failed",
      "validation_phases": {
        "syntax": {"status": "passed", "errors": []},
        "schema": {"status": "passed", "errors": []},
        "semantic": {"status": "warning", "errors": [], "warnings": 2},
        "business_rules": {"status": "failed", "errors": 1, "warnings": 0}
      },
      "issues": [
        {
          "code": "E301",
          "severity": "error",
          "message": "Destructive command not marked as destructive",
          "location": {
            "line": 59,
            "path": "body[0].body[1].shellCommand",
            "command": "rm -rf /tmp/installation-backup"
          },
          "fix_suggestion": "Add 'destructive: true' to this command"
        },
        {
          "code": "W401", 
          "severity": "warning",
          "message": "Command contains logic check, consider validation element",
          "location": {
            "line": 43,
            "path": "body[0].body[0].shellCommand",
            "command": "[ -n \"$SUDO_USER\" ] && echo 'sudo_active' || echo 'no_sudo'"
          },
          "fix_suggestion": "Convert to validation element with expected_output"
        }
      ]
    }
  ],
  "summary": {
    "total_files": 1,
    "passed": 0,
    "failed": 1,
    "errors": 1,
    "warnings": 2,
    "info": 0
  },
  "exit_code": 1
}
```

---

## 7. Error Codes

### 7.1 Code Categories

Following industry standards and viscriptlint patterns:

**Critical Errors (E000-E099)**: Syntax and parsing failures
- `E000`: YAML syntax error
- `E001`: File not found or unreadable
- `E002`: Empty file
- `E003`: Invalid file encoding

**Schema Errors (E100-E199)**: JSON Schema violations
- `E100`: Missing required field
- `E101`: Invalid data type
- `E102`: Constraint violation
- `E103`: Unknown field
- `E104`: Deprecated field usage

**Semantic Errors (E200-E299)**: Shell command analysis failures
- `E200`: Unparseable shell command
- `E201`: Invalid command syntax
- `E202`: Unsupported shell construct
- `E203`: Command analysis timeout

**Business Rule Errors (E300-E399)**: Destructive command violations
- `E301`: Destructive command not marked as destructive
- `E302`: Cannot analyze command for destructive operations
- `E303`: Unsafe command pattern detected

**Logic Check Warnings (W400-W499)**: Logic check promotion suggestions
- `W401`: Command contains logic check, consider validation element
- `W402`: Complex conditional detected in command

**Loop Detection Errors (E500-E599)**: Loop and circular reference violations
- `E501`: Circular reference detected in BR paths
- `E502`: Infinite loop in command references
- `E503`: Self-referential script or command

**Cross-Reference Errors (E600-E699)**: ID resolution failures
- `E601`: Unresolved script reference in BR path
- `E602`: Unresolved command reference in conditional
- `E603`: Duplicate script or command ID

### 7.2 Exit Codes

Following industry standards:
- `0`: Success (no errors, no warnings)
- `1`: Error (validation failed, invalid arguments, missing dependencies)
- `2`: Warning (validation passed with warnings)

---

## 8. Dependencies

### 8.1 Core Dependencies

**Required Libraries:**
```python
# Core functionality
pyyaml>=6.0           # YAML parsing and validation
jsonschema>=4.0       # JSON Schema validation
bashlex>=0.16         # Bash command parsing (primary)

# Alternative/fallback bash parsers
bashparser>=1.0       # Enhanced bash parsing capabilities
libbash>=0.1          # Python bindings to bash AST

# Utilities
pathlib              # Path manipulation (standard library)
argparse             # Command line interface (standard library)
json                 # JSON handling (standard library)
sys                  # System interaction (standard library)
os                   # Operating system interface (standard library)
re                   # Regular expressions (standard library)
```

**Optional Dependencies:**
```python
# Enhanced features
colorama>=0.4        # Cross-platform colored output
termcolor>=1.1       # Terminal color formatting
rich>=12.0           # Rich text and beautiful formatting
```

### 8.2 Bash Parser Selection Strategy

**Primary**: `bashlex` - Most mature and complete bash parser
**Fallback**: `bashparser` - Enhanced semantic analysis capabilities  
**Alternative**: `libbash` - Direct bash source integration

**Selection Logic**:
```python
def get_bash_parser():
    try:
        import bashlex
        return BashLexAnalyzer()
    except ImportError:
        try:
            import bashparser
            return BashParserAnalyzer()
        except ImportError:
            try:
                import libbash
                return LibBashAnalyzer()
            except ImportError:
                raise ImportError("No bash parser available. Install bashlex, bashparser, or libbash.")
```

---

## 9. Implementation Guidelines

### 9.1 Validation Pipeline Implementation

**Single-Pass Architecture**:
```python
class AiaiLinter:
    def __init__(self, verbose=False, strict=False, format_output="text"):
        self.verbose = verbose
        self.strict = strict
        self.format_output = format_output
        self.validators = [
            SyntaxValidator(),
            SchemaValidator(),
            SemanticValidator(),
            BusinessRulesValidator(),
            CrossReferenceValidator()
        ]
    
    def validate_file(self, file_path):
        # Load and parse file
        data = self._load_yaml_file(file_path)
        if not data:
            return ValidationResult(False, ["Failed to load file"])
        
        # Run all validators in parallel
        results = []
        for validator in self.validators:
            result = validator.validate(data, file_path)
            results.append(result)
        
        # Aggregate results
        return self._aggregate_results(results)
    
    def validate_package(self, package_path):
        # Load package manifest
        manifest = self._load_package_manifest(package_path)
        
        # Validate package structure
        package_result = self._validate_package_structure(package_path, manifest)
        if not package_result.success:
            return package_result
        
        # Validate individual scripts
        script_results = []
        for script_file in manifest.scripts:
            script_path = package_path / script_file
            script_result = self.validate_file(script_path)
            script_results.append(script_result)
        
        # Aggregate package results
        return self._aggregate_package_results(package_result, script_results)
```

### 9.2 Bash Command Analysis

**Semantic Analysis Implementation**:
```python
class BashSemanticAnalyzer:
    def __init__(self):
        self.destructive_patterns = self._load_destructive_patterns()
        self.logic_check_patterns = self._load_logic_check_patterns()
    
    def analyze_command(self, shell_command):
        try:
            # Parse command into AST
            ast = bashlex.parse(shell_command)
            
            # Extract analysis results
            analysis = CommandAnalysis()
            analysis.is_destructive = self._detect_destructive(ast)
            analysis.has_logic_checks = self._detect_logic_checks(ast)
            analysis.command_type = self._classify_command(ast)
            analysis.variables = self._extract_variables(ast)
            analysis.redirections = self._extract_redirections(ast)
            
            return analysis
            
        except bashlex.TokenizationError as e:
            return CommandAnalysis(error=f"Tokenization failed: {e}")
        except Exception as e:
            return CommandAnalysis(error=f"Analysis failed: {e}")
    
    def _detect_destructive(self, ast):
        """Detect destructive operations in command AST"""
        for node in ast:
            if node.kind == 'command':
                cmd_name = self._extract_command_name(node)
                if self._is_destructive_command(cmd_name):
                    return True
                    
                # Check for destructive patterns in arguments
                if self._has_destructive_patterns(node):
                    return True
        return False
```

### 9.3 Loop Detection Algorithm

**Graph-Based Cycle Detection**:
```python
class LoopDetector:
    def detect_loops(self, aiai_script):
        # Build dependency graphs
        command_graph = self._build_command_dependency_graph(aiai_script)
        script_graph = self._build_script_dependency_graph(aiai_script)
        
        # Detect cycles
        command_cycles = self._detect_cycles(command_graph)
        script_cycles = self._detect_cycles(script_graph)
        
        return LoopDetectionResult(command_cycles, script_cycles)
    
    def _detect_cycles(self, graph):
        """DFS-based cycle detection"""
        WHITE, GRAY, BLACK = 0, 1, 2
        colors = {node: WHITE for node in graph}
        cycles = []
        
        def dfs(node, path):
            if colors[node] == GRAY:
                # Found cycle
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            
            if colors[node] == BLACK:
                return
            
            colors[node] = GRAY
            path.append(node)
            
            for neighbor in graph.get(node, []):
                dfs(neighbor, path)
            
            path.pop()
            colors[node] = BLACK
        
        for node in graph:
            if colors[node] == WHITE:
                dfs(node, [])
        
        return cycles
```

---

## 10. Integration

### 10.1 CI/CD Integration

**GitHub Actions Example**:
```yaml
name: AIAI Script Validation
on: [push, pull_request]

jobs:
  validate-aiai:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install aiailint
      run: pip install aiailint
    - name: Validate AIAI Scripts
      run: |
        aiailint validate src/aiaiScript/ --format json --strict > validation-results.json
        cat validation-results.json
    - name: Upload validation results
      uses: actions/upload-artifact@v3
      with:
        name: validation-results
        path: validation-results.json
```

### 10.2 IDE Integration

**VS Code Extension Integration**:
```json
{
  "contributes": {
    "languages": [
      {
        "id": "aiai",
        "extensions": [".aiaiScript.yaml"]
      }
    ],
    "grammars": [
      {
        "language": "aiai",
        "scopeName": "source.aiai",
        "path": "./syntaxes/aiai.tmLanguage.json"
      }
    ],
    "problemMatchers": [
      {
        "name": "aiailint",
        "owner": "aiailint",
        "fileLocation": "absolute",
        "pattern": [
          {
            "regexp": "^(ERROR|WARNING|INFO):\\s+([EWI]\\d+)\\s+\\[Line\\s+(\\d+)\\]:\\s+(.*)$",
            "severity": 1,
            "code": 2,
            "line": 3,
            "message": 4
          }
        ]
      }
    ]
  }
}
```

---

## 11. Future Requirements

### 11.1 Proposed Additional Features

**Enhanced Command Analysis:**
- Support for more shell variants (zsh, fish, dash)
- Analysis of shell functions and aliases
- Detection of command substitution and process substitution patterns
- Integration with shellcheck for additional shell script validation

**Advanced Business Rules:**
- Custom business rule configuration via YAML/JSON files
- Rule severity customization (error/warning/info)
- Context-aware rule application (different rules for different script types)
- Rule exemption system with justification comments

**Performance Optimization:**
- Incremental validation for large packages
- Parallel processing of multiple files
- Caching of parsed ASTs for repeated validation
- Streaming validation for very large files

**Additional Output Formats:**
- SARIF (Static Analysis Results Interchange Format) for security tools
- TAP (Test Anything Protocol) for test frameworks
- Custom XML format for enterprise tools
- Integration with common reporting platforms

**Package-Level Validation:**
- Cross-package dependency validation
- Package versioning compatibility checks
- Manifest completeness validation
- Package integrity verification

### 11.2 Extension Points

**Plugin Architecture:**
```python
class AiaiLintPlugin:
    def __init__(self):
        self.name = "CustomPlugin"
        self.version = "1.0.0"
    
    def validate(self, aiai_script, context):
        """Custom validation logic"""
        pass
    
    def get_error_codes(self):
        """Return list of error codes this plugin uses"""
        pass

# Plugin registration
aiailint.register_plugin(CustomBusinessRulesPlugin())
```

**Custom Validators:**
- Domain-specific validation rules
- Organization-specific conventions
- Integration with external security scanning tools
- Custom command pattern detection

---

## 12. Additional Requirements for Review

### 12.1 Questions for Clarification

1. **Schema Evolution**: How should aiailint handle schema version mismatches between the tool and AIAI Scripts?

2. **Configuration Management**: Should aiailint support configuration files for customizing validation rules per project/organization?

3. **Incremental Validation**: For large packages with many scripts, should aiailint support incremental validation (only validate changed files)?

4. **Integration Dependencies**: Should aiailint bundle its own copy of aiai_schema.json or always reference the latest from the aiai/core directory?

5. **Bash Parser Fallbacks**: If the primary bash parser fails on a command, should aiailint fall back to simpler regex-based analysis or fail completely?

6. **Performance Targets**: What are the performance requirements for validating large packages (e.g., 100+ scripts)?

### 12.2 Potential Missing Requirements

**Security Considerations:**
- Should aiailint detect potential security vulnerabilities in commands (e.g., command injection, unsafe variable usage)?
- How should it handle commands that read sensitive files or environment variables?

**Multi-Language Support:**
- Should aiailint support commands in other languages (Python, PowerShell) embedded in AIAI Scripts?
- How should it handle mixed-language command sequences?

**Backwards Compatibility:**
- How should aiailint handle deprecated AIAI Schema features?
- Should it provide migration suggestions for outdated script patterns?

**Testing and Quality Assurance:**
- Should aiailint include built-in test data generators for validation testing?
- How should it validate its own validation rules for correctness?

---

## 13. Conclusion

This specification provides a comprehensive foundation for implementing aiailint as a robust, safe, and industry-standard validation tool for AIAI Scripts and packages. The design prioritizes safety through destructive command detection, maintains consistency with existing tools like viscriptlint, and provides extensibility for future enhancements.

The modular architecture enables independent development and testing of validation components, while the single-pass pipeline ensures optimal performance. The business rules focus on preventing irreversible damage to operator systems, making aiailint an essential safety tool for AIAI Script development.

Key implementation priorities:
1. **Safety First**: Destructive command detection and loop prevention
2. **Industry Standards**: CLI patterns, exit codes, and output formats
3. **Semantic Analysis**: Comprehensive bash command understanding
4. **Extensibility**: Plugin architecture and custom validation rules

This specification should be reviewed and refined based on your specific requirements and any additional constraints or features needed for your AIAI ecosystem.