# S7. GRUB Setup and Reboot

**Document**: Ubuntu BTRFS Installation Guide  
**Section**: S7 - GRUB Setup and Reboot  
**Document Version**: 5.1  
**Last Modified**: August 1, 2025

---

## 7.1 Document Overview

This document provides comprehensive procedures for configuring GRUB bootloader to properly handle BTRFS subvolumes and verifying the complete installation through system reboot. The focus is on ensuring the three-partition storage strategy boots correctly and all BTRFS subvolumes mount properly after system restart.

The procedures establish a robust boot configuration that supports BTRFS subvolumes, enables proper system recovery capabilities, and validates the complete installation through comprehensive post-reboot verification.

## 7.2 Document Structure

This section implements boot configuration and verification through four primary procedures:

1. **GRUB Configuration** - Configure GRUB for BTRFS subvolume support
2. **Boot Environment Setup** - Prepare system for proper boot sequence
3. **System Reboot** - Safely restart system with new configuration
4. **Post-Reboot Verification** - Comprehensive validation of installation

**Scope**: This document addresses the final boot configuration and verification steps. All previous sections (S1-S6) must be completed before proceeding.

## 7.3 Prerequisites

Successfully complete Sections S1-S6 before proceeding:
- S1: Three-partition storage strategy understanding
- S2: System readiness validation
- S3: Ubuntu installation with partitioning
- S4: System BTRFS subvolume configuration
- S5: ML BTRFS environment setup
- S6: Data partition configuration

---

## 7.4 Update GRUB for BTRFS

### 7.4.1 Configure GRUB Boot Parameters

```bash
# Update GRUB configuration to include BTRFS subvolume root
sudo sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="[^"]*/& rootflags=subvol=@/' /etc/default/grub

# Verify GRUB configuration change
grep "rootflags=subvol=@" /etc/default/grub && echo "SUCCESS: GRUB rootflags configured"
```

### 7.4.2 Add BTRFS Module to GRUB

```bash
# Add BTRFS module to GRUB preload modules
echo 'GRUB_PRELOAD_MODULES="btrfs"' | sudo tee -a /etc/default/grub

# Verify BTRFS module addition
grep "GRUB_PRELOAD_MODULES" /etc/default/grub && echo "SUCCESS: BTRFS module added to GRUB"
```

### 7.4.3 Configure Initramfs for BTRFS

```bash
# Add BTRFS module to initramfs
echo 'btrfs' | sudo tee -a /etc/initramfs-tools/modules

# Verify BTRFS module in initramfs
grep "btrfs" /etc/initramfs-tools/modules && echo "SUCCESS: BTRFS module added to initramfs"
```

### 7.4.4 Regenerate Boot Configuration

```bash
# Update initramfs with BTRFS support
sudo update-initramfs -u

# Update GRUB configuration
sudo update-grub

# Install GRUB to boot device
sudo grub-install /dev/nvme0n1

echo "SUCCESS: Boot configuration updated with BTRFS support"
```

### 7.4.5 Verify GRUB Configuration

```bash
# Check GRUB configuration
echo "=== GRUB Configuration Verification ==="
echo "1. GRUB default settings:"
cat /etc/default/grub

echo "2. GRUB menu entries:"
sudo grep -A 10 "menuentry" /boot/grub/grub.cfg | head -20

echo "3. BTRFS module in initramfs:"
lsinitramfs /boot/initrd.img-$(uname -r) | grep btrfs

echo "SUCCESS: GRUB configuration verified"
```

## 7.5 Test Configuration Before Reboot

### 7.5.1 Test Mount Configuration

```bash
# Test all mount configurations
sudo mount -av

# Verify all partitions mount correctly
mount | grep -E "(btrfs|ext4)" && echo "SUCCESS: All filesystems mounted"
```

### 7.5.2 Create Additional Mount Points

```bash
# Create snapshot mount points
sudo mkdir -p /.snapshots /ml/.snapshots

# Create service mount points
sudo mkdir -p /var/lib/docker /srv

# Verify mount points created
ls -la /.snapshots /ml/.snapshots /var/lib/docker /srv && echo "SUCCESS: Additional mount points created"
```

### 7.5.3 Clean Up Temporary Mounts

