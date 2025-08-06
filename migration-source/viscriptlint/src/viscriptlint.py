#!/usr/bin/env python3

"""
viscriptlint - Comprehensive viScript validation and linting tool
Version: 3.0
Purpose: Validate, migrate, and upgrade viScript files with industry-standard subcommand pattern
Schema: viscript_schema.json (JSON Schema Draft-07)

VALIDATION ALGORITHM:
====================

OVERVIEW:
---------
viscriptlint uses a single-pass validation algorithm with parallel validation phases.
All validations run independently on the same parsed data structure, then results
are aggregated in a single pass.

ALGORITHM FLOW:
---------------
1. FILE SYSTEM VALIDATION (Early Exit)
   - Check file existence
   - Validate file type (not directory)
   - Check file size (non-empty)
   - Exit immediately if any file system issues detected

2. JSON LOADING WITH EXCEPTION HANDLING
   - Attempt to parse JSON file
   - Catch all JSON parsing exceptions (JSONDecodeError, etc.)
   - Return detailed error with line/column information if parsing fails
   - Exit immediately if JSON cannot be parsed

3. PARALLEL VALIDATION PHASES (Single Pass)
   All validations run independently on the same parsed data:
   
   a) JSON Syntax Validation
      - Validate JSON syntax using Python's json.load()
      - Report syntax errors with precise line/column location
      - Error Code: E000 (JSON_SYNTAX_ERROR)
   
   b) JSON Schema Validation
      - External ajv tool integration (if available)
      - Schema compliance checking against viscript_schema.json
      - Detailed error reporting with JSON paths
      - Error Code: E001 (SCHEMA_VALIDATION_FAILED)
   
   c) Structure Validation
      - Required top-level fields: installation_type, version, phases
      - Required check fields: name, description, command, validation_type, severity
      - Error Code: E003 (MISSING_REQUIRED_FIELD)
   
   d) Content Validation
      - Severity field validation (critical/informational)
      - Validation type validation (return_value/output_pattern/both/none)
      - Error Codes: E004 (INVALID_SEVERITY), E005 (INVALID_VALIDATION_TYPE)
   
   e) Deprecation Detection
      - Deprecated fields: critical, weight
      - Error Codes: E100 (DEPRECATED_CRITICAL_FIELD), E101 (DEPRECATED_WEIGHT_FIELD)
   
   f) Unsupported Attribute Detection
      - Unsupported attributes: test_mode, conditional
      - Error Codes: E102 (UNSUPPORTED_TEST_MODE), E103 (UNSUPPORTED_CONDITIONAL)
   
   g) Common Issues Detection
      - Empty command detection (W001)
      - Missing pattern detection (W002)
      - Missing return value detection (W003)
      - Line/column number calculation for precise error reporting
   
   h) Analysis & Statistics
      - Check distribution analysis
      - Severity ratio analysis
      - Critical check presence validation
      - Warning Codes: W004 (NO_CRITICAL_CHECKS), W005 (HIGH_INFORMATIONAL_RATIO)

4. RESULT AGGREGATION (Single Pass)
   - Collect all errors, warnings, and info messages
   - Apply strict mode (treat warnings as errors if enabled)
   - Generate appropriate exit codes

ERROR HANDLING FOR CORRUPTED/MALFORMED FILES:
==============================================
1. File System Errors:
   - File not found: Immediate exit with error message
   - Not a file (directory): Immediate exit with error message
   - Empty file: Immediate exit with error message

2. JSON Parsing Errors:
   - Completely corrupted JSON: Early exit with syntax error
   - Malformed JSON (missing commas, brackets): Early exit with detailed error
   - Encoding issues: Early exit with encoding error message

3. Graceful Degradation:
   - Tool never crashes on corrupted files
   - Always returns appropriate exit codes
   - Provides meaningful error messages
   - Stops processing when JSON cannot be parsed

PERFORMANCE CHARACTERISTICS:
===========================
Time Complexity: O(n) where n = file size
- Single file read for all validations
- Parallel validation phases (no dependencies)
- Linear aggregation of results

Space Complexity: O(n) where n = file size
- Single JSON parse into memory
- Shared data structure across validations
- Minimal temporary storage

EXIT CODES (Industry Standard):
==============================
0 - SUCCESS (no errors, no warnings)
1 - ERROR (validation failed, invalid arguments, missing dependencies)
2 - WARNING (validation passed with warnings)

ERROR CODE SYSTEM:
=================
E000-E099: Critical errors (JSON syntax, schema validation, required fields)
E100-E199: Deprecated/unsupported fields
W001-W099: Common issues and warnings

OUTPUT FORMATS:
===============
1. Text Format: Human-readable with colors and formatting
2. JSON Format: Machine-readable for CI/CD integration

ADVANTAGES OF SINGLE-PASS DESIGN:
=================================
1. Efficiency: One file read, one JSON parse, parallel validations
2. Simplicity: Clear validation flow, independent phases
3. Extensibility: Easy to add new validation phases
4. Reliability: Graceful error handling, no crashes

COMPARISON WITH MULTI-PASS DESIGN:
==================================
Single-Pass (Current):
File → Parse → [Validation1, Validation2, ..., ValidationN] → Aggregate → Output

Multi-Pass (Alternative):
File → Parse → Validation1 → Parse → Validation2 → ... → Parse → ValidationN → Output

The single-pass design is more efficient and better suited for this validation use case
where all validations can run independently on the same parsed data structure.
"""

