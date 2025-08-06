# S5. ML Subvolume Setup

**Document**: Ubuntu BTRFS Installation Guide  
**Section**: S5 - ML Subvolume Setup (/dev/nvme0n1p4)  
**Document Version**: 5.1  
**Last Modified**: August 1, 2025

---

## 5.1 Document Overview

This document provides comprehensive procedures for configuring BTRFS subvolumes on the AI/ML development partition (/dev/nvme0n1p4) according to the three-partition storage strategy defined in Section S1. The focus is on creating an optimized development environment that supports experiment snapshots, model versioning, and service isolation while maintaining high performance for AI/ML workloads.

The procedures establish a structured ML development environment with separate subvolumes for projects, services, models, and Docker containers, enabling comprehensive experiment tracking and rollback capabilities essential for systematic AI/ML research and development.

## 5.2 Document Structure

This section implements ML partition subvolume configuration through six primary procedures:

1. **AI/ML Subvolume Creation** - Establish specialized subvolumes for ML development workflows
2. **Directory Structure Setup** - Create organized project and service hierarchies
3. **Mount Configuration** - Configure AI/ML optimized mount options and bind mounts
4. **Service Integration** - Set up Docker and service compatibility
5. **Performance Optimization** - Implement ML-specific BTRFS optimizations
6. **Validation and Testing** - Verify ML environment functionality and snapshot capabilities

**Scope**: This document addresses only the ML partition (/dev/nvme0n1p4). System partition configuration is covered in Section S4, and data partition setup is addressed in Section S6.

## 5.3 Prerequisites

Successfully complete Section S4 (System BTRFS Subvolume Setup) before proceeding.

---

## 5.4 Create AI/ML Subvolumes

### 5.4.1 Mount ML BTRFS Root

```bash
# Create mount point for ML BTRFS root access
sudo mkdir -p /mnt/ml-btrfs

# Mount the ML BTRFS partition directly to access subvolume root
sudo mount /dev/nvme0n1p4 /mnt/ml-btrfs

# Verify successful mount
mount | grep nvme0n1p4 && echo "SUCCESS: ML BTRFS partition mounted"
```

### 5.4.2 Create ML-Specific Subvolumes

```bash
# Create ML development subvolumes according to S1 strategy
sudo btrfs subvolume create /mnt/ml-btrfs/@ml-docker
sudo btrfs subvolume create /mnt/ml-btrfs/@ml-projects
sudo btrfs subvolume create /mnt/ml-btrfs/@ml-services
sudo btrfs subvolume create /mnt/ml-btrfs/@ml-models
sudo btrfs subvolume create /mnt/ml-btrfs/@ml-snapshots

# Verify ML subvolumes created successfully
sudo btrfs subvolume list /mnt/ml-btrfs

echo "SUCCESS: All 5 ML subvolumes created"
```

### 5.4.3 Create Initial Directory Structure

```bash
# Create comprehensive ML project directory structure
sudo mkdir -p /mnt/ml-btrfs/@ml-projects/{training,inference,experiments,notebooks,datasets,scripts}

# Create ML services directory structure
sudo mkdir -p /mnt/ml-btrfs/@ml-services/{jupyter,mlflow,tensorboard,apis,monitoring,logging}

# Create model storage directory structure
sudo mkdir -p /mnt/ml-btrfs/@ml-models/{pytorch,tensorflow,onnx,checkpoints,pretrained,converted}

# Create snapshot directory
sudo mkdir -p /mnt/ml-btrfs/@ml-snapshots

# Verify directory structure
echo "ML directory structure created:"
sudo find /mnt/ml-btrfs/@ml-* -type d | head -20
```

### 5.4.4 Subvolume Purpose and Rationale

