# S6. Data Partition Setup

**Document**: Ubuntu BTRFS Installation Guide  
**Section**: S6 - Data Partition Setup (/dev/nvme0n1p5)  
**Document Version**: 5.1  
**Last Modified**: August 1, 2025

---

## 6.1 Document Overview

This document provides comprehensive procedures for configuring the high-performance data partition (/dev/nvme0n1p5) according to the three-partition storage strategy defined in Section S1. The focus is on establishing optimized data storage for large datasets, model outputs, and archives using EXT4 filesystem for maximum performance with sequential read/write operations typical in AI/ML workloads.

The procedures establish a structured data environment with organized directories for datasets, outputs, cache, and archives, enabling efficient data management and high-performance access patterns essential for systematic AI/ML research and development.

## 6.2 Document Structure

This section implements data partition configuration through five primary procedures:

1. **Data Partition Mounting** - Mount and configure the EXT4 data partition
2. **Directory Structure Setup** - Create organized data storage hierarchies
3. **Performance Optimization** - Configure EXT4 for AI/ML workload optimization
4. **Data Management** - Implement efficient data organization and access patterns
5. **Validation and Testing** - Verify data partition functionality and performance

**Scope**: This document addresses only the data partition (/dev/nvme0n1p5). System partition configuration is covered in Section S4, and ML partition setup is addressed in Section S5.

## 6.3 Prerequisites

Successfully complete Section S5 (ML Subvolume Setup) before proceeding.

---

## 6.4 Configure Data Directory Structure

### 6.4.1 Create Data Mount Point

```bash
# Create data mount point
sudo mkdir -p /data

# Verify mount point creation
ls -la /data && echo "SUCCESS: Data mount point created"
```

### 6.4.2 Mount Data Partition

```bash
# Get data partition UUID
DATA_UUID=$(sudo blkid -s UUID -o value /dev/nvme0n1p5)
echo "Data partition UUID: $DATA_UUID"

# Verify UUID retrieval
[ -n "$DATA_UUID" ] && echo "SUCCESS: Data UUID retrieved" || echo "ERROR: Failed to get data UUID"

# Mount data partition
sudo mount /dev/nvme0n1p5 /data

# Verify successful mount
mount | grep nvme0n1p5 && echo "SUCCESS: Data partition mounted"
```

### 6.4.3 Create Comprehensive Data Directory Structure

```bash
# Create main data directory structure
sudo mkdir -p /data/{datasets,outputs,cache,archives,shared}

# Create detailed dataset directories
sudo mkdir -p /data/datasets/{training,validation,test,raw,processed,augmented}

# Create detailed output directories
sudo mkdir -p /data/outputs/{models,logs,checkpoints,tensorboard,mlflow,experiments}

# Create cache directories
sudo mkdir -p /data/cache/{preprocessing,downloads,temp,intermediate}

# Create archive directories
sudo mkdir -p /data/archives/{models,datasets,experiments,backups}

# Create shared directories
sudo mkdir -p /data/shared/{datasets,models,configs,templates}

# Verify directory structure
echo "Data directory structure created:"
find /data -type d | head -20
```

### 6.4.4 Set Appropriate Permissions

```bash
# Set ownership to current user for development access
sudo chown -R $USER:$USER /data

# Set appropriate permissions
sudo chmod -R 755 /data

# Verify permissions
ls -la /data/ && echo "SUCCESS: Data directory permissions set"
```

### 6.4.5 Create Data Organization Documentation

