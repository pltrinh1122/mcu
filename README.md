# Ubuntu-BTRFS AIAI Package (Development Version)

## Overview

The Ubuntu-BTRFS AIAI Package provides a complete, self-contained installation solution for Ubuntu 24.04 LTS with a three-partition BTRFS strategy optimized for AI/ML development workstations. This package implements the AIAI (AI Augmented Installation) framework, enabling AI-augmented installation execution with human operator oversight.

**Development Version Note**: This is the development version of the package. The specification files (`aiai_spec.md` and `aiai_schema.json`) are now actual files in the framework. For distribution versions, these will be included as actual files to ensure package independence.

## AIAI Package Structure

```
ubuntu-btrfs-aiai/
├── MANIFEST                       # Package manifest file (required)
├── docs/
│   └── OPERATOR_GUIDE.md          # Main operator documentation
├── src/
│   └── aiaiScript/
│       ├── btrfs_system_validation_aiaiscript.yaml
│       ├── btrfs_root_aiaiScript.yaml
│       ├── btrfs_system_subvolume_creation_aiaiScript.yaml
│       ├── btrfs_mount_configuration_aiaiScript.yaml
│       ├── btrfs_boot_configuration_aiaiScript.yaml
│       ├── btrfs_ml_aiaiScript.yaml
│       ├── btrfs_data_aiaiScript.yaml
│       ├── btrfs_data_migration_aiaiScript.yaml
│       ├── btrfs_pre_reboot_validation_aiaiScript.yaml
│       ├── btrfs_post_installation_validation_aiaiScript.yaml
│       └── docker_aiScript.yaml
├── aiai_spec.md                   # AIAI Specification (this document)
├── aiai_schema.json               # Machine-readable schema definition
└── README.md                      # Package overview and quick start
```

## Key Features

- **Complete AIAI Package**: Self-contained installation solution with all required components
- **Three-Partition Strategy**: System, ML, and Data partitions for optimal organization
- **BTRFS Optimization**: Copy-on-write filesystem with snapshots and compression
- **AI/ML Focus**: Optimized for machine learning workloads and GPU acceleration
- **Human-AI Partnership**: AI guidance with human control over critical decisions
- **Comprehensive Validation**: Pre and post-installation verification procedures
- **Error Recovery**: Built-in rollback mechanisms and troubleshooting procedures

## Installation Process

### AIAI Package Execution

1. **Package Validation**: AI Agent validates package structure using MANIFEST
2. **System Validation**: Hardware and environment prerequisite checks
3. **Storage Partitioning**: Three-partition BTRFS strategy implementation
4. **System Subvolume Setup**: BTRFS subvolume creation and configuration
5. **ML Environment Setup**: AI/ML development environment configuration
6. **Data Partition Setup**: Large dataset storage configuration
7. **Boot Configuration**: GRUB setup and system boot verification
8. **Post-Installation Validation**: Complete system verification and testing

### Execution Command

To execute this AIAI Package, provide the following prompt to your AI Agent:

```
Assume the role of the AI Agent and execute the installation package located at [PACKAGE_PATH]. Load the package, validate its structure, and execute the installation following the AIAI Specification. Execute shell commands directly with my permission and capture all console output (stdout and stderr) to ubuntu_btrfs_installation.txt in the current directory.
```

Replace `[PACKAGE_PATH]` with the filesystem path to the Ubuntu-BTRFS AIAI Package directory.

## System Requirements

### Hardware Requirements
- **Storage**: 2TB NVMe SSD (minimum 1.5TB)
- **Memory**: 64GB RAM (minimum 32GB)
- **GPU**: NVIDIA RTX 3070 or better (RTX 3080+ recommended)
- **CPU**: 8+ cores recommended
- **Network**: Internet connectivity for package downloads

### Software Requirements
- Ubuntu 24.04 LTS Live Boot USB
- UEFI boot mode enabled
- BTRFS kernel support
- Internet connectivity during installation

## Package Components

### Core Components
- **MANIFEST**: Package manifest listing all required files
- **aiai_spec.md**: AIAI Specification defining runtime behavior
- **aiai_schema.json**: Machine-readable schema for script validation
- **docs/OPERATOR_GUIDE.md**: Comprehensive operator documentation

### AIAI Scripts
- **System Validation**: Pre-installation hardware and environment checks
- **Storage Partitioning**: Three-partition BTRFS strategy implementation
- **BTRFS Configuration**: Subvolume creation and mount configuration
- **Boot Setup**: GRUB configuration and system boot verification
- **ML Environment**: AI/ML development environment setup
- **Data Migration**: Dataset organization and storage configuration
- **Validation Scripts**: Pre and post-installation verification

## Development vs Distribution Workflow

### Development Version (Current)
- **Actual Files**: `aiai_spec.md` and `aiai_schema.json` are actual files in the framework
- **Purpose**: Enables rapid development and testing with centralized specification management
- **Benefits**: Direct access to specification files with version control
- **Usage**: Ideal for development, testing, and iterative improvement

### Distribution Version (Future)
- **Actual Files**: `aiai_spec.md` and `aiai_schema.json` are actual files, not soft links
- **Purpose**: Self-contained package for distribution and deployment
- **Benefits**: Package independence, version control, and deployment reliability
- **Usage**: Production deployments, distribution to end users, and version-specific installations

### Conversion Process
When ready for distribution, the files are already actual files:

**Current Status:**
```bash
# Files are already actual files in framework/docs/
ls framework/docs/aiai_spec.md framework/docs/aiai_schema.json
```

**Automated Process:**
```bash
# Use the provided conversion script
./scripts/prepare_distribution.sh
```

## Package Validation

The AI Agent automatically validates the package structure before beginning installation:

- **MANIFEST file** must exist and list all components
- **All required files** must be present in the package
- **AIAI Scripts** must validate against the schema
- **Cross-references** must be resolvable within the package

If any validation fails, the installation will abort and the AI Agent will inform you of the issue.

## Documentation

- **docs/OPERATOR_GUIDE.md**: Complete operator guide with detailed procedures
- **aiai_spec.md**: AIAI Specification for runtime behavior
- **aiai_schema.json**: Machine-readable schema definition

## Version History

- **v1.0** - Initial AIAI Package release with complete self-contained installation solution
- **v6.x** - AIAI Package approach with comprehensive AI/ML optimization
- **v5.x** - aiaiScript schema and validation framework
- **v4.x** - Enhanced BTRFS subvolume management
- **v3.x** - Improved validation and error handling
- **v2.x** - Basic BTRFS setup and configuration

## Dependencies

- Ubuntu 24.04 LTS Live USB
- UEFI boot mode
- Minimum 32GB RAM (64GB recommended)
- NVIDIA GPU (RTX 3070+ recommended for ML workloads)
- Internet connection
- AIAI-compatible runtime environment

---

*This package implements the AIAI (AI Augmented Installation) framework for safe, guided installation execution with human operator oversight.* 