#!/usr/bin/env python3

"""
Basic integration tests for aiailint

Tests the main aiailint functionality with simple AIAI Scripts.
"""

import os
import sys
import tempfile
import yaml
from pathlib import Path

# Add the src directory to Python path for imports
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from aiailint import AiaiLinter
from utils.validation_result import ValidationResult


def create_test_script(content: dict) -> Path:
    """Create a temporary AIAI Script file for testing"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='_aiaiScript.yaml', delete=False)
    yaml.dump(content, temp_file, default_flow_style=False)
    temp_file.close()
    return Path(temp_file.name)


def test_valid_aiai_script():
    """Test validation of a valid AIAI Script"""
    valid_script = {
        'metadata': {
            'id': 'test-script',
            'intent': 'Test script for aiailint validation',
            'technicalProficiency': 'Intermediate'
        },
        'body': [
            {
                'type': 'command',
                'id': 'list-files',
                'intent': 'List files in current directory',
                'shellCommand': 'ls -la',
                'destructive': False
            }
        ]
    }
    
    script_path = create_test_script(valid_script)
    try:
        linter = AiaiLinter(verbose=True)
        result = linter.validate_file(script_path)
        
        assert result.success, f"Valid script should pass validation: {result.errors}"
        print("✓ Valid AIAI Script validation passed")
        
    finally:
        script_path.unlink()  # Clean up


def test_destructive_command_detection():
    """Test detection of unmarked destructive commands"""
    destructive_script = {
        'metadata': {
            'id': 'destructive-test',
            'intent': 'Test destructive command detection',
            'technicalProficiency': 'Expert'
        },
        'body': [
            {
                'type': 'command',
                'id': 'remove-files',
                'intent': 'Remove temporary files',
                'shellCommand': 'rm -rf /tmp/test-files',
                'destructive': False  # Should be True!
            }
        ]
    }
    
    script_path = create_test_script(destructive_script)
    try:
        linter = AiaiLinter(verbose=True)
        result = linter.validate_file(script_path)
        
        assert not result.success, "Script with unmarked destructive command should fail"
        
        # Check for specific error code
        has_destructive_error = any('E301' in error for error in result.errors)
        assert has_destructive_error, f"Should have E301 error for unmarked destructive command: {result.errors}"
        
        print("✓ Destructive command detection works")
        
    finally:
        script_path.unlink()  # Clean up


def test_logic_check_warning():
    """Test logic check promotion warning"""
    logic_script = {
        'metadata': {
            'id': 'logic-test',
            'intent': 'Test logic check detection',
            'technicalProficiency': 'Beginner'
        },
        'body': [
            {
                'type': 'command',
                'id': 'check-sudo',
                'intent': 'Check if running with sudo',
                'shellCommand': '[ -n "$SUDO_USER" ] && echo "sudo_active" || echo "no_sudo"',
                'destructive': False
            }
        ]
    }
    
    script_path = create_test_script(logic_script)
    try:
        linter = AiaiLinter(verbose=True)
        result = linter.validate_file(script_path)
        
        # Should pass but with warnings
        assert result.success, f"Script with logic checks should pass: {result.errors}"
        
        # Check for logic check warning
        has_logic_warning = any('W401' in warning for warning in result.warnings)
        assert has_logic_warning, f"Should have W401 warning for logic check: {result.warnings}"
        
        print("✓ Logic check detection works")
        
    finally:
        script_path.unlink()  # Clean up


def test_invalid_yaml():
    """Test handling of invalid YAML"""
    # Create invalid YAML file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='_aiaiScript.yaml', delete=False)
    temp_file.write("invalid: yaml: content: {\n")  # Broken YAML
    temp_file.close()
    
    script_path = Path(temp_file.name)
    try:
        linter = AiaiLinter(verbose=True)
        result = linter.validate_file(script_path)
        
        assert not result.success, "Invalid YAML should fail validation"
        print("✓ Invalid YAML handling works")
        
    finally:
        script_path.unlink()  # Clean up


def test_text_output_formatter():
    """Test text output formatting"""
    from utils.output_formatter import TextFormatter
    
    # Create a mock result
    result = ValidationResult(
        success=False,
        errors=["E301: Test error message"],
        warnings=["W401: Test warning message"],
        info=["I200: Test info message"]
    )
    
    formatter = TextFormatter(verbose=True, use_colors=False)
    output = formatter.format_result(result, Path("test.yaml"))
    
    assert "ERRORS:" in output
    assert "WARNINGS:" in output
    assert "E301: Test error message" in output
    assert "W401: Test warning message" in output
    
    print("✓ Text output formatter works")


def test_json_output_formatter():
    """Test JSON output formatting"""
    import json
    from utils.output_formatter import JsonFormatter
    
    # Create a mock result
    result = ValidationResult(
        success=False,
        errors=["E301: Test error message"],
        warnings=["W401: Test warning message"],
        info=[]
    )
    
    formatter = JsonFormatter()
    output = formatter.format_result(result, Path("test.yaml"))
    
    # Parse JSON to verify it's valid
    data = json.loads(output)
    
    assert data['validation']['status'] == 'failed'
    assert data['validation']['errors'] == 1
    assert data['validation']['warnings'] == 1
    assert len(data['issues']) == 2
    
    print("✓ JSON output formatter works")


def run_all_tests():
    """Run all basic tests"""
    print("Running aiailint basic tests...")
    print("=" * 40)
    
    try:
        test_valid_aiai_script()
        test_destructive_command_detection()
        test_logic_check_warning()
        test_invalid_yaml()
        test_text_output_formatter() 
        test_json_output_formatter()
        
        print("=" * 40)
        print("✓ All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)