```bash
# Create data organization guide
sudo tee /data/README.md << 'EOF'
# Data Partition Organization

## Directory Structure

### /data/datasets/
- `training/` - Training datasets
- `validation/` - Validation datasets  
- `test/` - Test datasets
- `raw/` - Raw, unprocessed data
- `processed/` - Preprocessed datasets
- `augmented/` - Data augmentation outputs

### /data/outputs/
- `models/` - Trained model files
- `logs/` - Training and inference logs
- `checkpoints/` - Model checkpoints
- `tensorboard/` - TensorBoard logs
- `mlflow/` - MLflow experiment tracking
- `experiments/` - Experiment outputs

### /data/cache/
- `preprocessing/` - Preprocessing cache
- `downloads/` - Downloaded datasets
- `temp/` - Temporary files
- `intermediate/` - Intermediate processing results

### /data/archives/
- `models/` - Archived model versions
- `datasets/` - Archived datasets
- `experiments/` - Archived experiment results
- `backups/` - System backups

### /data/shared/
- `datasets/` - Shared datasets
- `models/` - Shared model files
- `configs/` - Shared configurations
- `templates/` - Data processing templates

## Usage Guidelines
- Use descriptive naming conventions
- Include metadata files with datasets
- Maintain version control for important data
- Regular cleanup of temporary files
- Backup critical datasets to archives
EOF

echo "SUCCESS: Data organization documentation created"
```

## 6.5 Configure Data Partition Mount

### 6.5.1 Update Filesystem Table

```bash
# Add data partition mount to fstab with EXT4 optimizations
sudo tee -a /etc/fstab << EOF

# Data partition (EXT4 for high-performance sequential access)
UUID=$DATA_UUID  /data  ext4  defaults,noatime,nodiratime,data=writeback,barrier=0,commit=60  0 2
EOF

echo "SUCCESS: fstab updated with data partition mount"
```

### 6.5.2 EXT4 Mount Options for AI/ML Performance

| Option | Purpose | Benefit for AI/ML |
| --- | --- | --- |
| `defaults` | Standard mount options | Provides basic functionality |
| `noatime` | Disable access time updates | Improves performance for frequent file access |
| `nodiratime` | Disable directory access time | Further performance improvement |
| `data=writeback` | Writeback journaling mode | Better performance for large sequential writes |
| `barrier=0` | Disable write barriers | Improves performance on SSDs |
| `commit=60` | Commit data every 60 seconds | Balances performance and data safety |

### 6.5.3 Verify Mount Configuration

```bash
# Test mount configuration
sudo mount -fav

# Verify data partition is properly configured
mount | grep /data && echo "SUCCESS: Data partition mount verified"
```

## 6.6 Data Management Setup

### 6.6.1 Create Dataset Management Scripts

```bash
# Create dataset management utilities
sudo mkdir -p /data/scripts

# Create dataset organization script
sudo tee /data/scripts/organize_dataset.sh << 'EOF'
#!/bin/bash
# Dataset organization script

DATASET_NAME=$1
DATASET_PATH=$2

if [ -z "$DATASET_NAME" ] || [ -z "$DATASET_PATH" ]; then
    echo "Usage: $0 <dataset_name> <dataset_path>"
    exit 1
fi

# Create dataset directory structure
mkdir -p /data/datasets/raw/$DATASET_NAME
mkdir -p /data/datasets/processed/$DATASET_NAME
mkdir -p /data/datasets/training/$DATASET_NAME
mkdir -p /data/datasets/validation/$DATASET_NAME
mkdir -p /data/datasets/test/$DATASET_NAME

# Copy dataset to raw directory
cp -r $DATASET_PATH /data/datasets/raw/$DATASET_NAME/

# Create metadata file
cat > /data/datasets/raw/$DATASET_NAME/metadata.txt << METADATA
Dataset: $DATASET_NAME
Source: $DATASET_PATH
Date Added: $(date)
Size: $(du -sh /data/datasets/raw/$DATASET_NAME | cut -f1)
METADATA

echo "Dataset $DATASET_NAME organized successfully"
EOF

sudo chmod +x /data/scripts/organize_dataset.sh
echo "SUCCESS: Dataset management script created"
```

### 6.6.2 Create Data Cleanup Scripts

```bash
# Create data cleanup utility
sudo tee /data/scripts/cleanup_cache.sh << 'EOF'
#!/bin/bash
# Data cache cleanup script

echo "Cleaning up cache directories..."

# Clean temporary files older than 7 days
find /data/cache/temp -type f -mtime +7 -delete
find /data/cache/intermediate -type f -mtime +7 -delete

# Clean preprocessing cache older than 30 days
find /data/cache/preprocessing -type f -mtime +30 -delete

# Clean downloads cache older than 90 days
find /data/cache/downloads -type f -mtime +90 -delete

echo "Cache cleanup completed"
EOF

sudo chmod +x /data/scripts/cleanup_cache.sh
echo "SUCCESS: Data cleanup script created"
```

