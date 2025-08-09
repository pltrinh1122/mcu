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

NON_MCU_PREFIXES = (
    "__vibew-",
)

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
        
        self.valid_types = ['reference', 'instruction', 'instruction-agent', 'specification', 'note', 'backlog', 'backlog-item']
        self.valid_categories = ['framework', 'specification', 'template', 'example', 'governance']
        
    def validate_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """Validate a single MCU file."""
        errors: List[str] = []
        
        try:
            # Skip known non-MCU families by filename prefix
            base = os.path.basename(file_path)
            for prefix in NON_MCU_PREFIXES:
                if base.startswith(prefix):
                    return True, []
            
            # Skip templates from strict validation
            if os.path.abspath(file_path).replace('\\', '/').find('/templates/') != -1:
                return True, []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if not file_path.endswith('.md'):
                return True, []  # ignore non-markdown files
                
            # Only validate files that declare themselves as MCUs
            if '## Context Memory Unit:' not in content:
                return True, []
                
            metadata = self._extract_metadata(content)
            if not metadata:
                errors.append("No metadata section found")
                return False, errors
                
            errors.extend(self._validate_metadata(metadata))
            
            mcu_type = (metadata.get('type') or metadata.get('Type') or '').strip().lower()
            
            # Structure rules vary by type
            if mcu_type == 'note':
                errors.extend(self._validate_note_structure(content))
            elif mcu_type == 'backlog':
                errors.extend(self._validate_backlog_structure(content))
            elif mcu_type == 'backlog-item':
                errors.extend(self._validate_backlog_item_structure(content))
            else:
                errors.extend(self._validate_structure(content))
                errors.extend(self._validate_sections(content))
            
            return len(errors) == 0, errors
            
        except Exception as e:
            errors.append(f"Error reading file {file_path}: {str(e)}")
            return False, errors
    
    def _extract_metadata(self, content: str) -> Optional[Dict]:
        """Extract metadata from MCU file."""
        header_match = re.search(r'^## Context Memory Unit: (.+)$', content, re.MULTILINE)
        if not header_match:
            return None
        context_unit_id = header_match.group(1).strip()
        lines = content.split('\n')
        metadata: Dict[str, str] = {'context_unit_id': context_unit_id}
        for line in lines:
            if line.startswith('- **') and '**:' in line:
                key, value = line.split('**:', 1)
                key = key.replace('- **', '').strip()
                value = value.strip()
                metadata[key] = value
        return metadata
    
    def _validate_metadata(self, metadata: Dict) -> List[str]:
        errors: List[str] = []
        for field in self.required_metadata:
            if field not in metadata:
                errors.append(f"Missing required metadata field: {field}")
        # type/category checks (case-insensitive)
        mcu_type = (metadata.get('type') or metadata.get('Type') or '').strip().lower()
        if mcu_type and mcu_type not in self.valid_types:
            errors.append(f"Invalid type: {mcu_type}. Must be one of {self.valid_types}")
        category = (metadata.get('category') or metadata.get('Category') or '').strip().lower()
        if category and category not in self.valid_categories:
            errors.append(f"Invalid category: {category}. Must be one of {self.valid_categories}")
        # context_unit_id simple format check (allow variety but basic sanity)
        if 'context_unit_id' in metadata:
            if not re.match(r'^[a-z-]+-[a-z0-9-]+-\d{4}-\d{2}-\d{2}-\d{3,}$', metadata['context_unit_id']):
                errors.append("Invalid context_unit_id format. Expected: type-[tool]-YYYY-MM-DD-SEQ")
        return errors
    
    def _validate_structure(self, content: str) -> List[str]:
        errors: List[str] = []
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
        errors: List[str] = []
        if '## Executive Summary' in content and '**TL;DR**:' not in content:
            errors.append("Missing TL;DR in Executive Summary")
        if '## Quick Reference' in content and '### **Essential' not in content:
            errors.append("Missing Essential Requirements in Quick Reference")
        return errors
    
    def _validate_note_structure(self, content: str) -> List[str]:
        """Validate minimal structure for Note MCUs."""
        errors: List[str] = []
        if '## Notes' not in content:
            errors.append('Missing required section: ## Notes')
        timestamp_heading_re = re.compile(r'^## \[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\]', re.MULTILINE)
        if not timestamp_heading_re.search(content):
            errors.append('No timestamped note entries found (expected headings like ## [YYYY-MM-DDTHH:MM:SSZ])')
        return errors

    def _validate_backlog_structure(self, content: str) -> List[str]:
        """Validate minimal structure for Backlog MCUs."""
        errors: List[str] = []
        if '## Items Index' not in content:
            errors.append('Missing required section: ## Items Index')
        return errors

    def _validate_backlog_item_structure(self, content: str) -> List[str]:
        """Validate minimal structure for Backlog Item MCUs."""
        errors: List[str] = []
        if '## Source References' not in content:
            errors.append('Missing required section: ## Source References')
        else:
            # Require at least one markdown link in the Source References section
            # Rough check for a [text](link) pattern anywhere in the doc
            if not re.search(r'\[[^\]]+\]\([^\)]+\)', content):
                errors.append('No source references found (expected at least one [text](link))')
        return errors

    def validate_directory(self, directory: str) -> Dict[str, Tuple[bool, List[str]]]:
        results: Dict[str, Tuple[bool, List[str]]] = {}
        if os.path.isfile(directory):
            is_valid, errors = self.validate_file(directory)
            results[directory] = (is_valid, errors)
            return results
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    is_valid, errors = self.validate_file(file_path)
                    results[file_path] = (is_valid, errors)
        return results

def main():
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
    valid_count = sum(1 for _, (ok, _) in results.items() if ok)
    total_count = len(results)
    for file_path, (is_valid, errors) in results.items():
        if is_valid:
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            for error in errors:
                print(f"   - {error}")
    print("=" * 50)
    print(f"Validation complete: {valid_count}/{total_count} files valid")
    if any(not ok for ok, _ in results.values()):
        sys.exit(1)
    else:
        print("🎉 All MCU files are valid!")

if __name__ == "__main__":
    main()
