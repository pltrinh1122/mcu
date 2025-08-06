#!/usr/bin/env python3
"""
Unit tests for PackageLoader

Tests AIAI package loading and validation functionality.
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

from utils.package_loader import PackageLoader, load_aiai_package
from utils.validation_result import ValidationResult


class TestPackageLoader(unittest.TestCase):
    """Test cases for PackageLoader"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.loader = PackageLoader()
    
    def test_valid_package_structure(self):
        """Test loading of valid AIAI package structure"""
        with tempfile.TemporaryDirectory() as temp_dir:
            package_path = Path(temp_dir)
            
            # Create MANIFEST
            manifest_path = package_path / "MANIFEST"
            with open(manifest_path, 'w') as f:
                f.write("README.md\n")
                f.write("aiai_spec.md\n")
                f.write("aiai_schema.json\n")
                f.write("src/aiaiScript/test_script_aiaiScript.yaml\n")
                f.write("docs/OPERATOR_GUIDE.md\n")
            
            # Create required files
            (package_path / "README.md").write_text("# Test Package")
            (package_path / "aiai_spec.md").write_text("# AIAI Specification")
            (package_path / "aiai_schema.json").write_text('{"type": "object"}')
            
            # Create directories and files
            (package_path / "docs").mkdir()
            (package_path / "docs" / "OPERATOR_GUIDE.md").write_text("# Operator Guide")
            
            (package_path / "src").mkdir()
            (package_path / "src" / "aiaiScript").mkdir()
            (package_path / "src" / "aiaiScript" / "test_script_aiaiScript.yaml").write_text(
                yaml.dump({
                    'metadata': {'name': 'test', 'version': '1.0.0'},
                    'body': {'scripts': {'main': {'commands': []}}}
                })
            )
            
            results = self.loader.load_package(package_path)
            self.assertTrue(results.success, f"Valid package should pass: {results.errors}")
    
    def test_missing_required_files(self):
        """Test package with missing required files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            package_path = Path(temp_dir)
            
            # Create MANIFEST but no actual files
            manifest_path = package_path / "MANIFEST"
            with open(manifest_path, 'w') as f:
                f.write("README.md\n")
                f.write("missing_file.md\n")
            
            results = self.loader.load_package(package_path)
            self.assertFalse(results.success, "Missing files should fail")
            self.assertTrue(any("not found" in error for error in results.errors), 
                          "Should have file not found errors")
    
    def test_invalid_manifest_format(self):
        """Test package with invalid MANIFEST format"""
        with tempfile.TemporaryDirectory() as temp_dir:
            package_path = Path(temp_dir)
            
            # Create invalid MANIFEST
            manifest_path = package_path / "MANIFEST"
            with open(manifest_path, 'w') as f:
                f.write("README.md\n")
                f.write("  invalid_indentation\n")  # Invalid indentation
                f.write("file_with_spaces .md\n")   # Invalid filename
            
            results = self.loader.load_package(package_path)
            # Should still pass since we're lenient with MANIFEST parsing
            self.assertTrue(results.success, "Should handle invalid MANIFEST gracefully")
    
    def test_missing_aiai_scripts(self):
        """Test package with missing AIAI Script files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            package_path = Path(temp_dir)
            
            # Create MANIFEST with AIAI Script but no actual file
            manifest_path = package_path / "MANIFEST"
            with open(manifest_path, 'w') as f:
                f.write("README.md\n")
                f.write("src/aiaiScript/missing_script_aiaiScript.yaml\n")
            
            (package_path / "README.md").write_text("# Test Package")
            
            results = self.loader.load_package(package_path)
            self.assertFalse(results.success, "Missing AIAI Script should fail")
            self.assertTrue(any("not found" in error for error in results.errors), 
                          "Should have missing script error")
    
    def test_empty_aiai_scripts_directory(self):
        """Test package with empty AIAI Scripts directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            package_path = Path(temp_dir)
            
            # Create MANIFEST without AIAI Scripts
            manifest_path = package_path / "MANIFEST"
            with open(manifest_path, 'w') as f:
                f.write("README.md\n")
                f.write("docs/OPERATOR_GUIDE.md\n")
            
            (package_path / "README.md").write_text("# Test Package")
            (package_path / "docs").mkdir()
            (package_path / "docs" / "OPERATOR_GUIDE.md").write_text("# Guide")
            
            # Create empty aiaiScript directory
            (package_path / "src").mkdir()
            (package_path / "src" / "aiaiScript").mkdir()
            
            results = self.loader.load_package(package_path)
            self.assertTrue(results.success, "Empty scripts directory should pass")
    
    def test_invalid_aiai_script_files(self):
        """Test package with invalid AIAI Script files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            package_path = Path(temp_dir)
            
            # Create MANIFEST
            manifest_path = package_path / "MANIFEST"
            with open(manifest_path, 'w') as f:
                f.write("README.md\n")
                f.write("src/aiaiScript/invalid_script_aiaiScript.yaml\n")
            
            (package_path / "README.md").write_text("# Test Package")
            
            # Create invalid AIAI Script
            (package_path / "src").mkdir()
            (package_path / "src" / "aiaiScript").mkdir()
            (package_path / "src" / "aiaiScript" / "invalid_script_aiaiScript.yaml").write_text(
                "invalid: yaml: content"
            )
            
            results = self.loader.load_package(package_path)
            # Should pass since we only check file existence, not content
            self.assertTrue(results.success, "Should pass even with invalid script content")
    
    def test_package_validation(self):
        """Test complete package validation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            package_path = Path(temp_dir)
            
            # Create complete package structure
            manifest_path = package_path / "MANIFEST"
            with open(manifest_path, 'w') as f:
                f.write("README.md\n")
                f.write("aiai_spec.md\n")
                f.write("aiai_schema.json\n")
                f.write("src/aiaiScript/test_script_aiaiScript.yaml\n")
                f.write("docs/OPERATOR_GUIDE.md\n")
            
            # Create all required files
            (package_path / "README.md").write_text("# Test Package")
            (package_path / "aiai_spec.md").write_text("# AIAI Specification")
            (package_path / "aiai_schema.json").write_text('{"type": "object"}')
            
            (package_path / "docs").mkdir()
            (package_path / "docs" / "OPERATOR_GUIDE.md").write_text("# Operator Guide")
            
            (package_path / "src").mkdir()
            (package_path / "src" / "aiaiScript").mkdir()
            (package_path / "src" / "aiaiScript" / "test_script_aiaiScript.yaml").write_text(
                yaml.dump({
                    'metadata': {'name': 'test', 'version': '1.0.0'},
                    'body': {'scripts': {'main': {'commands': []}}}
                })
            )
            
            results = self.loader.load_package(package_path)
            self.assertTrue(results.success, f"Complete package should pass: {results.errors}")
    
    def test_package_scripts_validation(self):
        """Test validation of package scripts"""
        with tempfile.TemporaryDirectory() as temp_dir:
            package_path = Path(temp_dir)
            
            # Create package with scripts
            manifest_path = package_path / "MANIFEST"
            with open(manifest_path, 'w') as f:
                f.write("src/aiaiScript/test_script_aiaiScript.yaml\n")
            
            (package_path / "src").mkdir()
            (package_path / "src" / "aiaiScript").mkdir()
            (package_path / "src" / "aiaiScript" / "test_script_aiaiScript.yaml").write_text(
                yaml.dump({
                    'metadata': {'name': 'test', 'version': '1.0.0'},
                    'body': {'scripts': {'main': {'commands': []}}}
                })
            )
            
            results = self.loader.load_package(package_path)
            self.assertTrue(results.success, "Package with scripts should pass")
            
            script_files = self.loader.get_script_files()
            self.assertEqual(len(script_files), 1, "Should find one script file")
    
    def test_package_metadata_extraction(self):
        """Test extraction of package metadata"""
        with tempfile.TemporaryDirectory() as temp_dir:
            package_path = Path(temp_dir)
            
            # Create package with README
            manifest_path = package_path / "MANIFEST"
            with open(manifest_path, 'w') as f:
                f.write("README.md\n")
            
            (package_path / "README.md").write_text("# Test Package Title\n\nDescription")
            
            results = self.loader.load_package(package_path)
            self.assertTrue(results.success, "Package should load successfully")
            
            package_info = self.loader.get_package_info(package_path)
            self.assertEqual(package_info['title'], "Test Package Title", "Should extract title from README")
    
    def test_package_file_discovery(self):
        """Test discovery of package files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            package_path = Path(temp_dir)
            
            # Create package with various files
            manifest_path = package_path / "MANIFEST"
            with open(manifest_path, 'w') as f:
                f.write("README.md\n")
                f.write("src/aiaiScript/test1_aiaiScript.yaml\n")
                f.write("src/aiaiScript/test2_aiaiScript.yaml\n")
                f.write("docs/guide.md\n")
            
            (package_path / "README.md").write_text("# Test")
            (package_path / "src").mkdir()
            (package_path / "src" / "aiaiScript").mkdir()
            (package_path / "src" / "aiaiScript" / "test1_aiaiScript.yaml").write_text("test")
            (package_path / "src" / "aiaiScript" / "test2_aiaiScript.yaml").write_text("test")
            (package_path / "docs").mkdir()
            (package_path / "docs" / "guide.md").write_text("# Guide")
            
            results = self.loader.load_package(package_path)
            self.assertTrue(results.success, "Package should load successfully")
            
            required_files = self.loader.get_required_files()
            self.assertEqual(len(required_files), 4, "Should find 4 required files")
            
            script_files = self.loader.get_script_files()
            self.assertEqual(len(script_files), 2, "Should find 2 script files")
    
    def test_nonexistent_package(self):
        """Test loading of nonexistent package"""
        nonexistent_path = Path("/nonexistent/package")
        results = self.loader.load_package(nonexistent_path)
        self.assertFalse(results.success, "Nonexistent package should fail")
        self.assertTrue(any("not found" in error for error in results.errors), 
                       "Should have package not found error")


if __name__ == '__main__':
    unittest.main() 