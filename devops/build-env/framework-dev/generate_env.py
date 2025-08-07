#!/usr/bin/env python3
"""
Development Environment Generator
Generates new development environments from templates using YAML configuration
"""

import os
import sys
import yaml
import argparse
import shutil
from pathlib import Path
from typing import Dict, Any, List
import re

class EnvironmentGenerator:
    """Generates development environments from templates"""
    
    def __init__(self, template_dir: str = "dev-env-template"):
        self.template_dir = Path(template_dir)
        self.config_file = self.template_dir / "env-config.yaml"
        
    def load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if config_path:
            config_file = Path(config_path)
        else:
            # Try current directory first, then template directory
            config_file = Path("env-config.yaml")
            if not config_file.exists():
                config_file = self.config_file
            
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
            
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def replace_templates(self, content: str, variables: Dict[str, str]) -> str:
        """Replace template variables in content"""
        for key, value in variables.items():
            placeholder = '{{' + key + '}}'
            content = content.replace(placeholder, str(value))
        return content
    
    def process_file(self, file_path: Path, variables: Dict[str, str]) -> None:
        """Process a single file, replacing templates"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Replace templates
            new_content = self.replace_templates(content, variables)
            
            with open(file_path, 'w') as f:
                f.write(new_content)
                
            print(f"  ✓ Processed: {file_path}")
            
        except Exception as e:
            print(f"  ✗ Error processing {file_path}: {e}")
    
    def should_process_file(self, file_path: Path) -> bool:
        """Determine if file should be processed for template replacement"""
        processable_extensions = {
            '.md', '.sh', '.yml', '.yaml', '.toml', '.ini', 
            '.json', '.py', '.txt', '.cfg', '.conf'
        }
        return file_path.suffix.lower() in processable_extensions
    
    def generate_environment(self, component_name: str, config: Dict[str, Any] = None) -> None:
        """Generate a new development environment"""
        print(f"Generating environment for: {component_name}")
        
        # Load configuration
        if config is None:
            config = self.load_config()
        
        # Get variables
        variables = config.get('variables', {})
        variables['COMPONENT_NAME'] = component_name
        variables['COMPONENT_FULL_NAME'] = variables.get('COMPONENT_FULL_NAME', component_name)
        variables['COMPONENT_DESCRIPTION'] = variables.get('COMPONENT_DESCRIPTION', f"{component_name} component")
        
        # Process current directory files
        print("Processing template files...")
        for root, dirs, files in os.walk('.'):
            for file in files:
                file_path = Path(root) / file
                if self.should_process_file(file_path) and file_path.name != 'generate_env.py':
                    self.process_file(file_path, variables)
        
        print(f"Environment generated for: {component_name}")
        print("\nNext steps:")
        print(f"  1. Edit env-config.yaml if needed")
        print(f"  2. ./scripts/setup-env.sh")
    
    def validate_environment(self, component_name: str) -> bool:
        """Validate an existing environment"""
        env_dir = Path(f"{component_name}-dev")
        
        if not env_dir.exists():
            print(f"✗ Environment not found: {env_dir}")
            return False
        
        print(f"Validating environment: {env_dir}")
        
        # Check required files
        required_files = [
            "env-config.yaml",
            "README.md",
            "scripts/setup-env.sh",
            "scripts/run-tests.sh",
            "requirements/requirements.txt"
        ]
        
        all_valid = True
        for file_path in required_files:
            full_path = env_dir / file_path
            if full_path.exists():
                print(f"  ✓ {file_path}")
            else:
                print(f"  ✗ {file_path} (missing)")
                all_valid = False
        
        # Check configuration
        config_file = env_dir / "env-config.yaml"
        if config_file.exists():
            try:
                config = self.load_config(str(config_file))
                env_config = config.get('environment', {})
                comp_config = config.get('component', {})
                
                print(f"  ✓ Configuration loaded")
                print(f"    - Name: {env_config.get('name', 'N/A')}")
                print(f"    - Description: {env_config.get('description', 'N/A')}")
                print(f"    - Component Type: {comp_config.get('type', 'N/A')}")
                
            except Exception as e:
                print(f"  ✗ Configuration error: {e}")
                all_valid = False
        
        return all_valid
    
    def list_environments(self) -> List[str]:
        """List existing environments"""
        environments = []
        for item in Path('.').iterdir():
            if item.is_dir() and item.name.endswith('-dev') and item.name != 'dev-env-template':
                environments.append(item.name)
        return sorted(environments)
    
    def clean_environment(self, component_name: str) -> None:
        """Remove an environment"""
        env_dir = Path(f"{component_name}-dev")
        if env_dir.exists():
            shutil.rmtree(env_dir)
            print(f"Environment removed: {env_dir}")
        else:
            print(f"Environment not found: {env_dir}")
    
    def update_template(self, component_name: str) -> None:
        """Update template from existing environment"""
        env_dir = Path(f"{component_name}-dev")
        if not env_dir.exists():
            print(f"Environment not found: {env_dir}")
            return
        
        # Remove existing template
        if self.template_dir.exists():
            shutil.rmtree(self.template_dir)
        
        # Copy environment to template
        shutil.copytree(env_dir, self.template_dir)
        print(f"Template updated from {env_dir}")

def main():
    parser = argparse.ArgumentParser(description="Generate development environments from templates")
    parser.add_argument('action', choices=['create', 'validate', 'list', 'clean', 'update-template'],
                       help='Action to perform')
    parser.add_argument('--component', '-c', help='Component name')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--template-dir', default='dev-env-template',
                       help='Template directory')
    
    args = parser.parse_args()
    
    generator = EnvironmentGenerator(args.template_dir)
    
    if args.action == 'create':
        if not args.component:
            print("Error: --component is required for create action")
            sys.exit(1)
        generator.generate_environment(args.component)
        
    elif args.action == 'validate':
        if not args.component:
            print("Error: --component is required for validate action")
            sys.exit(1)
        success = generator.validate_environment(args.component)
        sys.exit(0 if success else 1)
        
    elif args.action == 'list':
        environments = generator.list_environments()
        if environments:
            print("Existing environments:")
            for env in environments:
                print(f"  - {env}")
        else:
            print("No environments found")
            
    elif args.action == 'clean':
        if not args.component:
            print("Error: --component is required for clean action")
            sys.exit(1)
        generator.clean_environment(args.component)
        
    elif args.action == 'update-template':
        if not args.component:
            print("Error: --component is required for update-template action")
            sys.exit(1)
        generator.update_template(args.component)

if __name__ == "__main__":
    main()
