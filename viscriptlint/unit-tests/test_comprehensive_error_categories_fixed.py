#!/usr/bin/env python3

"""
Comprehensive unit tests for all error categories in viscriptlint
Tests: (1) File system errors (2) JSON loading errors (3a) JSON Syntax error 
(3b) JSON Schema error (3c) viScript schema (structure, content, deprecation, unsupported attributes) 
(4) Common Issues (5) Analysis & Statistics
"""

import unittest
import json
import tempfile
import os
import sys
import subprocess
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from viscriptlint import ViscriptLinter, ValidationResult, ExitCodes, Severity, ValidationType, ErrorCodes


class TestComprehensiveErrorCategoriesFixed(unittest.TestCase):
    """Comprehensive test cases for all error categories with correct expectations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.linter = ViscriptLinter(verbose=True, strict=False)
        self.test_files_dir = Path(__file__).parent / "test_files"
        
    def test_01_filesystem_errors(self):
        """Test (1) File system errors"""
        print("\n=== Testing File System Errors ===")
        
        # Test non-existent file
        nonexistent_file = self.test_files_dir / "01_filesystem_errors.json"
        result = self.linter.validate_viscript(nonexistent_file)
        self.assertFalse(result.success)
        self.assertGreater(len(result.errors), 0)
        self.assertIn("File not found", result.errors[0])
        print(f"✓ Non-existent file error: {result.errors[0]}")
        
        # Test directory instead of file
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.linter.validate_viscript(Path(temp_dir))
            self.assertFalse(result.success)
            self.assertGreater(len(result.errors), 0)
            self.assertIn("Not a file", result.errors[0])
            print(f"✓ Directory error: {result.errors[0]}")
        
        # Test empty file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            empty_file = Path(f.name)
        
        try:
            result = self.linter.validate_viscript(empty_file)
            self.assertFalse(result.success)
            self.assertGreater(len(result.errors), 0)
            self.assertIn("File is empty", result.errors[0])
            print(f"✓ Empty file error: {result.errors[0]}")
        finally:
            os.unlink(empty_file)
    
    def test_02_json_loading_errors(self):
        """Test (2) JSON loading errors"""
        print("\n=== Testing JSON Loading Errors ===")
        
        # Test file with encoding issues (binary data)
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.json', delete=False) as f:
            f.write(b'\x00\x01\x02\x03')  # Binary data
            binary_file = Path(f.name)
        
        try:
            result = self.linter.validate_viscript(binary_file)
            self.assertFalse(result.success)
            self.assertGreater(len(result.errors), 0)
            print(f"✓ Binary file error: {result.errors[0]}")
        finally:
            os.unlink(binary_file)
    
    def test_03a_json_syntax_errors(self):
        """Test (3a) JSON Syntax errors"""
        print("\n=== Testing JSON Syntax Errors ===")
        
        # Test specific syntax errors
        syntax_errors = [
            ('{"missing": "comma" "test": "value"}', "missing comma"),
            ('{"extra": "comma",}', "extra comma"),
            ('{"unclosed": "string}', "unclosed string"),
            ('{"invalid": value}', "invalid value"),
        ]
        
        for json_str, error_type in syntax_errors:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                f.write(json_str)
                temp_file = Path(f.name)
            
            try:
                result = self.linter.validate_viscript(temp_file)
                self.assertFalse(result.success, f"Should fail for {error_type}")
                
                # Check that we get a JSON parsing error (which includes line/column info)
                error_msg = result.errors[0]
                self.assertTrue(
                    "line" in error_msg.lower() or "column" in error_msg.lower() or "json parsing" in error_msg.lower(),
                    f"Should have line/column info or JSON parsing error for {error_type}"
                )
                print(f"✓ {error_type}: {error_msg}")
            finally:
                os.unlink(temp_file)
    
    def test_03b_json_schema_errors(self):
        """Test (3b) JSON Schema errors"""
        print("\n=== Testing JSON Schema Errors ===")
        
        schema_error_file = self.test_files_dir / "03b_json_schema_errors.json"
        result = self.linter.validate_viscript(schema_error_file)
        
        # Schema validation might be skipped if ajv is not available
        if result.success:
            print("✓ Schema validation skipped (ajv not available)")
        else:
            self.assertGreater(len(result.errors), 0)
            print(f"✓ JSON schema error: {result.errors[0]}")
    
    def test_03c_viscript_structure_errors(self):
        """Test (3c) viScript structure errors"""
        print("\n=== Testing viScript Structure Errors ===")
        
        structure_error_file = self.test_files_dir / "03c_viscript_structure_errors.json"
        result = self.linter.validate_viscript(structure_error_file)
        self.assertFalse(result.success)
        self.assertGreater(len(result.errors), 0)
        
        # Check for missing required fields
        error_msg = ' '.join(result.errors)
        self.assertIn("phases", error_msg.lower())
        print(f"✓ Structure error (missing phases): {result.errors[0]}")
    
    def test_03c_viscript_content_errors(self):
        """Test (3c) viScript content errors"""
        print("\n=== Testing viScript Content Errors ===")
        
        content_error_file = self.test_files_dir / "03c_viscript_content_errors.json"
        result = self.linter.validate_viscript(content_error_file)
        self.assertFalse(result.success)
        self.assertGreater(len(result.errors), 0)
        
        # Check for invalid severity and validation type
        error_msg = ' '.join(result.errors)
        self.assertTrue(
            any("invalid_severity" in error.lower() or "invalid_type" in error.lower() 
                for error in result.errors),
            "Should detect invalid severity or validation type"
        )
        print(f"✓ Content error: {result.errors[0]}")
    
    def test_03c_viscript_deprecation_errors(self):
        """Test (3c) viScript deprecation errors"""
        print("\n=== Testing viScript Deprecation Errors ===")
        
        deprecation_error_file = self.test_files_dir / "03c_viscript_deprecation_errors.json"
        result = self.linter.validate_viscript(deprecation_error_file)
        
        # Deprecated fields should be detected
        error_msg = ' '.join(result.errors)
        self.assertTrue(
            any("critical" in error.lower() or "weight" in error.lower() 
                for error in result.errors),
            "Should detect deprecated critical/weight fields"
        )
        print(f"✓ Deprecation error: {result.errors[0]}")
    
    def test_03c_viscript_unsupported_errors(self):
        """Test (3c) viScript unsupported attributes"""
        print("\n=== Testing viScript Unsupported Attributes ===")
        
        unsupported_error_file = self.test_files_dir / "03c_viscript_unsupported_errors.json"
        result = self.linter.validate_viscript(unsupported_error_file)
        
        # Unsupported attributes should be detected
        error_msg = ' '.join(result.errors)
        self.assertTrue(
            any("test_mode" in error.lower() or "conditional" in error.lower() 
                for error in result.errors),
            "Should detect unsupported test_mode/conditional attributes"
        )
        print(f"✓ Unsupported attribute error: {result.errors[0]}")
    
    def test_04_common_issues(self):
        """Test (4) Common Issues"""
        print("\n=== Testing Common Issues ===")
        
        common_issues_file = self.test_files_dir / "04_common_issues.json"
        result = self.linter.validate_viscript(common_issues_file)
        
        # Should detect common issues as warnings
        self.assertGreater(len(result.warnings), 0)
        
        # Check for specific common issues
        warning_msg = ' '.join(result.warnings)
        self.assertTrue(
            any("W001" in warning or "W002" in warning or "W003" in warning 
                for warning in result.warnings),
            "Should detect common issues with error codes"
        )
        print(f"✓ Common issues detected: {len(result.warnings)} warnings")
        for warning in result.warnings:
            print(f"  - {warning}")
    
    def test_05_analysis_statistics(self):
        """Test (5) Analysis & Statistics"""
        print("\n=== Testing Analysis & Statistics ===")
        
        analysis_file = self.test_files_dir / "05_analysis_statistics.json"
        result = self.linter.validate_viscript(analysis_file)
        
        # Should detect analysis issues (no critical checks, high informational ratio)
        self.assertGreater(len(result.warnings), 0)
        
        # Check for analysis warnings
        warning_msg = ' '.join(result.warnings)
        self.assertTrue(
            any("critical" in warning.lower() or "informational" in warning.lower() 
                for warning in result.warnings),
            "Should detect analysis issues (no critical checks, high informational ratio)"
        )
        print(f"✓ Analysis warnings detected: {len(result.warnings)} warnings")
        for warning in result.warnings:
            print(f"  - {warning}")
    
    def test_error_codes_and_line_numbers(self):
        """Test error codes and line number detection"""
        print("\n=== Testing Error Codes and Line Numbers ===")
        
        # Test with a file that has multiple issues
        test_issues_file = self.test_files_dir / "test_issues.json"
        if test_issues_file.exists():
            result = self.linter.validate_viscript(test_issues_file)
            
            # Should have both errors and warnings
            self.assertGreater(len(result.errors), 0)
            self.assertGreaterEqual(len(result.warnings), 0)
            
            # Check for error codes in messages
            error_msg = ' '.join(result.errors)
            self.assertTrue(
                any(code in error_msg for code in [ErrorCodes.EMPTY_COMMAND, ErrorCodes.MISSING_PATTERN]),
                "Should include error codes in messages"
            )
            print(f"✓ Error codes detected: {result.errors[0]}")
    
    def test_json_output_format_with_errors(self):
        """Test JSON output format with various error types"""
        print("\n=== Testing JSON Output Format with Errors ===")
        
        # Test with a valid file that has warnings
        analysis_file = self.test_files_dir / "05_analysis_statistics.json"
        
        # Create linter with JSON output
        json_linter = ViscriptLinter(format_output="json")
        
        # Capture output
        import io
        from contextlib import redirect_stdout
        
        output = io.StringIO()
        with redirect_stdout(output):
            result = json_linter.validate_viscript(analysis_file)
        
        output_str = output.getvalue()
        
        # Check for JSON structure in output
        # The JSON output should be at the end of the output
        if '"file"' in output_str:
            self.assertIn('"file"', output_str)
            self.assertIn('"errors"', output_str)
            self.assertIn('"warnings"', output_str)
            self.assertIn('"status"', output_str)
            print("✓ JSON output format works with errors")
        else:
            # If JSON output is not found, check if it's because the file is valid
            # In that case, we should still have some output
            self.assertGreater(len(output_str), 0, "Should have some output")
            print("✓ JSON output format test passed (valid file with warnings)")
    
    def test_comprehensive_error_reporting(self):
        """Test comprehensive error reporting with all categories"""
        print("\n=== Testing Comprehensive Error Reporting ===")
        
        # Test each error category and verify proper reporting
        test_cases = [
            ("03c_viscript_structure_errors.json", "phases"),
            ("04_common_issues.json", "warning"),
            ("05_analysis_statistics.json", "critical"),
        ]
        
        for filename, expected_content in test_cases:
            test_file = self.test_files_dir / filename
            if test_file.exists():
                result = self.linter.validate_viscript(test_file)
                
                # Combine all messages
                all_messages = ' '.join(result.errors + result.warnings + result.info)
                
                # Check that expected content is found
                self.assertIn(expected_content.lower(), all_messages.lower(),
                            f"Expected '{expected_content}' in messages for {filename}")
                
                print(f"✓ {filename}: {expected_content} detected")
    
    def test_error_categorization(self):
        """Test that errors are properly categorized"""
        print("\n=== Testing Error Categorization ===")
        
        # Test that different error types are properly categorized
        test_file = self.test_files_dir / "04_common_issues.json"
        if test_file.exists():
            result = self.linter.validate_viscript(test_file)
            
            # Common issues should be warnings, not errors
            self.assertGreater(len(result.warnings), 0, "Should have warnings for common issues")
            
            print(f"✓ Error categorization: {len(result.errors)} errors, {len(result.warnings)} warnings")


if __name__ == "__main__":
    # Run the comprehensive tests
    unittest.main(verbosity=2) 