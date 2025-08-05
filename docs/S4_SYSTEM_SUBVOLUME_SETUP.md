# S4. System Subvolume Setup

**Document**: Ubuntu BTRFS Installation Guide
**Section**: S4 - System Subvolume Setup
**Document Version**: 5.10
**Last Modified**: August 1, 2025

---

## 4.1 Document Overview

This document provides comprehensive technical procedures for configuring BTRFS subvolumes on the system partition (/dev/nvme0n1p3) according to the three-partition storage strategy defined in Section S1. The focus is exclusively on system-level subvolume creation, data migration, and boot configuration to enable snapshot-based system management while maintaining clean separation between system state and volatile data.

The procedures transform a standard Ubuntu installation into a BTRFS subvolume-based system that supports atomic snapshots of core system components while excluding ephemeral data that would pollute snapshot storage. This foundation enables reliable system rollback capabilities essential for AI/ML development environments where system stability must be maintained alongside experimental software installations.

## 4.2 Document Structure

This section implements system partition subvolume configuration through eight primary procedures:

1. **System Subvolume Creation** - Establish core subvolumes for system root, user data, variable data, and snapshot storage
2. **Data Migration** - Transfer existing system data into appropriate subvolumes with verification procedures
3. **Mount Configuration** - Configure filesystem table (fstab) for subvolume-based mounting with AI/ML optimized parameters
4. **Boot System Updates** - Modify GRUB and initramfs configuration for BTRFS subvolume boot support
5. **Pre-Reboot Validation** - Comprehensive verification procedures to ensure system integrity before transition
6. **System Verification** - Post-reboot validation of subvolume functionality and snapshot capabilities
7. **Troubleshooting Procedures** - Recovery methods for common subvolume configuration issues
8. **Maintenance Guidelines** - Ongoing subvolume management and snapshot maintenance procedures

**Scope Limitation**: This document addresses only the system partition (/dev/nvme0n1p3). ML partition subvolume configuration (/dev/nvme0n1p4) is covered in Section S5, and data partition setup (/dev/nvme0n1p5) is addressed in Section S6.

## 4.3 Prerequisites

Successfully complete Section S3 before proceeding.

---

## 4.4 Execute Subvolume Creation

To mount the system BTRFS root and create all required subvolumes according to S1 strategy, use the Verified Installer framework:

```bash
# Execute subvolume creation using VI framework
sudo ./verified_installer.sh btrfs_system_subvolume_creation_viScript.json --verbose
```

**Review the creation results above. If all steps passed, proceed to Section 4.5 for data migration (or skip to Section 4.6 for new installations).**

**Critical**: Do not proceed to data migration if any subvolume creation step fails. Address failures before continuing.

**Troubleshooting**: If you encounter failures, refer to **Appendix A: System Subvolume Reference** for detailed output interpretation and subvolume design rationale.

## 4.5 Execute Data Migration (Optional)

**NOTE**: This section is **OPTIONAL** and can be **SKIPPED** for brand new system installations with no existing data to migrate.

**For existing systems**: Migrate system data to appropriate subvolumes using the Verified Installer framework:

```bash
# Execute data migration using VI framework
sudo ./verified_installer.sh btrfs_data_migration_viScript.json --verbose
```

**Review the migration results above. If all steps passed, proceed to Section 4.6 for mount configuration.**

**NOTE**: Migration time depends on existing system data volume. Typical installation requires 10-15 minutes.

**For new installations**: If you skipped this section, proceed directly to Section 4.6.

**Troubleshooting**: If you encounter failures, refer to **Appendix A: System Subvolume Reference** for detailed output interpretation and subvolume design rationale.

## 4.6 Execute Mount Configuration

Create optimized fstab entries for system subvolumes according to S1 strategy using the Verified Installer framework:

```bash
# Execute mount configuration using VI framework
sudo ./verified_installer.sh btrfs_mount_configuration_viScript.json --verbose
```

**Review the configuration results above. If all steps passed, proceed to Section 4.7 for boot configuration.**