### 6.6.3 Create Data Backup Scripts

```bash
# Create data backup utility
sudo tee /data/scripts/backup_data.sh << 'EOF'
#!/bin/bash
# Data backup script

BACKUP_DATE=$(date +%Y%m%d-%H%M)
BACKUP_DIR="/data/archives/backups/backup-$BACKUP_DATE"

echo "Creating backup: $BACKUP_DIR"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup important datasets
rsync -av --progress /data/datasets/ $BACKUP_DIR/datasets/

# Backup model outputs
rsync -av --progress /data/outputs/models/ $BACKUP_DIR/models/

# Backup experiment logs
rsync -av --progress /data/outputs/logs/ $BACKUP_DIR/logs/

# Create backup metadata
cat > $BACKUP_DIR/backup_info.txt << BACKUPINFO
Backup Date: $(date)
Backup Size: $(du -sh $BACKUP_DIR | cut -f1)
Source: /data
BACKUPINFO

echo "Backup completed: $BACKUP_DIR"
EOF

sudo chmod +x /data/scripts/backup_data.sh
echo "SUCCESS: Data backup script created"
```

## 6.7 Performance Optimization

### 6.7.1 Configure EXT4 for AI/ML Workloads

```bash
# Tune EXT4 filesystem for AI/ML performance
sudo tune2fs -o journal_data_writeback /dev/nvme0n1p5

# Set optimal read-ahead for sequential access
sudo blockdev --setra 8192 /dev/nvme0n1p5

echo "SUCCESS: EXT4 optimized for AI/ML workloads"
```

### 6.7.2 Configure I/O Scheduler

```bash
# Set I/O scheduler to none for NVMe drives
echo none | sudo tee /sys/block/nvme0n1/queue/scheduler

# Verify scheduler change
cat /sys/block/nvme0n1/queue/scheduler && echo "SUCCESS: I/O scheduler optimized"
```

### 6.7.3 Monitor Data Partition Performance

```bash
# Check data partition performance
echo "=== Data Partition Performance ==="
echo "1. Filesystem info:"
df -h /data

echo "2. I/O statistics:"
iostat -x 1 3 | grep nvme0n1p5

echo "3. Disk usage:"
du -sh /data/*

echo "SUCCESS: Data partition performance monitoring configured"
```

## 6.8 Data Environment Testing

### 6.8.1 Test Data Partition Functionality

```bash
# Test write performance
echo "Testing data partition write performance:"
time dd if=/dev/zero of=/data/test_write.dat bs=1M count=1000 2>/dev/null

# Test read performance
echo "Testing data partition read performance:"
time dd if=/data/test_write.dat of=/dev/null bs=1M 2>/dev/null

# Clean up test file
sudo rm /data/test_write.dat

echo "SUCCESS: Data partition performance testing completed"
```

### 6.8.2 Test Dataset Management

```bash
# Test dataset organization script
echo "Testing dataset management:"
/data/scripts/organize_dataset.sh test_dataset /tmp

# Verify test dataset organization
ls -la /data/datasets/raw/test_dataset/
cat /data/datasets/raw/test_dataset/metadata.txt

# Clean up test dataset
sudo rm -rf /data/datasets/*/test_dataset

echo "SUCCESS: Dataset management testing completed"
```

### 6.8.3 Test Data Backup

```bash
# Create test data for backup testing
mkdir -p /data/datasets/test_backup
echo "Test data for backup" > /data/datasets/test_backup/test.txt

# Test backup script
/data/scripts/backup_data.sh

# Verify backup
ls -la /data/archives/backups/
cat /data/archives/backups/*/backup_info.txt

# Clean up test backup
sudo rm -rf /data/archives/backups/* /data/datasets/test_backup

echo "SUCCESS: Data backup testing completed"
```

