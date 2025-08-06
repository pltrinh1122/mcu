"""
AIAI Package Loader

Loads and validates AIAI packages with MANIFEST files.
Supports the complete package structure validation.
"""

import os
from pathlib import Path
from typing import List, Set, Dict, Any
from utils.validation_result import ValidationResult


class PackageLoader:
    """Loads and validates AIAI package structure"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.manifest_files = []
        self.script_files = []
        self.required_files = []
    
    def load_package(self, package_path: Path) -> ValidationResult:
        """
        Load and validate AIAI package structure
        
        Args:
            package_path: Path to AIAI package directory
            
        Returns:
            ValidationResult with package validation results
        """
        errors = []
        warnings = []
        info = []
        
        if self.verbose:
            print(f"→ Loading AIAI package from {package_path}")
        
        # Check if package directory exists
        if not package_path.exists():
            errors.append(f"Package directory not found: {package_path}")
            return ValidationResult(False, errors, warnings, info, str(package_path))
        
        if not package_path.is_dir():
            errors.append(f"Package path is not a directory: {package_path}")
            return ValidationResult(False, errors, warnings, info, str(package_path))
        
        # Load MANIFEST file
        manifest_result = self._load_manifest(package_path)
        if not manifest_result.success:
            return manifest_result
        
        # Validate package structure
        structure_issues = self._validate_package_structure(package_path)
        errors.extend(structure_issues['errors'])
        warnings.extend(structure_issues['warnings'])
        
        # Validate file completeness
        completeness_issues = self._validate_file_completeness(package_path)
        errors.extend(completeness_issues['errors'])
        warnings.extend(completeness_issues['warnings'])
        
        if self.verbose:
            if errors:
                print(f"  ✗ Package validation failed with {len(errors)} errors")
            elif warnings:
                print(f"  ⚠ Package validation passed with {len(warnings)} warnings")
            else:
                print("  ✓ Package validation passed")
        
        success = len(errors) == 0
        return ValidationResult(success, errors, warnings, info, str(package_path))
    
    def get_script_files(self) -> List[str]:
        """Get list of AIAI Script files from loaded package"""
        return self.script_files.copy()
    
    def get_required_files(self) -> List[str]:
        """Get list of all required files from MANIFEST"""
        return self.required_files.copy()
    
    def _load_manifest(self, package_path: Path) -> ValidationResult:
        """Load and parse MANIFEST file"""
        manifest_path = package_path / "MANIFEST"
        
        if not manifest_path.exists():
            error = f"MANIFEST file not found in package: {package_path}"
            return ValidationResult(False, [error], [], [], str(package_path))
        
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Parse MANIFEST - simple text file with one file per line
            self.manifest_files = []
            self.script_files = []
            self.required_files = []
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Add to manifest files
                self.manifest_files.append(line)
                self.required_files.append(line)
                
                # Identify AIAI Script files
                if line.endswith('_aiaiScript.yaml') or line.endswith('_aiaiScript.yml'):
                    self.script_files.append(line)
            
            if self.verbose:
                print(f"  ✓ Loaded MANIFEST with {len(self.manifest_files)} files")
                print(f"  ✓ Found {len(self.script_files)} AIAI Script files")
            
            return ValidationResult(True, [], [], [], str(package_path))
            
        except Exception as e:
            error = f"Failed to read MANIFEST file: {e}"
            return ValidationResult(False, [error], [], [], str(package_path))
    
    def _validate_package_structure(self, package_path: Path) -> Dict[str, List[str]]:
        """Validate standard AIAI package directory structure"""
        errors = []
        warnings = []
        
        # Check for required directories
        required_dirs = ['docs', 'src/aiaiScript']
        
        for dir_path in required_dirs:
            full_path = package_path / dir_path
            if not full_path.exists():
                warnings.append(f"Recommended directory missing: {dir_path}")
            elif not full_path.is_dir():
                errors.append(f"Expected directory but found file: {dir_path}")
        
        # Check for required files
        required_files = ['README.md', 'aiai_spec.md', 'aiai_schema.json']
        
        for file_path in required_files:
            full_path = package_path / file_path
            if not full_path.exists():
                warnings.append(f"Recommended file missing: {file_path}")
            elif not full_path.is_file():
                errors.append(f"Expected file but found directory: {file_path}")
        
        # Check for operator guide
        docs_dir = package_path / 'docs'
        if docs_dir.exists():
            operator_guides = list(docs_dir.glob('*OPERATOR_GUIDE*.md'))
            if not operator_guides:
                warnings.append("No OPERATOR_GUIDE.md found in docs directory")
        
        return {'errors': errors, 'warnings': warnings}
    
    def _validate_file_completeness(self, package_path: Path) -> Dict[str, List[str]]:
        """Validate that all files listed in MANIFEST exist"""
        errors = []
        warnings = []
        
        # Check each file in MANIFEST
        for file_path in self.manifest_files:
            full_path = package_path / file_path
            
            if not full_path.exists():
                errors.append(f"File listed in MANIFEST but not found: {file_path}")
            elif full_path.is_dir():
                errors.append(f"MANIFEST lists directory as file: {file_path}")
        
        # Check for AIAI Scripts not in MANIFEST
        script_dirs = [package_path / 'src/aiaiScript']
        found_scripts = set()
        
        for script_dir in script_dirs:
            if script_dir.exists():
                for script_file in script_dir.glob('*_aiaiScript.yaml'):
                    rel_path = script_file.relative_to(package_path)
                    found_scripts.add(str(rel_path))
        
        manifest_scripts = set(self.script_files)
        
        # Scripts found but not in MANIFEST
        unlisted_scripts = found_scripts - manifest_scripts
        for script in unlisted_scripts:
            warnings.append(f"AIAI Script found but not listed in MANIFEST: {script}")
        
        # Scripts in MANIFEST but not found
        missing_scripts = manifest_scripts - found_scripts
        for script in missing_scripts:
            errors.append(f"AIAI Script listed in MANIFEST but not found: {script}")
        
        return {'errors': errors, 'warnings': warnings}
    
    def get_package_info(self, package_path: Path) -> Dict[str, Any]:
        """Get summary information about the package"""
        info = {
            'path': str(package_path),
            'manifest_files': len(self.manifest_files),
            'script_files': len(self.script_files),
            'required_files': len(self.required_files)
        }
        
        # Check for README
        readme_path = package_path / 'README.md'
        if readme_path.exists():
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('#'):
                        info['title'] = first_line.lstrip('#').strip()
            except:
                pass
        
        return info


def load_aiai_package(package_path: Path, verbose=False) -> ValidationResult:
    """
    Standalone function to load AIAI package
    
    Args:
        package_path: Path to AIAI package directory
        verbose: Enable verbose output
        
    Returns:
        ValidationResult with package loading results
    """
    loader = PackageLoader(verbose=verbose)
    return loader.load_package(package_path)