**Troubleshooting**: If you encounter failures, refer to **Appendix A: System Subvolume Reference** for detailed output interpretation and subvolume design rationale.



## 4.7 Execute Boot Configuration

Configure GRUB bootloader and initramfs for BTRFS subvolume support using the Verified Installer framework:

```bash
# Execute boot configuration using VI framework
sudo ./verified_installer.sh btrfs_boot_configuration_viScript.json --verbose
```

**Review the configuration results above. If all steps passed, proceed to Section 4.8 for pre-reboot validation.**

**Troubleshooting**: If you encounter failures, refer to **Appendix A: System Subvolume Reference** for detailed output interpretation and subvolume design rationale.

## 4.8 Execute Pre-Reboot Validation

To ensure system integrity before transitioning to BTRFS subvolumes, execute the comprehensive pre-reboot validation using the Verified Installer framework:

```bash
# Execute pre-reboot validation using VI framework
sudo ./verified_installer.sh btrfs_pre_reboot_validation_viScript.json --verbose

# Save validation output for troubleshooting
sudo ./verified_installer.sh btrfs_pre_reboot_validation_viScript.json > ~/S4_8_validation.txt
```

**Review the validation results above. If all checks passed, system is ready for reboot.**

**Troubleshooting**: If you encounter failures, refer to **Appendix A: System Subvolume Reference** for detailed output interpretation and troubleshooting procedures.

## 4.9 System Reboot and Verification

### 4.9.1 Reboot System

**CRITICAL**: Ensure all verification steps pass before rebooting:

```bash
echo "System configuration complete. Preparing for reboot..."
echo "WARNING: System will reboot from BTRFS subvolumes"
echo "Recovery: If boot fails, use Ubuntu live USB to restore from backup"

# Reboot system
sudo reboot
```

### 4.9.2 Post-Reboot Verification Using VI Framework

After successful reboot, execute comprehensive post-installation validation using the Verified Installer framework:

```bash
# Execute post-installation validation using VI framework
sudo ./verified_installer.sh ../src/btrfs_post_installation_validation_viScript.json --verbose

# Save validation report
sudo ./verified_installer.sh ../src/btrfs_post_installation_validation_viScript.json > ~/S4_9_validation.txt
```

**Expected Output**:

```bash
=== Post-Installation Validation ===
SUCCESS: root_btrfs_mount
SUCCESS: ml_btrfs_mount
SUCCESS: data_ext4_mount
SUCCESS: all_partition_mounts_verified
SUCCESS: filesystem_health_verified
SUCCESS: user_permissions_verified
SUCCESS: btrfs_subvolume_functionality
SUCCESS: vi_framework_self_testing
SUCCESS: All core systems operational
SYSTEM READY FOR AI/ML ENVIRONMENT CONFIGURATION
```

### 4.9.2.1 Additional Verification

```bash
# Verify EXT4 data mount
mount | grep ext4
```

**Expected Output**:

```
/dev/nvme0n1p5 on /data type ext4
```

### 4.9.2.2 Subvolume Structure Check

```bash
# Check subvolume structure
sudo btrfs subvolume list /
sudo btrfs subvolume list /ml
```

### 4.9.2.3 Filesystem Health Verification

```bash
# Verify filesystem health
sudo btrfs filesystem show
sudo btrfs filesystem df /
sudo btrfs filesystem df /ml
```

### 4.9.2.4 Space Usage Check

```bash
# Check available space with compression
df -h
sudo btrfs filesystem usage /
```

## 4.10 System Subvolume Testing

### 4.10.1 Test Snapshot Functionality

```bash
# Create test system snapshot
sudo btrfs subvolume snapshot / /.snapshots/test-system-$(date +%Y%m%d-%H%M)

# Create test ML snapshot (will be configured in S5)
sudo btrfs subvolume snapshot /ml /ml/.snapshots/test-ml-$(date +%Y%m%d-%H%M)

# List created snapshots
sudo btrfs subvolume list /.snapshots
sudo btrfs subvolume list /ml/.snapshots

echo "SUCCESS: Snapshot functionality verified"
```