| Subvolume | Snapshot Behavior | Strategic Purpose |
| --- | --- | --- |
| @ml-docker | **Excluded** | Docker has independent rollback mechanisms |
| @ml-projects | **Included** | All ML development content by default |
| @ml-services | **Included** | Service configurations and data |
| @ml-models | **Included** | Model files and checkpoints |
| @ml-snapshots | **Excluded** | Prevents recursive snapshot inclusion |

**Critical Design**: The ML subvolumes follow S1 strategy with comprehensive experiment snapshots while excluding Docker (which has its own versioning) and snapshots storage.

## 5.5 Configure ML Subvolume Mounts

### 5.5.1 Retrieve ML Partition UUID

```bash
# Get ML partition UUID for fstab configuration
ML_UUID=$(sudo blkid -s UUID -o value /dev/nvme0n1p4)
echo "ML BTRFS UUID: $ML_UUID"

# Verify UUID retrieval
[ -n "$ML_UUID" ] && echo "SUCCESS: ML UUID retrieved" || echo "ERROR: Failed to get ML UUID"
```

### 5.5.2 Update Filesystem Table

```bash
# Add ML BTRFS subvolume mounts to fstab with AI/ML optimized options
sudo tee -a /etc/fstab << EOF

# AI/ML BTRFS subvolumes (500GB partition) - S1 Strategy Implementation
# Docker storage (excluded from snapshots - Docker has independent versioning)
UUID=$ML_UUID  /ml/docker      btrfs  subvol=@ml-docker,defaults,noatime,nodatacow,space_cache=v2,discard=async  0 2

# ML projects and experiments (included in snapshots)
UUID=$ML_UUID  /ml/projects    btrfs  subvol=@ml-projects,defaults,noatime,compress=zstd:3,space_cache=v2,discard=async,autodefrag  0 2

# ML services and configurations (included in snapshots)
UUID=$ML_UUID  /ml/services    btrfs  subvol=@ml-services,defaults,noatime,compress=zstd:3,space_cache=v2,discard=async  0 2

# Model storage (light compression for large files)
UUID=$ML_UUID  /ml/models      btrfs  subvol=@ml-models,defaults,noatime,compress=zstd:1,space_cache=v2,discard=async  0 2

# ML snapshots storage (manual mount only)
UUID=$ML_UUID  /ml/.snapshots  btrfs  subvol=@ml-snapshots,defaults,noatime,compress=zstd:3,space_cache=v2,noauto  0 0
EOF

echo "SUCCESS: fstab updated with ML subvolumes"
```

### 5.5.3 ML-Specific BTRFS Mount Options

| Option | Purpose | Benefit for AI/ML |
| --- | --- | --- |
| `subvol=@ml-*` | Specify ML subvolume to mount | Enables ML-specific snapshots |
| `noatime` | Disable access time updates | Improves performance for frequent file access |
| `compress=zstd:3` | Enable ZSTD compression level 3 | Saves space on code/config files |
| `compress=zstd:1` | Light compression for models | Balances space and performance for large files |
| `nodatacow` | Disable copy-on-write for Docker | Improves Docker performance |
| `autodefrag` | Automatic defragmentation | Maintains performance for project files |
| `space_cache=v2` | Enable space cache version 2 | Improves filesystem performance |
| `discard=async` | Enable async SSD TRIM | Maintains SSD performance over time |

## 5.6 Create Mount Points and Bind Mounts

### 5.6.1 Create Mount Points

```bash
# Create ML mount points
sudo mkdir -p /ml/{docker,projects,services,models,.snapshots}

# Verify mount points created
ls -la /ml/ && echo "SUCCESS: ML mount points created"
```

### 5.6.2 Configure Service Compatibility

```bash
# Add bind mounts for service compatibility
sudo tee -a /etc/fstab << EOF

# Bind mounts for service compatibility
/ml/docker      /var/lib/docker     none  bind,x-systemd.requires=ml-docker.mount  0 0
/ml/services    /srv                none  bind,x-systemd.requires=ml-services.mount  0 0
EOF

echo "SUCCESS: Service compatibility bind mounts configured"
```

