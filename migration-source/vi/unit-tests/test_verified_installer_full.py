#!/usr/bin/env python3
"""
Full Unit Tests for verified_installer.py
Comprehensive tests including edge cases, error handling, and negative scenarios
Execution time: 1-2 minutes
Run on: Nightly builds, pre-release
"""

import unittest
import tempfile
import json
import subprocess
import sys
import os
from pathlib import Path
from typing import Dict, Any

# Add the verified-installer src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Add viscriptlint to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "viscriptlint" / "src"))

from verified_installer import VerifiedInstaller


class TestVerifiedInstallerFull(unittest.TestCase):
    """Full tests - comprehensive validation including edge cases and errors"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.installer = VerifiedInstaller(verbose=False)
        self.test_viscript = Path(__file__).parent / "test_clean_viscript.json"
        
        # Create temporary files for testing
        self.temp_dir = tempfile.mkdtemp()
        self.temp_files = []
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Remove temporary files
        for temp_file in self.temp_files:
            if Path(temp_file).exists():
                Path(temp_file).unlink()
    
    def create_temp_viscript(self, content: Dict[str, Any]) -> Path:
        """Create a temporary viScript file for testing"""
        temp_file = Path(self.temp_dir) / f"test_{len(self.temp_files)}.json"
        with open(temp_file, 'w') as f:
            json.dump(content, f, indent=2)
        self.temp_files.append(temp_file)
        return temp_file
    
    def get_env_with_viscriptlint(self):
        """Get environment with viscriptlint path"""
        env = os.environ.copy()
        viscriptlint_path = str(Path(__file__).parent.parent.parent / "viscriptlint" / "src")
        env['PYTHONPATH'] = f"{viscriptlint_path}:{env.get('PYTHONPATH', '')}"
        return env
    
    def test_no_arguments(self):
        """Test behavior with no arguments"""
        script_path = Path(__file__).parent.parent / "src" / "verified_installer.py"
        
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            env=self.get_env_with_viscriptlint()
        )
        
        self.assertNotEqual(result.returncode, 0, "No arguments should fail")
        # Check either stdout or stderr for error message
        error_output = result.stdout + result.stderr
        self.assertIn("error:", error_output.lower(), "Should show error for missing file")
    
    def test_nonexistent_viscript(self):
        """Test with non-existent viScript file"""
        script_path = Path(__file__).parent.parent / "src" / "verified_installer.py"
        
        result = subprocess.run(
            [sys.executable, str(script_path), "nonexistent.json"],
            capture_output=True,
            text=True,
            env=self.get_env_with_viscriptlint()
        )
        
        self.assertNotEqual(result.returncode, 0, "Non-existent file should fail")
        # Check either stdout or stderr for error message
        error_output = result.stdout + result.stderr
        self.assertIn("not found", error_output, "Should show file not found error")
    
    def test_invalid_json_viscript(self):
        """Test with invalid JSON viScript"""
        script_path = Path(__file__).parent.parent / "src" / "verified_installer.py"
        
        # Create invalid JSON file
        invalid_json = self.create_temp_viscript({"invalid": "json"})
        
        result = subprocess.run(
            [sys.executable, str(script_path), str(invalid_json)],
            capture_output=True,
            text=True,
            env=self.get_env_with_viscriptlint()
        )
        
        self.assertNotEqual(result.returncode, 0, "Invalid JSON should fail")
    
    def test_deprecated_fields_rejection(self):
        """Test that deprecated fields are rejected"""
        deprecated_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "description": "Test phase",
                    "checks": [
                        {
                            "name": "test_check",
                            "description": "Test check",
                            "command": "echo 'test'",
                            "validation_type": "return_value",
                            "expected_return": 0,
                            "severity": "critical",
                            "critical": True,  # Deprecated field
                            "weight": 2  # Deprecated field
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(deprecated_viscript)
        
        # Should fail validation due to deprecated fields
        success = self.installer.load_viscript(temp_file)
        self.assertFalse(success, "viScript with deprecated fields should fail validation")
    
    def test_missing_severity_field(self):
        """Test that missing severity field is rejected"""
        missing_severity_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "description": "Test phase",
                    "checks": [
                        {
                            "name": "test_check",
                            "description": "Test check",
                            "command": "echo 'test'",
                            "validation_type": "return_value",
                            "expected_return": 0
                            # Missing severity field
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(missing_severity_viscript)
        
        # Should fail validation due to missing severity
        success = self.installer.load_viscript(temp_file)
        self.assertFalse(success, "viScript with missing severity should fail validation")
    
    def test_invalid_severity_value(self):
        """Test that invalid severity values are rejected"""
        invalid_severity_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "description": "Test phase",
                    "checks": [
                        {
                            "name": "test_check",
                            "description": "Test check",
                            "command": "echo 'test'",
                            "validation_type": "return_value",
                            "expected_return": 0,
                            "severity": "invalid_severity"  # Invalid severity
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(invalid_severity_viscript)
        
        # Should fail validation due to invalid severity
        success = self.installer.load_viscript(temp_file)
        self.assertFalse(success, "viScript with invalid severity should fail validation")
    
    def test_missing_required_fields(self):
        """Test missing required fields validation"""
        missing_fields_viscript = {
            "installation_type": "test",
            # Missing version
            "phases": [
                {
                    "name": "test_phase",
                    # Missing description
                    "checks": [
                        {
                            "name": "test_check",
                            # Missing description
                            "command": "echo 'test'",
                            # Missing validation_type
                            "severity": "informational"
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(missing_fields_viscript)
        
        # Should fail validation due to missing required fields
        success = self.installer.load_viscript(temp_file)
        self.assertFalse(success, "viScript with missing required fields should fail validation")
    
    def test_invalid_validation_type(self):
        """Test invalid validation type rejection"""
        invalid_validation_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "description": "Test phase",
                    "checks": [
                        {
                            "name": "test_check",
                            "description": "Test check",
                            "command": "echo 'test'",
                            "validation_type": "invalid_type",  # Invalid validation type
                            "severity": "informational"
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(invalid_validation_viscript)
        
        # Should fail validation due to invalid validation type
        success = self.installer.load_viscript(temp_file)
        self.assertFalse(success, "viScript with invalid validation type should fail validation")
    
    def test_empty_command_validation(self):
        """Test empty command validation"""
        empty_command_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "description": "Test phase",
                    "checks": [
                        {
                            "name": "empty_check",
                            "description": "Test check with empty command",
                            "command": "",  # Empty command
                            "validation_type": "return_value",
                            "expected_return": 0,
                            "severity": "informational"
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(empty_command_viscript)
        
        # Should fail validation due to empty command
        success = self.installer.load_viscript(temp_file)
        self.assertFalse(success, "viScript with empty command should fail validation")
    
    def test_complex_command_validation(self):
        """Test complex command with special characters"""
        complex_command_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "description": "Test phase",
                    "checks": [
                        {
                            "name": "complex_check",
                            "description": "Test check with complex command",
                            "command": "echo 'test with spaces and \"quotes\" and \\backslashes\\'",
                            "validation_type": "output_pattern",
                            "expected_pattern": "test with spaces and \"quotes\" and \\\\backslashes\\\\",
                            "severity": "critical"
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(complex_command_viscript)
        
        # Should load successfully
        success = self.installer.load_viscript(temp_file)
        self.assertTrue(success, "viScript with complex command should load successfully")
    
    def test_unicode_character_validation(self):
        """Test Unicode characters in descriptions"""
        unicode_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "description": "Test phase with Unicode: 🚀",
                    "checks": [
                        {
                            "name": "unicode_check",
                            "description": "Test check with Unicode: ✅",
                            "command": "echo 'unicode_test'",
                            "validation_type": "return_value",
                            "expected_return": 0,
                            "severity": "informational"
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(unicode_viscript)
        
        # Should load successfully
        success = self.installer.load_viscript(temp_file)
        self.assertTrue(success, "viScript with Unicode characters should load successfully")
    
    def test_special_characters_in_names(self):
        """Test special characters in check names"""
        special_chars_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "description": "Test phase",
                    "checks": [
                        {
                            "name": "special_chars_test_123",
                            "description": "Test check with special characters in name",
                            "command": "echo 'special_chars_test'",
                            "validation_type": "return_value",
                            "expected_return": 0,
                            "severity": "critical"
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(special_chars_viscript)
        
        # Should load successfully
        success = self.installer.load_viscript(temp_file)
        self.assertTrue(success, "viScript with special characters in names should load successfully")
    
    def test_long_description_validation(self):
        """Test very long descriptions"""
        long_desc_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "description": "Test phase with very long description that exceeds normal limits and should be handled gracefully by the system without causing any issues or errors during validation or execution",
                    "checks": [
                        {
                            "name": "long_desc_check",
                            "description": "Test check with very long description that exceeds normal limits and should be handled gracefully by the system without causing any issues or errors during validation or execution",
                            "command": "echo 'long_description_test'",
                            "validation_type": "return_value",
                            "expected_return": 0,
                            "severity": "informational"
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(long_desc_viscript)
        
        # Should load successfully
        success = self.installer.load_viscript(temp_file)
        self.assertTrue(success, "viScript with long descriptions should load successfully")
    
    def test_unexpected_attributes_rejection(self):
        """Test that unexpected attributes are rejected"""
        unexpected_attrs_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "unexpected_top_level": "should_be_rejected",
            "phases": [
                {
                    "name": "test_phase",
                    "description": "Test phase",
                    "unexpected_phase_attr": "should_be_rejected",
                    "checks": [
                        {
                            "name": "unexpected_check",
                            "description": "Test check with unexpected attributes",
                            "command": "echo 'unexpected_attributes_test'",
                            "validation_type": "return_value",
                            "expected_return": 0,
                            "severity": "informational",
                            "unexpected_string": "this_should_be_rejected",
                            "unexpected_number": 42,
                            "unexpected_boolean": True,
                            "unexpected_array": ["item1", "item2"],
                            "unexpected_object": {
                                "nested_key": "nested_value",
                                "another_nested": 123
                            },
                            "unexpected_null": None
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(unexpected_attrs_viscript)
        
        # Should fail validation due to unexpected attributes
        success = self.installer.load_viscript(temp_file)
        self.assertFalse(success, "viScript with unexpected attributes should fail validation")
    
    def test_failure_scenario_validation(self):
        """Test various failure scenarios"""
        failure_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "failure_tests",
                    "description": "Test various failure scenarios",
                    "checks": [
                        {
                            "name": "nonexistent_command",
                            "description": "Try to execute non-existent command",
                            "command": "nonexistent_command_that_fails",
                            "validation_type": "return_value",
                            "expected_return": 0,
                            "severity": "informational"
                        },
                        {
                            "name": "wrong_pattern",
                            "description": "Check for pattern that doesn't exist",
                            "command": "echo 'hello world'",
                            "validation_type": "output_pattern",
                            "expected_pattern": "nonexistent_pattern",
                            "severity": "informational"
                        },
                        {
                            "name": "critical_failure",
                            "description": "Critical check that should fail",
                            "command": "false",
                            "validation_type": "return_value",
                            "expected_return": 0,
                            "severity": "critical"
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(failure_viscript)
        
        # Should load successfully (validation should pass even for failure scenarios)
        success = self.installer.load_viscript(temp_file)
        self.assertTrue(success, "viScript with failure scenarios should load successfully")
    
    def test_all_validation_types(self):
        """Test all validation types comprehensively"""
        all_validation_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "validation_tests",
                    "description": "Test all validation types",
                    "checks": [
                        {
                            "name": "return_value_test",
                            "description": "Test return value validation",
                            "command": "echo 'return_test'",
                            "validation_type": "return_value",
                            "expected_return": 0,
                            "severity": "informational"
                        },
                        {
                            "name": "output_pattern_test",
                            "description": "Test output pattern validation",
                            "command": "echo 'pattern_test'",
                            "validation_type": "output_pattern",
                            "expected_pattern": "pattern",
                            "severity": "informational"
                        },
                        {
                            "name": "both_validation_test",
                            "description": "Test both return value and pattern validation",
                            "command": "echo 'both_test'",
                            "validation_type": "both",
                            "expected_return": 0,
                            "expected_pattern": "both",
                            "severity": "critical"
                        },
                        {
                            "name": "none_validation_test",
                            "description": "Test no validation (execute only)",
                            "command": "echo 'execute_only'",
                            "validation_type": "none",
                            "severity": "informational"
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(all_validation_viscript)
        
        # Should load successfully
        success = self.installer.load_viscript(temp_file)
        self.assertTrue(success, "viScript with all validation types should load successfully")


class TestVerifiedInstallerFullIntegration(unittest.TestCase):
    """Full integration tests - comprehensive end-to-end scenarios"""
    
    def test_end_to_end_comprehensive_execution(self):
        """Test comprehensive end-to-end execution with complex viScript"""
        # Create a comprehensive test viScript
        comprehensive_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "description": "Comprehensive test viScript",
            "prerequisites": {
                "required_viScripts": ["prereq1.json", "prereq2.json"],
                "warnings": ["This is a comprehensive test warning"]
            },
            "phases": [
                {
                    "name": "phase_1",
                    "description": "First phase with multiple checks",
                    "checks": [
                        {
                            "name": "echo_test",
                            "description": "Test echo command",
                            "command": "echo 'test'",
                            "validation_type": "output_pattern",
                            "expected_pattern": "test",
                            "severity": "informational"
                        },
                        {
                            "name": "success_test",
                            "description": "Test successful command",
                            "command": "echo 'success'",
                            "validation_type": "return_value",
                            "expected_return": 0,
                            "severity": "critical"
                        }
                    ]
                },
                {
                    "name": "phase_2",
                    "description": "Second phase with different validation types",
                    "checks": [
                        {
                            "name": "both_validation_test",
                            "description": "Test both validations",
                            "command": "echo 'both test'",
                            "validation_type": "both",
                            "expected_return": 0,
                            "expected_pattern": "both",
                            "severity": "critical"
                        },
                        {
                            "name": "none_validation_test",
                            "description": "Test no validation",
                            "command": "echo 'execute only'",
                            "validation_type": "none",
                            "severity": "informational"
                        }
                    ]
                }
            ],
            "next_step": "next_comprehensive_viscript.json"
        }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(comprehensive_viscript, f)
            temp_file = Path(f.name)
        
        try:
            # Test the Python script directly
            script_path = Path(__file__).parent.parent / "src" / "verified_installer.py"
            
            # Set PYTHONPATH for viscriptlint import
            env = os.environ.copy()
            viscriptlint_path = str(Path(__file__).parent.parent.parent / "viscriptlint" / "src")
            env['PYTHONPATH'] = f"{viscriptlint_path}:{env.get('PYTHONPATH', '')}"
            
            result = subprocess.run(
                [sys.executable, str(script_path), str(temp_file)],
                capture_output=True,
                text=True,
                env=env,
                input="y\n"  # Answer 'yes' to confirmation prompt
            )
            
            # Should execute successfully
            self.assertIn("SUCCESS", result.stdout, "Should show successful check execution")
            
        finally:
            # Clean up
            if temp_file.exists():
                temp_file.unlink()


def run_full_tests():
    """Run full tests only"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add full test cases
    suite.addTests(loader.loadTestsFromTestCase(TestVerifiedInstallerFull))
    suite.addTests(loader.loadTestsFromTestCase(TestVerifiedInstallerFullIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n=== Full Test Summary ===")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\n=== Failures ===")
        for test, traceback in result.failures:
            print(f"FAIL: {test}")
            print(traceback)
    
    if result.errors:
        print(f"\n=== Errors ===")
        for test, traceback in result.errors:
            print(f"ERROR: {test}")
            print(traceback)
    
    return len(result.failures) + len(result.errors) == 0


if __name__ == "__main__":
    # Set up environment for testing
    os.environ['PYTHONPATH'] = f"{Path(__file__).parent.parent.parent / 'viscriptlint' / 'src'}:{os.environ.get('PYTHONPATH', '')}"
    
    success = run_full_tests()
    sys.exit(0 if success else 1) 