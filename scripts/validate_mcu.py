#!/usr/bin/env python3
"""
MCU Validation Script

This script validates MCU files for compliance with the MCU specification.
It checks metadata completeness, content structure, and quality standards.
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class MCUValidator:
    """Validates MCU files against the specification."""
    
    def __init__(self):
        self.required_metadata = [
            'context_unit_id',
            'Created',
            'Updated',
            'Type',
            'Version',
            'Project',
            'Tool',
            'Category',
            'Tags'
        ]
        
        self.valid_types = ['reference', 'instruction', 'instruction-agent', 'specification']
        self.valid_categories = ['framework', 'specification', 'template', 'example']
        
    def validate_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """Validate a single MCU file."""
        errors = []
        warnings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check if file is markdown
            if not file_path.endswith('.md'):
                errors.append(f"File must be markdown format: {file_path}")
                return False, errors
                
            # Extract metadata section
            metadata = self._extract_metadata(content)
            if not metadata:
                errors.append("No metadata section found")
                return False, errors
                
            # Validate metadata fields
            metadata_errors = self._validate_metadata(metadata)
            errors.extend(metadata_errors)
            
            # Validate content structure
            structure_errors = self._validate_structure(content)
            errors.extend(structure_errors)
            
            # Check for required sections
            section_errors = self._validate_sections(content)
            errors.extend(section_errors)
            
            return len(errors) == 0, errors
            
        except Exception as e:
            errors.append(f"Error reading file {file_path}: {str(e)}")
            return False, errors
    
    def _extract_metadata(self, content: str) -> Optional[Dict]:
        """Extract metadata from MCU file."""
        # Look for metadata section
        metadata_match = re.search(r'## Context Memory Unit: ([^\n]+)', content)
        if not metadata_match:
            return None
            
        # Extract context_unit_id from the header
        context_unit_id = metadata_match.group(1)
        
        # Extract metadata lines
        lines = content.split('\n')
        metadata = {'context_unit_id': context_unit_id}
        
        for line in lines:
            if line.startswith('- **') and '**:' in line:
                key, value = line.split('**:', 1)
                key = key.replace('- **', '').strip()
                value = value.strip()
                metadata[key] = value
                
        return metadata
    
    def _validate_metadata(self, metadata: Dict) -> List[str]:
        """Validate metadata fields."""
        errors = []
        
        # Check required fields
        for field in self.required_metadata:
            if field not in metadata:
                errors.append(f"Missing required metadata field: {field}")
                
        # Validate type field
        if 'type' in metadata:
            if metadata['type'] not in self.valid_types:
                errors.append(f"Invalid type: {metadata['type']}. Must be one of {self.valid_types}")
                
        # Validate category field
        if 'category' in metadata:
            if metadata['category'] not in self.valid_categories:
                errors.append(f"Invalid category: {metadata['category']}. Must be one of {self.valid_categories}")
                
        # Validate context_unit_id format
        if 'context_unit_id' in metadata:
            if not re.match(r'^[a-z-]+-\d{4}-\d{2}-\d{2}-\d{3}$', metadata['context_unit_id']):
                errors.append("Invalid context_unit_id format. Expected: type-YYYY-MM-DD-XXX")
                
        return errors
    
    def _validate_structure(self, content: str) -> List[str]:
        """Validate content structure."""
        errors = []
        
        # Check for required sections
        required_sections = [
            '## Executive Summary',
            '## Quick Reference',
            '## Detailed Reference'
        ]
        
        for section in required_sections:
            if section not in content:
                errors.append(f"Missing required section: {section}")
                
        return errors
    
    def _validate_sections(self, content: str) -> List[str]:
        """Validate section content."""
        errors = []
        
        # Check for TL;DR in Executive Summary
        if '## Executive Summary' in content:
            if '**TL;DR**:' not in content:
                errors.append("Missing TL;DR in Executive Summary")
                
        # Check for Quick Reference content
        if '## Quick Reference' in content:
            if '### **Essential' not in content:
                errors.append("Missing Essential Requirements in Quick Reference")
                
        return errors
    
    def validate_directory(self, directory: str) -> Dict[str, Tuple[bool, List[str]]]:
        """Validate all MCU files in a directory."""
        results = {}
        
        # If directory is a file, validate just that file
        if os.path.isfile(directory):
            is_valid, errors = self.validate_file(directory)
            results[directory] = (is_valid, errors)
            return results
            
        # Walk directory for markdown files
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    is_valid, errors = self.validate_file(file_path)
                    results[file_path] = (is_valid, errors)
                    
        return results

def main():
    """Main validation function."""
    validator = MCUValidator()
    
    if len(sys.argv) < 2:
        print("Usage: python validate_mcu.py <directory>")
        sys.exit(1)
        
    directory = sys.argv[1]
    
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        sys.exit(1)
        
    print(f"Validating MCU files in: {directory}")
    print("=" * 50)
    
    results = validator.validate_directory(directory)
    
    valid_count = 0
    total_count = len(results)
    
    for file_path, (is_valid, errors) in results.items():
        if is_valid:
            print(f"✅ {file_path}")
            valid_count += 1
        else:
            print(f"❌ {file_path}")
            for error in errors:
                print(f"   - {error}")
                
    print("=" * 50)
    print(f"Validation complete: {valid_count}/{total_count} files valid")
    
    if valid_count < total_count:
        sys.exit(1)
    else:
        print("🎉 All MCU files are valid!")

if __name__ == "__main__":
    main()
