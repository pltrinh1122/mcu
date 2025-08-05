# S3. Storage Partitioning

**Document**: Ubuntu BTRFS Installation Guide  
**Section**: S3 - Storage Partitioning  
**Document Version**: 5.3  
**Last Modified**: July 31, 2025

---

## Document Overview

This section provides comprehensive step-by-step procedures for installing Ubuntu 24.04 LTS with the three-partition BTRFS storage strategy optimized for AI/ML development workstations. The installation process implements the storage architecture defined in Section S1 and validated in Section S2.

## Document Structure

This section follows a sequential installation workflow:

1. **S3.1 Process Overview** - Installation context, workflow, and safety considerations
2. **S3.2 Pre-Installation Validation** - Comprehensive system validation using VI framework
3. **S3.3 GUI Installer Launch** - Start Ubuntu installer with network connectivity
4. **S3.4 Manual Partitioning** - Configure three-partition AI/ML storage strategy
5. **S3.5 GUI User Account Configuration** - Create AI/ML optimized user setup
6. **S3.6 GUI Confirm and Execute Installation** - Final verification and installation execution
7. **S3.7 Post-Installation System Boot** - First boot and basic functionality verification
8. **S3.8 Validation Results and Next Steps** - Post-installation validation and next steps

## **Prerequisites**

Complete Section S2 (Prerequisites & Verification) with either "SYSTEM OPTIMAL" or "SYSTEM ADEQUATE" status before proceeding.

---

## S3.1 Process Overview

### S3.1.1 Installation Context

**Starting Point**: Terminal session from Ubuntu 24.04 LTS USB boot environment (completed Section S2)

**Installation Approach**: GUI-based Ubuntu installer with manual partitioning for AI/ML optimization

**Expected Duration**: 45-60 minutes total (15 minutes configuration + 30-45 minutes installation)

### S3.1.2 Installation Workflow

The installation follows this structured sequence:

1. **Pre-Installation Validation** - Comprehensive safety and compatibility checks
2. **GUI Installer Launch** - Start Ubuntu installer with network connectivity
3. **Manual Partitioning** - Configure three-partition AI/ML storage strategy
4. **User Account Setup** - Create AI/ML optimized user configuration
5. **Installation Execution** - Execute destructive installation process
6. **System Boot** - First boot and basic functionality verification
7. **Post-Installation Validation** - Comprehensive system validation

### S3.1.3 Critical Safety Overview

**Destructive Operations**: This installation will permanently erase all data on the target disk

**Safety Checkpoints**:

- Pre-installation validation with comprehensive system checks
- Manual verification of partition configuration before execution
- Post-installation validation to confirm successful deployment

**Recovery Preparation**: Ensure important data is backed up and Ubuntu USB is available for emergency recovery

## S3.2 Pre-Installation Validation

### S3.2.1 Overview

**Purpose**: Comprehensive system validation before launching the GUI installer

**Context**: Execute from Ubuntu Live USB terminal environment after completing Section S2

**Expected Duration**: 5-10 minutes

### S3.2.2 Execute Pre-Installation Validation

**MANDATORY**: Run the comprehensive pre-installation validation using the Verified Installer framework:

**Framework Reference**: See **[VERIFIED_INSTALLER.md](VERIFIED_INSTALLER.md)** for complete documentation.

**Execution Commands**:

```bash
# Execute pre-installation validation using VI framework
sudo ./verified_installer.sh ../src/btrfs_system_validation_viScript.json --verbose

# Save validation report
sudo ./verified_installer.sh ../src/btrfs_system_validation_viScript.json > ~/S3_2_validation.txt
```

### S3.2.3 Validation Requirements

**Proceed to S3.3 only if the VI framework shows**:

- **STATUS: SUCCESS** or **SYSTEM OPTIMAL**
- **Zero critical errors detected**
- **All FAIL items resolved**

**Key validation areas**:

- Ubuntu 24.04 LTS environment confirmed
- Target disk identified and adequate capacity
- UEFI boot mode active
- BTRFS kernel support available
- Adequate system memory (30GB+ recommended)
- NVIDIA GPU detected
- Internet connectivity functional
- Planned partition layout verified

**If validation fails**:

1. Resolve all FAIL status items identified in the VI output
2. Re-run the validation: `sudo ./verified_installer.sh ../src/btrfs_system_validation_viScript.json --verbose`
3. Do not proceed until validation passes completely

