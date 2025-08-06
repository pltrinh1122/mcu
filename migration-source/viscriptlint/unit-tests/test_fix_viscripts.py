#!/usr/bin/env python3

"""
Unit tests for fix_viscripts.py
Tests schema fixing functionality with various scenarios
"""

import unittest
import json
import tempfile
import os
import sys
import subprocess
import shutil
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestFixViscripts(unittest.TestCase):
    """Test cases for fix_viscripts.py functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.script_path = Path(__file__).parent.parent / "src" / "fix_viscripts.py"
        self.test_data_dir = Path(__file__).parent
        
    def create_test_viscript(self, data):
        """Helper to create a temporary test viScript file"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(data, temp_file, indent=2)
        temp_file.close()
        return Path(temp_file.name)
    
    def test_fix_viscript_file_with_critical_field(self):
        """Test fixing viScript with deprecated critical field"""
        test_data = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "checks": [
                        {
                            "name": "test_check",
                            "description": "Test check",
                            "command": "echo test",
                            "critical": True,  # Deprecated field
                            "weight": 1  # Deprecated field
                        }
                    ]
                }
            ]
        }
        
        test_file = self.create_test_viscript(test_data)
        backup_file = test_file.with_suffix(test_file.suffix + ".backup")
        
        try:
            # Run fix script
            result = subprocess.run(
                [sys.executable, str(self.script_path), str(test_file)],
                capture_output=True,
                text=True
            )
            
            self.assertEqual(result.returncode, 0)
            
            # Check that backup was created
            self.assertTrue(backup_file.exists())
            
            # Check that file was fixed
            with open(test_file, 'r') as f:
                fixed_data = json.load(f)
            
            # Check that deprecated fields were removed
            check = fixed_data["phases"][0]["checks"][0]
            self.assertNotIn("critical", check)
            self.assertNotIn("weight", check)
            
            # Check that severity was added
            self.assertIn("severity", check)
            self.assertEqual(check["severity"], "critical")
            
            # Check that validation_type was added
            self.assertIn("validation_type", check)
            self.assertEqual(check["validation_type"], "none")
            
        finally:
            # Cleanup
            if test_file.exists():
                os.unlink(test_file)
            if backup_file.exists():
                os.unlink(backup_file)
    
    def test_fix_viscript_file_with_false_critical(self):
        """Test fixing viScript with critical=False"""
        test_data = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "checks": [
                        {
                            "name": "test_check",
                            "description": "Test check",
                            "command": "echo test",
                            "critical": False  # Should become informational
                        }
                    ]
                }
            ]
        }
        
        test_file = self.create_test_viscript(test_data)
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.script_path), str(test_file)],
                capture_output=True,
                text=True
            )
            
            self.assertEqual(result.returncode, 0)
            
            with open(test_file, 'r') as f:
                fixed_data = json.load(f)
            
            check = fixed_data["phases"][0]["checks"][0]
            self.assertEqual(check["severity"], "informational")
            
        finally:
            if test_file.exists():
                os.unlink(test_file)
    
    def test_fix_viscript_file_with_expected_pattern(self):
        """Test fixing viScript with expected_pattern (should set validation_type to output_pattern)"""
        test_data = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "checks": [
                        {
                            "name": "test_check",
                            "description": "Test check",
                            "command": "echo test",
                            "expected_pattern": "test_pattern",
                            "severity": "critical"
                        }
                    ]
                }
            ]
        }
        
        test_file = self.create_test_viscript(test_data)
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.script_path), str(test_file)],
                capture_output=True,
                text=True
            )
            
            self.assertEqual(result.returncode, 0)
            
            with open(test_file, 'r') as f:
                fixed_data = json.load(f)
            
            check = fixed_data["phases"][0]["checks"][0]
            self.assertEqual(check["validation_type"], "output_pattern")
            
        finally:
            if test_file.exists():
                os.unlink(test_file)
    
    def test_fix_viscript_file_with_expected_return(self):
        """Test fixing viScript with expected_return (should set validation_type to return_value)"""
        test_data = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "checks": [
                        {
                            "name": "test_check",
                            "description": "Test check",
                            "command": "echo test",
                            "expected_return": 0,
                            "severity": "critical"
                        }
                    ]
                }
            ]
        }
        
        test_file = self.create_test_viscript(test_data)
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.script_path), str(test_file)],
                capture_output=True,
                text=True
            )
            
            self.assertEqual(result.returncode, 0)
            
            with open(test_file, 'r') as f:
                fixed_data = json.load(f)
            
            check = fixed_data["phases"][0]["checks"][0]
            self.assertEqual(check["validation_type"], "return_value")
            
        finally:
            if test_file.exists():
                os.unlink(test_file)
    
    def test_fix_viscript_file_already_fixed(self):
        """Test fixing viScript that's already in correct format"""
        test_data = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "checks": [
                        {
                            "name": "test_check",
                            "description": "Test check",
                            "command": "echo test",
                            "validation_type": "none",
                            "severity": "critical"
                        }
                    ]
                }
            ]
        }
        
        test_file = self.create_test_viscript(test_data)
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.script_path), str(test_file)],
                capture_output=True,
                text=True
            )
            
            self.assertEqual(result.returncode, 0)
            
            # File should remain unchanged
            with open(test_file, 'r') as f:
                fixed_data = json.load(f)
            
            self.assertEqual(fixed_data, test_data)
            
        finally:
            if test_file.exists():
                os.unlink(test_file)
    
    def test_fix_viscript_file_nonexistent(self):
        """Test fixing nonexistent file"""
        result = subprocess.run(
            [sys.executable, str(self.script_path), "/nonexistent/file.json"],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 1)
        self.assertIn("Error: File not found", result.stdout)
    
    def test_fix_viscript_file_invalid_json(self):
        """Test fixing file with invalid JSON"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json}')
            invalid_file = Path(f.name)
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.script_path), str(invalid_file)],
                capture_output=True,
                text=True
            )
            
            self.assertEqual(result.returncode, 1)
            
        finally:
            os.unlink(invalid_file)
    
    def test_fix_viscript_file_help(self):
        """Test help functionality"""
        result = subprocess.run(
            [sys.executable, str(self.script_path), "--help"],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("viScript Schema Fix Script", result.stdout)
    
    def test_fix_viscript_file_no_args(self):
        """Test running without arguments (should error out)"""
        result = subprocess.run(
            [sys.executable, str(self.script_path)],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 1)
        self.assertIn("Error: File argument is required", result.stdout)
        self.assertIn("Usage: python3 fix_viscripts.py <file>", result.stdout)
    
    def test_fix_viscript_file_complex_scenario(self):
        """Test fixing viScript with multiple complex scenarios"""
        test_data = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "checks": [
                        {
                            "name": "check1",
                            "description": "Check with critical=True",
                            "command": "echo test1",
                            "critical": True,
                            "weight": 5
                        },
                        {
                            "name": "check2",
                            "description": "Check with critical=False",
                            "command": "echo test2",
                            "critical": False,
                            "weight": 3
                        },
                        {
                            "name": "check3",
                            "description": "Check with expected_pattern",
                            "command": "echo test3",
                            "expected_pattern": "test3",
                            "severity": "critical"
                        },
                        {
                            "name": "check4",
                            "description": "Check with expected_return",
                            "command": "echo test4",
                            "expected_return": 0,
                            "severity": "informational"
                        },
                        {
                            "name": "check5",
                            "description": "Check with neither pattern nor return",
                            "command": "echo test5",
                            "severity": "critical"
                        }
                    ]
                }
            ]
        }
        
        test_file = self.create_test_viscript(test_data)
        backup_file = test_file.with_suffix(test_file.suffix + ".backup")
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.script_path), str(test_file)],
                capture_output=True,
                text=True
            )
            
            self.assertEqual(result.returncode, 0)
            self.assertTrue(backup_file.exists())
            
            with open(test_file, 'r') as f:
                fixed_data = json.load(f)
            
            checks = fixed_data["phases"][0]["checks"]
            
            # Check 1: critical=True should become severity=critical, validation_type=none
            self.assertEqual(checks[0]["severity"], "critical")
            self.assertEqual(checks[0]["validation_type"], "none")
            self.assertNotIn("critical", checks[0])
            self.assertNotIn("weight", checks[0])
            
            # Check 2: critical=False should become severity=informational, validation_type=none
            self.assertEqual(checks[1]["severity"], "informational")
            self.assertEqual(checks[1]["validation_type"], "none")
            self.assertNotIn("critical", checks[1])
            self.assertNotIn("weight", checks[1])
            
            # Check 3: expected_pattern should set validation_type=output_pattern
            self.assertEqual(checks[2]["validation_type"], "output_pattern")
            
            # Check 4: expected_return should set validation_type=return_value
            self.assertEqual(checks[3]["validation_type"], "return_value")
            
            # Check 5: neither pattern nor return should set validation_type=none
            self.assertEqual(checks[4]["validation_type"], "none")
            
        finally:
            if test_file.exists():
                os.unlink(test_file)
            if backup_file.exists():
                os.unlink(backup_file)
    
    def test_fix_empty_expected_pattern_informational(self):
        """Test fixing empty expected_pattern for informational checks"""
        test_data = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "checks": [
                        {
                            "name": "informational_check",
                            "description": "Test informational check",
                            "command": "echo test",
                            "validation_type": "output_pattern",
                            "expected_pattern": "",
                            "severity": "informational"
                        }
                    ]
                }
            ]
        }
        
        test_file = self.create_test_viscript(test_data)
        backup_file = test_file.with_suffix(test_file.suffix + ".backup")
        
        try:
            # Run fix script
            result = subprocess.run(
                [sys.executable, str(self.script_path), str(test_file)],
                capture_output=True,
                text=True
            )
            
            self.assertEqual(result.returncode, 0)
            
            # Check that file was fixed
            with open(test_file, 'r') as f:
                fixed_data = json.load(f)
            
            check = fixed_data["phases"][0]["checks"][0]
            self.assertEqual(check["validation_type"], "none")
            self.assertNotIn("expected_pattern", check)
            self.assertEqual(check["severity"], "informational")
            
        finally:
            # Cleanup
            if test_file.exists():
                os.unlink(test_file)
            if backup_file.exists():
                os.unlink(backup_file)
    
    def test_fix_empty_expected_pattern_critical(self):
        """Test fixing empty expected_pattern for critical checks"""
        test_data = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "checks": [
                        {
                            "name": "critical_check",
                            "description": "Test critical check",
                            "command": "echo test",
                            "validation_type": "output_pattern",
                            "expected_pattern": "",
                            "severity": "critical"
                        }
                    ]
                }
            ]
        }
        
        test_file = self.create_test_viscript(test_data)
        backup_file = test_file.with_suffix(test_file.suffix + ".backup")
        
        try:
            # Run fix script
            result = subprocess.run(
                [sys.executable, str(self.script_path), str(test_file)],
                capture_output=True,
                text=True
            )
            
            self.assertEqual(result.returncode, 0)
            
            # Check that file was fixed
            with open(test_file, 'r') as f:
                fixed_data = json.load(f)
            
            check = fixed_data["phases"][0]["checks"][0]
            self.assertEqual(check["validation_type"], "none")
            self.assertNotIn("expected_pattern", check)
            self.assertEqual(check["severity"], "critical")
            
        finally:
            # Cleanup
            if test_file.exists():
                os.unlink(test_file)
            if backup_file.exists():
                os.unlink(backup_file)
    
    def test_fix_empty_expected_pattern_general(self):
        """Test fixing empty expected_pattern for any severity"""
        test_data = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "checks": [
                        {
                            "name": "general_check",
                            "description": "Test general check",
                            "command": "echo test",
                            "validation_type": "output_pattern",
                            "expected_pattern": ""
                            # No severity specified
                        }
                    ]
                }
            ]
        }
        
        test_file = self.create_test_viscript(test_data)
        backup_file = test_file.with_suffix(test_file.suffix + ".backup")
        
        try:
            # Run fix script
            result = subprocess.run(
                [sys.executable, str(self.script_path), str(test_file)],
                capture_output=True,
                text=True
            )
            
            self.assertEqual(result.returncode, 0)
            
            # Check that file was fixed
            with open(test_file, 'r') as f:
                fixed_data = json.load(f)
            
            check = fixed_data["phases"][0]["checks"][0]
            self.assertEqual(check["validation_type"], "none")
            self.assertNotIn("expected_pattern", check)
            
        finally:
            # Cleanup
            if test_file.exists():
                os.unlink(test_file)
            if backup_file.exists():
                os.unlink(backup_file)
    
    def test_fix_regression_issues_file(self):
        """Test fixing the regression issues file with multiple problems"""
        test_file = Path(__file__).parent / "test_issues.json"
        backup_file = test_file.with_suffix(test_file.suffix + ".backup")
        
        # Create a backup of the original file
        if not backup_file.exists():
            shutil.copy2(test_file, backup_file)
        
        try:
            # Run fix script
            result = subprocess.run(
                [sys.executable, str(self.script_path), str(test_file)],
                capture_output=True,
                text=True
            )
            
            self.assertEqual(result.returncode, 0)
            
            # Check that file was fixed
            with open(test_file, 'r') as f:
                fixed_data = json.load(f)
            
            check = fixed_data["phases"][0]["checks"][0]
            
            # Should fix empty expected_pattern
            self.assertEqual(check["validation_type"], "none")
            self.assertNotIn("expected_pattern", check)
            self.assertEqual(check["severity"], "informational")
            
            # Note: empty command is not fixed by fix_viscripts.py
            # as it's a validation issue, not a schema issue
            
        finally:
            # Restore the original file for future tests
            if backup_file.exists():
                shutil.copy2(backup_file, test_file)


if __name__ == "__main__":
    unittest.main() 