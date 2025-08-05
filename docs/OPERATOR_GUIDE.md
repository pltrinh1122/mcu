# Ubuntu-BTRFS AIAI Package Operator Guide

**Document Version:** 1.0  
**Last Modified:** January 2025

---

## Installation Overview

This AIAI Package provides a complete, self-contained installation solution for Ubuntu 24.04 LTS with a three-partition BTRFS strategy optimized for AI/ML development workstations. The configuration separates system management, development environments, and large dataset storage for maximum flexibility and performance.

The installation uses the AIAI (AI Augmented Installation) framework, where the AI Agent handles package validation, script execution, and operator guidance while maintaining human control over all critical decisions.

## Prerequisites

### System Requirements

**Hardware Requirements:**
- **Storage**: 2TB NVMe SSD (minimum 1.5TB)
- **Memory**: 64GB RAM (minimum 32GB)
- **GPU**: NVIDIA RTX 3070 or better (RTX 3080+ recommended)
- **CPU**: 8+ cores recommended
- **Network**: Internet connectivity for package downloads

**Software Requirements:**
- Ubuntu 24.04 LTS Live Boot USB
- UEFI boot mode enabled
- BTRFS kernel support
- Internet connectivity during installation

### Pre-Installation Setup

1. **Create Live Boot USB**: Download Ubuntu 24.04 LTS and create bootable USB
2. **Backup Data**: Ensure all important data is backed up
3. **Disable Secure Boot**: Temporarily disable Secure Boot in BIOS if needed
4. **Prepare Target System**: Boot from USB and verify hardware detection

## Quick Start Guide

### AIAI Package Installation

1. **Ensure Package Completeness**: Verify all components are present using the MANIFEST file
2. **Execute AIAI Package**: Provide the following prompt to your AI Agent:

```
Assume the role of the AI Agent and execute the installation package located at [PACKAGE_PATH]. Load the package, validate its structure, and execute the installation following the AIAI Specification. Execute shell commands directly with my permission and capture all console output (stdout and stderr) to ubuntu_btrfs_installation.txt in the current directory.
```

3. **Replace Placeholders**: 
   - Replace `[PACKAGE_PATH]` with the filesystem path to the Ubuntu-BTRFS AIAI Package directory
4. **Monitor Execution**: The AI Agent will automatically:
   - Load and validate the package using the MANIFEST file
   - Parse the AIAI Specification and Schema
   - Identify the main installation script
   - Execute the installation with operator oversight
   - Capture all output to `ubuntu_btrfs_installation.txt`

### Package Validation

The AI Agent validates the package structure before beginning installation:
- **MANIFEST file** must exist and list all components
- **All required files** must be present in the package
- **AIAI Scripts** must validate against the schema
- **Cross-references** must be resolvable within the package

If any validation fails, the installation will abort and the AI Agent will inform you of the issue.

## Storage Strategy and Architecture

### Three-Partition Storage Strategy

**Partition Layout:**
| Device | Size | Type | Mount Point | Strategic Purpose |
| --- | --- | --- | --- | --- |
| nvme0n1p1 | 1G | FAT32 | /boot/efi | System boot requirements |
| nvme0n1p2 | 64G | swap | [swap] | Memory overflow & hibernation |
| nvme0n1p3 | 200G | BTRFS | / | System with snapshot capability |
| nvme0n1p4 | 500G | BTRFS | /ml | Active AI/ML development workspace |
| nvme0n1p5 | 1.2T | EXT4 | /data | Training data & archive storage |

### Strategic Design Principles

**Separation of Concerns**: Isolate system stability, active development, and data archival into distinct storage domains with appropriate technologies.

**Performance Optimization**: Match filesystem characteristics to data access patterns - snapshots for development, high-throughput for datasets.

**Workflow Integration**: Support complete AI/ML experiment lifecycle from data preparation through model archival.

### BTRFS Subvolume Strategy

**System Partition Subvolumes:**
- `@` - Root filesystem (included in snapshots)
- `@home` - User home directories (independent snapshots)
- `@var-log` - System logs (excluded from snapshots)
- `@var-cache` - Cache data (excluded from snapshots)
- `@var-tmp` - Temporary files (excluded from snapshots)
- `@var-spool` - Mail/print queues (excluded from snapshots)
- `@var-backups` - System backup files (excluded from snapshots)
- `@snapshots` - System snapshots (excluded from snapshots)