**Validation report saved to**: `~/S3_2_validation.txt`

## S3.3 Launch GUI Installer and Configure

### S3.3.1 Start Ubuntu Installer

**Launch the graphical Ubuntu installer**:

```bash
# Launch Ubuntu installer from terminal
sudo ubiquity --desktop &

# Alternative method if ubiquity is not available
sudo ubuntu-desktop-installer &

# Wait for GUI installer to load
echo "Ubuntu installer launching..."
echo "Proceed with GUI configuration when installer window appears"
```

**Expected Result**: Ubuntu installer GUI window opens with welcome screen

### S3.3.2 Initial Installer Configuration

**Configure these settings in the Ubuntu installer GUI**:

| Setting | Selection | Purpose |
| --- | --- | --- |
| **Language** | English (US) | Maximum ML framework compatibility |
| **Keyboard Layout** | English (US) or appropriate | Match your physical keyboard |
| **WiFi Connection** | Connect to network | Required for drivers and updates |
| **Installation Type** | Interactive installation | Full control over configuration |
| **Updates and Software** | Install third-party software | **CRITICAL** - NVIDIA driver support |
| **Download Updates** | Download updates while installing | Latest kernel and security patches |

**CRITICAL**: Ensure "Install third-party software for graphics and Wi-Fi hardware" is **ENABLED** - this is essential for NVIDIA GPU support.

### S3.3.3 Pre-Partitioning Configuration Check

**Before proceeding to partitioning, verify**:

- Network connection is active and stable
- Third-party software installation is enabled
- Installer is ready for manual partitioning configuration

## S3.4 GUI Manual Partitioning

### S3.4.1 Select Manual Partitioning

**In the Ubuntu installer**:

1. **Installation type screen**: Select "Something else"
2. **Reason**: Enable manual partition configuration for AI/ML optimization
3. **Click "Continue"** to proceed to partition editor

### S3.4.2 Create Partition Layout

**Configure partitions in this exact sequence using the GUI partition editor**:

### S3.4.2.1 Create EFI System Partition (automatic)

- **Select device for boot loader installation**: Select `/dev/nvme0n1` (entire disk)
- **CRITICAL**: Do NOT select a partition like `/dev/nvme0n1p1`
- **Review and accept default**
  - **Size**: `1024 MB`
  - **Use as**: `EFI System Partition`
  - **Mount point**: `/boot/efi`
  - **Format the partition**: `Checked`
- **Click "OK"**

### S3.4.2.2 Create Swap Partition

- **Select free space and Click "+" to add partition**
  - **Size**: `65536 MB` (64GB) or adjust per validation script recommendation
  - **Use as**: `swap area`
- **Click "OK"**

### S3.4.2.3 Create System Root Partition (BTRFS)

- **Select free space and Click "+" to add partition**
  - **Size**: `204800 MB` (200GB)
  - **Use as**: `btrfs journaling file system`
  - **Mount point**: `/`
  - **Format the partition**: `Checked`
- **Click "OK"**

### S3.4.2.4 Create AI/ML Development Partition (BTRFS)

- **Select free space and Click "+" to add partition**
  - **Size**: `512000 MB` (500GB)
  - **Use as**: `btrfs journaling file system`
  - **Mount point**: `/ml`
  - **Format the partition**: `Checked`
- **Click "OK"**

### S3.4.2.5 Create Training Data Partition (EXT4)

- **Select free space and Click "+" to add partition**
  - **Size**: Use remaining space (leave size field empty or enter maximum)
  - **Use as**: `Ext4 journaling file system`
  - **Mount point**: `/data`
  - **Format the partition**: `Checked`
- **Click "OK"**

### S3.4.4 Partition Configuration Verification

**Before proceeding, verify the partition table shows**:

| Device | Size | Type | Mount Point | Format |
| --- | --- | --- | --- | --- |
| `/dev/nvme0n1p1` | 1GB | EFI System | `/boot/efi` | ✓ |
| `/dev/nvme0n1p2` | 64GB | swap | swap |  |
| `/dev/nvme0n1p3` | 200GB | btrfs | `/` | ✓ |
| `/dev/nvme0n1p4` | 500GB | btrfs | `/ml` | ✓ |
| `/dev/nvme0n1p5` | ~1.2TB | ext4 | `/data` | ✓ |