### 5.6.3 Create Service Directories

```bash
# Create service directories for immediate use
sudo mkdir -p /var/lib/docker /srv

# Set appropriate permissions
sudo chown root:root /var/lib/docker /srv
sudo chmod 755 /var/lib/docker /srv

echo "SUCCESS: Service directories created with proper permissions"
```

## 5.7 Mount and Test ML Subvolumes

### 5.7.1 Mount ML Subvolumes

```bash
# Mount all ML subvolumes
sudo mount -a

# Verify all ML mounts are active
mount | grep ml && echo "SUCCESS: All ML subvolumes mounted"
```

### 5.7.2 Test ML Environment

```bash
# Test write permissions on ML directories
sudo touch /ml/projects/test-file && sudo rm /ml/projects/test-file && echo "SUCCESS: Projects directory writable"
sudo touch /ml/services/test-file && sudo rm /ml/services/test-file && echo "SUCCESS: Services directory writable"
sudo touch /ml/models/test-file && sudo rm /ml/models/test-file && echo "SUCCESS: Models directory writable"

# Test Docker directory
sudo touch /ml/docker/test-file && sudo rm /ml/docker/test-file && echo "SUCCESS: Docker directory writable"
```

### 5.7.3 Verify Directory Structure

```bash
# Display ML directory structure
echo "ML Environment Structure:"
tree /ml/ 2>/dev/null || find /ml/ -type d | head -20

# Check subvolume status
sudo btrfs subvolume list /ml
```

## 5.8 Configure ML Development Environment

### 5.8.1 Set Up Project Templates

```bash
# Create standard project template
sudo mkdir -p /ml/projects/templates/{pytorch,tensorflow,notebook,api}

# Create template structure
sudo tee /ml/projects/templates/pytorch/README.md << 'EOF'
# PyTorch Project Template

## Project Structure
- `models/` - Model definitions
- `data/` - Data loading and preprocessing
- `training/` - Training scripts
- `inference/` - Inference scripts
- `utils/` - Utility functions
- `configs/` - Configuration files

## Usage
1. Copy this template to your project directory
2. Modify configuration files
3. Start development
EOF

echo "SUCCESS: Project templates created"
```

### 5.8.2 Configure Service Directories

```bash
# Create service configuration directories
sudo mkdir -p /ml/services/{jupyter,mlflow,tensorboard}/config
sudo mkdir -p /ml/services/{jupyter,mlflow,tensorboard}/data

# Create service startup scripts
sudo tee /ml/services/jupyter/start.sh << 'EOF'
#!/bin/bash
# Jupyter service startup script
cd /ml/projects
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
EOF

sudo chmod +x /ml/services/jupyter/start.sh
echo "SUCCESS: Service directories and scripts configured"
```

### 5.8.3 Set Up Model Storage

```bash
# Create model organization structure
sudo mkdir -p /ml/models/{pretrained,checkpoints,converted}/{pytorch,tensorflow,onnx}

# Create model metadata files
sudo tee /ml/models/README.md << 'EOF'
# Model Storage

## Directory Structure
- `pretrained/` - Pre-trained models from repositories
- `checkpoints/` - Training checkpoints and saved models
- `converted/` - Converted models for deployment

## Model Types
- `pytorch/` - PyTorch models (.pth, .pt)
- `tensorflow/` - TensorFlow models (.pb, .h5)
- `onnx/` - ONNX models (.onnx)

## Usage
- Store models with descriptive names
- Include model metadata and version information
- Use consistent naming conventions
EOF

echo "SUCCESS: Model storage structure configured"
```

## 5.9 Performance Optimization

### 5.9.1 Configure BTRFS Quotas

```bash
# Enable quotas for ML partition
sudo btrfs quota enable /ml

# Set quota limits for ML subvolumes (optional)
sudo btrfs qgroup limit 1G /ml/projects
sudo btrfs qgroup limit 2G /ml/models
sudo btrfs qgroup limit 1G /ml/services

echo "SUCCESS: BTRFS quotas configured for ML environment"
```