**ML Partition Subvolumes:**
- `@ml` - ML development environment (included in snapshots)
- `@ml-docker` - Docker containers (excluded from snapshots)
- `@ml-projects` - ML projects and experiments (included in snapshots)
- `@ml-services` - ML services and configurations (included in snapshots)
- `@ml-models` - AI models and checkpoints (included in snapshots)
- `@ml-snapshots` - ML snapshots (excluded from snapshots)

## Detailed Installation Procedures

### Phase 1: System Validation

The installation begins with comprehensive system validation to ensure all prerequisites are met:

**Validation Checks:**
- Live boot environment detection
- Target disk identification and capacity verification
- UEFI boot mode confirmation
- BTRFS kernel support verification
- Memory capacity assessment
- NVIDIA GPU detection
- Internet connectivity testing

**Critical Failures** (Must be resolved before proceeding):
- Not running from live boot environment
- Target disk not detected or insufficient capacity
- System not in UEFI mode
- BTRFS kernel support missing
- RAM below minimum requirements
- No compatible NVIDIA GPU found
- No internet connectivity

### Phase 2: Storage Partitioning

**Three-Partition Strategy:**
1. **System Partition** (200GB): Ubuntu OS and applications
2. **ML Partition** (500GB): AI/ML development environments
3. **Data Partition** (1200GB): Large datasets and model storage

**Partition Layout:**
- EFI: 1GB (FAT32)
- System: 200GB (BTRFS)
- ML: 500GB (BTRFS)
- Data: 1200GB (BTRFS)
- Swap: 64GB (Linux swap)

### Phase 3: BTRFS Subvolume Setup

**System Subvolumes:**
- `@` - Root filesystem
- `@home` - User home directories
- `@var` - Variable data
- `@tmp` - Temporary files
- `@snapshots` - System snapshots

**ML Subvolumes:**
- `@ml` - ML development environment
- `@models` - AI model storage
- `@datasets` - Training datasets
- `@cache` - ML framework caches

### Phase 4: Mount Configuration

**Mount Points:**
- `/` - System root (BTRFS subvolume @)
- `/home` - User directories (BTRFS subvolume @home)
- `/ml` - ML development environment (BTRFS subvolume @ml)
- `/data` - Large datasets (BTRFS subvolume @datasets)

### Phase 5: Boot Configuration

**GRUB Setup:**
- Install GRUB to EFI partition
- Configure BTRFS root detection
- Set up kernel parameters for BTRFS
- Enable subvolume mounting

### Phase 6: AI/ML Environment Setup

**Docker Configuration:**
- Install Docker with NVIDIA runtime
- Configure GPU passthrough
- Set up ML development containers
- Configure volume mounts for datasets

**ML Framework Installation:**
- PyTorch with CUDA support
- TensorFlow with GPU acceleration
- Hugging Face Transformers
- Stable Diffusion toolchain

### Phase 7: Data Migration

**Dataset Organization:**
- Structured dataset storage
- Model version management
- Training artifact organization
- Backup and snapshot strategies

## System Validation and Troubleshooting

### Understanding Validation Results

**Validation Output**: The system validation aiaiScript provides detailed hardware and environment checks with specific output patterns.

**Key Validation Patterns**:

**Critical Failures** (Must be resolved before proceeding):
- `live_boot_detection` fails - Not running from live boot environment
- `target_disk_found` missing - Target disk not detected
- `insufficient_capacity` - Disk capacity below 1.5TB
- `uefi_mode` missing - System not in UEFI mode
- `btrfs_not_supported` - BTRFS kernel support missing
- `insufficient_memory` - RAM below 30GB
- `No NVIDIA GPU detected` - No compatible GPU found
- `no_internet` - No internet connectivity

**Success Indicators**:
- `live_boot_detected` - Running from live boot environment
- `ubuntu_24_04` - Correct Ubuntu version
- `target_disk_found` - Target disk detected
- `sufficient_capacity` - Disk capacity adequate
- `uefi_mode` - UEFI boot mode active
- `btrfs_supported` - BTRFS support available
- `optimal_memory` or `adequate_memory` - RAM sufficient
- `NVIDIA` - Compatible GPU detected
- `internet_available` - Internet connectivity confirmed

