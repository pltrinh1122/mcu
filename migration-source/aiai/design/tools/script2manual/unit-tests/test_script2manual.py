#!/usr/bin/env python3
"""
Unit tests for script2manual.py

Tests the AIAI Script to Manual Instructions Generator
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path
import yaml

# Add the parent directory to the path so we can import script2manual
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from script2manual import Script2Manual


class TestScript2Manual(unittest.TestCase):
    """Test cases for Script2Manual class"""

    def setUp(self):
        """Set up test fixtures"""
        self.generator = Script2Manual()
        self.test_data_dir = Path(__file__).parent / "test_data"
        self.test_outputs_dir = Path(__file__).parent / "test_outputs"

    def test_load_scripts_valid_directory(self):
        """Test loading scripts from a valid directory"""
        self.generator.load_scripts(str(self.test_data_dir))
        self.assertIn("sample_aiaiScript", self.generator.scripts)
        self.assertIn("complex_aiaiScript", self.generator.scripts)

    def test_load_scripts_invalid_directory(self):
        """Test loading scripts from an invalid directory"""
        with self.assertRaises(FileNotFoundError):
            self.generator.load_scripts("/nonexistent/directory")

    def test_extract_phase_info_with_phase(self):
        """Test extracting phase information from script with phase metadata"""
        script_data = {
            "metadata": {
                "context": {
                    "phase": {
                        "name": "system-validation",
                        "number": 1,
                        "description": "Validate system prerequisites"
                    }
                }
            }
        }
        phase_info = self.generator.extract_phase_info(script_data)
        self.assertIsNotNone(phase_info)
        self.assertEqual(phase_info["name"], "system-validation")
        self.assertEqual(phase_info["number"], 1)

    def test_extract_phase_info_without_phase(self):
        """Test extracting phase information from script without phase metadata"""
        script_data = {
            "metadata": {
                "context": {
                    "dependencies": ["Ubuntu 24.04"]
                }
            }
        }
        phase_info = self.generator.extract_phase_info(script_data)
        self.assertIsNone(phase_info)

    def test_extract_commands_simple(self):
        """Test extracting commands from a simple script"""
        script_data = {
            "body": [
                {
                    "type": "command",
                    "id": "test-command",
                    "intent": "Test command",
                    "shellCommand": "echo 'test'",
                    "destructive": False,
                    "conditional": False
                },
                {
                    "type": "validation",
                    "id": "test-validation",
                    "intent": "Test validation",
                    "command": "echo 'validation'",
                    "expected_output": "validation",
                    "critical": True,
                    "on_fail": "abort"
                }
            ]
        }
        commands = self.generator.extract_commands(script_data)
        self.assertEqual(len(commands), 2)
        
        # Check command
        self.assertEqual(commands[0]["id"], "test-command")
        self.assertEqual(commands[0]["command"], "echo 'test'")
        self.assertFalse(commands[0]["destructive"])
        
        # Check validation
        self.assertEqual(commands[1]["id"], "test-validation")
        self.assertEqual(commands[1]["command"], "echo 'validation'")
        self.assertTrue(commands[1]["is_validation"])
        self.assertEqual(commands[1]["expected_output"], "validation")

    def test_extract_commands_nested_scripts(self):
        """Test extracting commands from nested script structure"""
        script_data = {
            "body": [
                {
                    "type": "script",
                    "scriptType": "procedure",
                    "id": "nested-script",
                    "body": [
                        {
                            "type": "command",
                            "id": "nested-command",
                            "intent": "Nested command",
                            "shellCommand": "echo 'nested'",
                            "destructive": False,
                            "conditional": False
                        }
                    ]
                }
            ]
        }
        commands = self.generator.extract_commands(script_data)
        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0]["id"], "nested-command")
        self.assertEqual(commands[0]["command"], "echo 'nested'")

    def test_generate_manual_content_basic(self):
        """Test generating manual content from basic script"""
        # Load a simple test script
        self.generator.load_scripts(str(self.test_data_dir))
        
        content = self.generator.generate_manual_content()
        
        # Check that content was generated
        self.assertIsInstance(content, str)
        self.assertIn("# Manual Installation Instructions", content)
        self.assertIn("## Source Scripts", content)
        self.assertIn("## Overview", content)
        self.assertIn("## Troubleshooting", content)
        
        # Check that source scripts are listed
        self.assertIn("btrfs_system_validation_aiaiscript.yaml", content)
        self.assertIn("sample_aiaiScript.yaml", content)

    def test_generate_manual_content_with_phases(self):
        """Test generating manual content with phase selection"""
        self.generator.load_scripts(str(self.test_data_dir))
        
        # Test with specific phase selection
        content = self.generator.generate_manual_content(["system-validation"])
        
        self.assertIn("Phase 1: System-Validation", content)
        self.assertIn("Validate system prerequisites", content)

    def test_generate_manual_content_no_scripts(self):
        """Test generating manual content with no scripts loaded"""
        content = self.generator.generate_manual_content()
        
        # Should still generate header and troubleshooting
        self.assertIn("# Manual Installation Instructions", content)
        self.assertIn("## Troubleshooting", content)

    def test_generate_manual_file_output(self):
        """Test generating manual to file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_file:
            output_file = tmp_file.name
        
        try:
            self.generator.load_scripts(str(self.test_data_dir))
            self.generator.generate_manual(str(self.test_data_dir), output_file)
            
            # Check that file was created and has content
            self.assertTrue(os.path.exists(output_file))
            with open(output_file, 'r') as f:
                content = f.read()
                self.assertIn("# Manual Installation Instructions", content)
        finally:
            # Clean up
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_generate_manual_with_phase_selection(self):
        """Test generating manual with specific phase selection"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp_file:
            output_file = tmp_file.name
        
        try:
            self.generator.load_scripts(str(self.test_data_dir))
            self.generator.generate_manual(
                str(self.test_data_dir), 
                output_file, 
                ["system-validation"]
            )
            
            # Check that file was created
            self.assertTrue(os.path.exists(output_file))
            with open(output_file, 'r') as f:
                content = f.read()
                self.assertIn("Phase 1: System-Validation", content)
        finally:
            # Clean up
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_handle_invalid_yaml(self):
        """Test handling of invalid YAML files"""
        # Create a temporary invalid YAML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp_file:
            tmp_file.write("invalid: yaml: content: [")
            tmp_file.flush()
            invalid_file = tmp_file.name
        
        try:
            # Create a temporary directory with the invalid file
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                invalid_path = temp_path / "invalid.yaml"
                os.rename(invalid_file, invalid_path)
                
                # Should not raise an exception, but should log a warning
                self.generator.load_scripts(str(temp_path))
                self.assertEqual(len(self.generator.scripts), 0)
        finally:
            # Clean up
            if os.path.exists(invalid_file):
                os.unlink(invalid_file)

    def test_handle_missing_required_fields(self):
        """Test handling of scripts with missing required fields"""
        script_data = {
            "body": [
                {
                    "type": "command",
                    "id": "missing-shellCommand",
                    "intent": "This command is missing shellCommand"
                },
                {
                    "type": "validation",
                    "id": "missing-command",
                    "intent": "This validation is missing command",
                    "expected_output": "test_output"
                }
            ]
        }
        
        commands = self.generator.extract_commands(script_data)
        
        # Should handle missing fields gracefully
        self.assertEqual(len(commands), 2)
        self.assertEqual(commands[0]["command"], "")  # Missing shellCommand
        self.assertEqual(commands[1]["command"], "")  # Missing command

    def test_handle_unknown_element_types(self):
        """Test handling of unknown element types"""
        script_data = {
            "body": [
                {
                    "type": "unknown_type",
                    "id": "unknown-element",
                    "intent": "This is an unknown element type"
                },
                {
                    "type": "command",
                    "id": "valid-command",
                    "intent": "This is a valid command",
                    "shellCommand": "echo 'valid command'"
                }
            ]
        }
        
        commands = self.generator.extract_commands(script_data)
        
        # Should only extract valid commands, skip unknown types
        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0]["id"], "valid-command")

    def test_validation_output_format(self):
        """Test that validation steps include proper verification format"""
        self.generator.load_scripts(str(self.test_data_dir))
        content = self.generator.generate_manual_content()
        
        # Check that validation steps include verification sections
        self.assertIn("**Verification**:", content)
        self.assertIn("# Run the command and check output", content)
        self.assertIn("# Expected:", content)

    def test_destructive_operation_warnings(self):
        """Test that destructive operations are properly marked"""
        script_data = {
            "body": [
                {
                    "type": "command",
                    "id": "destructive-command",
                    "intent": "Destructive operation",
                    "shellCommand": "sudo rm -rf /",
                    "destructive": True,
                    "conditional": False
                }
            ]
        }
        
        commands = self.generator.extract_commands(script_data)
        self.assertTrue(commands[0]["destructive"])
        
        content = self.generator.generate_manual_content()
        # The content should include warnings for destructive operations
        # (This would be tested in the actual generation, but we're testing the extraction here)

    def test_conditional_command_handling(self):
        """Test handling of conditional commands"""
        script_data = {
            "body": [
                {
                    "type": "command",
                    "id": "conditional-command",
                    "intent": "Conditional command",
                    "shellCommand": "echo 'conditional'",
                    "destructive": False,
                    "conditional": True
                }
            ]
        }
        
        commands = self.generator.extract_commands(script_data)
        self.assertTrue(commands[0]["conditional"])

    def test_btrfs_system_validation_user_data(self):
        """Test processing of real user data from btrfs_system_validation_aiaiscript.yaml"""
        # Load the specific user test data
        self.generator.load_scripts(str(self.test_data_dir))
        
        # Verify the btrfs script was loaded
        self.assertIn("btrfs_system_validation_aiaiscript", self.generator.scripts)
        
        # Get the script data
        btrfs_script = self.generator.scripts["btrfs_system_validation_aiaiscript"]
        
        # Test metadata extraction
        self.assertEqual(btrfs_script["metadata"]["id"], "btrfs-system-validation")
        self.assertEqual(btrfs_script["metadata"]["intent"], "Comprehensive System Validation for Ubuntu Installation Preparation (Generic + AI/ML)")
        self.assertEqual(btrfs_script["metadata"]["technicalProficiency"], "Expert")
        
        # Test context extraction
        context = btrfs_script["metadata"]["context"]
        self.assertIn("dependencies", context)
        self.assertIn("compatibility", context)
        self.assertIn("designPrinciples", context)
        
        # Test command extraction from complex nested structure
        commands = self.generator.extract_commands(btrfs_script)
        
        # Should extract commands from the nested script structure
        self.assertGreater(len(commands), 0, "Should extract at least some commands from the complex nested structure")
        
        # Test that we have validation commands
        validation_commands = [cmd for cmd in commands if cmd.get("is_validation")]
        self.assertGreater(len(validation_commands), 0, "Should have validation commands")
        
        # Test that we have regular commands
        regular_commands = [cmd for cmd in commands if not cmd.get("is_validation")]
        self.assertGreater(len(regular_commands), 0, "Should have regular commands")
        
        # Test specific command extraction
        command_ids = [cmd["id"] for cmd in commands]
        expected_ids = ["live-boot-detection", "ubuntu-version-check", "target-disk-detection", "disk-capacity-check"]
        
        # Check that at least some expected commands are present
        found_expected = any(expected_id in command_ids for expected_id in expected_ids)
        self.assertTrue(found_expected, "Should find some of the expected command IDs")
        
        # Test manual generation with user data
        content = self.generator.generate_manual_content()
        
        # Should include content from the btrfs script
        self.assertIn("Btrfs System Validation Aiaiscript", content)
        self.assertIn("Verify running from live boot environment", content)
        
        # Test that critical validations are properly marked
        critical_validations = [cmd for cmd in commands if cmd.get("is_validation") and cmd.get("critical")]
        self.assertGreater(len(critical_validations), 0, "Should have critical validation steps")

    def test_script_source_references(self):
        """Test that the manual includes references to original script names"""
        self.generator.load_scripts(str(self.test_data_dir))
        content = self.generator.generate_manual_content()
        
        # Should include source scripts section
        self.assertIn("## Source Scripts", content)
        self.assertIn("This manual was generated from the following aiaiScript files:", content)
        
        # Should list all loaded scripts
        self.assertIn("`btrfs_system_validation_aiaiscript.yaml`", content)
        self.assertIn("`sample_aiaiScript.yaml`", content)
        self.assertIn("`complex_aiaiScript.yaml`", content)
        
        # Should include source references in each phase/section
        self.assertIn("**Source**: `sample_aiaiScript.yaml`", content)
        self.assertIn("**Source**: `btrfs_system_validation_aiaiscript.yaml`", content)

    def test_load_scripts_single_file(self):
        """Test loading a single YAML file"""
        # Test with a specific file
        single_file = self.test_data_dir / "sample_aiaiScript.yaml"
        self.generator.load_scripts(str(single_file))
        
        # Should load only that one script
        self.assertEqual(len(self.generator.scripts), 1)
        self.assertIn("sample_aiaiScript", self.generator.scripts)
        
        # Should not load other scripts from the directory
        self.assertNotIn("complex_aiaiScript", self.generator.scripts)
        self.assertNotIn("btrfs_system_validation_aiaiscript", self.generator.scripts)

    def test_load_scripts_directory(self):
        """Test loading scripts from a directory"""
        self.generator.load_scripts(str(self.test_data_dir))
        
        # Should load all valid YAML files from directory
        self.assertGreaterEqual(len(self.generator.scripts), 3)  # At least sample, complex, and btrfs
        self.assertIn("sample_aiaiScript", self.generator.scripts)
        self.assertIn("complex_aiaiScript", self.generator.scripts)
        self.assertIn("btrfs_system_validation_aiaiscript", self.generator.scripts)

    def test_load_scripts_invalid_file_extension(self):
        """Test loading a file with invalid extension"""
        # Create a temporary file with wrong extension
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
            tmp_file.write("test: content")
            tmp_file.flush()
            invalid_file = tmp_file.name
        
        try:
            # Should raise ValueError for invalid extension
            with self.assertRaises(ValueError) as context:
                self.generator.load_scripts(invalid_file)
            self.assertIn("must have .yaml or .yml extension", str(context.exception))
        finally:
            # Clean up
            if os.path.exists(invalid_file):
                os.unlink(invalid_file)

    def test_load_scripts_nonexistent_path(self):
        """Test loading from a nonexistent path"""
        with self.assertRaises(FileNotFoundError):
            self.generator.load_scripts("/nonexistent/path")

    def test_generate_manual_single_file_vs_directory(self):
        """Test that manual generation works for both single files and directories"""
        # Test single file
        single_file = self.test_data_dir / "sample_aiaiScript.yaml"
        self.generator.load_scripts(str(single_file))
        single_file_content = self.generator.generate_manual_content()
        
        # Reset generator and test directory
        self.generator = Script2Manual()
        self.generator.load_scripts(str(self.test_data_dir))
        directory_content = self.generator.generate_manual_content()
        
        # Single file content should be a subset of directory content
        self.assertIn("sample_aiaiScript.yaml", single_file_content)
        self.assertIn("sample_aiaiScript.yaml", directory_content)
        
        # Directory content should have more scripts
        self.assertIn("btrfs_system_validation_aiaiscript.yaml", directory_content)
        # Single file content should not have other scripts
        self.assertNotIn("btrfs_system_validation_aiaiscript.yaml", single_file_content)


if __name__ == "__main__":
    unittest.main() 