### 4.10.2 Cleanup Test Snapshots

```bash
# Remove test snapshots
sudo btrfs subvolume delete /.snapshots/test-system-*
sudo btrfs subvolume delete /ml/.snapshots/test-ml-*

echo "SUCCESS: Test snapshots cleaned up"
```

### 4.10.3 Performance Verification

```bash
# Test compression effectiveness
sudo compsize / 2>/dev/null || echo "NOTE: Install compsize for compression analysis"

# Verify snapshot cleanliness (should show system without volatile data)
echo "System snapshot preview (excluding volatile /var data):"
sudo btrfs subvolume snapshot / /.snapshots/preview-test-$(date +%Y%m%d-%H%M)
sudo du -sh /.snapshots/preview-test-*
sudo btrfs subvolume list /.snapshots

# Check filesystem performance
sudo btrfs filesystem df /
sudo btrfs filesystem usage /

# Verify space efficiency with S1 strategy implementation
echo "Logical vs Physical space usage (S1 compliant subvolumes):"
df -h / /home /var/log /var/cache /var/tmp /var/spool /var/backups

# Cleanup preview snapshot
sudo btrfs subvolume delete /.snapshots/preview-test-*
```

## 4.11 System Configuration Validation

### 4.11.1 Boot Process Verification

```bash
# Check boot time and services
systemd-analyze blame | head -10

# Verify critical services started
systemctl status systemd-resolved
systemctl status NetworkManager
systemctl status snapd 2>/dev/null || echo "NOTE: Snapd not installed"
```

### 4.11.2 File System Integrity

```bash
# Check BTRFS filesystem health
sudo btrfs scrub start /
sudo btrfs scrub status /

# Verify no filesystem errors
dmesg | grep -i error | tail -5 || echo "SUCCESS: No recent filesystem errors"
```

### 4.11.3 User Environment Verification

```bash
# Verify user home directory access
ls -la ~ && echo "SUCCESS: Home directory accessible"

# Test write permissions
touch ~/test-file && rm ~/test-file && echo "SUCCESS: Home directory writable"

# Check user permissions on AI/ML directories
ls -la /ml /data && echo "SUCCESS: AI/ML directories accessible"
```

## 4.12 Troubleshooting System Subvolumes

### 4.12.1 Common Boot Issues

### 4.12.1.1 System Fails to Boot

**Symptoms**: GRUB error, kernel panic, or emergency mode

**Diagnosis**:

```bash
# Boot from Ubuntu Live USB
sudo mkdir -p /mnt/recovery
sudo mount -o subvol=@ /dev/nvme0n1p3 /mnt/recovery
sudo mount -o subvol=@home /dev/nvme0n1p3 /mnt/recovery/home
sudo mount -o subvol=@var /dev/nvme0n1p3 /mnt/recovery/var
sudo mount /dev/nvme0n1p1 /mnt/recovery/boot/efi
```

**Recovery**:

```bash
# Chroot into system
sudo mount --bind /dev /mnt/recovery/dev
sudo mount --bind /proc /mnt/recovery/proc
sudo mount --bind /sys /mnt/recovery/sys
sudo chroot /mnt/recovery

# Repair GRUB
update-grub
grub-install /dev/nvme0n1
update-initramfs -u
exit

# Cleanup and reboot
sudo umount -R /mnt/recovery
sudo reboot
```

### 4.12.1.2 Subvolume Mount Failures

**Symptoms**: Partitions not mounting, fstab errors, missing /var subdirectories

**Solution**:

```bash
# Check fstab syntax
sudo mount -fav

# Verify UUIDs are correct
sudo blkid | grep nvme0n1p3
sudo grep nvme0n1p3 /etc/fstab

# Remount with correct options
sudo mount -o remount,subvol=@ /

# Create missing /var mount points if needed
sudo mkdir -p /var/log /var/cache /var/tmp /var/spool /var/backups

# Test individual volatile /var subvolume mounts
sudo mount -o subvol=@var-log /dev/nvme0n1p3 /var/log
sudo mount -o subvol=@var-cache /dev/nvme0n1p3 /var/cache
```