import json
import sys
import os
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

# Exit codes (aligned with industry standards)
class ExitCodes:
    SUCCESS = 0
    ERROR = 1
    WARNING = 2
    INVALID_ARGS = 1
    DEPENDENCY_MISSING = 1

class Severity(Enum):
    CRITICAL = "critical"
    INFORMATIONAL = "informational"

class ValidationType(Enum):
    RETURN_VALUE = "return_value"
    OUTPUT_PATTERN = "output_pattern"
    BOTH = "both"
    NONE = "none"

# Error codes for industry-standard linting
class ErrorCodes:
    # Schema validation errors (E001-E099)
    SCHEMA_VALIDATION_FAILED = "E001"
    EMPTY_PATTERN = "E002"
    MISSING_REQUIRED_FIELD = "E003"
    INVALID_SEVERITY = "E004"
    INVALID_VALIDATION_TYPE = "E005"
    
    # Deprecated/unsupported fields (E100-E199)
    DEPRECATED_CRITICAL_FIELD = "E100"
    DEPRECATED_WEIGHT_FIELD = "E101"
    UNSUPPORTED_TEST_MODE = "E102"
    UNSUPPORTED_CONDITIONAL = "E103"
    
    # Common issues (W001-W099)
    EMPTY_COMMAND = "W001"
    MISSING_PATTERN = "W002"
    MISSING_RETURN_VALUE = "W003"
    NO_CRITICAL_CHECKS = "W004"
    HIGH_INFORMATIONAL_RATIO = "W005"

@dataclass
class LintIssue:
    """Individual lint issue with location and code"""
    line: Optional[int]
    column: Optional[int]
    code: str
    message: str
    severity: str  # "error" or "warning"

@dataclass
class ValidationResult:
    """Result of validation operation with industry-standard linting"""
    success: bool
    errors: List[str]
    warnings: List[str]
    info: List[str]
    lint_issues: List[LintIssue] = None
    
    def __post_init__(self):
        if self.lint_issues is None:
            self.lint_issues = []

