#!/usr/bin/env python3

"""
aiailint - Comprehensive AIAI Script validation and linting tool
Version: 1.0
Purpose: Validate, analyze, and lint AIAI Script files with industry-standard subcommand pattern
Schema: aiai_schema.json (JSON Schema Draft-07)

VALIDATION ALGORITHM:
====================

OVERVIEW:
---------
aiailint uses a single-pass validation algorithm with parallel validation phases.
All validations run independently on the same parsed data structure, then results
are aggregated in a single pass.

ALGORITHM FLOW:
---------------
1. INPUT PROCESSING (Early Exit)
   - Check file/package existence and type
   - Validate file size and permissions
   - Exit immediately if any input issues detected

2. YAML LOADING WITH EXCEPTION HANDLING
   - Attempt to parse YAML file
   - Catch all YAML parsing exceptions
   - Return detailed error with line/column information if parsing fails
   - Exit immediately if YAML cannot be parsed

3. PARALLEL VALIDATION PHASES (Single Pass)
   All validations run independently on the same parsed data:
   
   a) YAML Syntax Validation
      - Validate YAML syntax using Python's yaml.safe_load()
      - Report syntax errors with precise line/column location
      - Error Code: E000-E099 (SYNTAX_ERROR)
   
   b) JSON Schema Validation
      - Schema compliance checking against aiai_schema.json
      - Detailed error reporting with JSON paths
      - Error Code: E100-E199 (SCHEMA_VALIDATION_FAILED)
   
   c) Semantic Validation
      - Shell command parsing using bashlex
      - Command structure and safety analysis
      - Error Code: E200-E299 (SEMANTIC_VALIDATION_FAILED)
   
   d) Business Rules Validation
      - Destructive command detection and validation
      - Logic check promotion suggestions
      - Error Code: E300-E699 (BUSINESS_RULES_FAILED)
   
   e) Cross-Reference Validation
      - Loop detection and circular reference checking
      - ID resolution and reachability analysis
      - Error Code: E500-E699 (CROSS_REFERENCE_FAILED)

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

2. YAML Parsing Errors:
   - Completely corrupted YAML: Early exit with syntax error
   - Malformed YAML (missing brackets, quotes): Early exit with detailed error
   - Encoding issues: Early exit with encoding error message

3. Graceful Degradation:
   - Tool never crashes on corrupted files
   - Always returns appropriate exit codes
   - Provides meaningful error messages
   - Stops processing when YAML cannot be parsed

PERFORMANCE CHARACTERISTICS:
===========================
Time Complexity: O(n) where n = file size
- Single file read for all validations
- Parallel validation phases (no dependencies)
- Linear aggregation of results

Space Complexity: O(n) where n = file size
- Single YAML parse into memory
- Shared data structure across validations
- Minimal temporary storage

EXIT CODES (Industry Standard):
==============================
0 - SUCCESS (no errors, no warnings)
1 - ERROR (validation failed, invalid arguments, missing dependencies)
2 - WARNING (validation passed with warnings)
"""

import yaml
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import IntEnum

# Add current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from validators.syntax_validator import SyntaxValidator
    from validators.schema_validator import SchemaValidator
    from validators.semantic_validator import SemanticValidator
    from validators.business_rules import BusinessRulesValidator
    from validators.cross_reference import CrossReferenceValidator

    # Import utility modules
    from utils.package_loader import PackageLoader
    from utils.error_formatter import ErrorFormatter
    from utils.output_formatter import OutputFormatter, TextFormatter, JsonFormatter
except ImportError as e:
    print(f"Error importing aiailint modules: {e}")
    print("Please ensure all required dependencies are installed:")
    print("  pip install pyyaml jsonschema")
    print("  pip install bashlex  # or bashparser or libbash")
    sys.exit(1)


class ExitCodes(IntEnum):
    """Industry-standard exit codes for linting tools"""
    SUCCESS = 0      # No errors, no warnings
    ERROR = 1        # Validation failed, invalid arguments, missing dependencies
    WARNING = 2      # Validation passed with warnings