### 5.9.2 Optimize for AI/ML Workloads

```bash
# Set optimal BTRFS mount options for ML workloads
sudo mount -o remount,autodefrag /ml/projects
sudo mount -o remount,autodefrag /ml/services

# Configure compression for different data types
sudo mount -o remount,compress=zstd:3 /ml/projects
sudo mount -o remount,compress=zstd:1 /ml/models

echo "SUCCESS: ML-specific BTRFS optimizations applied"
```

### 5.9.3 Monitor Performance

```bash
# Check BTRFS filesystem status
sudo btrfs filesystem df /ml
sudo btrfs filesystem usage /ml

# Check compression effectiveness
sudo compsize /ml 2>/dev/null || echo "NOTE: Install compsize for compression analysis"
```

## 5.10 ML Environment Validation

### 5.10.1 Test Snapshot Functionality

```bash
# Create test ML snapshot
sudo btrfs subvolume snapshot /ml/projects /ml/.snapshots/test-projects-$(date +%Y%m%d-%H%M)

# Create test services snapshot
sudo btrfs subvolume snapshot /ml/services /ml/.snapshots/test-services-$(date +%Y%m%d-%H%M)

# List created snapshots
sudo btrfs subvolume list /ml/.snapshots

echo "SUCCESS: ML snapshot functionality verified"
```

### 5.10.2 Test Docker Integration

```bash
# Test Docker directory permissions
sudo touch /ml/docker/test-file && sudo rm /ml/docker/test-file && echo "SUCCESS: Docker directory accessible"

# Verify Docker can use the directory
docker info 2>/dev/null && echo "SUCCESS: Docker can access ML storage" || echo "NOTE: Docker not installed yet"
```

### 5.10.3 Verify Service Bind Mounts

```bash
# Test service bind mounts
sudo mount -a
mount | grep "bind" | grep ml && echo "SUCCESS: Service bind mounts active"

# Test service directory access
sudo touch /srv/test-file && sudo rm /srv/test-file && echo "SUCCESS: Service directory writable"
```

## 5.11 ML Environment Testing

### 5.11.1 Create Test Project

```bash
# Create a test ML project
sudo mkdir -p /ml/projects/test-project/{models,data,training,notebooks}

# Create test files
sudo tee /ml/projects/test-project/README.md << 'EOF'
# Test ML Project

This is a test project to verify ML environment functionality.

## Structure
- `models/` - Model files
- `data/` - Dataset files
- `training/` - Training scripts
- `notebooks/` - Jupyter notebooks

## Testing
- File creation and deletion
- Snapshot functionality
- Performance characteristics
EOF

echo "SUCCESS: Test ML project created"
```

### 5.11.2 Test Snapshot and Rollback

```bash
# Create snapshot of test project
sudo btrfs subvolume snapshot /ml/projects/test-project /ml/.snapshots/test-project-backup-$(date +%Y%m%d-%H%M)

# Modify test project
sudo tee /ml/projects/test-project/test-modification.txt << 'EOF'
This is a test modification to verify snapshot functionality.
EOF

# Verify modification
ls -la /ml/projects/test-project/

# Restore from snapshot (demonstration)
echo "Snapshot created. To restore:"
echo "sudo btrfs subvolume delete /ml/projects/test-project"
echo "sudo btrfs subvolume snapshot /ml/.snapshots/test-project-backup-* /ml/projects/test-project"

echo "SUCCESS: ML snapshot and rollback testing completed"
```

### 5.11.3 Performance Testing

```bash
# Test file creation performance
echo "Testing ML environment performance:"
time sudo dd if=/dev/zero of=/ml/projects/test-file bs=1M count=100 2>/dev/null
sudo rm /ml/projects/test-file

# Test compression effectiveness
sudo btrfs filesystem df /ml
sudo btrfs filesystem usage /ml

echo "SUCCESS: ML environment performance testing completed"
```