class ViscriptLinter:
    """Main viscriptlint class with subcommand support"""
    
    def __init__(self, verbose: bool = False, strict: bool = False, format_output: str = "text"):
        # Public interface - what users should access
        self._verbose = verbose
        self._strict = strict
        self._format_output = format_output
        
        # Protected implementation details
        self._script_dir = Path(__file__).parent
        self._schema_file = self._script_dir / "viscript_schema.json"
    
    # Public properties - controlled access to internal state
    @property
    def verbose(self) -> bool:
        """Get verbose mode setting"""
        return self._verbose
    
    @verbose.setter
    def verbose(self, value: bool) -> None:
        """Set verbose mode with validation"""
        if not isinstance(value, bool):
            raise ValueError("verbose must be a boolean")
        self._verbose = value
    
    @property
    def strict(self) -> bool:
        """Get strict mode setting"""
        return self._strict
    
    @strict.setter
    def strict(self, value: bool) -> None:
        """Set strict mode with validation"""
        if not isinstance(value, bool):
            raise ValueError("strict must be a boolean")
        self._strict = value
    
    @property
    def format_output(self) -> str:
        """Get output format setting"""
        return self._format_output
    
    @format_output.setter
    def format_output(self, value: str) -> None:
        """Set output format with validation"""
        if value not in ["text", "json"]:
            raise ValueError("format_output must be 'text' or 'json'")
        self._format_output = value
    
    @property
    def script_dir(self) -> Path:
        """Get script directory (read-only)"""
        return self._script_dir
    
    @property
    def schema_file(self) -> Path:
        """Get schema file path (read-only)"""
        return self._schema_file
    
    def find_json_path_location(self, file_path: Path, json_path: str) -> Tuple[Optional[int], Optional[int]]:
        """Find line and column for a JSON path in the file"""
        return self._locate_json_path_in_file(file_path, json_path)
    
    def _locate_json_path_in_file(self, file_path: Path, json_path: str) -> Tuple[Optional[int], Optional[int]]:
        """Protected implementation of JSON path location"""
        try:
            content = self._read_file_content(file_path)
            lines = content.split('\n')
            
            # Parse the JSON path (e.g., '/phases/1/checks/3/expected_pattern')
            path_parts = json_path.strip("'").split('/')[1:]  # Remove leading empty string
            
            # Simple heuristic: look for the field name in the file
            field_name = path_parts[-1]  # e.g., "expected_pattern"
            
            return self._find_field_in_lines(lines, field_name)
        except Exception:
            return None, None
    
    def _read_file_content(self, file_path: Path) -> str:
        """Private helper to read file content"""
        with open(file_path, 'r') as f:
            return f.read()
    
    def _find_field_in_lines(self, lines: List[str], field_name: str) -> Tuple[Optional[int], Optional[int]]:
        """Private helper to find field in lines"""
        for line_num, line in enumerate(lines, 1):
            if f'"{field_name}"' in line:
                # Find the column position
                col_pos = line.find(f'"{field_name}"') + 1
                return line_num, col_pos
        return None, None
        
    def log_message(self, level: str, message: str) -> None:
        """Log a message with appropriate color and formatting"""
        color_map = {
            "ERROR": Colors.RED,
            "WARNING": Colors.YELLOW,
            "SUCCESS": Colors.GREEN,
            "INFO": Colors.BLUE
        }
        color = color_map.get(level, "")
        print(f"{color}[{level}]{Colors.NC} {message}")
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are available"""
        # Python version uses native JSON parsing, no external dependencies required
        return True
    
    def validate_json_syntax(self, file_path: Path) -> ValidationResult:
        """Validate JSON syntax with detailed error reporting"""
        try:
            with open(file_path, 'r') as f:
                json.load(f)
            return ValidationResult(True, [], [], ["JSON syntax is valid"])
        except json.JSONDecodeError as e:
            # Enhanced error reporting with line/column information
            error_details = f"Invalid JSON syntax at line {e.lineno}, column {e.colno}: {e.msg}"
            return ValidationResult(False, [error_details], [], [])
    
    def validate_json_schema(self, file_path: Path) -> ValidationResult:
        """Validate against JSON Schema using ajv if available"""
        if not self.schema_file.exists():
            return ValidationResult(True, [], ["Schema file not found"], ["Skipping formal schema validation"])
        
        try:
            result = subprocess.run(
                ["ajv", "validate", "-s", str(self.schema_file), "-d", str(file_path)],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                return ValidationResult(True, [], [], ["JSON Schema validation passed"])
            else:
                # Parse ajv error output for industry-standard lint reporting
                detailed_errors = self._parse_ajv_errors(result.stderr, file_path)
                
                if detailed_errors:
                    return ValidationResult(False, ["JSON Schema validation failed"] + detailed_errors, [], [])
                else:
                    return ValidationResult(False, ["JSON Schema validation failed"], [], 
                                        [f"Run 'ajv validate -s {self.schema_file} -d {file_path}' for detailed errors"])
        except FileNotFoundError:
            return ValidationResult(True, [], ["ajv not available, skipping JSON Schema validation"], 
                                ["Install ajv with: npm install -g ajv-cli"])
    
    def _parse_ajv_errors(self, stderr_output: str, file_path: Path) -> List[str]:
        """Parse ajv error output into industry-standard lint format"""
        detailed_errors = []
        
        try:
            # Parse the JSON error array from ajv output
            error_lines = stderr_output.strip().split('\n')
            json_start = None
            json_end = None
            
            # Find the JSON array in the output
            for i, line in enumerate(error_lines):
                if line.strip() == '[':
                    json_start = i
                elif line.strip() == ']':
                    json_end = i + 1
                    break
            
            if json_start is not None and json_end is not None:
                # Parse ajv output manually since it's not valid JSON
                errors = self._parse_ajv_error_array(error_lines[json_start:json_end])
                
                for error in errors:
                    # Extract error details
                    instance_path = error.get('instancePath', '')
                    message = error.get('message', '')
                    keyword = error.get('keyword', '')
                    
                    # Find line and column for this error
                    line_num, col_num = self.find_json_path_location(file_path, instance_path)
                    
                    # Create industry-standard lint error format
                    if line_num and col_num:
                        # Format: file:line:col  error  code  message
                        error_code = self._get_error_code_for_keyword(keyword)
                        detailed_errors.append(f"{file_path}:{line_num}:{col_num}  error  {error_code}  {message}")
                    else:
                        # Fallback format without line/column
                        error_code = self._get_error_code_for_keyword(keyword)
                        detailed_errors.append(f"{file_path}  error  {error_code}  {instance_path}: {message}")
            else:
                # Fallback parsing for non-JSON output
                for line in error_lines:
                    if line.strip() and not line.startswith('schema') and not line.startswith('error:'):
                        if 'message:' in line:
                            error_msg = line.split('message:')[-1].strip()
                            detailed_errors.append(f"{file_path}  error  {ErrorCodes.SCHEMA_VALIDATION_FAILED}  {error_msg}")
                        elif 'instancePath:' in line:
                            path = line.split('instancePath:')[-1].strip()
                            detailed_errors.append(f"{file_path}  error  {ErrorCodes.SCHEMA_VALIDATION_FAILED}  {path}")
                        else:
                            detailed_errors.append(f"{file_path}  error  {ErrorCodes.SCHEMA_VALIDATION_FAILED}  {line.strip()}")
        
        except Exception as e:
            # Fallback to simple error reporting
            detailed_errors.append(f"{file_path}  error  {ErrorCodes.SCHEMA_VALIDATION_FAILED}  Schema validation failed")
        
        return detailed_errors
    
    def _parse_ajv_error_array(self, error_lines: List[str]) -> List[Dict[str, str]]:
        """Parse ajv error array manually since it's not valid JSON"""
        errors = []
        current_error = {}
        
        for line in error_lines:
            line = line.strip()
            if line == '[' or line == ']':
                continue
            elif line == '{':
                current_error = {}
            elif line == '}':
                if current_error:
                    errors.append(current_error)
                current_error = {}
            elif ':' in line:
                # Parse key-value pairs
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().rstrip(',')
                
                # Remove quotes if present
                if value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                elif value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                
                current_error[key] = value
        
        return errors
    
    def _get_error_code_for_keyword(self, keyword: str) -> str:
        """Map ajv keywords to error codes"""
        keyword_to_code = {
            'type': ErrorCodes.INVALID_VALIDATION_TYPE,
            'required': ErrorCodes.MISSING_REQUIRED_FIELD,
            'minLength': ErrorCodes.EMPTY_PATTERN,
            'enum': ErrorCodes.INVALID_VALIDATION_TYPE,
            'pattern': ErrorCodes.INVALID_VALIDATION_TYPE,
            'format': ErrorCodes.INVALID_VALIDATION_TYPE,
            'minimum': ErrorCodes.INVALID_VALIDATION_TYPE,
            'maximum': ErrorCodes.INVALID_VALIDATION_TYPE,
        }
        return keyword_to_code.get(keyword, ErrorCodes.SCHEMA_VALIDATION_FAILED)
    
    def check_required_fields(self, data: Dict[str, Any]) -> ValidationResult:
        """Check for required top-level fields"""
        required_fields = ["installation_type", "version", "phases"]
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return ValidationResult(False, [f"Missing required fields: {', '.join(missing_fields)}"], [], [])
        else:
            return ValidationResult(True, [], [], ["All required fields present"])
    
    def validate_check_required_fields(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate that all checks have required fields"""
        required_check_fields = ["name", "description", "command", "validation_type", "severity"]
        missing_fields = []
        
        for phase in data.get("phases", []):
            for check in phase.get("checks", []):
                missing = [field for field in required_check_fields if field not in check]
                if missing:
                    missing_fields.append(f"{check.get('name', 'unnamed_check')}: {', '.join(missing)}")
        
        if missing_fields:
            return ValidationResult(False, ["Checks missing required fields:"] + missing_fields, [], [])
        else:
            return ValidationResult(True, [], [], ["All checks have required fields"])
    
    def validate_severity_fields(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate severity fields"""
        errors = []
        
        for phase in data.get("phases", []):
            for check in phase.get("checks", []):
                if "severity" not in check:
                    errors.append(f"{check.get('name', 'unnamed_check')}: missing severity field")
                elif check["severity"] not in [s.value for s in Severity]:
                    errors.append(f"{check.get('name', 'unnamed_check')}: invalid severity '{check['severity']}'")
        
        if errors:
            return ValidationResult(False, errors, [], [])
        else:
            return ValidationResult(True, [], [], ["All severity fields valid"])
    
    def validate_validation_types(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate validation types"""
        errors = []
        valid_types = [t.value for t in ValidationType]
        
        for phase in data.get("phases", []):
            for check in phase.get("checks", []):
                if "validation_type" in check and check["validation_type"] not in valid_types:
                    errors.append(f"{check.get('name', 'unnamed_check')}: invalid validation_type '{check['validation_type']}'")
        
        if errors:
            return ValidationResult(False, errors, [], [])
        else:
            return ValidationResult(True, [], [], ["All validation types valid"])
    
    def check_deprecated_fields(self, data: Dict[str, Any]) -> ValidationResult:
        """Check for deprecated fields"""
        deprecated_fields = ["critical", "weight"]
        found_deprecated = []
        
        for phase in data.get("phases", []):
            for check in phase.get("checks", []):
                for field in deprecated_fields:
                    if field in check:
                        found_deprecated.append(field)
        
        if found_deprecated:
            return ValidationResult(False, [f"Found deprecated fields: {', '.join(set(found_deprecated))}"], 
                                ["Use 'severity' field instead of 'critical' or 'weight'"], [])
        else:
            return ValidationResult(True, [], [], ["No deprecated fields found"])
    
    def check_unsupported_attributes(self, data: Dict[str, Any]) -> ValidationResult:
        """Check for unsupported attributes"""
        unsupported_fields = ["test_mode", "conditional"]
        found_unsupported = []
        
        for phase in data.get("phases", []):
            for check in phase.get("checks", []):
                for field in unsupported_fields:
                    if field in check:
                        found_unsupported.append(field)
        
        if found_unsupported:
            return ValidationResult(False, [f"Found unsupported attributes: {', '.join(set(found_unsupported))}"], 
                                ["These attributes are documented but not actually supported by verified_installer.sh",
                                 "Remove these attributes for cleaner code and proper functionality"], [])
        else:
            return ValidationResult(True, [], [], ["No unsupported attributes found"])
    
    def check_common_issues(self, data: Dict[str, Any], file_path: Path) -> ValidationResult:
        """Check for common issues with line numbers and error codes"""
        errors = []
        warnings = []
        lint_issues = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception:
            lines = []
        
        for phase_idx, phase in enumerate(data.get("phases", [])):
            for check_idx, check in enumerate(phase.get("checks", [])):
                check_name = check.get('name', 'unnamed_check')
                
                # Find line number for this check
                line_num = None
                for i, line in enumerate(lines, 1):
                    if f'"{check_name}"' in line:
                        line_num = i
                        break
                
                # Check for empty commands
                if not check.get("command"):
                    error_msg = f"{check_name}: empty command"
                    if line_num:
                        errors.append(f"{file_path}:{line_num}:1  error  {ErrorCodes.EMPTY_COMMAND}  {error_msg}")
                    else:
                        errors.append(error_msg)
                
                # Check for missing expected_pattern in output_pattern validation
                if check.get("validation_type") == "output_pattern" and not check.get("expected_pattern"):
                    warning_msg = f"{check_name}: output_pattern without expected_pattern"
                    if line_num:
                        warnings.append(f"{file_path}:{line_num}:1  warning  {ErrorCodes.MISSING_PATTERN}  {warning_msg}")
                    else:
                        warnings.append(warning_msg)
                
                # Check for missing expected_return in return_value validation
                if check.get("validation_type") == "return_value" and "expected_return" not in check:
                    warning_msg = f"{check_name}: return_value without expected_return"
                    if line_num:
                        warnings.append(f"{file_path}:{line_num}:1  warning  {ErrorCodes.MISSING_RETURN_VALUE}  {warning_msg}")
                    else:
                        warnings.append(warning_msg)
        
        return ValidationResult(len(errors) == 0, errors, warnings, [], lint_issues)
    
    def analyze_check_distribution(self, data: Dict[str, Any]) -> ValidationResult:
        """Analyze check distribution"""
        total_checks = sum(len(phase.get("checks", [])) for phase in data.get("phases", []))
        return_value_checks = 0
        output_pattern_checks = 0
        both_checks = 0
        none_checks = 0
        critical_checks = 0
        informational_checks = 0
        
        for phase in data.get("phases", []):
            for check in phase.get("checks", []):
                validation_type = check.get("validation_type")
                severity = check.get("severity")
                
                if validation_type == "return_value":
                    return_value_checks += 1
                elif validation_type == "output_pattern":
                    output_pattern_checks += 1
                elif validation_type == "both":
                    both_checks += 1
                elif validation_type == "none":
                    none_checks += 1
                
                if severity == "critical":
                    critical_checks += 1
                elif severity == "informational":
                    informational_checks += 1
        
        info = []
        warnings = []
        
        if self.verbose:
            info.extend([
                f"Total checks: {total_checks}",
                f"Return value checks: {return_value_checks}",
                f"Output pattern checks: {output_pattern_checks}",
                f"Both validation checks: {both_checks}",
                f"Execute only checks: {none_checks}",
                f"Critical severity checks: {critical_checks}",
                f"Informational severity checks: {informational_checks}"
            ])
        
        if critical_checks == 0:
            warnings.append("No critical severity checks found")
        
        if informational_checks > total_checks * 3 // 4:
            warnings.append(f"High ratio of informational checks ({informational_checks}/{total_checks})")
        
        return ValidationResult(True, [], warnings, info)
    
    def check_documented_optional_fields(self, data: Dict[str, Any]) -> ValidationResult:
        """Check for documented optional fields"""
        removed_fields = ["mount_points", "services", "filesystems", "test_operations", "dependencies", "post_verification"]
        found_removed = [field for field in removed_fields if field in data]
        
        warnings = []
        info = []
        
        if found_removed:
            warnings.append(f"Found removed top-level fields: {', '.join(found_removed)}")
            info.extend([
                "These fields were removed from the schema and will be ignored",
                "Consider removing them from your viScript for cleaner code"
            ])
        
        if "next_step" in data:
            info.append("Found next_step attribute (recommended for guidance)")
        
        return ValidationResult(True, [], warnings, info)
    
    def validate_viscript(self, file_path: Path) -> ValidationResult:
        """Main validation function - public interface"""
        print(f"=== Validating viScript: {file_path} ===")
        print()
        
        return self._run_validation_pipeline(file_path)
    
    def _run_validation_pipeline(self, file_path: Path) -> ValidationResult:
        """Protected implementation of validation pipeline"""
        # File system validation
        file_check_result = self._validate_file_system(file_path)
        if not file_check_result.success:
            return file_check_result
        
        # Load JSON data
        data = self._load_json_data(file_path)
        if data is None:
            return ValidationResult(False, ["Error reading file: JSON parsing failed"], [], [])
        
        # Run all validations
        validation_results = self._run_all_validations(data, file_path)
        
        # Aggregate and log results
        return self._aggregate_validation_results(validation_results)
    
    def _validate_file_system(self, file_path: Path) -> ValidationResult:
        """Protected implementation of file system validation"""
        if not file_path.exists():
            return ValidationResult(False, [f"File not found: {file_path}"], [], [])
        
        if not file_path.is_file():
            return ValidationResult(False, [f"Not a file: {file_path}"], [], [])
        
        if file_path.stat().st_size == 0:
            return ValidationResult(False, [f"File is empty: {file_path}"], [], [])
        
        return ValidationResult(True, [], [], [])
    
    def _load_json_data(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Protected implementation of JSON data loading with detailed error reporting"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            # Log the detailed JSON error for debugging
            error_details = f"JSON parsing failed at line {e.lineno}, column {e.colno}: {e.msg}"
            self.log_message("ERROR", error_details)
            return None
        except Exception as e:
            self.log_message("ERROR", f"Unexpected error reading file: {e}")
            return None
    
    def _run_all_validations(self, data: Dict[str, Any], file_path: Path) -> List[ValidationResult]:
        """Protected implementation of running all validations"""
        return [
            self.validate_json_syntax(file_path),
            self.validate_json_schema(file_path),
            self.check_required_fields(data),
            self.validate_check_required_fields(data),
            self.validate_severity_fields(data),
            self.validate_validation_types(data),
            self.check_deprecated_fields(data),
            self.check_unsupported_attributes(data),
            self.check_common_issues(data, file_path),
            self.analyze_check_distribution(data),
            self.check_documented_optional_fields(data)
        ]
    
    def _aggregate_validation_results(self, validation_results: List[ValidationResult]) -> ValidationResult:
        """Protected implementation of result aggregation"""
        all_errors = []
        all_warnings = []
        all_info = []
        
        for result in validation_results:
            all_errors.extend(result.errors)
            all_warnings.extend(result.warnings)
            all_info.extend(result.info)
        
        # Log results
        self._log_validation_results(all_errors, all_warnings, all_info)
        
        return ValidationResult(len(all_errors) == 0, all_errors, all_warnings, all_info)
    
    def _log_validation_results(self, errors: List[str], warnings: List[str], info: List[str]) -> None:
        """Protected implementation of result logging"""
        for error in errors:
            self.log_message("ERROR", error)
        
        for warning in warnings:
            self.log_message("WARNING", warning)
        
        for info_msg in info:
            self.log_message("INFO", info_msg)
    
    def fix_viscript(self, file_path: Path) -> ValidationResult:
        """Fix a viScript file - automatically resolves schema issues"""
        print(f"=== Fixing viScript: {file_path} ===")
        print()
        
        return self._run_fix_pipeline(file_path)
    
    def _run_fix_pipeline(self, file_path: Path) -> ValidationResult:
        """Protected implementation of fix pipeline"""
        # Check file existence
        if not file_path.exists():
            return ValidationResult(False, [f"File not found: {file_path}"], [], [])
        
        # Create backup
        backup_result = self._create_backup(file_path)
        if not backup_result.success:
            return backup_result
        
        # Load and analyze data
        data = self._load_json_data(file_path)
        if data is None:
            return ValidationResult(False, ["Error reading file: JSON parsing failed"], [], [])
        
        # Check if fixes are needed
        needs_fixing, issues_found = self._analyze_fix_requirements(data)
        
        if needs_fixing:
            return self._execute_fix_script(file_path, issues_found)
        else:
            self.log_message("SUCCESS", "File already uses current schema - no fixes needed")
            return ValidationResult(True, [], [], [])
    
    def _create_backup(self, file_path: Path) -> ValidationResult:
        """Protected implementation of backup creation"""
        backup_path = file_path.with_suffix(file_path.suffix + ".backup")
        if not backup_path.exists():
            try:
                import shutil
                shutil.copy2(file_path, backup_path)
                self.log_message("INFO", f"Created backup: {backup_path}")
                return ValidationResult(True, [], [], [])
            except Exception as e:
                return ValidationResult(False, [f"Failed to create backup: {e}"], [], [])
        return ValidationResult(True, [], [], [])
    
    def _analyze_fix_requirements(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Protected implementation of fix requirement analysis"""
        needs_fixing = False
        issues_found = []
        
        # Check for deprecated fields
        for phase in data.get("phases", []):
            for check in phase.get("checks", []):
                if "critical" in check or "weight" in check:
                    needs_fixing = True
                    issues_found.append("deprecated critical/weight fields")
                    break
            if needs_fixing:
                break
        
        # Check for missing validation_type
        for phase in data.get("phases", []):
            for check in phase.get("checks", []):
                if "validation_type" not in check:
                    needs_fixing = True
                    if "missing validation_type" not in issues_found:
                        issues_found.append("missing validation_type")
                    break
            if needs_fixing:
                break
        
        # Check for empty expected_pattern in informational checks
        for phase in data.get("phases", []):
            for check in phase.get("checks", []):
                if (check.get("validation_type") == "output_pattern" and 
                    check.get("expected_pattern") == "" and 
                    check.get("severity") == "informational"):
                    needs_fixing = True
                    if "empty expected_pattern" not in issues_found:
                        issues_found.append("empty expected_pattern")
                    break
            if needs_fixing:
                break
        
        return needs_fixing, issues_found
    
    def _execute_fix_script(self, file_path: Path, issues_found: List[str]) -> ValidationResult:
        """Protected implementation of fix script execution"""
        self.log_message("INFO", f"Found issues to fix: {', '.join(issues_found)}")
        
        # Use the consolidated fix script for all fixes
        fix_script = self._script_dir / "fix_viscripts.py"
        
        if fix_script.exists():
            self.log_message("INFO", f"Using consolidated fix script: {fix_script.name}")
            try:
                result = subprocess.run(
                    [sys.executable, str(fix_script), str(file_path)],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if result.returncode == 0:
                    self.log_message("SUCCESS", "All schema issues fixed successfully")
                    return ValidationResult(True, [], [], [])
                else:
                    return ValidationResult(False, ["Fix operation failed"], [result.stderr], [])
            except Exception as e:
                return ValidationResult(False, [f"Fix operation failed: {e}"], [], [])
        else:
            return ValidationResult(False, [f"Fix script not found: {fix_script}"], [], [])
    
    def generate_summary(self, file_path: Path, result: ValidationResult) -> None:
        """Generate validation summary with industry-standard formatting"""
        if self.format_output == "json":
            self._generate_json_summary(file_path, result)
        else:
            self._generate_text_summary(file_path, result)
    
    def _generate_text_summary(self, file_path: Path, result: ValidationResult) -> None:
        """Generate traditional text summary"""
        print()
        print("=== VALIDATION SUMMARY ===")
        print(f"File: {file_path}")
        print(f"Errors: {len(result.errors)}")
        print(f"Warnings: {len(result.warnings)}")
        
        if len(result.errors) == 0:
            if len(result.warnings) == 0:
                self.log_message("SUCCESS", "Status: PASSED")
            else:
                self.log_message("WARNING", "Status: PASSED WITH WARNINGS")
        else:
            self.log_message("ERROR", "Status: FAILED")
        
        if len(result.errors) > 0:
            print()
            print("Please fix the errors above before using this viScript.")
        
        if len(result.warnings) > 0:
            print()
            print("Consider addressing the warnings above for better viScript quality.")
    
    def _generate_json_summary(self, file_path: Path, result: ValidationResult) -> None:
        """Generate JSON summary for CI/CD integration"""
        summary = {
            "file": str(file_path),
            "errors": [],
            "warnings": [],
            "summary": {
                "errors": len(result.errors),
                "warnings": len(result.warnings),
                "status": "failed" if len(result.errors) > 0 else "passed"
            }
        }
        
        # Parse errors and warnings for JSON format
        for error in result.errors:
            if ":" in error and "error" in error:
                parts = error.split("  ")
                if len(parts) >= 3:
                    location = parts[0]
                    code = parts[2]
                    message = "  ".join(parts[3:]) if len(parts) > 3 else ""
                    
                    if ":" in location:
                        file_line_col = location.split(":")
                        if len(file_line_col) >= 3:
                            summary["errors"].append({
                                "line": int(file_line_col[1]),
                                "column": int(file_line_col[2]),
                                "code": code,
                                "message": message,
                                "rule": code.lower().replace(" ", "-")
                            })
        
        for warning in result.warnings:
            if ":" in warning and "warning" in warning:
                parts = warning.split("  ")
                if len(parts) >= 3:
                    location = parts[0]
                    code = parts[2]
                    message = "  ".join(parts[3:]) if len(parts) > 3 else ""
                    
                    if ":" in location:
                        file_line_col = location.split(":")
                        if len(file_line_col) >= 3:
                            summary["warnings"].append({
                                "line": int(file_line_col[1]),
                                "column": int(file_line_col[2]),
                                "code": code,
                                "message": message,
                                "rule": code.lower().replace(" ", "-")
                            })
        
        print(json.dumps(summary, indent=2))

def show_help():
    """Show main help"""
    help_text = """
viscriptlint - Comprehensive viScript validation and linting tool

Usage: ./viscriptlint <COMMAND> [OPTIONS] [FILE]

COMMANDS:
    validate <file>     Validate viScript file (default command)
    fix <file>          Automatically fix schema issues in viScript
    help                Show this help message

OPTIONS:
    --verbose, -v       Show detailed output
    --strict            Enable strict mode (treat warnings as errors)
    --format <type>     Output format: text (default) or json
    --help, -h         Show help for specific command

EXIT CODES:
    0  - Success (no errors, no warnings)
    1  - Error (validation failed, invalid arguments, missing dependencies)
    2  - Warning (validation passed with warnings)

EXAMPLES:
    # Basic validation (default command)
    ./viscriptlint validate system_validation_viScript.json
    ./viscriptlint system_validation_viScript.json

    # Verbose validation with detailed output
    ./viscriptlint validate btrfs_root_viScript.json --verbose

    # Strict validation (warnings as errors)
    ./viscriptlint validate ../ubuntu-btrfs-installer/src/docker_viScript.json --strict

    # Fix schema issues automatically
    ./viscriptlint fix old_schema_viscript.json

    # Script integration example
    ./viscriptlint validate file.json
    case $? in
        0) echo "Validation passed" ;;
        1) echo "Validation failed" ;;
        2) echo "Validation passed with warnings" ;;
    esac
"""
    print(help_text.strip())

def show_command_help(command: str):
    """Show command-specific help"""
    help_texts = {
        "validate": """
viscriptlint validate - Validate viScript file

Usage: ./viscriptlint validate <file> [OPTIONS]

ARGUMENTS:
    <file>              viScript file to validate

OPTIONS:
    --verbose, -v       Show detailed validation output
    --strict            Enable strict mode (treat warnings as errors)

EXAMPLES:
    ./viscriptlint validate system_validation_viScript.json
    ./viscriptlint validate file.json --verbose --strict
""",
        "fix": """
viscriptlint fix - Automatically fix schema issues in viScript

Usage: ./viscriptlint fix <file> [OPTIONS]

ARGUMENTS:
    <file>              viScript file to fix

OPTIONS:
    --verbose, -v       Show detailed fix output

EXAMPLES:
    ./viscriptlint fix old_schema_viscript.json
    ./viscriptlint fix file.json --verbose

DESCRIPTION:
    Automatically detects and fixes common schema issues:
    - Converts deprecated critical/weight fields to severity format
    - Adds missing validation_type fields
    - Handles both explicit boolean and truthy/falsy values
    - Creates backup files before making changes
"""
    }
    
    print(help_texts.get(command, show_help()).strip())

def main():
    """Main function"""
    # Parse arguments manually to handle backward compatibility
    args = sys.argv[1:]
    
    command = "validate"  # Default command
    file_path = None
    verbose = False
    strict = False
    format_output = "text"
    help_requested = False
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg in ["--help", "-h"]:
            help_requested = True
        elif arg in ["--verbose", "-v"]:
            verbose = True
        elif arg in ["--strict"]:
            strict = True
        elif arg in ["--format"]:
            if i + 1 < len(args):
                format_output = args[i + 1]
                i += 1
            else:
                print("Error: --format requires a value (text or json)")
                sys.exit(ExitCodes.INVALID_ARGS)
        elif arg in ["validate", "fix", "help"]:
            command = arg
        elif not file_path and not arg.startswith("-"):
            # Assume it's a file for backward compatibility
            file_path = arg
        else:
            print(f"Error: Invalid argument: {arg}")
            show_help()
            sys.exit(ExitCodes.INVALID_ARGS)
        
        i += 1
    
    # Handle help
    if help_requested or command == "help":
        if file_path and file_path not in ["validate", "fix", "help"]:
            show_command_help(file_path)
        else:
            show_help()
        sys.exit(ExitCodes.SUCCESS)
    
    # Check if file is specified
    if not file_path:
        print("Error: File is required")
        show_help()
        sys.exit(ExitCodes.INVALID_ARGS)
    
    # Initialize linter
    linter = ViscriptLinter(verbose=verbose, strict=strict, format_output=format_output)
    
    # Check dependencies
    if not linter.check_dependencies():
        sys.exit(ExitCodes.DEPENDENCY_MISSING)
    
    # Execute command
    file_path = Path(file_path)
    
    if command == "validate":
        result = linter.validate_viscript(file_path)
        linter.generate_summary(file_path, result)
        
        if strict and result.warnings:
            linter.log_message("ERROR", "Strict mode enabled - warnings treated as errors")
            sys.exit(ExitCodes.ERROR)
        
        if result.errors:
            sys.exit(ExitCodes.ERROR)
        elif result.warnings:
            sys.exit(ExitCodes.WARNING)
        else:
            sys.exit(ExitCodes.SUCCESS)
    
    elif command == "fix":
        result = linter.fix_viscript(file_path)
        if result.errors:
            sys.exit(ExitCodes.ERROR)
        else:
            sys.exit(ExitCodes.SUCCESS)
    
    else:
        print(f"Error: Unknown command: {command}")
        show_help()
        sys.exit(ExitCodes.INVALID_ARGS)

if __name__ == "__main__":
    main() 