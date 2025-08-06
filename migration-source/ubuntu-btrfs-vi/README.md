# Ubuntu BTRFS viScript Installer

## Overview

The Ubuntu BTRFS viScript Installer module provides a comprehensive system for installing Ubuntu 24.04 LTS with BTRFS filesystem optimized for AI/ML development workstations using the viScript framework.

## Module Structure

```
ubuntu-btrfs-vi/
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
│   └── viScript/           # viScript files
│       └── *_viScript.json
└── unit-tests/             # Unit tests (future)
```

## Key Features

- **Three-Partition Strategy**: System, ML, and Data partitions
- **BTRFS Optimization**: Copy-on-write filesystem with snapshots
- **AI/ML Focus**: Optimized for machine learning workloads
- **Comprehensive Documentation**: Step-by-step installation guide
- **Validation Scripts**: Pre and post-installation verification
- **viScript Framework**: JSON-based verification and installation scripts

## Installation Process

1. **System Validation** (S2): Hardware and environment checks
2. **Storage Partitioning** (S3): Disk partitioning strategy
3. **System Subvolume Setup** (S4): BTRFS subvolume creation
4. **ML Subvolume Setup** (S5): Machine learning partition
5. **Data Partition Setup** (S6): Data storage configuration
6. **GRUB Setup** (S7): Bootloader configuration

## viScript Format

- **Location**: `src/viScript/`
- **Format**: JSON files following viScript schema
- **Usage**: Compatible with VI framework
- **Purpose**: Traditional verification and installation scripts
- **Features**: 
  - JSON-based configuration
  - Schema validation
  - Batch execution
  - Comprehensive logging

## Usage

```bash
# Run system validation (viScript format)
sudo ./vi/src/verified_installer.sh src/viScript/btrfs_system_validation_viScript.json

# Validate viScript files
./viscriptlint/src/viscriptlint.sh src/viScript/btrfs_system_validation_viScript.json
```

## Dependencies

- Ubuntu 24.04 LTS Live USB
- UEFI boot mode
- Minimum 16GB RAM
- NVIDIA GPU (optional, for ML workloads)
- Internet connection
- VI framework and viscriptlint tools

## Documentation

See the `docs/` directory for comprehensive installation guides and troubleshooting information. 