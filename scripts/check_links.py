#!/usr/bin/env python3
"""
MCU Link Checker

This script checks for broken links in MCU documentation files.
It validates internal links, external links, and cross-references.
"""

import os
import sys
import re
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from urllib.parse import urlparse, urljoin

class LinkChecker:
    """Checks links in MCU documentation files."""
    
    def __init__(self):
        self.broken_links = []
        self.valid_links = []
        self.external_links = []
        
    def check_file(self, file_path: str) -> List[Dict]:
        """Check links in a single file."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find all markdown links
            link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            links = re.findall(link_pattern, content)
            
            for link_text, link_url in links:
                issue = self._validate_link(file_path, link_text, link_url)
                if issue:
                    issues.append(issue)
                    
        except Exception as e:
            issues.append({
                'file': file_path,
                'type': 'error',
                'message': f"Error reading file: {str(e)}"
            })
            
        return issues
    
    def _validate_link(self, file_path: str, link_text: str, link_url: str) -> Optional[Dict]:
        """Validate a single link."""
        # Skip external links for now (can be added later)
        if link_url.startswith('http'):
            return None
            
        # Check if it's a relative link
        if link_url.startswith('./') or link_url.startswith('../'):
            return self._check_relative_link(file_path, link_text, link_url)
            
        # Check if it's an anchor link
        if link_url.startswith('#'):
            return self._check_anchor_link(file_path, link_text, link_url)
            
        # Check if it's a file link
        return self._check_file_link(file_path, link_text, link_url)
    
    def _check_relative_link(self, file_path: str, link_text: str, link_url: str) -> Optional[Dict]:
        """Check relative links."""
        file_dir = os.path.dirname(file_path)
        target_path = os.path.join(file_dir, link_url)
        
        if not os.path.exists(target_path):
            return {
                'file': file_path,
                'type': 'broken_link',
                'link_text': link_text,
                'link_url': link_url,
                'message': f"Target file does not exist: {target_path}"
            }
            
        return None
    
    def _check_anchor_link(self, file_path: str, link_text: str, link_url: str) -> Optional[Dict]:
        """Check anchor links."""
        # For now, just check if the anchor format is valid
        if not re.match(r'^#[a-zA-Z0-9_-]+$', link_url):
            return {
                'file': file_path,
                'type': 'invalid_anchor',
                'link_text': link_text,
                'link_url': link_url,
                'message': f"Invalid anchor format: {link_url}"
            }
            
        return None
    
    def _check_file_link(self, file_path: str, link_text: str, link_url: str) -> Optional[Dict]:
        """Check file links."""
        file_dir = os.path.dirname(file_path)
        target_path = os.path.join(file_dir, link_url)
        
        if not os.path.exists(target_path):
            return {
                'file': file_path,
                'type': 'broken_link',
                'link_text': link_text,
                'link_url': link_url,
                'message': f"Target file does not exist: {target_path}"
            }
            
        return None
    
    def check_directory(self, directory: str) -> List[Dict]:
        """Check all markdown files in a directory."""
        all_issues = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    issues = self.check_file(file_path)
                    all_issues.extend(issues)
                    
        return all_issues

def main():
    """Main link checking function."""
    checker = LinkChecker()
    
    if len(sys.argv) < 2:
        print("Usage: python check_links.py <directory>")
        sys.exit(1)
        
    directory = sys.argv[1]
    
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        sys.exit(1)
        
    print(f"Checking links in: {directory}")
    print("=" * 50)
    
    issues = checker.check_directory(directory)
    
    if not issues:
        print("🎉 No link issues found!")
        return
        
    for issue in issues:
        print(f"❌ {issue['file']}")
        print(f"   - {issue['message']}")
        if 'link_text' in issue:
            print(f"   - Link: [{issue['link_text']}]({issue['link_url']})")
        print()
        
    print(f"Found {len(issues)} link issues")
    sys.exit(1)

if __name__ == "__main__":
    main()
