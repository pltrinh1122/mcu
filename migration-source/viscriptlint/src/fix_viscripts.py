#!/usr/bin/env python3

"""
viScript Schema Fix Script
Automatically fixes schema issues in viScript files with enhanced handling
"""

import json
import sys
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List

def fix_viscript_file(filename: str) -> bool:
    """Fix a single viScript file with enhanced handling."""
    print(f"Fixing: {filename}")
    
    # Create backup
    backup_filename = f"{filename}.backup"
    if not os.path.exists(backup_filename):
        shutil.copy2(filename, backup_filename)
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Process each phase and check with enhanced logic
        if 'phases' in data:
            for phase in data['phases']:
                if 'checks' in phase:
                    for check in phase['checks']:
                        # Convert critical to severity (enhanced handling)
                        if 'critical' in check:
                            # Handle both explicit boolean and truthy/falsy values
                            if check['critical'] is True or check['critical']:
                                check['severity'] = 'critical'
                            elif check['critical'] is False or not check['critical']:
                                check['severity'] = 'informational'
                            else:
                                # Handle unexpected critical values
                                print(f"    Warning: Unexpected critical value '{check['critical']}' in {check.get('name', 'unnamed_check')}")
                                check['severity'] = 'critical' if check['critical'] else 'informational'
                            del check['critical']
                        
                        # Remove weight field completely
                        if 'weight' in check:
                            del check['weight']
                        
                        # Add validation_type if missing (enhanced logic)
                        if 'validation_type' not in check:
                            if 'expected_pattern' in check:
                                check['validation_type'] = 'output_pattern'
                            elif 'expected_return' in check:
                                check['validation_type'] = 'return_value'
                            else:
                                # For checks with neither expected_pattern nor expected_return
                                check['validation_type'] = 'none'
                        
                        # Fix empty expected_pattern for informational checks
                        if (check.get('validation_type') == 'output_pattern' and 
                            check.get('expected_pattern') == '' and 
                            check.get('severity') == 'informational'):
                            check['validation_type'] = 'none'
                            del check['expected_pattern']
                            print(f"    Fixed empty expected_pattern for informational check: {check.get('name', 'unnamed')}")
                        
                        # Fix empty expected_pattern for critical checks (change to none)
                        elif (check.get('validation_type') == 'output_pattern' and 
                              check.get('expected_pattern') == '' and 
                              check.get('severity') == 'critical'):
                            check['validation_type'] = 'none'
                            del check['expected_pattern']
                            print(f"    Fixed empty expected_pattern for critical check: {check.get('name', 'unnamed')}")
                        
                        # Fix any remaining empty expected_pattern issues
                        elif (check.get('validation_type') == 'output_pattern' and 
                              check.get('expected_pattern') == ''):
                            check['validation_type'] = 'none'
                            del check['expected_pattern']
                            print(f"    Fixed empty expected_pattern for check: {check.get('name', 'unnamed')}")
        
        # Write the fixed file with proper formatting
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"  ✓ Fixed {filename}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error fixing {filename}: {e}")
        return False

def show_help():
    """Show help information."""
    help_text = """
viScript Schema Fix Script

Usage: python3 fix_viscripts.py <FILE>

ARGUMENTS:
    FILE                    viScript file to fix (required)

DESCRIPTION:
    Automatically fixes common schema issues in viScript files:
    - Converts deprecated critical/weight fields to severity format
    - Adds missing validation_type fields
    - Fixes empty expected_pattern issues (changes to validation_type: none)
    - Handles both explicit boolean and truthy/falsy critical values
    - Creates backup files before making changes

FEATURES:
    - Enhanced critical value handling (explicit boolean + truthy/falsy)
    - Comprehensive empty pattern detection and fixing
    - Detailed error reporting for edge cases
    - Automatic backup creation
    - Enhanced validation_type assignment
    - Support for both informational and critical checks
    - Single file processing

EXAMPLES:
    # Fix specific file
    python3 fix_viscripts.py my_viscript.json

    # Show this help
    python3 fix_viscripts.py --help
"""
    print(help_text.strip())

def main():
    """Main function to fix viScript files with enhanced handling."""
    # Check for help argument
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        show_help()
        return
    
    # Check if a file was provided as argument
    if len(sys.argv) < 2:
        print("Error: File argument is required")
        print("Usage: python3 fix_viscripts.py <file>")
        print("Use --help for more information")
        sys.exit(1)
    
    specific_file = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(specific_file):
        print(f"Error: File not found: {specific_file}")
        sys.exit(1)
    
    print("=== Python viScript Schema Fix ===")
    print(f"Fixing schema issues in: {specific_file}")
    print("")
    
    if fix_viscript_file(specific_file):
        print("")
        print("=== Summary ===")
        print(f"Successfully fixed: {specific_file}")
        print("Backup file created with .backup extension")
        print("")
        print("Next steps:")
        print("1. Review fixed file for any manual adjustments needed")
        print("2. Test viScript file with: ./verified_installer.sh <file> --test")
        print("3. Remove .backup file after confirming everything works")
    else:
        print("")
        print("=== Summary ===")
        print(f"Failed to fix: {specific_file}")
        sys.exit(1)

if __name__ == "__main__":
    main() 