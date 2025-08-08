#!/usr/bin/env python3
"""
MCU Generator

This script generates MCU files from templates with proper metadata.
It helps create new MCUs with the correct structure and metadata.
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

class MCUGenerator:
    """Generates MCU files from templates."""
    
    def __init__(self):
        self.templates_dir = "templates"
        self.valid_types = ['reference', 'instruction', 'instruction-agent']
        
    def generate_mcu(self, mcu_type: str, name: str, output_dir: str = ".") -> bool:
        """Generate a new MCU file from template."""
        if mcu_type not in self.valid_types:
            print(f"Invalid MCU type: {mcu_type}")
            print(f"Valid types: {self.valid_types}")
            return False
            
        # Find template file
        template_file = f"MCU_{mcu_type.upper().replace('-', '_')}_TEMPLATE.md"
        template_path = os.path.join(self.templates_dir, template_file)
        
        if not os.path.exists(template_path):
            print(f"Template not found: {template_path}")
            return False
            
        # Generate metadata
        metadata = self._generate_metadata(mcu_type, name)
        
        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
            
        # Replace placeholders
        content = self._replace_placeholders(template_content, metadata)
        
        # Create output file
        output_file = f"{name}.md"
        output_path = os.path.join(output_dir, output_file)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Generated MCU: {output_path}")
        return True
    
    def _generate_metadata(self, mcu_type: str, name: str) -> Dict:
        """Generate metadata for new MCU."""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Generate context unit ID
        sequence = "001"  # Could be made more sophisticated
        context_unit_id = f"{mcu_type}-{name.lower().replace(' ', '-')}-{date_str}-{sequence}"
        
        return {
            'context_unit_id': context_unit_id,
            'created_at': time_str,
            'updated_at': time_str,
            'type': mcu_type,
            'version': '1.0',
            'project': 'MCU',
            'tool': name.upper().replace(' ', '_'),
            'category': 'specification',
            'tags': [mcu_type, 'specification', 'template']
        }
    
    def _replace_placeholders(self, template_content: str, metadata: Dict) -> str:
        """Replace placeholders in template with metadata."""
        content = template_content
        
        # Replace metadata section
        metadata_section = f"""## Context Memory Unit: {metadata['context_unit_id']}
- **Created**: {metadata['created_at']}
- **Updated**: {metadata['updated_at']}
- **Type**: {metadata['type']}
- **Version**: {metadata['version']}
- **Project**: {metadata['project']}
- **Tool**: {metadata['tool']}
- **Category**: {metadata['category']}
- **Tags**: {metadata['tags']}"""
        
        # Find and replace metadata section
        metadata_pattern = r'## Context Memory Unit: [^\n]+\n(?:- \*\*[^*]+\*\*: [^\n]+\n)*'
        content = re.sub(metadata_pattern, metadata_section, content)
        
        return content
    
    def list_templates(self):
        """List available templates."""
        print("Available MCU templates:")
        print("=" * 30)
        
        for template_file in os.listdir(self.templates_dir):
            if template_file.endswith('_TEMPLATE.md'):
                mcu_type = template_file.replace('MCU_', '').replace('_TEMPLATE.md', '').lower().replace('_', '-')
                print(f"- {mcu_type}: {template_file}")
                
        print(f"\nUsage: python generate_mcu.py <type> <name> [output_dir]")
        print(f"Example: python generate_mcu.py reference my-reference-doc")

def main():
    """Main generation function."""
    generator = MCUGenerator()
    
    if len(sys.argv) < 2:
        print("Usage: python generate_mcu.py <type> <name> [output_dir]")
        print("       python generate_mcu.py --list")
        sys.exit(1)
        
    if sys.argv[1] == "--list":
        generator.list_templates()
        return
        
    if len(sys.argv) < 3:
        print("Usage: python generate_mcu.py <type> <name> [output_dir]")
        sys.exit(1)
        
    mcu_type = sys.argv[1]
    name = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "."
    
    success = generator.generate_mcu(mcu_type, name, output_dir)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
