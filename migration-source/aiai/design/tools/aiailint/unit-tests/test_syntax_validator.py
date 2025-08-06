#!/usr/bin/env python3
"""
Unit tests for SyntaxValidator

Tests YAML syntax validation functionality.
"""

import unittest
import tempfile
import yaml
import sys
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from validators.syntax_validator import SyntaxValidator, validate_yaml_file
from utils.validation_result import ValidationResult


class TestSyntaxValidator(unittest.TestCase):
    """Test cases for SyntaxValidator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = SyntaxValidator()
    
    def test_valid_yaml_syntax(self):
        """Test that valid YAML syntax passes validation"""
        valid_yaml = {
            'metadata': {
                'name': 'test_script',
                'version': '1.0.0'
            },
            'body': {
                'scripts': {
                    'main': {
                        'commands': [
                            {'shellCommand': 'echo "Hello World"'}
                        ]
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(valid_yaml, f)
            temp_file = Path(f.name)
        
        try:
            results = validate_yaml_file(temp_file)
            self.assertTrue(results.success, f"Valid YAML should pass: {results.errors}")
        finally:
            temp_file.unlink()
    
    def test_invalid_yaml_syntax(self):
        """Test that invalid YAML syntax fails validation"""
        invalid_yaml = """
        metadata:
          name: test_script
        body:
          scripts:
            main:
              commands:
                - shellCommand: echo "Hello World"
                  - invalid: indentation
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(invalid_yaml)
            temp_file = Path(f.name)
        
        try:
            results = validate_yaml_file(temp_file)
            self.assertFalse(results.success, "Invalid YAML should fail")
            self.assertTrue(any("E000" in error for error in results.errors), 
                          "Should have YAML syntax error")
        finally:
            temp_file.unlink()
    
    def test_missing_required_fields(self):
        """Test that missing required fields are detected"""
        incomplete_yaml = {
            'metadata': {
                'name': 'test_script'
                # Missing version
            }
            # Missing body
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(incomplete_yaml, f)
            temp_file = Path(f.name)
        
        try:
            results = validate_yaml_file(temp_file)
            # Should pass syntax validation but may have warnings
            self.assertTrue(results.success, "Should pass syntax validation")
            self.assertTrue(len(results.warnings) > 0, "Should have warnings about structure")
        finally:
            temp_file.unlink()
    
    def test_nonexistent_file(self):
        """Test validation of nonexistent file"""
        results = validate_yaml_file(Path("/nonexistent/file.yaml"))
        self.assertFalse(results.success, "Nonexistent file should fail")
        self.assertTrue(any("E001" in error for error in results.errors), 
                       "Should have file not found error")
    
    def test_file_validation(self):
        """Test validation of YAML files"""
        test_data = {
            'metadata': {'name': 'test'},
            'body': {'scripts': {'main': {'commands': []}}}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_data, f)
            temp_file = Path(f.name)
        
        try:
            results = validate_yaml_file(temp_file)
            self.assertTrue(results.success, "Valid file should pass")
        finally:
            temp_file.unlink()
    
    def test_empty_content(self):
        """Test validation of empty content"""
        empty_yaml = {}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(empty_yaml, f)
            temp_file = Path(f.name)
        
        try:
            results = validate_yaml_file(temp_file)
            self.assertFalse(results.success, "Empty content should fail")
            self.assertTrue(any("E001" in error for error in results.errors), 
                          "Should have empty file error")
        finally:
            temp_file.unlink()
    
    def test_unicode_content(self):
        """Test validation of Unicode content"""
        unicode_yaml = {
            'metadata': {
                'name': 'test_script_unicode',
                'description': 'Script with Unicode: 你好世界'
            },
            'body': {
                'scripts': {
                    'main': {
                        'commands': [
                            {'shellCommand': 'echo "Unicode: 你好世界"'}
                        ]
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
            yaml.dump(unicode_yaml, f, allow_unicode=True)
            temp_file = Path(f.name)
        
        try:
            results = validate_yaml_file(temp_file)
            self.assertTrue(results.success, "Unicode content should pass")
        finally:
            temp_file.unlink()


if __name__ == '__main__':
    unittest.main() 