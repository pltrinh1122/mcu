#!/usr/bin/env python3
"""
AIAI Script to Manual Instructions Generator

Converts aiaiScript YAML files into human-readable manual installation instructions.
"""

import argparse
import yaml
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class Script2Manual:
    def __init__(self):
        self.scripts = {}
        self.phases = {}
        self.current_phase = 1
        
    def load_scripts(self, input_path: str) -> None:
        """Load aiaiScript files from the input path (file or directory)."""
        path = Path(input_path)
        if not path.exists():
            raise FileNotFoundError(f"Input path not found: {input_path}")
        
        yaml_files = []
        
        if path.is_file():
            # Single file provided
            if path.suffix.lower() in ['.yaml', '.yml']:
                yaml_files = [path]
                print(f"Processing single file: {path}")
            else:
                raise ValueError(f"File must have .yaml or .yml extension: {input_path}")
        elif path.is_dir():
            # Directory provided - find all YAML files
            yaml_files = list(path.glob("*.yaml")) + list(path.glob("*.yml"))
            print(f"Processing directory: {path} (found {len(yaml_files)} YAML files)")
        else:
            raise ValueError(f"Input path must be a file or directory: {input_path}")
            
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r') as f:
                    script_data = yaml.safe_load(f)
                    script_name = yaml_file.stem
                    self.scripts[script_name] = script_data
                    print(f"Loaded script: {script_name}")
            except Exception as e:
                print(f"Warning: Could not load {yaml_file}: {e}")
                
    def extract_phase_info(self, script_data: Dict) -> Optional[Dict]:
        """Extract phase information from script metadata."""
        if 'metadata' in script_data and 'context' in script_data['metadata']:
            context = script_data['metadata']['context']
            if 'phase' in context:
                return context['phase']
        return None
        
    def extract_commands(self, script_data: Dict) -> List[Dict]:
        """Extract all commands from a script recursively."""
        commands = []
        
        def extract_from_body(body):
            if not body:
                return
                
            for item in body:
                if item.get('type') == 'command':
                    commands.append({
                        'id': item.get('id', 'unknown'),
                        'intent': item.get('intent', 'No description'),
                        'command': item.get('shellCommand', ''),
                        'destructive': item.get('destructive', False),
                        'conditional': item.get('conditional', False)
                    })
                elif item.get('type') == 'validation':
                    commands.append({
                        'id': item.get('id', 'unknown'),
                        'intent': item.get('intent', 'No description'),
                        'command': item.get('command', ''),
                        'expected_output': item.get('expected_output', ''),
                        'critical': item.get('critical', False),
                        'on_fail': item.get('on_fail', ''),
                        'is_validation': True
                    })
                elif item.get('type') == 'script':
                    # Recursively extract from nested script
                    if 'body' in item:
                        extract_from_body(item['body'])
                        
        if 'body' in script_data:
            extract_from_body(script_data['body'])
            
        return commands
        
    def generate_manual_content(self, selected_phases: Optional[List[str]] = None) -> str:
        """Generate manual installation content from loaded scripts."""
        content = []
        
        # Header
        content.append("# Manual Installation Instructions")
        content.append("")
        content.append("*This document was automatically generated from aiaiScript files.*")
        content.append("")
        
        # List source scripts
        if self.scripts:
            content.append("## Source Scripts")
            content.append("")
            content.append("This manual was generated from the following aiaiScript files:")
            content.append("")
            for script_name in sorted(self.scripts.keys()):
                content.append(f"- `{script_name}.yaml`")
            content.append("")
        content.append("## Overview")
        content.append("")
        content.append("This manual provides step-by-step instructions for manual installation.")
        content.append("Each step includes the command to execute, its purpose, and expected outcomes.")
        content.append("")
        
        # Process scripts
        for script_name, script_data in self.scripts.items():
            # Check if we should include this script based on phase selection
            phase_info = self.extract_phase_info(script_data)
            if selected_phases and phase_info:
                phase_name = phase_info.get('name', '')
                if phase_name not in selected_phases:
                    continue
                    
            # Extract script metadata
            metadata = script_data.get('metadata', {})
            script_intent = metadata.get('intent', f'Execute {script_name}')
            
            # Determine phase information
            if phase_info:
                phase_name = phase_info.get('name', 'unknown')
                phase_number = phase_info.get('number', self.current_phase)
                phase_desc = phase_info.get('description', '')
                content.append(f"## Phase {phase_number}: {phase_name.title()}")
                content.append("")
                content.append(f"**Source**: `{script_name}.yaml`")
                if phase_desc:
                    content.append(f"**Purpose**: {phase_desc}")
                content.append("")
            else:
                content.append(f"## {script_name.replace('_', ' ').title()}")
                content.append("")
                content.append(f"**Source**: `{script_name}.yaml`")
                content.append("")
                
            # Extract and format commands
            commands = self.extract_commands(script_data)
            
            for i, cmd in enumerate(commands, 1):
                content.append(f"### Step {i}: {cmd['intent']}")
                content.append("")
                
                # Format command information in a readable way with proper line breaks
                content.append(f"**Purpose**: {cmd['intent']}  ")
                
                # Add validation-specific information
                if cmd.get('is_validation'):
                    if cmd.get('critical'):
                        content.append("**Critical**: Yes - must pass to continue  ")
                    content.append(f"**On Failure**: {cmd.get('on_fail', 'skip')}  ")
                
                # Don't add expected output here - it will be in the verification block
                
                # Add warnings and notes
                if cmd.get('destructive'):
                    content.append("**Warning**: This is a destructive operation  ")
                if cmd.get('conditional'):
                    content.append("**Note**: This command is conditional  ")
                        
                content.append("")
                
                # Add verification steps for validations - don't show redundant command block
                if cmd.get('is_validation') and cmd.get('expected_output'):
                    # Skip the regular command block for validations since verification includes it
                    pass
                else:
                    # Show command block only for non-validation commands
                    content.append("```bash")
                    content.append(cmd['command'])
                    content.append("```")
                    content.append("")
                
                # Add verification block for validations
                if cmd.get('is_validation') and cmd.get('expected_output'):
                    content.append("**Verification**:")
                    content.append("")
                    content.append("```bash")
                    content.append(f"# Run the command and check output")
                    content.append(f"{cmd['command']}")
                    content.append("")
                    content.append(f"# Expected:")
                    content.append(f"{cmd['expected_output']}")
                    content.append("```")
                    content.append("")
                    
            content.append("---")
            content.append("")
            
            if phase_info:
                self.current_phase += 1
                
        # Add troubleshooting section
        content.append("## Troubleshooting")
        content.append("")
        content.append("### Common Issues")
        content.append("")
        content.append("**Command fails with permission error**:")
        content.append("- Ensure you're running with sudo privileges")
        content.append("- Check if the command requires elevated permissions")
        content.append("")
        content.append("**Validation step fails**:")
        content.append("- Verify the system meets the requirements")
        content.append("- Check if all prerequisites are installed")
        content.append("- Review the expected output format")
        content.append("")
        content.append("**Destructive operation warnings**:")
        content.append("- Double-check the target before proceeding")
        content.append("- Ensure you have backups if needed")
        content.append("- Verify you're working on the correct system")
        content.append("")
        
        return "\n".join(content)
        
    def generate_manual(self, input_path: str, output_file: str, selected_phases: Optional[List[str]] = None) -> None:
        """Generate manual installation instructions."""
        print(f"Loading scripts from: {input_path}")
        self.load_scripts(input_path)
        
        if not self.scripts:
            print("Error: No valid aiaiScript files found")
            sys.exit(1)
            
        print(f"Generating manual instructions...")
        content = self.generate_manual_content(selected_phases)
        
        # Ensure output directory exists
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write output file
        with open(output_file, 'w') as f:
            f.write(content)
            
        print(f"Manual instructions written to: {output_file}")
        print(f"Generated from {len(self.scripts)} script files")


def main():
    parser = argparse.ArgumentParser(
        description="Generate manual installation instructions from aiaiScript files"
    )
    parser.add_argument(
        "--input", 
        required=True,
        help="Input path: directory containing aiaiScript YAML files, or single YAML file"
    )
    parser.add_argument(
        "--output", 
        required=False,
        help="Output file for generated manual instructions (default: manual_instructions.md)"
    )
    parser.add_argument(
        "--phases",
        help="Comma-separated list of specific phases to include (optional)"
    )
    
    args = parser.parse_args()
    
    # Set default output filename if not provided
    output_file = args.output
    if not output_file:
        output_file = "manual_instructions.md"
        print(f"No output file specified, using default: {output_file}")
    
    # Parse phases if specified
    selected_phases = None
    if args.phases:
        selected_phases = [phase.strip() for phase in args.phases.split(',')]
        print(f"Including phases: {selected_phases}")
    
    # Generate manual
    generator = Script2Manual()
    generator.generate_manual(args.input, output_file, selected_phases)


if __name__ == "__main__":
    main() 