## 6.9 Data Security and Access Control

### 6.9.1 Set Up Data Access Permissions

```bash
# Create data access groups
sudo groupadd ml-users
sudo usermod -a -G ml-users $USER

# Set appropriate permissions for shared data
sudo chmod 775 /data/shared
sudo chgrp ml-users /data/shared

echo "SUCCESS: Data access permissions configured"
```

### 6.9.2 Configure Data Encryption (Optional)

```bash
# Check if encryption is needed
echo "For sensitive data, consider using LUKS encryption:"
echo "sudo cryptsetup luksFormat /dev/nvme0n1p5"
echo "sudo cryptsetup luksOpen /dev/nvme0n1p5 data_crypt"
echo "sudo mkfs.ext4 /dev/mapper/data_crypt"

echo "NOTE: Encryption will impact performance but provides security"
```

## 6.10 Data Monitoring and Maintenance

### 6.10.1 Set Up Data Monitoring

```bash
# Create data monitoring script
sudo tee /data/scripts/monitor_data.sh << 'EOF'
#!/bin/bash
# Data partition monitoring script

echo "=== Data Partition Status ==="
echo "1. Disk usage:"
df -h /data

echo "2. Directory sizes:"
du -sh /data/*

echo "3. Recent files (last 24 hours):"
find /data -type f -mtime -1 | head -10

echo "4. Large files (>100MB):"
find /data -type f -size +100M -exec ls -lh {} \;

echo "5. I/O statistics:"
iostat -x 1 1 | grep nvme0n1p5
EOF

sudo chmod +x /data/scripts/monitor_data.sh
echo "SUCCESS: Data monitoring script created"
```

### 6.10.2 Configure Automated Maintenance

```bash
# Create maintenance cron job
sudo tee /etc/cron.daily/data-maintenance << 'EOF'
#!/bin/bash
# Daily data maintenance

# Run cache cleanup
/data/scripts/cleanup_cache.sh

# Run data monitoring
/data/scripts/monitor_data.sh

# Log maintenance activities
echo "$(date): Daily data maintenance completed" >> /var/log/data-maintenance.log
EOF

sudo chmod +x /etc/cron.daily/data-maintenance
echo "SUCCESS: Automated data maintenance configured"
```

## 6.11 Final Data Environment Verification

### 6.11.1 Comprehensive Data Environment Test

```bash
# Verify data environment is ready
echo "=== Data Environment Verification ==="

echo "1. Mount status:"
mount | grep /data

echo "2. Directory structure:"
tree /data -L 2 2>/dev/null || find /data -maxdepth 2 -type d

echo "3. Permissions:"
ls -la /data/

echo "4. Available space:"
df -h /data

echo "5. Scripts availability:"
ls -la /data/scripts/

echo "6. Performance test:"
dd if=/dev/zero of=/data/perf_test.dat bs=1M count=100 2>/dev/null
dd if=/data/perf_test.dat of=/dev/null bs=1M 2>/dev/null
sudo rm /data/perf_test.dat

echo "SUCCESS: Data environment verification completed"
```

### 6.11.2 Data Environment Documentation