### 4.12.2 Performance Issues

### 4.12.2.1 Slow Boot Times

**Diagnosis**:

```bash
systemd-analyze
systemd-analyze blame
```

**Optimization**:

```bash
# Disable unnecessary services
sudo systemctl disable snapd 2>/dev/null || true
sudo systemctl mask systemd-networkd-wait-online.service
```

### 4.12.2.2 Storage Performance

**Diagnosis**:

```bash
sudo btrfs filesystem df /
sudo iostat -x 1 5
```

**Optimization**:

```bash
# Enable quotas if needed for AI/ML resource management
sudo btrfs quota enable /
sudo btrfs quota enable /ml
```

## 4.13 System Subvolume Maintenance

### 4.13.1 Regular Maintenance Tasks

```bash
# Weekly filesystem scrub (data integrity check)
sudo btrfs scrub start /

# Monthly balance operation (if >50% metadata usage)
sudo btrfs balance start -dusage=50 /

# Quarterly defragmentation (if needed)
sudo btrfs filesystem defragment -r -v /home
```

### 4.13.2 Snapshot Management

```bash
# Create clean system maintenance snapshot (excludes volatile /var data per S1 strategy)
sudo btrfs subvolume snapshot / /.snapshots/maintenance-$(date +%Y%m%d)

# Create independent home directory snapshot
sudo btrfs subvolume snapshot /home /.snapshots/home-$(date +%Y%m%d)

# List all snapshots
sudo btrfs subvolume list /.snapshots

# Verify snapshot cleanliness (should not contain /var/log, /var/cache, etc.)
echo "Snapshot verification - checking for excluded volatile data:"
sudo ls /.snapshots/maintenance-$(date +%Y%m%d)/var/ 2>/dev/null && echo "WARNING: Snapshot contains /var data" || echo "SUCCESS: Clean snapshot without volatile /var data"

# Delete old snapshots (keep last 10 system snapshots)
sudo btrfs subvolume list /.snapshots | grep maintenance | awk '{print $9}' | tail -n +11 | xargs -r sudo btrfs subvolume delete

# Delete old home snapshots (keep last 5)
sudo btrfs subvolume list /.snapshots | grep home | awk '{print $9}' | tail -n +6 | xargs -r sudo btrfs subvolume delete
```

**Next Steps**: System BTRFS subvolumes are now configured and verified. Proceed to **Section S5: AI/ML BTRFS Environment Setup** to configure the ML partition subvolumes and services.

---

## Appendix A: System Subvolume Reference

### A.1 VI Framework Output Interpretation

The VI framework will display real-time progress and create a detailed log file. Expected successful output includes:

```bash
=== BTRFS Subvolume Creation Validation ===
SUCCESS: system_device_verification
SUCCESS: btrfs_tools_availability
SUCCESS: sudo_privileges_check
SUCCESS: mount_point_creation
SUCCESS: system_btrfs_mount_operation
SUCCESS: system_root_subvolume
SUCCESS: home_subvolume
SUCCESS: var_log_subvolume
SUCCESS: var_cache_subvolume
SUCCESS: var_tmp_subvolume
SUCCESS: var_spool_subvolume
SUCCESS: var_backups_subvolume
SUCCESS: snapshots_subvolume
SUCCESS: All 8 system subvolumes created successfully
READY FOR NEXT STEP: Section 4.5 - Migrate System Data to Subvolumes
```

### A.2 Subvolume Purpose and Rationale

| Subvolume | Snapshot Behavior | Strategic Purpose |
| --- | --- | --- |
| @ (root) | **Included** | Core system state (OS, /var/lib, configs, packages) |
| @home | **Independent Snapshots** | Personal data with separate lifecycle |
| @var-log | **Excluded** | Ephemeral log data prevents snapshot bloat |
| @var-cache | **Excluded** | Regenerable cache data (packages, browsers) |
| @var-tmp | **Excluded** | Temporary files and application scratch space |
| @var-spool | **Excluded** | Mail/print queues and transient data |
| @var-backups | **Excluded** | System backup files to prevent recursion |
| @snapshots | **Excluded** | Prevents recursive snapshot inclusion |

