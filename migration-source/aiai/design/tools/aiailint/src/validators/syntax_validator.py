"""
YAML Syntax Validator for AIAI Scripts

Validates YAML syntax and basic structure of AIAI Script files.
Error Codes: E000-E099 (Critical syntax errors)
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from utils.validation_result import ValidationResult


class SyntaxValidator:
    """Validates YAML syntax and basic file structure"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
    
    def validate(self, data: Dict[str, Any], file_path: Path) -> ValidationResult:
        """
        Validate YAML syntax and basic structure
        
        Args:
            data: Parsed YAML data (already loaded by main pipeline)
            file_path: Path to the file being validated
            
        Returns:
            ValidationResult with syntax validation results
        """
        errors = []
        warnings = []
        info = []
        
        if self.verbose:
            print("→ Running YAML syntax validation...")
        
        # Since data is already parsed by the main pipeline, we know YAML syntax is valid
        # However, we can perform additional structural checks here
        
        # Check if data is a dictionary (expected root structure)
        if not isinstance(data, dict):
            errors.append("E000: Root element must be a YAML mapping/dictionary")
            return ValidationResult(False, errors, warnings, info, str(file_path))
        
        # Check for completely empty file
        if not data:
            errors.append("E001: YAML file is empty or contains no data")
            return ValidationResult(False, errors, warnings, info, str(file_path))
        
        # Check for basic required top-level structure
        if 'metadata' not in data and 'body' not in data:
            warnings.append("W000: File does not appear to be an AIAI Script (missing 'metadata' and 'body')")
        
        # Validate YAML structure depth (prevent extremely nested structures)
        max_depth = self._calculate_max_depth(data)
        if max_depth > 20:
            warnings.append(f"W001: YAML structure is very deeply nested (depth: {max_depth})")
        
        # Check for potential YAML issues
        yaml_issues = self._check_yaml_best_practices(data)
        warnings.extend(yaml_issues)
        
        if self.verbose:
            if errors:
                print(f"  ✗ Found {len(errors)} syntax errors")
            elif warnings:
                print(f"  ⚠ Found {len(warnings)} syntax warnings")
            else:
                print("  ✓ YAML syntax validation passed")
        
        success = len(errors) == 0
        return ValidationResult(success, errors, warnings, info, str(file_path))
    
    def _calculate_max_depth(self, obj, current_depth=0):
        """Calculate maximum nesting depth of YAML structure"""
        if not isinstance(obj, (dict, list)):
            return current_depth
        
        if isinstance(obj, dict):
            if not obj:
                return current_depth
            return max(self._calculate_max_depth(v, current_depth + 1) for v in obj.values())
        
        if isinstance(obj, list):
            if not obj:
                return current_depth
            return max(self._calculate_max_depth(item, current_depth + 1) for item in obj)
        
        return current_depth
    
    def _check_yaml_best_practices(self, data: Dict[str, Any]) -> List[str]:
        """Check for YAML best practices and potential issues"""
        warnings = []
        
        # Check for very long strings that might indicate embedded scripts
        self._check_long_strings(data, warnings)
        
        # Check for suspicious key patterns
        self._check_suspicious_keys(data, warnings)
        
        return warnings
    
    def _check_long_strings(self, obj, warnings, path="", max_length=1000):
        """Check for exceptionally long string values"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                self._check_long_strings(value, warnings, new_path, max_length)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                self._check_long_strings(item, warnings, new_path, max_length)
        elif isinstance(obj, str) and len(obj) > max_length:
            warnings.append(f"W002: Very long string value at {path} ({len(obj)} characters)")
    
    def _check_suspicious_keys(self, obj, warnings, path=""):
        """Check for potentially problematic key names"""
        if not isinstance(obj, dict):
            return
        
        # Check for keys that might indicate embedded code or security issues
        suspicious_patterns = [
            'eval', 'exec', 'system', 'shell', 'subprocess',
            'password', 'secret', 'token', 'key', 'credential'
        ]
        
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key
            
            # Check if key name contains suspicious patterns
            key_lower = key.lower()
            for pattern in suspicious_patterns:
                if pattern in key_lower:
                    warnings.append(f"W003: Potentially sensitive key name '{key}' at {new_path}")
            
            # Recursively check nested structures
            if isinstance(value, dict):
                self._check_suspicious_keys(value, warnings, new_path)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        self._check_suspicious_keys(item, warnings, f"{new_path}[{i}]")


def validate_yaml_file(file_path: Path, verbose=False) -> ValidationResult:
    """
    Standalone function to validate YAML syntax of a file
    
    Args:
        file_path: Path to YAML file to validate
        verbose: Enable verbose output
        
    Returns:
        ValidationResult with validation details
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        validator = SyntaxValidator(verbose=verbose)
        return validator.validate(data, file_path)
        
    except yaml.YAMLError as e:
        error_msg = f"E000: YAML syntax error: {e}"
        return ValidationResult(False, [error_msg], [], [], str(file_path))
    except FileNotFoundError:
        error_msg = f"E001: File not found: {file_path}"
        return ValidationResult(False, [error_msg], [], [], str(file_path))
    except Exception as e:
        error_msg = f"E002: Unexpected error reading file: {e}"
        return ValidationResult(False, [error_msg], [], [], str(file_path))