```bash
# Create comprehensive data environment guide
sudo tee /data/DATA_ENVIRONMENT.md << 'EOF'
# Data Environment Guide

## Overview
This data partition (/dev/nvme0n1p5) is configured with EXT4 filesystem optimized for AI/ML workloads requiring high-performance sequential read/write operations.

## Key Features
- **High Performance**: EXT4 with writeback journaling for optimal sequential I/O
- **Organized Structure**: Comprehensive directory hierarchy for datasets, outputs, and archives
- **Automated Management**: Scripts for dataset organization, cleanup, and backup
- **Monitoring**: Performance monitoring and maintenance automation

## Directory Structure
- `/data/datasets/` - Training, validation, and test datasets
- `/data/outputs/` - Model outputs, logs, and experiment results
- `/data/cache/` - Temporary files and preprocessing cache
- `/data/archives/` - Long-term storage and backups
- `/data/shared/` - Shared resources and configurations
- `/data/scripts/` - Management and utility scripts

## Usage Guidelines
1. Use descriptive naming for datasets and outputs
2. Regular cleanup of temporary files
3. Backup important data to archives
4. Monitor disk usage and performance
5. Use provided scripts for common tasks

## Performance Optimization
- I/O scheduler: none (optimized for NVMe)
- Read-ahead: 8192 sectors
- Journaling: writeback mode
- Mount options: noatime, nodiratime, barrier=0

## Maintenance
- Daily automated cleanup and monitoring
- Weekly performance checks
- Monthly backup verification
- Quarterly full system backup

## Scripts Available
- `organize_dataset.sh` - Dataset organization utility
- `cleanup_cache.sh` - Cache cleanup utility
- `backup_data.sh` - Data backup utility
- `monitor_data.sh` - Performance monitoring

## Next Steps
After completing data partition setup, proceed to Section S7 for system boot configuration.
EOF

echo "SUCCESS: Data environment documentation created"
```

## 6.12 Troubleshooting Data Partition

### 6.12.1 Common Issues

### 6.12.1.1 Mount Failures

**Symptoms**: Data partition not mounting, fstab errors

**Solution**:

```bash
# Check fstab syntax
sudo mount -fav

# Verify UUIDs are correct
sudo blkid | grep nvme0n1p5
sudo grep nvme0n1p5 /etc/fstab

# Manual mount test
sudo mount /dev/nvme0n1p5 /data
```

### 6.12.1.2 Performance Issues

**Symptoms**: Slow data access, poor I/O performance

**Diagnosis**:

```bash
# Check I/O scheduler
cat /sys/block/nvme0n1/queue/scheduler

# Check read-ahead settings
cat /sys/block/nvme0n1/queue/read_ahead_kb

# Monitor I/O performance
iostat -x 1 5
```

**Optimization**:

```bash
# Set optimal I/O scheduler
echo none | sudo tee /sys/block/nvme0n1/queue/scheduler

# Set optimal read-ahead
echo 8192 | sudo tee /sys/block/nvme0n1/queue/read_ahead_kb

# Remount with optimized options
sudo mount -o remount,noatime,nodiratime /data
```

### 6.12.2 Data Recovery

### 6.12.2.1 Corrupted Filesystem

**Symptoms**: Filesystem errors, data corruption

**Solution**:

```bash
# Unmount data partition
sudo umount /data

# Check filesystem
sudo e2fsck -f /dev/nvme0n1p5

# Remount after repair
sudo mount /dev/nvme0n1p5 /data
```

### 6.12.2.2 Data Recovery from Backups

**Procedure**:

```bash
# List available backups
ls -la /data/archives/backups/

# Restore from specific backup
BACKUP_DIR="/data/archives/backups/backup-YYYYMMDD-HHMM"
rsync -av $BACKUP_DIR/datasets/ /data/datasets/
rsync -av $BACKUP_DIR/models/ /data/outputs/models/
```

## 6.13 Data Environment Maintenance

### 6.13.1 Regular Maintenance Tasks

```bash
# Weekly data partition check
sudo e2fsck -f /dev/nvme0n1p5

# Monthly performance optimization
sudo tune2fs -o journal_data_writeback /dev/nvme0n1p5

# Quarterly full backup
/data/scripts/backup_data.sh
```

### 6.13.2 Performance Monitoring

```bash
# Set up performance monitoring
echo "*/5 * * * * /data/scripts/monitor_data.sh >> /var/log/data-monitor.log" | sudo crontab -

# Check performance logs
tail -f /var/log/data-monitor.log
```

**Next Steps**: Data partition is now configured and optimized for AI/ML workloads. Proceed to **Section S7: System Boot Configuration** to configure GRUB and ensure proper boot sequence.

---

**Data Environment Ready**: The data partition now operates with EXT4 filesystem optimized for high-performance sequential access patterns typical in AI/ML workloads. The environment provides organized data management with automated maintenance and comprehensive monitoring capabilities. 