@dataclass
class ValidationResult:
    """Result of validation operation"""
    success: bool
    errors: List[str]
    warnings: List[str]
    info: List[str]
    file_path: Optional[str] = None
    
    @property
    def has_issues(self) -> bool:
        return len(self.errors) > 0 or len(self.warnings) > 0 or len(self.info) > 0


@dataclass
class ValidationIssue:
    """Individual validation issue"""
    code: str
    severity: str  # "error", "warning", "info"
    message: str
    line: Optional[int] = None
    path: Optional[str] = None
    command: Optional[str] = None
    fix_suggestion: Optional[str] = None


class AiaiLinter:
    """Main aiailint class with subcommand support"""
    
    def __init__(self, verbose=False, strict=False, format_output="text", no_semantic=False, business_rules_only=False):
        self.verbose = verbose
        self.strict = strict
        self.format_output = format_output
        self.no_semantic = no_semantic
        self.business_rules_only = business_rules_only
        
        # Initialize validators
        self.validators = []
        if not business_rules_only:
            self.validators.extend([
                SyntaxValidator(verbose=verbose),
                SchemaValidator(verbose=verbose),
            ])
            if not no_semantic:
                self.validators.append(SemanticValidator(verbose=verbose))
        
        # Always include business rules and cross-reference validation
        self.validators.extend([
            BusinessRulesValidator(verbose=verbose),
            CrossReferenceValidator(verbose=verbose)
        ])
        
        # Initialize formatters
        self.error_formatter = ErrorFormatter()
        if format_output == "json":
            self.output_formatter = JsonFormatter()
        else:
            self.output_formatter = TextFormatter(verbose=verbose)
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are available"""
        try:
            import yaml
            import jsonschema
            # Try to import bash parser
            try:
                import bashlex
                if self.verbose:
                    print("✓ Using bashlex for shell command analysis")
            except ImportError:
                try:
                    import bashparser
                    if self.verbose:
                        print("✓ Using bashparser for shell command analysis")
                except ImportError:
                    print("Warning: No bash parser available. Install bashlex or bashparser for semantic analysis.")
                    if not self.no_semantic:
                        print("Use --no-semantic to skip semantic analysis.")
                        return False
            return True
        except ImportError as e:
            print(f"Error: Required dependency missing: {e}")
            print("Install required packages: pip install pyyaml jsonschema bashlex")
            return False
    
    def validate_file(self, file_path: Union[str, Path]) -> ValidationResult:
        """Main validation function for single file - public interface"""
        file_path = Path(file_path)
        
        if self.verbose:
            print(f"=== Validating AIAI Script: {file_path} ===")
            print()
        
        return self._run_validation_pipeline(file_path)
    
    def validate_package(self, package_path: Union[str, Path]) -> ValidationResult:
        """Main validation function for AIAI package - public interface"""
        package_path = Path(package_path)
        
        if self.verbose:
            print(f"=== Validating AIAI Package: {package_path} ===")
            print()
        
        # Load and validate package structure
        package_loader = PackageLoader(verbose=self.verbose)
        package_result = package_loader.load_package(package_path)
        
        if not package_result.success:
            return package_result
        
        # Validate individual scripts in package
        script_results = []
        for script_file in package_loader.get_script_files():
            script_path = package_path / script_file
            script_result = self.validate_file(script_path)
            script_results.append(script_result)
        
        # Aggregate package results
        return self._aggregate_package_results(package_result, script_results)
    
    def _run_validation_pipeline(self, file_path: Path) -> ValidationResult:
        """Protected implementation of validation pipeline"""
        # File system validation
        file_check_result = self._validate_file_system(file_path)
        if not file_check_result.success:
            return file_check_result
        
        # Load YAML data
        data = self._load_yaml_data(file_path)
        if data is None:
            return ValidationResult(False, ["Error reading file: YAML parsing failed"], [], [])
        
        # Run all validations
        validation_results = self._run_all_validations(data, file_path)
        
        # Aggregate and return results
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
    
    def _load_yaml_data(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Load and parse YAML file with error handling"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data is None:
                    return {}
                return data
        except yaml.YAMLError as e:
            if self.verbose:
                print(f"YAML parsing error: {e}")
            return None
        except Exception as e:
            if self.verbose:
                print(f"File reading error: {e}")
            return None
    
    def _run_all_validations(self, data: Dict[str, Any], file_path: Path) -> List[ValidationResult]:
        """Run all validation phases in parallel"""
        results = []
        
        for validator in self.validators:
            try:
                result = validator.validate(data, file_path)
                results.append(result)
            except Exception as e:
                # Validator-specific error handling
                error_msg = f"{validator.__class__.__name__} failed: {e}"
                results.append(ValidationResult(False, [error_msg], [], []))
        
        return results
    
    def _aggregate_validation_results(self, results: List[ValidationResult]) -> ValidationResult:
        """Aggregate results from all validation phases"""
        all_errors = []
        all_warnings = []
        all_info = []
        
        for result in results:
            all_errors.extend(result.errors)
            all_warnings.extend(result.warnings)
            all_info.extend(result.info)
        
        # Determine overall success
        has_errors = len(all_errors) > 0
        has_warnings = len(all_warnings) > 0
        
        # In strict mode, treat warnings as errors
        if self.strict and has_warnings:
            all_errors.extend(all_warnings)
            all_warnings = []
            has_errors = True
        
        success = not has_errors
        
        return ValidationResult(success, all_errors, all_warnings, all_info)
    
    def _aggregate_package_results(self, package_result: ValidationResult, script_results: List[ValidationResult]) -> ValidationResult:
        """Aggregate package-level and script-level validation results"""
        all_errors = package_result.errors.copy()
        all_warnings = package_result.warnings.copy()
        all_info = package_result.info.copy()
        
        for result in script_results:
            all_errors.extend(result.errors)
            all_warnings.extend(result.warnings)
            all_info.extend(result.info)
        
        # Apply strict mode
        if self.strict and all_warnings:
            all_errors.extend(all_warnings)
            all_warnings = []
        
        success = len(all_errors) == 0
        
        return ValidationResult(success, all_errors, all_warnings, all_info)


def show_help():
    """Show main help information"""
    help_text = """