**Critical Design**: The @ subvolume preserves essential /var/lib data (package databases, application state) while excluding volatile data through dedicated subvolumes.

### A.3 Troubleshooting Common Issues

**When is data migration needed?**

- **New installations**: Skip Section 4.5 - no existing data to migrate
- **Existing systems**: Run Section 4.5 to migrate existing data to subvolumes
- **Upgrades**: Run Section 4.5 to preserve existing data during BTRFS conversion

**If VI framework reports failures:**

1. **Check Prerequisites**: Ensure all required viScripts completed successfully
2. **Verify Permissions**: Confirm sudo privileges are available
3. **Check Disk Space**: Ensure adequate space for subvolume creation
4. **Review Error Messages**: Specific error patterns indicate different issues
5. **Re-run Validation**: Use `--verbose` flag for detailed output

**Common Error Patterns:**

- `system_device_missing`: Target disk not found
- `btrfs_tools_missing`: BTRFS utilities not installed
- `sudo_privileges_required`: Need administrative access
- `mount_point_not_ready`: Temporary mount point issues

**Recovery Options:**

- Restore from backup if available
- Re-run individual viScript phases
- Check system logs for detailed error information

### A.4 BTRFS Mount Options Explanation

| Option | Purpose | Benefit for AI/ML |
| --- | --- | --- |
| `subvol=@` | Specify subvolume to mount | Enables subvolume-based snapshots |
| `noatime` | Disable access time updates | Improves performance for frequent file access |
| `compress=zstd:3` | Enable ZSTD compression level 3 | Saves space on code/config files |
| `space_cache=v2` | Enable space cache version 2 | Improves filesystem performance |
| `discard=async` | Enable async SSD TRIM | Maintains SSD performance over time |

**Technical Note**: The `noauto` option on snapshots prevents automatic mounting, allowing manual management.

### A.5 Pre-Reboot Validation Troubleshooting

**If pre-reboot validation (Section 4.8) reports failures:**

1. **Review the detailed log file** specified in script output
2. **Check specific error messages** for each failed validation step
3. **Verify subvolume creation** completed successfully in Section 4.4
4. **Confirm data migration** completed successfully in Section 4.5
5. **Re-run individual commands** from failed validation steps manually

**Recovery Option**: If critical failures occur, restore from the backup snapshot created in Section 4.5.1.

**Common Pre-Reboot Validation Issues:**

- `fstab_syntax_invalid`: Check fstab file syntax and UUID references
- `mount_test_failed`: Verify all partitions are accessible and mountable
- `subvolume_verification_failed`: Confirm all required subvolumes exist
- `permissions_setting_failed`: Check sudo privileges and file permissions

### A.6 Pre-Reboot Validation Output Interpretation

The VI framework will display real-time progress and create a detailed log file. Expected successful output includes:

```bash
=== BTRFS Pre-Reboot Validation ===
SUCCESS: fstab_syntax_validation
SUCCESS: test_mount_all_filesystems
SUCCESS: snapshots_directory_creation
SUCCESS: volatile_var_mount_points
SUCCESS: ml_partition_mount_points
SUCCESS: additional_system_directories
SUCCESS: snapshots_permissions_setting
SUCCESS: system_subvolume_verification
SUCCESS: home_subvolume_verification
SUCCESS: excluded_subvolumes_verification
SUCCESS: snapshots_subvolume_verification
SUCCESS: All 8 system subvolumes verified
SYSTEM READY FOR REBOOT TO BTRFS SUBVOLUMES
```

**Critical**: Do not proceed with reboot if any validation step fails. Address failures before continuing.

---

**System Ready**: The system partition now operates with BTRFS subvolumes providing snapshot capability, compression efficiency, and organized data management. The foundation is prepared for AI/ML development environment configuration.