```bash
# Unmount temporary BTRFS root mounts
sudo umount /mnt/system-btrfs 2>/dev/null || true
sudo umount /mnt/ml-btrfs 2>/dev/null || true

# Verify temporary mounts are unmounted
mount | grep mnt && echo "WARNING: Temporary mounts still active" || echo "SUCCESS: Temporary mounts cleaned up"
```

### 7.5.4 Final Pre-Reboot Verification

```bash
# Verify all critical components
echo "=== Pre-Reboot System Verification ==="

echo "1. BTRFS filesystems:"
sudo btrfs filesystem show

echo "2. Subvolume structure:"
sudo btrfs subvolume list /
sudo btrfs subvolume list /ml

echo "3. Mount points:"
mount | grep -E "(btrfs|ext4)"

echo "4. Available space:"
df -h

echo "5. GRUB configuration:"
sudo grub-probe --target=fs_uuid /boot

echo "SUCCESS: Pre-reboot verification completed"
```

## 7.6 System Reboot

### 7.6.1 Prepare for Reboot

```bash
# Save current system state
echo "System configuration completed at $(date)" | sudo tee /var/log/btrfs-installation.log

# Create reboot notification
echo "=== SYSTEM REBOOT NOTIFICATION ==="
echo "All BTRFS subvolumes and partitions have been configured."
echo "GRUB has been updated to support BTRFS subvolumes."
echo "System will reboot in 10 seconds..."
echo "After reboot, verify all mounts and subvolumes are working correctly."
echo "=================================="

# Countdown to reboot
for i in {10..1}; do
    echo "Rebooting in $i seconds..."
    sleep 1
done
```

### 7.6.2 Execute System Reboot

```bash
# Reboot system with new configuration
echo "Initiating system reboot..."
sudo reboot
```

**IMPORTANT**: The system will now reboot. After reboot, proceed to Section 7.7 for post-reboot verification.

---

## 7.7 Post-Reboot Verification

### 7.7.1 Verify All Mounts

```bash
# Check all BTRFS and EXT4 mounts
echo "=== Post-Reboot Mount Verification ==="

echo "1. BTRFS mounts:"
mount | grep btrfs

echo "2. EXT4 mounts:"
mount | grep ext4

echo "3. All filesystem mounts:"
mount | grep -E "(btrfs|ext4)" && echo "SUCCESS: All filesystems mounted correctly"
```

### 7.7.2 Check Subvolume Structure

```bash
# Verify system subvolumes
echo "=== Subvolume Structure Verification ==="

echo "1. System subvolumes:"
sudo btrfs subvolume list /

echo "2. ML subvolumes:"
sudo btrfs subvolume list /ml

echo "3. Subvolume mount points:"
ls -la /ml/
ls -la /.snapshots /ml/.snapshots 2>/dev/null || echo "Snapshot directories will be created on first snapshot"
```

### 7.7.3 Verify Filesystem Health

```bash
# Check BTRFS filesystem status
echo "=== Filesystem Health Check ==="

echo "1. BTRFS filesystem information:"
sudo btrfs filesystem show

echo "2. System partition usage:"
sudo btrfs filesystem df /

echo "3. ML partition usage:"
sudo btrfs filesystem df /ml

echo "4. Overall disk usage:"
df -h

echo "SUCCESS: Filesystem health verified"
```

### 7.7.4 Test Snapshot Capability

```bash
# Test system snapshot functionality
echo "=== Snapshot Functionality Test ==="

# Create test system snapshot
sudo btrfs subvolume snapshot / /.snapshots/test-system-$(date +%s)

# Create test ML snapshot
sudo btrfs subvolume snapshot /ml/projects /ml/.snapshots/test-projects-$(date +%s)

echo "1. System snapshots created:"
sudo btrfs subvolume list /.snapshots

echo "2. ML snapshots created:"
sudo btrfs subvolume list /ml/.snapshots

echo "SUCCESS: Snapshot functionality verified"
```

### 7.7.5 Clean Up Test Snapshots

```bash
# Remove test snapshots
echo "=== Cleaning Up Test Snapshots ==="

# Delete test system snapshots
sudo btrfs subvolume delete /.snapshots/test-system-* 2>/dev/null || true

# Delete test ML snapshots
sudo btrfs subvolume delete /ml/.snapshots/test-projects-* 2>/dev/null || true

echo "1. Remaining system snapshots:"
sudo btrfs subvolume list /.snapshots 2>/dev/null || echo "No system snapshots"

echo "2. Remaining ML snapshots:"
sudo btrfs subvolume list /ml/.snapshots 2>/dev/null || echo "No ML snapshots"

echo "SUCCESS: Test snapshots cleaned up"
```