**Manual Assessment Required**:
After validation completes, manually assess your system based on the output patterns:
- **All critical checks pass** → Proceed to installation
- **Some critical failures** → Resolve issues before proceeding
- **Warnings present** → Consider addressing for optimal performance

### Critical Error Resolution

**Boot Mode Error (BIOS/Legacy detected)**:
- **Cause**: System booting in BIOS/Legacy mode
- **Solution**: Access BIOS setup, enable UEFI mode, disable CSM/Legacy support
- **Verification**: Reboot from USB and re-run validation

**BTRFS Support Missing**:
- **Cause**: Kernel lacks BTRFS support
- **Solution**: Verify Ubuntu 24.04 LTS installation media integrity
- **Alternative**: Re-download ISO and recreate installation USB

**Storage Insufficient**:
- **Cause**: Less than 1.5TB available storage
- **Solution**: Install larger NVMe SSD (2TB+ recommended)
- **Alternative**: External storage for datasets (reduced performance)

**GPU Missing**:
- **Cause**: No NVIDIA GPU detected
- **Solution**: Install compatible NVIDIA GPU (RTX 3070+ recommended)
- **Alternative**: CPU-only workflows (severely limited)

**Memory Insufficient**:
- **Cause**: Less than 32GB RAM
- **Solution**: Upgrade to 64GB+ RAM
- **Alternative**: Reduced workflow capabilities

**Network Issues**:
- **Cause**: No internet connectivity
- **Solution**: Configure network settings, check cables
- **Alternative**: Manual driver installation (advanced)

## Hardware Configuration Adjustments

### Storage Adjustments (1.5TB - 2TB systems)

**Partition Size Adjustments**:

| Standard (2TB) | Adjusted (1.5TB) | Purpose |
| --- | --- | --- |
| Data: 1200GB | Data: 700GB | Reduced dataset storage |
| ML: 500GB | ML: 400GB | Smaller development space |
| System: 200GB | System: 150GB | Minimal system |
| Swap: 64GB | Swap: 32GB | Matches reduced RAM scenarios |
| EFI: 1GB | EFI: 1GB | Unchanged |

**Installation Modifications**:
- Use adjusted partition sizes during installation
- Prioritize essential base models only
- Implement aggressive cleanup policies

### Memory Adjustments (32GB - 48GB systems)

**Configuration Changes**:

| Component | Standard (64GB) | Adjusted (32-48GB) |
| --- | --- | --- |
| **Swap Size** | 64GB | 16-32GB |
| **Docker Memory** | 16GB limit | 8GB limit |
| **Batch Sizes** | 4-8 images | 1-2 images |
| **Model Loading** | Multiple models | Single model |

**Section Modifications**:
- Reduce swap partition size during installation
- Add Docker memory limits
- Implement gradient checkpointing for training workflows

### GPU Adjustments (RTX 3060/3070 class)

**Training Optimizations**:

| Setting | Optimal GPU | Limited GPU |
| --- | --- | --- |
| **Model Focus** | SDXL, Flux | SD1.5 primarily |
| **Batch Size** | 4-8 | 1-2 |
| **Resolution** | 1024x1024 | 512x512 |
| **Precision** | Mixed (fp16) | fp32 → fp16 |

**Workflow Adjustments**:
- Focus on SD1.5 models (lower VRAM requirements)
- Use gradient accumulation instead of large batches
- Implement model offloading techniques

### Network Adjustments (Limited connectivity)

**Offline Preparation**:
- Download base models before installation
- Prepare offline package cache
- Use local package mirrors

**Installation Modifications**:
- Skip online updates during installation
- Manual driver installation post-setup
- Local repository setup

## Hardware Upgrade Recommendations

### Priority Upgrade Path

**For systems with multiple limitations**:

1. **Memory upgrade** (32GB → 64GB) - $200-400
2. **GPU upgrade** (RTX 3060 → RTX 3080+) - $600-1200  
3. **Storage upgrade** (1.5TB → 2TB+) - $200-400

### Budget-Conscious Alternatives

**No Upgrade Path**:
- Focus on SD1.5 models exclusively
- Use cloud compute for large experiments
- Implement aggressive model pruning

## Troubleshooting

### Common Issues

**Mount Issues:**
```bash
# Check fstab configuration
sudo mount -a

# Manual mount test
sudo mount -t btrfs /dev/nvme0n1p4 /ml
```