aiailint - AIAI Script Validation and Linting Tool

USAGE:
    aiailint [COMMAND] [OPTIONS] [FILE/PACKAGE]

COMMANDS:
    validate    Validate AIAI Script file or package (default)
    help        Show help information

OPTIONS:
    --package, -p       Validate entire AIAI package instead of single file
    --verbose, -v       Detailed validation output with explanations
    --strict            Treat warnings as errors (changes exit code)
    --format FORMAT     Output format: 'text' (default) or 'json'
    --no-semantic       Skip semantic analysis (syntax and schema only)
    --business-rules-only  Run only business rule validation
    --help, -h          Show this help information

EXAMPLES:
    # Basic file validation
    aiailint validate script.yaml
    aiailint script.yaml  # Backward compatible
    
    # Package validation
    aiailint validate --package /path/to/aiai-package/
    aiailint --package /path/to/aiai-package/
    
    # Verbose output with JSON format
    aiailint validate script.yaml --verbose --format json
    
    # Strict mode for CI/CD
    aiailint validate script.yaml --strict
    
    # Business rules only
    aiailint validate script.yaml --business-rules-only

EXIT CODES:
    0    Success (no errors, no warnings)
    1    Error (validation failed)
    2    Warning (validation passed with warnings)

For more information, visit: https://github.com/your-org/aiai
"""
    print(help_text.strip())


def show_command_help(command: str):
    """Show help for specific commands"""
    help_texts = {
        "validate": """
aiailint validate - Validate AIAI Script files and packages

