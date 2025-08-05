# Ubuntu-BTRFS Troubleshooting

**Document**: Ubuntu-BTRFS Troubleshooting

**Section:** N/A

**Document Version:** 2.x

**Last Modified:** August 1, 2025

---

## Document Purpose

Troubleshoot issues with Ubuntu-BTRFS Installation for AI/ML per the document: [UBUNTU_BTRFS_INSTALLER.md](UBUNTU_BTRFS_INSTALLER.md)

## Intended Audience

- System administrators implementing AI/ML development environments
- DevOps engineers managing machine learning infrastructure
- AI/ML researchers requiring robust development workflows
- Technical users with intermediate to advanced Linux system administration experience

## Document Structure

- Each section should be read and executed in the sequence presented below.
- Versioning standard:
  - Major version (1.x) updated when changes cascades to across sections.
  - Minor version (x.1) updated per iteration of individual sections.

---

## S1 Troubleshooting Common Issues

**Mount Issues:**

- Check `/etc/fstab` configuration: `sudo mount -a`
- Manual mount test: `sudo mount -t btrfs /dev/nvme0n1p4 /ml`

**Permission Issues:**

- Fix ownership: `sudo chown $USER:$USER /ml /data`
- Fix permissions: `sudo chmod 755 /ml /data`

**BTRFS Problems:**

- Install tools: `sudo apt install btrfs-progs`
- Load kernel module: `sudo modprobe btrfs`

**EFI Boot Issues:**

- Reinstall GRUB: `sudo grub-install /dev/nvme0n1`
- Update configuration: `sudo update-grub`

### S2 Common Installation Issues

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

### Installation Validation Checklist

## S3 System Validation Troubleshooting

### S3.1 Understanding Validation Results

**Validation Output**: The system validation viScript provides detailed hardware and environment checks with specific output patterns.

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
- **All critical checks pass** → Proceed to Section S3
- **Some critical failures** → Resolve issues before proceeding
- **Warnings present** → Consider addressing for optimal performance

### S3.2 Critical Error Resolution

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

### S3.3 Configuration Adjustments

#### S3.3.1 Storage Adjustments (1.5TB - 2TB systems)

**Partition Size Adjustments**:

| Standard (2TB) | Adjusted (1.5TB) | Purpose |
| --- | --- | --- |
| Data: 1200GB | Data: 700GB | Reduced dataset storage |
| ML: 500GB | ML: 400GB | Smaller development space |
| System: 200GB | System: 150GB | Minimal system |
| Swap: 64GB | Swap: 32GB | Matches reduced RAM scenarios |
| EFI: 1GB | EFI: 1GB | Unchanged |

**Installation Modifications**:

- In Section S3.3, use adjusted partition sizes
- Prioritize essential base models only
- Implement aggressive cleanup policies

#### S3.3.2 Memory Adjustments (32GB - 48GB systems)

**Configuration Changes**:

| Component | Standard (64GB) | Adjusted (32-48GB) |
| --- | --- | --- |
| **Swap Size** | 64GB | 16-32GB |
| **Docker Memory** | 16GB limit | 8GB limit |
| **Batch Sizes** | 4-8 images | 1-2 images |
| **Model Loading** | Multiple models | Single model |

**Section Modifications**:

- **S3.3**: Reduce swap partition size
- **S5**: Add Docker memory limits
- **Training workflows**: Implement gradient checkpointing

#### S3.3.3 GPU Adjustments (RTX 3060/3070 class)

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

#### S3.3.4 Network Adjustments (Limited connectivity)

**Offline Preparation**:

- Download base models before installation
- Prepare offline package cache
- Use local package mirrors

**Installation Modifications**:

- Skip online updates during installation
- Manual driver installation post-setup
- Local repository setup

### S3.4 Hardware Upgrade Recommendations

#### S3.4.1 Priority Upgrade Path

**For systems with multiple limitations**:

1. **Memory upgrade** (32GB → 64GB) - $200-400
2. **GPU upgrade** (RTX 3060 → RTX 3080+) - $600-1200  
3. **Storage upgrade** (1.5TB → 2TB+) - $200-400

#### S3.4.2 Budget-Conscious Alternatives

**No Upgrade Path**:
- Focus on SD1.5 models exclusively
- Use cloud compute for large experiments
- Implement aggressive model pruning
