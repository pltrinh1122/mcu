#!/usr/bin/env python3
"""
Integration tests for aiailint tool
"""

import unittest
import subprocess
import tempfile
import os
from pathlib import Path
import sys
import json

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))


class TestAiailintIntegration(unittest.TestCase):
    """Integration tests for aiailint tool"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.aiailint_path = src_dir / "aiailint.py"
    
    def test_basic_file_validation(self):
        """Test basic file validation functionality"""
        test_file = self.test_data_dir / "valid_scripts" / "basic_validation.yaml"
        
        if test_file.exists():
            result = subprocess.run([
                sys.executable, str(self.aiailint_path), 
                "validate", "--file", str(test_file)
            ], capture_output=True, text=True)
            
            self.assertEqual(result.returncode, 0)
            self.assertIn("Validation completed", result.stdout)
    
    def test_invalid_file_validation(self):
        """Test validation of invalid files"""
        test_file = self.test_data_dir / "invalid_scripts" / "syntax_error.yaml"
        
        if test_file.exists():
            result = subprocess.run([
                sys.executable, str(self.aiailint_path), 
                "validate", "--file", str(test_file)
            ], capture_output=True, text=True)
            
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("error", result.stderr.lower())
    
    def test_destructive_commands_validation(self):
        """Test validation of scripts with destructive commands"""
        test_file = self.test_data_dir / "invalid_scripts" / "unmarked_destructive.yaml"
        
        if test_file.exists():
            result = subprocess.run([
                sys.executable, str(self.aiailint_path), 
                "validate", "--file", str(test_file)
            ], capture_output=True, text=True)
            
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("destructive", result.stderr.lower())
    
    def test_json_output_format(self):
        """Test JSON output format"""
        test_file = self.test_data_dir / "valid_scripts" / "basic_validation.yaml"
        
        if test_file.exists():
            result = subprocess.run([
                sys.executable, str(self.aiailint_path), 
                "validate", "--file", str(test_file), "--format", "json"
            ], capture_output=True, text=True)
            
            self.assertEqual(result.returncode, 0)
            
            # Try to parse JSON output
            try:
                json_output = json.loads(result.stdout)
                self.assertIn("success", json_output)
                self.assertIn("errors", json_output)
                self.assertIn("warnings", json_output)
            except json.JSONDecodeError:
                self.fail("Output is not valid JSON")
    
    def test_package_validation(self):
        """Test package validation functionality"""
        package_path = self.test_data_dir / "test_packages" / "valid_package"
        
        if package_path.exists():
            result = subprocess.run([
                sys.executable, str(self.aiailint_path), 
                "validate", "--package", str(package_path)
            ], capture_output=True, text=True)
            
            self.assertEqual(result.returncode, 0)
            self.assertIn("Package validation", result.stdout)
    
    def test_help_output(self):
        """Test help output"""
        result = subprocess.run([
            sys.executable, str(self.aiailint_path), "--help"
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage", result.stdout.lower())
        self.assertIn("aiailint", result.stdout)
    
    def test_validate_subcommand_help(self):
        """Test validate subcommand help"""
        result = subprocess.run([
            sys.executable, str(self.aiailint_path), "validate", "--help"
        ], capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("validate", result.stdout.lower())
        self.assertIn("--file", result.stdout)
        self.assertIn("--package", result.stdout)
    
    def test_nonexistent_file(self):
        """Test handling of nonexistent file"""
        result = subprocess.run([
            sys.executable, str(self.aiailint_path), 
            "validate", "--file", "/nonexistent/file.yaml"
        ], capture_output=True, text=True)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())
    
    def test_nonexistent_package(self):
        """Test handling of nonexistent package"""
        result = subprocess.run([
            sys.executable, str(self.aiailint_path), 
            "validate", "--package", "/nonexistent/package"
        ], capture_output=True, text=True)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())
    
    def test_invalid_command_line_options(self):
        """Test handling of invalid command line options"""
        result = subprocess.run([
            sys.executable, str(self.aiailint_path), 
            "validate", "--invalid-option"
        ], capture_output=True, text=True)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())
    
    def test_missing_file_argument(self):
        """Test handling of missing file argument"""
        result = subprocess.run([
            sys.executable, str(self.aiailint_path), 
            "validate", "--file"
        ], capture_output=True, text=True)
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("error", result.stderr.lower())
    
    def test_verbose_output(self):
        """Test verbose output mode"""
        test_file = self.test_data_dir / "valid_scripts" / "basic_validation.yaml"
        
        if test_file.exists():
            result = subprocess.run([
                sys.executable, str(self.aiailint_path), 
                "validate", "--file", str(test_file), "--verbose"
            ], capture_output=True, text=True)
            
            self.assertEqual(result.returncode, 0)
            self.assertIn("verbose", result.stdout.lower())
    
    def test_multiple_validation_issues(self):
        """Test validation of script with multiple issues"""
        test_file = self.test_data_dir / "invalid_scripts" / "false_destructive.yaml"
        
        if test_file.exists():
            result = subprocess.run([
                sys.executable, str(self.aiailint_path), 
                "validate", "--file", str(test_file)
            ], capture_output=True, text=True)
            
            # Should have warnings but not necessarily errors
            self.assertIn("warning", result.stderr.lower())
    
    def test_circular_reference_detection(self):
        """Test detection of circular references"""
        test_file = self.test_data_dir / "invalid_scripts" / "circular_reference.yaml"
        
        if test_file.exists():
            result = subprocess.run([
                sys.executable, str(self.aiailint_path), 
                "validate", "--file", str(test_file)
            ], capture_output=True, text=True)
            
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("circular", result.stderr.lower())
    
    def test_logic_check_promotion_suggestions(self):
        """Test suggestions for logic check promotion"""
        test_file = self.test_data_dir / "valid_scripts" / "logic_checks.yaml"
        
        if test_file.exists():
            result = subprocess.run([
                sys.executable, str(self.aiailint_path), 
                "validate", "--file", str(test_file)
            ], capture_output=True, text=True)
            
            # Should have warnings about logic checks
            self.assertIn("logic", result.stderr.lower())
    
    def test_readonly_commands_not_destructive(self):
        """Test that read-only commands are not flagged as destructive"""
        test_file = self.test_data_dir / "valid_scripts" / "readonly_commands.yaml"
        
        if test_file.exists():
            result = subprocess.run([
                sys.executable, str(self.aiailint_path), 
                "validate", "--file", str(test_file)
            ], capture_output=True, text=True)
            
            # Should pass validation without destructive warnings
            self.assertEqual(result.returncode, 0)
            self.assertNotIn("destructive", result.stderr.lower())


if __name__ == '__main__':
    unittest.main() 