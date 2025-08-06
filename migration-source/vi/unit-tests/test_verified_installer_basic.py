#!/usr/bin/env python3
"""
Basic Unit Tests for verified_installer.py
Focuses on clean/positive test cases for fast validation
Execution time: < 30 seconds
Run on: Every commit/push
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


class TestVerifiedInstallerBasic(unittest.TestCase):
    """Basic tests - clean/positive cases for fast validation"""
    
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
    
    def test_script_existence(self):
        """Test that the Python script exists and is executable"""
        script_path = Path(__file__).parent.parent / "src" / "verified_installer.py"
        self.assertTrue(script_path.exists(), "verified_installer.py should exist")
        self.assertTrue(script_path.is_file(), "verified_installer.py should be a file")
    
    def test_test_viscript_existence(self):
        """Test that the test viScript exists"""
        self.assertTrue(self.test_viscript.exists(), "Test viScript should exist")
    
    def test_help_functionality(self):
        """Test help functionality"""
        script_path = Path(__file__).parent.parent / "src" / "verified_installer.py"
        
        result = subprocess.run(
            [sys.executable, str(script_path), "--help"],
            capture_output=True,
            text=True,
            env=self.get_env_with_viscriptlint()
        )
        
        self.assertEqual(result.returncode, 0, "Help should exit with code 0")
        self.assertIn("usage:", result.stdout.lower(), "Help should show usage")
    
    def test_valid_viscript_validation(self):
        """Test validation of a valid viScript"""
        if not self.test_viscript.exists():
            self.skipTest("Test viScript not found")
        
        # Test that the viScript loads and validates
        success = self.installer.load_viscript(self.test_viscript)
        self.assertTrue(success, "Valid viScript should load successfully")
    
    def test_validation_result_structure(self):
        """Test that validation results have proper structure"""
        if not self.test_viscript.exists():
            self.skipTest("Test viScript not found")
        
        # Test validation
        success = self.installer.validate_viscript(self.test_viscript)
        
        # Should return a boolean
        self.assertIsInstance(success, bool, "Validation should return boolean")
    
    def test_check_execution(self):
        """Test check execution functionality"""
        if not self.test_viscript.exists():
            self.skipTest("Test viScript not found")
        
        # Load the test viScript
        success = self.installer.load_viscript(self.test_viscript)
        self.assertTrue(success, "Should load test viScript")
        
        # Test executing a check
        check_result = self.installer.execute_check("test_phase", "test_check")
        self.assertIsNotNone(check_result, "Should return a check result")
    
    def test_phase_execution(self):
        """Test phase execution functionality"""
        if not self.test_viscript.exists():
            self.skipTest("Test viScript not found")
        
        # Load the test viScript
        success = self.installer.load_viscript(self.test_viscript)
        self.assertTrue(success, "Should load test viScript")
        
        # Test executing a phase
        phase_result = self.installer.execute_phase("test_phase")
        self.assertIsNotNone(phase_result, "Should return a phase result")
    
    def test_prerequisite_confirmation(self):
        """Test prerequisite confirmation functionality"""
        # Create a viScript with prerequisites
        viscript_with_prereqs = {
            "installation_type": "test",
            "version": "1.0",
            "prerequisites": {
                "required_viScripts": ["prereq1.json", "prereq2.json"],
                "warnings": ["This is a test warning"]
            },
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
                            "severity": "critical"
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(viscript_with_prereqs)
        
        # Load the viScript
        success = self.installer.load_viscript(temp_file)
        self.assertTrue(success, "Should load viScript with prerequisites")
        
        # Test that prerequisite confirmation shows required scripts
        # Note: This test doesn't actually prompt for input, just verifies the method exists
        self.assertTrue(hasattr(self.installer, 'prompt_prerequisite_confirmation'),
                       "Should have prerequisite confirmation method")
    
    def test_simple_viscript_structure(self):
        """Test simple viScript structure validation"""
        simple_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "description": "Simple test viScript",
            "phases": [
                {
                    "name": "simple_phase",
                    "description": "Simple test phase",
                    "checks": [
                        {
                            "name": "simple_check",
                            "description": "Simple test check",
                            "command": "echo 'simple'",
                            "validation_type": "return_value",
                            "expected_return": 0,
                            "severity": "informational"
                        }
                    ]
                }
            ]
        }
        
        temp_file = self.create_temp_viscript(simple_viscript)
        
        # Should load successfully
        success = self.installer.load_viscript(temp_file)
        self.assertTrue(success, "Simple viScript should load successfully")
    
    def test_verbose_mode(self):
        """Test verbose mode functionality"""
        script_path = Path(__file__).parent.parent / "src" / "verified_installer.py"
        
        if not self.test_viscript.exists():
            self.skipTest("Test viScript not found")
        
        result = subprocess.run(
            [sys.executable, str(script_path), str(self.test_viscript), "--verbose"],
            capture_output=True,
            text=True,
            env=self.get_env_with_viscriptlint(),
            input="n\n"  # Answer 'no' to confirmation prompt
        )
        
        # Should show verbose output
        self.assertIn("VERBOSE MODE", result.stdout, "Should show verbose mode message")


class TestVerifiedInstallerBasicIntegration(unittest.TestCase):
    """Basic integration tests - clean end-to-end scenarios"""
    
    def test_end_to_end_simple_execution(self):
        """Test end-to-end execution with a simple viScript"""
        # Create a simple test viScript
        simple_viscript = {
            "installation_type": "test",
            "version": "1.0",
            "phases": [
                {
                    "name": "test_phase",
                    "description": "Test phase",
                    "checks": [
                        {
                            "name": "echo_test",
                            "description": "Test echo command",
                            "command": "echo 'test'",
                            "validation_type": "output_pattern",
                            "expected_pattern": "test",
                            "severity": "informational"
                        }
                    ]
                }
            ]
        }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(simple_viscript, f)
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


def run_basic_tests():
    """Run basic tests only"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add basic test cases
    suite.addTests(loader.loadTestsFromTestCase(TestVerifiedInstallerBasic))
    suite.addTests(loader.loadTestsFromTestCase(TestVerifiedInstallerBasicIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n=== Basic Test Summary ===")
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
    
    success = run_basic_tests()
    sys.exit(0 if success else 1) 