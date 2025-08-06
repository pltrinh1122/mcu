# AIAI Design Guidelines

This directory contains design guidelines, templates, and tools for AIAI package designers.

## Contents

### `docs/`
Design documentation and templates:
- **`OPERATOR_GUIDE_TEMPLATE.md`** - Template for creating operator guides
- **`PACKAGE_DESIGN_GUIDELINES.md`** - Comprehensive design principles and patterns
- **`TEMPLATE_ANALYSIS.md`** - Analysis of template design decisions

### `tools/`
Design and development tools:
- **`script2manual.py`** - Generate manual installation instructions from aiaiScript files

### `scripts/`
Utility scripts for package development and maintenance.

### `examples/`
Reference implementations and example packages (future).

## Audience

This content is intended for:
- **Package Designers**: Creating AIAI installation packages
- **Documentation Writers**: Writing operator guides and documentation
- **Tool Developers**: Building tools for package development

## Usage

### For Package Designers
1. Read `docs/PACKAGE_DESIGN_GUIDELINES.md` for design principles
2. Use `docs/OPERATOR_GUIDE_TEMPLATE.md` as a starting point
3. Use `tools/script2manual.py` to generate manual instructions

### For Documentation Writers
1. Follow the operator guide template structure
2. Reference design guidelines for best practices
3. Use the manual generation tool for consistency

## Design Principles

- **Scripts vs Phases**: Clear distinction between atomic operations and logical milestones
- **Single Source of Truth**: aiaiScript files as authoritative source
- **Human-AI Partnership**: Design for both AI execution and human oversight
- **Flexibility**: Support various installation types and complexity levels

## Tools

### script2manual.py
Converts aiaiScript YAML files into human-readable manual instructions:

```bash
# Generate complete manual
python3 tools/script2manual.py --input src/aiaiScript/ --output docs/MANUAL_INSTALLATION.md

# Generate specific phases
python3 tools/script2manual.py --input src/aiaiScript/ --output docs/MANUAL_INSTALLATION.md --phases "system-validation,storage-setup"
```

## Version

Current version: 1.0
Last updated: August 5, 2025 