"""
Test utilities for aiailint tests.

This module provides utility functions and helpers for aiailint testing.
"""

import yaml
from pathlib import Path
from typing import Optional, Dict, Any


def create_test_script(content: str, filename: str = "test_script.yaml") -> Path:
    """
    Create a test script file with given content.
    
    Args:
        content: YAML content to write to the file
        filename: Name of the file to create
        
    Returns:
        Path: Path to the created test script file
    """
    script_path = Path("tests/test_data") / filename
    script_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(script_path, 'w') as f:
        f.write(content)
    
    return script_path


def validate_yaml_syntax(content: str) -> bool:
    """
    Validate YAML syntax.
    
    Args:
        content: YAML content to validate
        
    Returns:
        bool: True if YAML syntax is valid, False otherwise
    """
    try:
        yaml.safe_load(content)
        return True
    except yaml.YAMLError:
        return False


def load_test_script(script_path: Path) -> Optional[Dict[str, Any]]:
    """
    Load and parse a test script file.
    
    Args:
        script_path: Path to the script file
        
    Returns:
        Optional[Dict[str, Any]]: Parsed YAML content or None if invalid
    """
    try:
        with open(script_path, 'r') as f:
            return yaml.safe_load(f)
    except (yaml.YAMLError, FileNotFoundError):
        return None


def create_validation_result(is_valid: bool, errors: list = None) -> Dict[str, Any]:
    """
    Create a validation result object for testing.
    
    Args:
        is_valid: Whether the validation passed
        errors: List of validation errors
        
    Returns:
        Dict[str, Any]: Validation result object
    """
    return {
        "is_valid": is_valid,
        "errors": errors or []
    }


def get_test_data_path(category: str, filename: str) -> Path:
    """
    Get the path to a test data file.
    
    Args:
        category: Test data category (valid_scripts, invalid_scripts)
        filename: Name of the test file
        
    Returns:
        Path: Path to the test data file
    """
    return Path("tests/test_data") / category / filename