## 5.12 Cleanup and Final Verification

### 5.12.1 Cleanup Test Files

```bash
# Remove test snapshots
sudo btrfs subvolume delete /ml/.snapshots/test-* 2>/dev/null || true

# Remove test project
sudo rm -rf /ml/projects/test-project

# Clean up test files
sudo rm -f /ml/services/test-file /ml/models/test-file /ml/docker/test-file /srv/test-file

echo "SUCCESS: Test files cleaned up"
```

### 5.12.2 Final Environment Verification

```bash
# Verify ML environment is ready
echo "=== ML Environment Verification ==="
echo "1. Mount points:"
mount | grep ml

echo "2. Directory structure:"
ls -la /ml/

echo "3. Subvolumes:"
sudo btrfs subvolume list /ml

echo "4. Filesystem status:"
sudo btrfs filesystem df /ml

echo "5. Permissions:"
ls -ld /ml/*/

echo "SUCCESS: ML environment verification completed"
```

## 5.13 Troubleshooting ML Subvolumes

### 5.13.1 Common Issues

### 5.13.1.1 Mount Failures

**Symptoms**: ML subvolumes not mounting, fstab errors

**Solution**:

```bash
# Check fstab syntax
sudo mount -fav

# Verify UUIDs are correct
sudo blkid | grep nvme0n1p4
sudo grep nvme0n1p4 /etc/fstab

# Manual mount test
sudo mount -o subvol=@ml-projects /dev/nvme0n1p4 /ml/projects
```

### 5.13.1.2 Permission Issues

**Symptoms**: Cannot write to ML directories

**Solution**:

```bash
# Check ownership
ls -la /ml/

# Fix permissions if needed
sudo chown -R $USER:$USER /ml/projects
sudo chown -R $USER:$USER /ml/services
sudo chown -R $USER:$USER /ml/models

# Verify Docker directory permissions
sudo chown root:root /ml/docker
sudo chmod 755 /ml/docker
```

### 5.13.2 Performance Issues

### 5.13.2.1 Slow File Operations

**Diagnosis**:

```bash
# Check BTRFS status
sudo btrfs filesystem df /ml
sudo btrfs filesystem usage /ml

# Check mount options
mount | grep ml
```

**Optimization**:

```bash
# Remount with optimized options
sudo mount -o remount,autodefrag,compress=zstd:3 /ml/projects
sudo mount -o remount,autodefrag,compress=zstd:1 /ml/models
```

## 5.14 ML Environment Maintenance

### 5.14.1 Regular Maintenance Tasks

```bash
# Weekly ML filesystem scrub
sudo btrfs scrub start /ml

# Monthly balance operation (if >50% metadata usage)
sudo btrfs balance start -dusage=50 /ml

# Quarterly defragmentation
sudo btrfs filesystem defragment -r -v /ml/projects
```

### 5.14.2 Snapshot Management

```bash
# Create ML environment maintenance snapshot
sudo btrfs subvolume snapshot /ml/projects /ml/.snapshots/maintenance-$(date +%Y%m%d)

# List all ML snapshots
sudo btrfs subvolume list /ml/.snapshots

# Delete old snapshots (keep last 10)
sudo btrfs subvolume list /ml/.snapshots | grep maintenance | awk '{print $9}' | tail -n +11 | xargs -r sudo btrfs subvolume delete
```

**Next Steps**: ML BTRFS subvolumes are now configured and verified. Proceed to **Section S6: Data Partition Setup** to configure the high-performance data storage for datasets and archives.

---

**ML Environment Ready**: The ML partition now operates with BTRFS subvolumes providing comprehensive experiment snapshots, model versioning, and service isolation. The environment is optimized for AI/ML development workflows with systematic LoRA training research capabilities. 