**STOP**: Do not click "Install Now" until all partitions are correctly configured and verified.

## S3.5 GUI User Account Configuration

### S3.5.1 User Account Settings

**Configure user account for AI/ML development**:

| Field | Recommendation | Example |
| --- | --- | --- |
| **Your name** | Full name | AI ML Developer |
| **Your computer's name** | Descriptive hostname | ml-workstation or lora-dev |
| **Pick a username** | Short, lowercase, no spaces | aidev, mluser, trainer |
| **Choose a password** | Strong password | Use password manager |
| **Confirm password** | Match above | - |

### S3.5.2 Login Configuration

**Security settings**:

| Setting | Recommendation | Rationale |
| --- | --- | --- |
| **Require password to log in** | **SELECTED** | Security for valuable research data |
| **Log in automatically** | **NOT SELECTED** | Manual login provides security layer |

### S3.5.3 Username Guidelines for AI/ML

**Best practices for username selection**:

- **Keep it short**: Reduces path lengths in ML project directories
- **Use lowercase**: Ensures compatibility with command-line tools
- **No spaces or special characters**: Prevents shell scripting issues
- **Make it descriptive**: Helps identify purpose (aidev, mlresearch, trainer)

**Good examples**: `aidev`, `mluser`, `trainer`, `researcher`, `lora`**Avoid**: `ai user`, `ML-Dev`, `user123`, `admin`

## S3.6 GUI Confirm and Execute Installation

### S3.6.1 Installation Summary Review

**The Ubuntu installer will display a final installation summary screen. Carefully review all settings before proceeding.**

**Expected Installation Summary Display**:

```bash
Installation Summary
====================

Ubuntu 24.04 LTS will be installed to:
  /dev/nvme0n1

The following partitions will be created:
  /dev/nvme0n1p1  1GB     EFI System Partition  /boot/efi
  /dev/nvme0n1p2  64GB    Linux swap            swap
  /dev/nvme0n1p3  200GB   btrfs                 /
  /dev/nvme0n1p4  500GB   btrfs                 /ml
  /dev/nvme0n1p5  ~1.2TB  ext4                  /data

Additional software:
  ☑ Install third-party software
  ☑ Download updates while installing

User account:
  Username: [your-username]
  Computer name: [your-hostname]
```

### S3.6.2 Critical Final Verification Checklist

**Before clicking "Install Now," verify each item in the installer**:

| Configuration Item | Expected Value | Status |
| --- | --- | --- |
| **Installation Target** | `/dev/nvme0n1` (entire disk) | [ ] ✓ VERIFIED |
| **Partition Count** | 5 partitions total | [ ] ✓ VERIFIED |
| **EFI Partition** | 1GB, `/boot/efi`, EFI System | [ ] ✓ VERIFIED |
| **Swap Partition** | 32-64GB, swap area | [ ] ✓ VERIFIED |
| **Root Partition** | 200GB, btrfs, `/` | [ ] ✓ VERIFIED |
| **ML Partition** | 500GB, btrfs, `/ml` | [ ] ✓ VERIFIED |
| **Data Partition** | Remaining space, ext4, `/data` | [ ] ✓ VERIFIED |
| **Format All Partitions** | All partitions will be formatted | [ ] ✓ VERIFIED |
| **Third-party Software** | Enabled (for NVIDIA drivers) | [ ] ✓ VERIFIED |
| **Download Updates** | Enabled | [ ] ✓ VERIFIED |
| **User Account** | Configured correctly | [ ] ✓ VERIFIED |

### S3.6.3 Final Safety Confirmation

**CRITICAL SAFETY REMINDER**: This is your last opportunity to cancel before data destruction begins.

**Confirm these safety requirements**:

- [ ]  **Important data is backed up** to external storage
- [ ]  **Backup has been tested** and is accessible
- [ ]  **This is the correct target disk** (`/dev/nvme0n1`)
- [ ]  **You understand all data will be permanently erased**
- [ ]  **Ubuntu USB is available** for emergency recovery if needed

### S3.6.4 Execute Installation

**Only proceed if all verification items are checked**:

1. **Final Review**: One last look at the installation summary
2. **Click "Install Now"** in the Ubuntu installer GUI
3. **Partition Warning Dialog**: The installer will show a final warning about partition changes
4. **Click "Continue"** to confirm partition changes
    - **WARNING: POINT OF NO RETURN**: Data destruction begins immediately
    - **Cannot be undone** once this confirmation is given