## 7.8 Comprehensive System Verification

### 7.8.1 Verify Boot Configuration

```bash
# Check boot configuration
echo "=== Boot Configuration Verification ==="

echo "1. Current kernel:"
uname -r

echo "2. GRUB configuration:"
sudo grep "rootflags=subvol=@" /proc/cmdline && echo "SUCCESS: BTRFS subvolume root configured" || echo "ERROR: BTRFS subvolume root not found"

echo "3. Initramfs modules:"
lsinitramfs /boot/initrd.img-$(uname -r) | grep btrfs && echo "SUCCESS: BTRFS modules in initramfs" || echo "ERROR: BTRFS modules not found in initramfs"
```

### 7.8.2 Verify Service Compatibility

```bash
# Check service mount points
echo "=== Service Compatibility Verification ==="

echo "1. Docker directory:"
ls -la /var/lib/docker && echo "SUCCESS: Docker directory accessible" || echo "WARNING: Docker directory not found"

echo "2. Service directory:"
ls -la /srv && echo "SUCCESS: Service directory accessible" || echo "WARNING: Service directory not found"

echo "3. Data partition:"
ls -la /data && echo "SUCCESS: Data partition accessible" || echo "ERROR: Data partition not accessible"
```

### 7.8.3 Performance Verification

```bash
# Test system performance
echo "=== Performance Verification ==="

echo "1. Boot time analysis:"
systemd-analyze time

echo "2. Boot process breakdown:"
systemd-analyze blame | head -10

echo "3. Filesystem performance test:"
echo "Testing write performance..."
time dd if=/dev/zero of=/tmp/test_write.dat bs=1M count=100 2>/dev/null
echo "Testing read performance..."
time dd if=/tmp/test_write.dat of=/dev/null bs=1M 2>/dev/null
sudo rm /tmp/test_write.dat

echo "SUCCESS: Performance verification completed"
```

## 7.9 Final System Validation

### 7.9.1 Complete System Health Check

```bash
# Comprehensive system validation
echo "=== Complete System Health Check ==="

echo "1. System information:"
echo "   OS: $(lsb_release -d | cut -f2)"
echo "   Kernel: $(uname -r)"
echo "   Architecture: $(uname -m)"

echo "2. Storage configuration:"
echo "   System partition: $(df -h / | tail -1)"
echo "   ML partition: $(df -h /ml | tail -1)"
echo "   Data partition: $(df -h /data | tail -1)"

echo "3. BTRFS status:"
sudo btrfs filesystem show

echo "4. Mount summary:"
mount | grep -E "(btrfs|ext4)" | wc -l && echo " filesystems mounted"

echo "5. Available space:"
df -h | grep -E "(Filesystem|/$|/ml|/data)"

echo "SUCCESS: Complete system health check completed"
```

### 7.9.2 Create System Documentation

```bash
# Create system configuration documentation
sudo tee /var/log/btrfs-installation-summary.txt << 'EOF'
=== Ubuntu BTRFS Installation Summary ===
Installation Date: $(date)
System: $(lsb_release -d | cut -f2)
Kernel: $(uname -r)

=== Storage Configuration ===
System Partition: $(df -h / | tail -1 | awk '{print $1 " " $2}')
ML Partition: $(df -h /ml | tail -1 | awk '{print $1 " " $2}')
Data Partition: $(df -h /data | tail -1 | awk '{print $1 " " $2}')

=== BTRFS Subvolumes ===
System Subvolumes:
$(sudo btrfs subvolume list / | head -5)

ML Subvolumes:
$(sudo btrfs subvolume list /ml | head -5)

=== Mount Points ===
$(mount | grep -E "(btrfs|ext4)" | head -10)

=== Installation Status ===
- System BTRFS subvolumes configured
- ML BTRFS environment setup
- Data partition optimized
- GRUB configured for BTRFS
- System rebooted successfully
- All mounts verified
- Snapshot functionality tested

=== Next Steps ===
1. Install AI/ML development tools (Section S9)
2. Configure snapshot management (Section S10)
3. Set up monitoring and maintenance (Section S12)
EOF

echo "SUCCESS: System documentation created at /var/log/btrfs-installation-summary.txt"
```

