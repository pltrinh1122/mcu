# Ubuntu BTRFS Installation Framework

A comprehensive framework for installing Ubuntu 24.04 LTS with BTRFS filesystem optimized for AI/ML development workstations.

## Project Structure

This workspace contains multiple modules supporting both viScript and aiaiScript implementations:

```
.
├── ubuntu-btrfs-vi/          # viScript-based Ubuntu BTRFS installation
├── ubuntu-btrfs-aiai/        # aiaiScript-based Ubuntu BTRFS installation
├── viscriptlint/             # viScript validation and linting tool
├── vi/                       # Core VI framework
└── README.md                 # This file
```

## Modules

### 1. Ubuntu BTRFS viScript Implementation (ubuntu-btrfs-vi)
Complete system for installing Ubuntu with BTRFS filesystem using viScript framework.

**Key Features:**
- Three-partition strategy (System, ML, Data)
- BTRFS optimization with snapshots
- Comprehensive documentation
- Pre and post-installation validation
- JSON-based viScript files

**Location:** `ubuntu-btrfs-vi/`

### 2. Ubuntu BTRFS aiaiScript Implementation (ubuntu-btrfs-aiai)
Complete system for installing Ubuntu with BTRFS filesystem using aiaiScript framework.

**Key Features:**
- Three-partition strategy (System, ML, Data)
- BTRFS optimization with snapshots
- Comprehensive documentation
- Pre and post-installation validation
- YAML-based aiaiScript files with AI assistance
- Human-AI collaboration features

**Location:** `ubuntu-btrfs-aiai/`

### 3. viscriptlint
Validation and linting tool for viScript files used by the VI framework.

**Key Features:**
- JSON syntax validation
- Schema compliance checking
- Best practices enforcement
- CI/CD integration with standard exit codes

**Location:** `viscriptlint/`

### 4. VI Framework (vi)
Core framework for verifying various types of installations using JSON-based viScript files.

**Key Features:**
- Generic installation type support
- Flexible viScript system
- Batch execution capabilities
- Comprehensive logging and reporting

**Location:** `vi/`

## Quick Start

### viScript Implementation
```bash
# Validate system readiness
sudo ./vi/src/verified_installer.sh ubuntu-btrfs-vi/src/viScript/btrfs_system_validation_viScript.json

# Validate viScript files
./viscriptlint/src/viscriptlint.sh ubuntu-btrfs-vi/src/viScript/btrfs_system_validation_viScript.json
```

### aiaiScript Implementation
```bash
# Execute system validation (requires aiaiScript runtime)
# sudo ./aiai-runtime.sh ubuntu-btrfs-aiai/src/aiaiScript/btrfs_system_validation_aiaiScript.yaml

# Note: aiaiScript implementation requires AIAI-compatible runtime environment
```

## Documentation

Each module contains its own comprehensive documentation:

- **Ubuntu BTRFS viScript**: See `ubuntu-btrfs-vi/docs/`
- **Ubuntu BTRFS aiaiScript**: See `ubuntu-btrfs-aiai/docs/`
- **viscriptlint**: See `viscriptlint/docs/`
- **VI Framework**: See `vi/docs/`

## Development

### Module Structure
Each module follows a consistent structure:
```
module-name/
├── docs/          # Documentation
├── src/           # Source files
└── unit-tests/    # Unit tests
```

### Testing
```bash
# Test viscriptlint integration
./viscriptlint/unit-tests/test_viscriptlint_integration.sh

# Test VI framework
./vi/src/unit_test_verified_installer.sh
```

## Implementation Differences

### viScript Implementation
- Uses JSON-based viScript files
- Compatible with VI framework
- Traditional verification and installation approach
- Mature, tested implementation

### aiaiScript Implementation
- Uses YAML-based aiaiScript files
- Requires AIAI-compatible runtime
- AI-augmented installation with human-AI partnership
- Natural language descriptions and contextual guidance

## Dependencies

- **System**: Ubuntu 24.04 LTS Live USB, UEFI boot mode
- **Hardware**: Minimum 16GB RAM, NVIDIA GPU (optional)
- **Software**: `jq` (JSON processing), `bash`, `sudo`
- **aiaiScript**: AIAI-compatible runtime environment

## License

This framework is provided as-is for educational and operational purposes. Please ensure compliance with your organization's policies when using this framework.