#!/usr/bin/env python3
"""
Unit tests for BusinessRulesValidator

Tests business rule validation functionality including destructive command detection
and logic check promotion suggestions.
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

from validators.business_rules import BusinessRulesValidator
from utils.validation_result import ValidationResult


class TestBusinessRulesValidator(unittest.TestCase):
    """Test cases for BusinessRulesValidator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = BusinessRulesValidator()
    
    def test_unmarked_destructive_detection(self):
        """Test detection of destructive commands not marked as destructive"""
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
                                'shellCommand': 'rm -rf /tmp/test',
                                'destructive': False  # Should be True
                            },
                            {
                                'shellCommand': 'mkfs.ext4 /dev/sdb1',
                                'destructive': False  # Should be True
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
            self.assertFalse(results.success, "Unmarked destructive commands should fail")
            self.assertTrue(any("destructive" in error.lower() for error in results.errors), 
                          "Should have destructive command errors")
        finally:
            temp_file.unlink()
    
    def test_properly_marked_destructive(self):
        """Test that properly marked destructive commands pass validation"""
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
                                'shellCommand': 'rm -rf /tmp/test',
                                'destructive': True  # Correctly marked
                            },
                            {
                                'shellCommand': 'mkfs.ext4 /dev/sdb1',
                                'destructive': True  # Correctly marked
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
            self.assertTrue(results.success, f"Properly marked destructive commands should pass: {results.errors}")
        finally:
            temp_file.unlink()
    
    def test_false_destructive_detection(self):
        """Test detection of commands incorrectly marked as destructive"""
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
                                'shellCommand': 'ls -la',
                                'destructive': True  # Should be False
                            },
                            {
                                'shellCommand': 'echo "Hello World"',
                                'destructive': True  # Should be False
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
            self.assertFalse(results.success, "False destructive marking should fail")
            self.assertTrue(any("destructive" in error.lower() for error in results.errors), 
                          "Should have false destructive errors")
        finally:
            temp_file.unlink()
    
    def test_logic_check_promotion_suggestion(self):
        """Test suggestions for logic check promotion"""
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
                                'shellCommand': '[ -n "$SUDO_USER" ] && echo "sudo_active" || echo "no_sudo"',
                                'destructive': False
                            },
                            {
                                'shellCommand': 'test -f /etc/passwd && echo "exists" || echo "missing"',
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
            # Should pass but with suggestions
            self.assertTrue(results.success, "Logic checks should pass validation")
            self.assertTrue(len(results.warnings) > 0, "Should have logic check promotion warnings")
        finally:
            temp_file.unlink()
    
    def test_validation_elements_not_promoted(self):
        """Test that validation elements are not suggested for promotion"""
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
            yaml.dump(script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(script, temp_file)
            self.assertTrue(results.success, "Validation elements should pass")
            # Should not have logic check promotion warnings for validation elements
            logic_warnings = [w for w in results.warnings if "logic" in w.lower()]
            self.assertEqual(len(logic_warnings), 0, "Should not suggest promotion for validation elements")
        finally:
            temp_file.unlink()
    
    def test_readonly_commands_not_destructive(self):
        """Test that read-only commands are not flagged as destructive"""
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
                                'shellCommand': 'ls -la',
                                'destructive': False
                            },
                            {
                                'shellCommand': 'cat /etc/passwd',
                                'destructive': False
                            },
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
            yaml.dump(script, f)
            temp_file = Path(f.name)
        
        try:
            results = self.validator.validate(script, temp_file)
            self.assertTrue(results.success, f"Read-only commands should pass: {results.errors}")
        finally:
            temp_file.unlink()
    
    def test_mixed_script_validation(self):
        """Test validation of script with mixed command types"""
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
                                'shellCommand': 'ls -la',
                                'destructive': False
                            },
                            {
                                'shellCommand': 'rm -rf /tmp/test',
                                'destructive': True  # Correctly marked
                            },
                            {
                                'shellCommand': 'echo "Hello World"',
                                'destructive': False
                            },
                            {
                                'shellCommand': 'mkfs.ext4 /dev/sdb1',
                                'destructive': False  # Should be True
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
            self.assertFalse(results.success, "Mixed script with unmarked destructive should fail")
            self.assertTrue(any("destructive" in error.lower() for error in results.errors), 
                          "Should have destructive command errors")
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
                                'shellCommand': 'rm -rf /tmp/test',
                                'destructive': True
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