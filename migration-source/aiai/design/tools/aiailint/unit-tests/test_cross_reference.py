#!/usr/bin/env python3
"""
Unit tests for CrossReferenceValidator

Tests cross-reference validation functionality including circular reference detection
and unreachable element detection.
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

from validators.cross_reference import CrossReferenceValidator
from utils.validation_result import ValidationResult


class TestCrossReferenceValidator(unittest.TestCase):
    """Test cases for CrossReferenceValidator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = CrossReferenceValidator()
    
    def test_valid_references(self):
        """Test that valid cross-references pass validation"""
        script = {
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
                        'next_step': 'setup_script'
                    },
                    'setup_script': {
                        'commands': [
                            {
                                'shellCommand': 'mkdir -p /tmp/test',
                                'destructive': False
                            }
                        ],
                        'next_step': 'cleanup_script'
                    },
                    'cleanup_script': {
                        'commands': [
                            {
                                'shellCommand': 'rm -rf /tmp/test',
                                'destructive': True
                            }
                        ]
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(script, temp_file)
            self.assertTrue(results.success, f"Valid references should pass: {results.errors}")
        finally:
            temp_file.unlink()
    
    def test_missing_reference(self):
        """Test detection of missing script references"""
        script = {
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
                        'next_step': 'nonexistent_script'  # Missing script
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(script, temp_file)
            self.assertFalse(results.success, "Missing reference should fail")
            self.assertTrue(any("reference" in error.lower() for error in results.errors), 
                          "Should have missing reference error")
        finally:
            temp_file.unlink()
    
    def test_circular_reference_detection(self):
        """Test detection of circular references"""
        script = {
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
                        'next_step': 'setup_script'
                    },
                    'setup_script': {
                        'commands': [
                            {
                                'shellCommand': 'mkdir -p /tmp/test',
                                'destructive': False
                            }
                        ],
                        'next_step': 'main'  # Circular reference
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(script, temp_file)
            self.assertFalse(results.success, "Circular reference should fail")
            self.assertTrue(any("circular" in error.lower() for error in results.errors), 
                          "Should have circular reference error")
        finally:
            temp_file.unlink()
    
    def test_unreachable_elements(self):
        """Test detection of unreachable elements"""
        script = {
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
                        'next_step': 'setup_script'
                    },
                    'setup_script': {
                        'commands': [
                            {
                                'shellCommand': 'mkdir -p /tmp/test',
                                'destructive': False
                            }
                        ]
                        # No next_step, so cleanup_script is unreachable
                    },
                    'cleanup_script': {
                        'commands': [
                            {
                                'shellCommand': 'rm -rf /tmp/test',
                                'destructive': True
                            }
                        ]
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(script, temp_file)
            self.assertFalse(results.success, "Unreachable elements should fail")
            self.assertTrue(any("unreachable" in error.lower() for error in results.errors), 
                          "Should have unreachable element error")
        finally:
            temp_file.unlink()
    
    def test_self_reference(self):
        """Test detection of self-references"""
        script = {
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
                        'next_step': 'main'  # Self-reference
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(script, temp_file)
            self.assertFalse(results.success, "Self-reference should fail")
            self.assertTrue(any("circular" in error.lower() for error in results.errors), 
                          "Should have circular reference error")
        finally:
            temp_file.unlink()
    
    def test_complex_circular_reference(self):
        """Test detection of complex circular references"""
        script = {
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
                        'next_step': 'setup_script'
                    },
                    'setup_script': {
                        'commands': [
                            {
                                'shellCommand': 'mkdir -p /tmp/test',
                                'destructive': False
                            }
                        ],
                        'next_step': 'process_script'
                    },
                    'process_script': {
                        'commands': [
                            {
                                'shellCommand': 'echo "Processing"',
                                'destructive': False
                            }
                        ],
                        'next_step': 'main'  # Creates circular reference
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(script, temp_file)
            self.assertFalse(results.success, "Complex circular reference should fail")
            self.assertTrue(any("circular" in error.lower() for error in results.errors), 
                          "Should have circular reference error")
        finally:
            temp_file.unlink()
    
    def test_valid_script_without_references(self):
        """Test validation of script without cross-references"""
        script = {
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
                            },
                            {
                                'shellCommand': 'ls -la',
                                'destructive': False
                            }
                        ]
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(script, temp_file)
            self.assertTrue(results.success, f"Script without references should pass: {results.errors}")
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