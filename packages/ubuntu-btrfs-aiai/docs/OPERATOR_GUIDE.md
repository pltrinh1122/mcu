# Ubuntu BTRFS AIAI Package - Operator Guide

## Overview

This package contains AIAI Scripts for automating Ubuntu BTRFS installation and configuration processes.

## Package Structure

```
ubuntu-btrfs-aiai/
├── docs/                    # Documentation
│   └── OPERATOR_GUIDE.md   # This file
├── src/
│   └── aiaiScript/         # AIAI Script files
├── MANIFEST                # Package manifest
└── README.md              # Package overview
```

## Common Components

This package includes shared components from the `../common/` directory:

- `../common/specs/aiai_schema.json` - AIAI Schema specification
- `../common/specs/aiai_spec.md` - AIAI Specification documentation

## Usage

1. Ensure all dependencies are met
2. Review the AIAI Scripts in `src/aiaiScript/`
3. Execute scripts according to the installation workflow
4. Validate system state after each phase

## Dependencies

- Ubuntu/Debian system
- BTRFS filesystem support
- Common AIAI components 