### S3.6.5 Installation Progress Monitoring

**Monitor installation progress through the GUI (30-45 minutes)**:

The Ubuntu installer will display progress through these phases:

| Phase | Expected Duration | What's Happening |
| --- | --- | --- |
| **Creating Partitions** | 2-3 minutes | Formatting disk and creating partition table |
| **Installing Base System** | 10-15 minutes | Core Ubuntu packages and kernel |
| **Installing Third-party Software** | 5-10 minutes | NVIDIA drivers and proprietary components |
| **Installing Additional Packages** | 15-20 minutes | Complete package installation |
| **Final Configuration** | 3-5 minutes | System setup and cleanup |

**During Installation**:

- **Stay near the computer**: Installation may prompt for additional input
- **Do not power off** or disconnect the system
- **Do not remove USB** until installation completes
- **Monitor for error messages** and note any issues

**Installation Slideshow**: Ubuntu will display information about features and capabilities during installation.

## S3.7 Post-Installation System Boot

### S3.7.1 Installation Completion

**When installation completes**:

1. **Remove installation media**: Ubuntu installer will prompt to remove USB
2. **Click "Restart Now"** to reboot system
3. **Remove USB drive** when prompted
4. **System reboots** from NVMe drive

### S3.7.2 First Boot Sequence

**Expected boot process**:

1. **UEFI firmware** loads and detects Ubuntu bootloader
2. **GRUB bootloader** appears with Ubuntu option selected
3. **Ubuntu kernel** loads with BTRFS and EXT4 support
4. **Login screen** appears for user account

### S3.7.3 Initial Login

**Log in to system**:

1. **Enter username** created during installation
2. **Enter password**
3. **Desktop environment loads** (Ubuntu with GNOME)
4. **Verify basic functionality** before proceeding to validation

### S3.7.4 Post-Installation Validation

**Execute comprehensive post-installation validation using the Verified Installer framework**:

```bash
# Execute post-installation validation using VI framework
sudo ./verified_installer.sh ../src/btrfs_post_installation_validation_viScript.json --verbose

# Save validation report
sudo ./verified_installer.sh ../src/btrfs_post_installation_validation_viScript.json > ~/S3_7_validation.txt
```

**This validation includes**:

- Ubuntu version and system information verification
- All partition mount verification (EFI, Root BTRFS, ML BTRFS, Data EXT4)
- Filesystem health verification (BTRFS and EXT4)
- Hardware detection (NVIDIA GPU, network interfaces)
- Network connectivity and repository access
- User permissions on ML and data directories
- BTRFS subvolume and compression functionality testing
- VI framework self-testing

## S3.8 Validation Results and Next Steps

### S3.8.1 Validation Requirements

**Proceed to Section S4 only if the VI framework shows**:

- **STATUS: SUCCESS** or **INSTALLATION SUCCESSFUL**
- **Zero critical errors detected**
- **All core systems operational**

**Key validation areas**:

- Ubuntu 24.04 LTS installation confirmed
- All partition mounts correct (EFI, Root BTRFS, ML BTRFS, Data EXT4)
- Swap partition active
- BTRFS and EXT4 filesystem health verified
- EFI boot system functional
- NVIDIA GPU detected
- Network connectivity working
- User permissions correct for ML and data directories
- BTRFS subvolume functionality operational

### S3.8.2 Troubleshooting Installation Issues

Refer to [UBUNTU-BTRFS_TROUBLESHOOTING.md](UBUNTU-BTRFS_TROUBLESHOOTING.md).

### S3.8.3 Next Steps

After successful installation verification:

1. **Save validation report** (`~/S3_7_validation.txt`) for future reference
2. **Document any warnings** for future attention
3. **Proceed to Section S4**: System BTRFS Subvolume Setup
4. **Continue to Section S5**: AI/ML BTRFS Environment Setup
5. **Configure Section S6**: Data Partition Setup

**CRITICAL**: Do not skip the subvolume configuration sections - they are essential for the AI/ML workflow integration.

---

**Installation Complete**: System is ready for AI/ML environment configuration. Proceed to **Section S4: System BTRFS Subvolume Setup** to configure the snapshot and versioning capabilities required for LoRA training workflows.