**Permission Issues:**
```bash
# Fix ownership
sudo chown $USER:$USER /ml /data

# Fix permissions
sudo chmod 755 /ml /data
```

**BTRFS Problems:**
```bash
# Install tools
sudo apt install btrfs-progs

# Load kernel module
sudo modprobe btrfs
```

**EFI Boot Issues:**
```bash
# Reinstall GRUB
sudo grub-install /dev/nvme0n1

# Update configuration
sudo update-grub
```

### UEFI Boot Problems

**Symptoms**: System fails to boot, GRUB not found

**Solution**:
```bash
# Boot from USB rescue mode
sudo mount /dev/nvme0n1p3 /mnt
sudo mount /dev/nvme0n1p1 /mnt/boot/efi
sudo grub-install --target=x86_64-efi --efi-directory=/mnt/boot/efi --bootloader-id=ubuntu /dev/nvme0n1
```

### Partition Size Errors

**Symptoms**: Insufficient space warnings during installation

**Solution**: Verify partition sizes match the planned layout:
- Reduce other partitions if necessary
- Ensure 2TB total capacity is correctly detected

### NVIDIA Driver Issues

**Symptoms**: GPU not detected, graphics problems

**Solution**: Nvidia drivers will be properly configured in later sections

**Temporary**: Use open-source drivers until proprietary drivers are installed

## Validation Procedures

### Pre-Reboot Validation

**System Checks:**
- BTRFS filesystem integrity
- Mount point configuration
- GRUB boot configuration
- User account setup
- Network connectivity

### Post-Installation Validation

**Environment Verification:**
- Docker container functionality
- GPU acceleration testing
- ML framework installation
- Dataset access verification
- Performance benchmarking

## Post-Installation Configuration

### Performance Optimization

**System Tuning:**
- Enable BTRFS compression
- Configure swap optimization
- Set up automatic snapshots
- Optimize Docker storage driver

**ML Environment Setup:**
- Configure model caching
- Set up dataset versioning
- Enable automatic backups
- Configure monitoring tools

### Security Considerations

**Access Control:**
- Configure user permissions
- Set up SSH key authentication
- Enable firewall rules
- Configure backup encryption

**Data Protection:**
- Implement regular snapshots
- Set up offsite backups
- Configure data encryption
- Monitor system integrity

## Error Recovery

### Rollback Procedures

**System Rollback:**
- Use BTRFS snapshots for system recovery
- Restore from previous system state
- Recover user data from snapshots
- Reinstall if necessary

**Data Recovery:**
- Restore from backup snapshots
- Recover from external backups
- Use data integrity checks
- Rebuild datasets if needed

### Manual Intervention

**When AI Agent Cannot Proceed:**
- Assess the specific error condition
- Consult troubleshooting section
- Perform manual recovery steps
- Resume with AI Agent when possible

## Legacy Installation Support

### Manual Installation (Non-AIAI)

For systems that cannot use the AIAI Package approach:

1. **Follow Manual Sequence**:
   - Execute individual aiaiScript files in order
   - `src/aiaiScript/btrfs_root_aiaiScript.yaml`
   - `src/aiaiScript/btrfs_system_subvolume_creation_aiaiScript.yaml`
   - `src/aiaiScript/btrfs_mount_configuration_aiaiScript.yaml`
   - `src/aiaiScript/btrfs_boot_configuration_aiaiScript.yaml`
   - `src/aiaiScript/btrfs_ml_aiaiScript.yaml`
   - `src/aiaiScript/btrfs_data_aiaiScript.yaml`

2. **Manual Validation**:
   - Run system validation scripts manually
   - Verify each step before proceeding
   - Document any deviations from standard procedures

## Version History

- **v1.0** - Initial AIAI Package release with complete self-contained installation solution
- **v6.x** - AIAI Package approach with comprehensive AI/ML optimization
- **v5.x** - aiaiScript schema and validation framework
- **v4.x** - Enhanced BTRFS subvolume management
- **v3.x** - Improved validation and error handling
- **v2.x** - Basic BTRFS setup and configuration

---

*This document serves as the comprehensive operator guide for the Ubuntu BTRFS AIAI Package. All installation procedures are designed to work with the AIAI framework for safe, guided installation execution.* 