## 7.10 Troubleshooting Post-Reboot Issues

### 7.10.1 Common Boot Issues

### 7.10.1.1 GRUB Boot Failures

**Symptoms**: System fails to boot, GRUB errors

**Diagnosis**:

```bash
# Check GRUB configuration
sudo cat /etc/default/grub

# Check kernel command line
cat /proc/cmdline

# Check initramfs
ls -la /boot/initrd.img-*
```

**Solution**:

```bash
# Reinstall GRUB if needed
sudo grub-install /dev/nvme0n1
sudo update-grub

# Regenerate initramfs
sudo update-initramfs -u
```

### 7.10.1.2 BTRFS Mount Failures

**Symptoms**: BTRFS subvolumes not mounting

**Diagnosis**:

```bash
# Check BTRFS filesystem status
sudo btrfs filesystem show

# Check subvolume list
sudo btrfs subvolume list /

# Check mount configuration
cat /etc/fstab
```

**Solution**:

```bash
# Manual mount test
sudo mount -o subvol=@ /dev/nvme0n1p3 /
sudo mount -o subvol=@ml-projects /dev/nvme0n1p4 /ml/projects
```

### 7.10.2 Performance Issues

### 7.10.2.1 Slow Boot Times

**Diagnosis**:

```bash
# Analyze boot time
systemd-analyze time
systemd-analyze blame | head -10
```

**Optimization**:

```bash
# Optimize BTRFS mount options
sudo mount -o remount,noatime,compress=zstd:3 /

# Check for unnecessary services
systemctl list-unit-files --state=enabled | grep -v systemd
```

### 7.10.2.2 Filesystem Performance Issues

**Diagnosis**:

```bash
# Check BTRFS status
sudo btrfs filesystem df /
sudo btrfs filesystem usage /

# Check I/O performance
iostat -x 1 5
```

**Optimization**:

```bash
# Balance BTRFS filesystem
sudo btrfs balance start -dusage=50 /

# Defragment if needed
sudo btrfs filesystem defragment -r -v /
```

## 7.11 System Maintenance After Reboot

### 7.11.1 Regular Maintenance Tasks

```bash
# Set up automated maintenance
sudo tee /etc/cron.weekly/btrfs-maintenance << 'EOF'
#!/bin/bash
# Weekly BTRFS maintenance

# Scrub system partition
sudo btrfs scrub start /

# Scrub ML partition
sudo btrfs scrub start /ml

# Balance if metadata usage > 50%
sudo btrfs filesystem usage / | grep "Metadata" | awk '{if($3 > 50) system("sudo btrfs balance start -musage=50 /")}'
sudo btrfs filesystem usage /ml | grep "Metadata" | awk '{if($3 > 50) system("sudo btrfs balance start -musage=50 /ml")}'

echo "$(date): Weekly BTRFS maintenance completed" >> /var/log/btrfs-maintenance.log
EOF

sudo chmod +x /etc/cron.weekly/btrfs-maintenance
echo "SUCCESS: Automated BTRFS maintenance configured"
```

### 7.11.2 Performance Monitoring

```bash
# Set up performance monitoring
sudo tee /etc/cron.daily/system-monitoring << 'EOF'
#!/bin/bash
# Daily system monitoring

# Check disk usage
df -h > /var/log/disk-usage-$(date +%Y%m%d).log

# Check BTRFS status
sudo btrfs filesystem df / >> /var/log/btrfs-status-$(date +%Y%m%d).log
sudo btrfs filesystem df /ml >> /var/log/btrfs-status-$(date +%Y%m%d).log

# Check for errors
dmesg | grep -i error | tail -10 >> /var/log/system-errors-$(date +%Y%m%d).log
EOF

sudo chmod +x /etc/cron.daily/system-monitoring
echo "SUCCESS: System monitoring configured"
```

**Next Steps**: System boot configuration is complete and verified. Proceed to **Section S9: AI/ML Development Tools Installation** to set up the development environment.

---

**System Ready**: The Ubuntu BTRFS installation is now complete with proper boot configuration, verified subvolume mounts, and comprehensive system validation. The three-partition storage strategy is fully operational and ready for AI/ML development workflows. 