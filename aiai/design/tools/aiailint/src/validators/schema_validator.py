"""
JSON Schema Validator for AIAI Scripts

Validates AIAI Scripts against the formal JSON Schema definition.
Error Codes: E100-E199 (Schema validation errors)
"""

import json
import jsonschema
from pathlib import Path
from typing import Dict, Any, List
from utils.validation_result import ValidationResult


class SchemaValidator:
    """Validates AIAI Scripts against JSON Schema"""
    
    def __init__(self, verbose=False, schema_path=None):
        self.verbose = verbose
        self.schema_path = schema_path
        self.schema = None
        self._load_schema()
    
    def _load_schema(self):
        """Load AIAI Schema from file"""
        try:
            if self.schema_path:
                schema_file = Path(self.schema_path)
            else:
                # Try to find schema in standard locations
                schema_file = self._find_schema_file()
            
            if not schema_file.exists():
                if self.verbose:
                    print(f"Warning: AIAI schema file not found at {schema_file}")
                self.schema = None
                return
            
            with open(schema_file, 'r', encoding='utf-8') as f:
                self.schema = json.load(f)
            
            if self.verbose:
                print(f"✓ Loaded AIAI schema from {schema_file}")
                
        except Exception as e:
            if self.verbose:
                print(f"Warning: Failed to load AIAI schema: {e}")
            self.schema = None
    
    def _find_schema_file(self) -> Path:
        """Find AIAI schema file in standard locations"""
        # Look for schema in multiple locations relative to this file
        current_dir = Path(__file__).parent
        
        # Possible schema locations
        schema_locations = [
            # Copy in src directory
            current_dir / "aiai_schema.json",
            # Reference to core schema
            current_dir / "../../../core/aiai_schema.json", 
            current_dir / "../../../../core/aiai_schema.json",
            # Alternative locations
            current_dir / "../schemas/aiai_schema.json",
            Path("aiai_schema.json"),  # Current working directory
        ]
        
        for location in schema_locations:
            if location.exists():
                return location.resolve()
        
        # Default to core location
        return current_dir / "../../../core/aiai_schema.json"
    
    def validate(self, data: Dict[str, Any], file_path: Path) -> ValidationResult:
        """
        Validate AIAI Script against JSON Schema
        
        Args:
            data: Parsed YAML data to validate
            file_path: Path to the file being validated
            
        Returns:
            ValidationResult with schema validation results
        """
        errors = []
        warnings = []
        info = []
        
        if self.verbose:
            print("→ Running JSON Schema validation...")
        
        # Check if schema is available
        if self.schema is None:
            warnings.append("W100: AIAI schema not available - skipping schema validation")
            if self.verbose:
                print("  ⚠ Schema validation skipped (schema not found)")
            return ValidationResult(True, errors, warnings, info, str(file_path))
        
        try:
            # Validate against schema
            jsonschema.validate(instance=data, schema=self.schema)
            
            if self.verbose:
                print("  ✓ JSON Schema validation passed")
            
            # Additional schema-specific checks
            additional_issues = self._additional_schema_checks(data)
            warnings.extend(additional_issues)
            
        except jsonschema.ValidationError as e:
            # Format schema validation error
            error_msg = self._format_schema_error(e)
            errors.append(error_msg)
            
            if self.verbose:
                print(f"  ✗ Schema validation failed: {error_msg}")
        
        except jsonschema.SchemaError as e:
            # Schema itself is invalid
            error_msg = f"E101: Invalid AIAI schema: {e.message}"
            errors.append(error_msg)
            
            if self.verbose:
                print(f"  ✗ Schema error: {error_msg}")
        
        except Exception as e:
            error_msg = f"E102: Schema validation error: {e}"
            errors.append(error_msg)
            
            if self.verbose:
                print(f"  ✗ Unexpected schema validation error: {error_msg}")
        
        success = len(errors) == 0
        return ValidationResult(success, errors, warnings, info, str(file_path))
    
    def _format_schema_error(self, error: jsonschema.ValidationError) -> str:
        """Format schema validation error with helpful context"""
        # Build path to the problematic element
        path_parts = []
        for part in error.absolute_path:
            if isinstance(part, int):
                path_parts.append(f"[{part}]")
            else:
                path_parts.append(str(part))
        
        path_str = ".".join(path_parts) if path_parts else "root"
        
        # Create descriptive error message
        if error.validator == "required":
            missing_props = ", ".join(f"'{prop}'" for prop in error.validator_value)
            return f"E100: Missing required properties {missing_props} at {path_str}"
        
        elif error.validator == "type":
            expected_type = error.validator_value
            actual_value = error.instance
            return f"E103: Expected {expected_type} but got {type(actual_value).__name__} at {path_str}"
        
        elif error.validator == "enum":
            allowed_values = ", ".join(f"'{v}'" for v in error.validator_value)
            return f"E104: Value must be one of: {allowed_values} at {path_str}"
        
        elif error.validator == "pattern":
            pattern = error.validator_value
            return f"E105: Value does not match required pattern '{pattern}' at {path_str}"
        
        elif error.validator == "additionalProperties":
            return f"E106: Additional property not allowed at {path_str}"
        
        elif error.validator == "minLength":
            min_len = error.validator_value
            return f"E107: Value too short (minimum {min_len} characters) at {path_str}"
        
        elif error.validator == "maxLength":
            max_len = error.validator_value
            return f"E108: Value too long (maximum {max_len} characters) at {path_str}"
        
        else:
            # Generic schema error
            return f"E109: Schema validation failed at {path_str}: {error.message}"
    
    def _additional_schema_checks(self, data: Dict[str, Any]) -> List[str]:
        """Perform additional schema-related checks"""
        warnings = []
        
        # Check for deprecated fields (if defined in schema)
        deprecated_fields = self._check_deprecated_fields(data)
        warnings.extend(deprecated_fields)
        
        # Check for recommended best practices
        best_practice_issues = self._check_best_practices(data)
        warnings.extend(best_practice_issues)
        
        return warnings
    
    def _check_deprecated_fields(self, data: Dict[str, Any], path="") -> List[str]:
        """Check for deprecated fields based on schema metadata"""
        warnings = []
        
        # Known deprecated fields (can be extracted from schema in future)
        deprecated_fields = {
            'critical': 'Use severity field instead',
            'weight': 'No longer supported',
            'test_mode': 'Feature not implemented',
            'conditional': 'Use validation elements instead'
        }
        
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key
                
                # Check if this key is deprecated
                if key in deprecated_fields:
                    reason = deprecated_fields[key]
                    warnings.append(f"W101: Deprecated field '{key}' at {current_path}: {reason}")
                
                # Recursively check nested structures
                if isinstance(value, (dict, list)):
                    nested_warnings = self._check_deprecated_fields(value, current_path)
                    warnings.extend(nested_warnings)
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path}[{i}]"
                if isinstance(item, (dict, list)):
                    nested_warnings = self._check_deprecated_fields(item, current_path)
                    warnings.extend(nested_warnings)
        
        return warnings
    
    def _check_best_practices(self, data: Dict[str, Any]) -> List[str]:
        """Check for AIAI Script best practices"""
        warnings = []
        
        # Check for missing optional but recommended fields
        if isinstance(data, dict):
            metadata = data.get('metadata', {})
            
            # Check for missing context information
            if 'context' not in metadata:
                warnings.append("W102: Consider adding 'context' section to metadata for better AI guidance")
            
            # Check for empty intent descriptions
            if 'intent' in metadata and not metadata['intent'].strip():
                warnings.append("W103: Intent description should not be empty")
            
            # Check for very short intent descriptions
            if 'intent' in metadata and len(metadata['intent'].strip()) < 10:
                warnings.append("W104: Intent description is very short - consider adding more detail")
            
            # Check body structure
            body = data.get('body', [])
            if isinstance(body, list) and len(body) == 0:
                warnings.append("W105: Script body is empty")
        
        return warnings


def validate_against_schema(data: Dict[str, Any], schema_path: str = None, verbose=False) -> ValidationResult:
    """
    Standalone function to validate data against AIAI schema
    
    Args:
        data: Data to validate
        schema_path: Optional path to schema file
        verbose: Enable verbose output
        
    Returns:
        ValidationResult with validation details
    """
    validator = SchemaValidator(verbose=verbose, schema_path=schema_path)
    return validator.validate(data, Path(""))  # No file path for standalone validation