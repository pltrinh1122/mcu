# AIAI Framework

This directory contains the AIAI (AI Augmented Installation) framework, organized by audience and purpose.

## Structure

### `core/` - For Module Developers
Contains the core AIAI specification and schema for implementers:

- **`aiai_spec.md`** - Runtime behavior specification
- **`aiai_schema.json`** - Machine-readable schema definition
- **`aiai_schema_documentation.md`** - Human-readable schema documentation

### `design/` - For Package Designers
Contains design guidelines, templates, and tools for package creators:

- **`docs/`** - Design documentation and templates
  - `OPERATOR_GUIDE_TEMPLATE.md` - Template for operator guides
  - `PACKAGE_DESIGN_GUIDELINES.md` - Design principles and patterns
  - `TEMPLATE_ANALYSIS.md` - Analysis of template design decisions
- **`tools/`** - Design and development tools
  - `script2manual.py` - Generate manual instructions from aiaiScripts
- **`scripts/`** - Utility scripts for package development
- **`examples/`** - Reference implementations (future)

## Usage

### For Module Developers
Reference the `core/` specification and schema for implementing AIAI-compatible systems.

### For Package Designers
Use the `design/` guidelines and tools to create AIAI packages that follow best practices.

## Design Principles

- **Separation of Concerns**: Core specification separate from design guidance
- **Audience Focus**: Clear organization by intended user
- **Maintainability**: Independent evolution of core vs. design content
- **Consistency**: Shared principles across all components 