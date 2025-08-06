"""
AIAI Script Validator

Validates AIAI Scripts against the specification.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class AIAIScriptValidator:
    """Validates AIAI Scripts against the specification."""
    
    def __init__(self, schema_path: Optional[str] = None):
        """Initialize the validator with optional schema path."""
        self.schema_path = schema_path or "framework/docs/aiai_schema.json"
        self.schema = self._load_schema()
    
    def _load_schema(self) -> Dict[str, Any]:
        """Load the AIAI Script schema."""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Schema file not found at {self.schema_path}")
            return {}
    
    def validate_script(self, script_path: str) -> bool:
        """Validate a single AIAI Script file."""
        try:
            with open(script_path, 'r') as f:
                script_data = yaml.safe_load(f)
            
            # Basic validation - check required fields
            if not isinstance(script_data, dict):
                print(f"Error: {script_path} - Script must be a YAML object")
                return False
            
            if 'metadata' not in script_data:
                print(f"Error: {script_path} - Missing 'metadata' section")
                return False
            
            if 'steps' not in script_data:
                print(f"Error: {script_path} - Missing 'steps' section")
                return False
            
            print(f"✓ {script_path} - Basic validation passed")
            return True
            
        except yaml.YAMLError as e:
            print(f"Error: {script_path} - Invalid YAML: {e}")
            return False
        except Exception as e:
            print(f"Error: {script_path} - {e}")
            return False
    
    def validate_directory(self, directory_path: str) -> bool:
        """Validate all AIAI Scripts in a directory."""
        directory = Path(directory_path)
        if not directory.exists():
            print(f"Error: Directory {directory_path} does not exist")
            return False
        
        yaml_files = list(directory.glob("*.yaml")) + list(directory.glob("*.yml"))
        if not yaml_files:
            print(f"Warning: No YAML files found in {directory_path}")
            return True
        
        all_valid = True
        for yaml_file in yaml_files:
            if not self.validate_script(str(yaml_file)):
                all_valid = False
        
        return all_valid


def main():
    """Main entry point for the validator."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python validator.py <script_path_or_directory>")
        sys.exit(1)
    
    validator = AIAIScriptValidator()
    target = sys.argv[1]
    
    if Path(target).is_file():
        success = validator.validate_script(target)
    else:
        success = validator.validate_directory(target)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 