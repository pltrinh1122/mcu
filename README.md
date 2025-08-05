# Ubuntu BTRFS AIAI Installer

## Overview

The Ubuntu BTRFS AIAI Installer module provides a comprehensive system for installing Ubuntu 24.04 LTS with BTRFS filesystem optimized for AI/ML development workstations using the AIAI script framework.

## Module Structure

```
ubuntu-btrfs-aiai/
├── docs/                    # Documentation
│   ├── UBUNTU_BTRFS_INSTALLER.md
│   ├── S1_THREE_PARTITION_STORAGE_STRATEGY.md
│   ├── S2_SYSTEM_READINESS_CHECKLIST.md
│   ├── S3_STORAGE_PARTITIONING.md
│   ├── S4_SYSTEM_SUBVOLUME_SETUP.md
│   ├── S5_ML_SUBVOLUME_SETUP.md
│   ├── S6_DATA_PARTITION_SETUP.md
│   ├── S7_GRUB_SETUP_AND_REBOOT.md
│   └── UBUNTU-BTRFS_TROUBLESHOOTING.md
├── src/                     # Source files
│   └── aiaiScript/         # AIAI script files (YAML format)
│       └── *_aiaiScript.yaml
└── unit-tests/             # Unit tests (future)
```

## Key Features

- **Three-Partition Strategy**: System, ML, and Data partitions
- **BTRFS Optimization**: Copy-on-write filesystem with snapshots
- **AI/ML Focus**: Optimized for machine learning workloads
- **Comprehensive Documentation**: Step-by-step installation guide
- **Validation Scripts**: Pre and post-installation verification
- **AIAI Script Framework**: AI-augmented installation with human-AI partnership

## Installation Process

1. **System Validation** (S2): Hardware and environment checks
2. **Storage Partitioning** (S3): Disk partitioning strategy
3. **System Subvolume Setup** (S4): BTRFS subvolume creation
4. **ML Subvolume Setup** (S5): Machine learning partition
5. **Data Partition Setup** (S6): Data storage configuration
6. **GRUB Setup** (S7): Bootloader configuration

## AIAI Script Format

### AIAI Script Format
- **Location**: `src/aiaiScript/`
- **Format**: YAML files following AIAI schema v1.2
- **Usage**: Requires AIAI-compatible runtime
- **Purpose**: AI-augmented installation with human-AI partnership
- **Features**: 
  - Natural language descriptions
  - AI-assisted decision making
  - Human-AI collaboration
  - Contextual guidance

## Usage

```bash
# Run system validation (AIAI script format)
# Note: AIAI scripts are in YAML format and require AIAI-compatible runtime
# Example: ./aiai-runtime src/aiaiScript/btrfs_system_validation_aiaiScript.yaml
```

## Dependencies

- Ubuntu 24.04 LTS Live USB
- UEFI boot mode
- Minimum 16GB RAM
- NVIDIA GPU (optional, for ML workloads)
- Internet connection
- AIAI-compatible runtime environment

## Documentation

See the `docs/` directory for comprehensive installation guides and troubleshooting information. 