USAGE:
    aiailint validate [OPTIONS] FILE
    aiailint validate [OPTIONS] --package PACKAGE_DIR

DESCRIPTION:
    Validates AIAI Script files for syntax, schema compliance, semantic
    correctness, and business rule adherence. Can validate individual
    files or complete AIAI packages.

OPTIONS:
    --package, -p       Validate entire AIAI package
    --verbose, -v       Show detailed validation information
    --strict            Treat warnings as errors
    --format FORMAT     Output format: 'text' or 'json'
    --no-semantic       Skip shell command semantic analysis
    --business-rules-only  Only run business rule validation

VALIDATION PHASES:
    1. Syntax        - YAML parsing and structure validation
    2. Schema        - JSON Schema compliance checking  
    3. Semantic      - Shell command analysis (bashlex)
    4. Business Rules - Destructive command detection
    5. Cross-Reference - Loop detection and ID resolution

EXAMPLES:
    aiailint validate btrfs_system_validation_aiaiScript.yaml
    aiailint validate --package ubuntu-btrfs-aiai/ --format json
    aiailint validate script.yaml --business-rules-only --verbose
"""
    }
    
    print(help_texts.get(command, show_help()).strip())


def main():
    """Main function with argument parsing and command dispatch"""
    # Parse arguments manually for backward compatibility and flexibility
    args = sys.argv[1:]
    
    # Default values
    command = "validate"
    target_path = None
    package_mode = False
    verbose = False
    strict = False
    format_output = "text"
    no_semantic = False
    business_rules_only = False
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
        elif arg in ["--package", "-p"]:
            package_mode = True
        elif arg in ["--no-semantic"]:
            no_semantic = True
        elif arg in ["--business-rules-only"]:
            business_rules_only = True
        elif arg in ["--format"]:
            if i + 1 < len(args):
                format_output = args[i + 1]
                i += 1
            else:
                print("Error: --format requires a value (text or json)")
                sys.exit(ExitCodes.ERROR)
        elif arg in ["validate", "help"]:
            command = arg
        elif not target_path and not arg.startswith("-"):
            # Assume it's a file/package path
            target_path = arg
        else:
            print(f"Error: Invalid argument: {arg}")
            show_help()
            sys.exit(ExitCodes.ERROR)
        
        i += 1
    
    # Handle help
    if help_requested or command == "help":
        if target_path and target_path not in ["validate", "help"]:
            show_command_help(target_path)
        else:
            show_help()
        sys.exit(ExitCodes.SUCCESS)
    
    # Validate format option
    if format_output not in ["text", "json"]:
        print("Error: --format must be 'text' or 'json'")
        show_help()
        sys.exit(ExitCodes.ERROR)
    
    # Check if target is specified
    if not target_path:
        print("Error: File or package path is required")
        show_help()
        sys.exit(ExitCodes.ERROR)
    
    # Initialize linter
    linter = AiaiLinter(
        verbose=verbose,
        strict=strict,
        format_output=format_output,
        no_semantic=no_semantic,
        business_rules_only=business_rules_only
    )
    
    # Check dependencies
    if not linter.check_dependencies():
        sys.exit(ExitCodes.ERROR)
    
    # Execute validation
    target_path = Path(target_path)
    
    try:
        if package_mode:
            result = linter.validate_package(target_path)
        else:
            result = linter.validate_file(target_path)
        
        # Output results
        output = linter.output_formatter.format_result(result, target_path, package_mode)
        print(output)
        
        # Determine exit code
        if not result.success:
            sys.exit(ExitCodes.ERROR)
        elif result.warnings and not strict:
            sys.exit(ExitCodes.WARNING)
        else:
            sys.exit(ExitCodes.SUCCESS)
            
    except KeyboardInterrupt:
        print("\nValidation interrupted by user")
        sys.exit(ExitCodes.ERROR)
    except Exception as e:
        print(f"Error: Unexpected error during validation: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(ExitCodes.ERROR)


if __name__ == "__main__":
    main()