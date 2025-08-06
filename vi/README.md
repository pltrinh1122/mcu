# VI Framework

## Overview

The VI Framework is a comprehensive, parameterized system for verifying various types of installations. It provides a standardized approach to installation validation while maintaining flexibility for different installation types and requirements.

## Module Structure

```
vi/
├── docs/                    # Documentation
│   ├── VERIFIED_INSTALLER.md # Main documentation
│   ├── BATCH_EXECUTION_SUMMARY.md
│   ├── PREREQUISITE_PROMPT_EXAMPLE.md
│   └── viScript_coherence_analysis.md
├── src/                     # Source files
│   ├── verified_installer.py # Main VI framework (Python)
│   ├── verified_installer.py # Main verification script (Python)
│   ├── test_verified_installer_basic.py # Basic unit tests
│   ├── test_verified_installer_full.py # Full unit tests
│   └── verified_installer.py # Main installer script (Python)
└── unit-tests/             # Unit tests (future)
```

## Key Features

- **Generic Installation Support**: Any installation type defined in viScript files
- **Flexible viScript System**: JSON-based configuration with strict schema validation
- **Text Output Formats**: Simple success/failed/warning messages
- **Advanced Features**: Test mode, verbose logging, dependency checking
- **Batch Execution**: Automated processing of multiple viScripts

## Usage

### Basic Usage

```bash
# System validation
sudo python3 ./src/verified_installer.py system_validation_viScript.json

# BTRFS installation verification with verbose output
sudo python3 ./src/verified_installer.py btrfs_root_viScript.json --verbose

# Docker installation with test mode
sudo python3 ./src/verified_installer.py ../ubuntu-btrfs-vi/src/docker_viScript.json --test

# Custom installation verification
sudo python3 ./src/verified_installer.py custom_viScript.json
```

### Batch Execution

```bash
# Execute multiple viScripts in sequence
sudo python3 ./src/verified_installer.py system_validation_viScript.json

# Test mode with verbose output
sudo python3 ./src/verified_installer.py btrfs_root_viScript.json --test --verbose
```

### Output Redirection

```bash
# Generate text report
sudo python3 ./src/verified_installer.py btrfs_root_viScript.json > report.txt

# Verbose mode for detailed logging
sudo python3 ./src/verified_installer.py ../ubuntu-btrfs-vi/src/docker_viScript.json --verbose
```

## viScript Structure

The framework uses JSON viScript files to define verification steps:

```json
{
  "installation_type": "btrfs_root",
  "version": "2.0",
  "description": "Installation description",
  "phases": [
    {
      "name": "phase_name",
      "description": "Phase description",
      "checks": [
        {
          "name": "check_name",
          "description": "Check description",
          "command": "command_to_execute",
          "validation_type": "return_value|output_pattern|both|none",
          "expected_return": 0,
          "expected_pattern": "expected_output_pattern",
          "severity": "critical|informational"
        }
      ]
    }
  ],
  "next_step": "next_viscript_filename.json"
}
```

## Validation Types

- **return_value**: Validate command exit code
- **output_pattern**: Validate command output matches pattern
- **both**: Validate both return value and output pattern
- **none**: Execute command without validation

## Severity Levels

- **critical**: Failure causes overall verification to fail
- **informational**: Failure creates warning but doesn't fail overall verification

## Installation Types

- **system_validation**: Pre-installation system checks
- **btrfs_root**: BTRFS root partition verification
- **btrfs_ml**: BTRFS ML partition verification
- **btrfs_data**: BTRFS data partition verification
- **docker**: Docker installation verification
- **custom**: User-defined installation types

## Testing

Run the unit tests:

```bash
# Basic tests (fast validation)
python3 ./unit-tests/test_verified_installer_basic.py

# Full tests (comprehensive validation)
python3 ./unit-tests/test_verified_installer_full.py
```

## Dependencies

- `python3`: Python 3.x (required for execution)
- `viscriptlint`: viScript validation framework
- `sudo`: Administrative privileges for system operations

## Documentation

See `docs/VERIFIED_INSTALLER.md` for comprehensive framework documentation and examples. 