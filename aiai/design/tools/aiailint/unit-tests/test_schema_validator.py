#!/usr/bin/env python3
"""
Unit tests for SchemaValidator

Tests JSON Schema validation functionality for AIAI Scripts.
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

from validators.schema_validator import SchemaValidator
from utils.validation_result import ValidationResult


class TestSchemaValidator(unittest.TestCase):
    """Test cases for SchemaValidator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = SchemaValidator()
    
    def test_valid_schema(self):
        """Test that valid AIAI Script passes schema validation"""
        valid_script = {
            'metadata': {
                'name': 'test_script',
                'version': '1.0.0',
                'description': 'Test script'
            },
            'body': {
                'scripts': {
                    'main': {
                        'commands': [
                            {
                                'shellCommand': 'echo "Hello World"',
                                'destructive': False
                            }
                        ]
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(valid_script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(valid_script, temp_file)
            self.assertTrue(results.success, f"Valid schema should pass: {results.errors}")
        finally:
            temp_file.unlink()
    
    def test_missing_required_metadata(self):
        """Test that missing required metadata fields are detected"""
        invalid_script = {
            'metadata': {
                'name': 'test_script'
                # Missing version
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
            yaml.dump(invalid_script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(invalid_script, temp_file)
            self.assertFalse(results.success, "Missing required fields should fail")
            self.assertTrue(any("schema" in error.lower() for error in results.errors), 
                          "Should have schema validation errors")
        finally:
            temp_file.unlink()
    
    def test_invalid_element_type(self):
        """Test that invalid element types are detected"""
        invalid_script = {
            'metadata': {
                'name': 'test_script',
                'version': '1.0.0'
            },
            'body': {
                'scripts': {
                    'main': {
                        'commands': [
                            {
                                'type': 'invalid_type',  # Invalid type
                                'shellCommand': 'echo "Hello World"'
                            }
                        ]
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(invalid_script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(invalid_script, temp_file)
            self.assertFalse(results.success, "Invalid element type should fail")
        finally:
            temp_file.unlink()
    
    def test_missing_required_body_fields(self):
        """Test that missing required body fields are detected"""
        invalid_script = {
            'metadata': {
                'name': 'test_script',
                'version': '1.0.0'
            },
            'body': {
                'scripts': {
                    'main': {
                        'commands': [
                            {
                                # Missing shellCommand
                                'destructive': False
                            }
                        ]
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(invalid_script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(invalid_script, temp_file)
            self.assertFalse(results.success, "Missing required fields should fail")
        finally:
            temp_file.unlink()
    
    def test_invalid_destructive_type(self):
        """Test that invalid destructive field type is detected"""
        invalid_script = {
            'metadata': {
                'name': 'test_script',
                'version': '1.0.0'
            },
            'body': {
                'scripts': {
                    'main': {
                        'commands': [
                            {
                                'shellCommand': 'echo "Hello World"',
                                'destructive': 'yes'  # Should be boolean
                            }
                        ]
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(invalid_script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(invalid_script, temp_file)
            self.assertFalse(results.success, "Invalid destructive type should fail")
        finally:
            temp_file.unlink()
    
    def test_validation_element(self):
        """Test that validation elements are properly validated"""
        valid_script = {
            'metadata': {
                'name': 'test_script',
                'version': '1.0.0'
            },
            'body': {
                'scripts': {
                    'main': {
                        'commands': [
                            {
                                'shellCommand': 'echo "Hello World"',
                                'destructive': False
                            }
                        ],
                        'validations': [
                            {
                                'shellCommand': '[ -f /etc/passwd ]',
                                'expectedOutput': '0'
                            }
                        ]
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(valid_script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(valid_script, temp_file)
            self.assertTrue(results.success, f"Valid validation element should pass: {results.errors}")
        finally:
            temp_file.unlink()
    
    def test_script_element(self):
        """Test that script elements are properly validated"""
        valid_script = {
            'metadata': {
                'name': 'test_script',
                'version': '1.0.0'
            },
            'body': {
                'scripts': {
                    'main': {
                        'commands': [
                            {
                                'shellCommand': 'echo "Hello World"',
                                'destructive': False
                            }
                        ]
                    },
                    'setup': {
                        'commands': [
                            {
                                'shellCommand': 'mkdir -p /tmp/test',
                                'destructive': False
                            }
                        ]
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(valid_script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(valid_script, temp_file)
            self.assertTrue(results.success, f"Valid script elements should pass: {results.errors}")
        finally:
            temp_file.unlink()
    
    def test_file_validation(self):
        """Test validation of YAML files"""
        test_data = {
            'metadata': {
                'name': 'test_script',
                'version': '1.0.0'
            },
            'body': {
                'scripts': {
                    'main': {
                        'commands': [
                            {'shellCommand': 'echo "test"', 'destructive': False}
                        ]
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_data, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(test_data, temp_file)
            self.assertTrue(results.success, "Valid file should pass")
        finally:
            temp_file.unlink()
    
    def test_nonexistent_file(self):
        """Test validation of nonexistent file"""
        test_data = {'metadata': {'name': 'test'}, 'body': {'scripts': {}}}
        results = self.validator.validate(test_data, Path("/nonexistent/file.yaml"))
        # Should still work since we're passing the data directly
        self.assertTrue(results.success, "Should work with data even if file doesn't exist")


if __name__ == '__main__':
    unittest.main() 