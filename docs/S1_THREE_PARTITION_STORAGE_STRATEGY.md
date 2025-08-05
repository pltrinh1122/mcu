# S1. Storage Strategy

**Document**: Ubuntu BTRFS Installation Guide  
**Section**: S1 - Storage Strategy  
**Version**: 5.1  
**Last Updated**: July 31, 2025

---

## Document Purpose

This document specifies the three-partition storage architecture designed for AI/ML development workstations running Ubuntu 24.04 LTS with BTRFS filesystem optimization. It provides comprehensive technical guidance for implementing a storage strategy that separates system management, development environments, and large dataset storage for maximum flexibility and performance.

## Document Structure

This section is organized into six main components:

1. **Storage Architecture Overview** - High-level partition layout and design principles
2. **Snapshot-Enabled Development** - BTRFS subvolume strategies for system and ML partitions
3. **Data Organization Strategy** - EXT4-based append-only archive design
4. **Workflow Integration** - How partitions work together in AI/ML development
5. **Capacity Planning** - Expected utilization patterns and growth management

---

## S1.1 Storage Architecture Overview

### S1.1.1 Partition Layout

| Device | Size | Type | Mount Point | Strategic Purpose |
| --- | --- | --- | --- | --- |
| nvme0n1p1 | 1G | FAT32 | /boot/efi | System boot requirements |
| nvme0n1p2 | 64G | swap | [swap] | Memory overflow & hibernation |
| nvme0n1p3 | 200G | BTRFS | / | System with snapshot capability |
| nvme0n1p4 | 500G | BTRFS | /ml | Active AI/ML development workspace |
| nvme0n1p5 | 1.2T | EXT4 | /data | Training data & archive storage |

### S1.1.2 Strategic Design Principles

**Separation of Concerns**: Isolate system stability, active development, and data archival into distinct storage domains with appropriate technologies.

**Performance Optimization**: Match filesystem characteristics to data access patterns - snapshots for development, high-throughput for datasets.

**Workflow Integration**: Support complete AI/ML experiment lifecycle from data preparation through model archival.

## S1.2 Snapshot-Enabled Development (BTRFS Partitions)

### S1.2.1 BTRFS Snapshot Design Principle

**Default Inclusion**: All content within a BTRFS partition is automatically included in snapshots unless explicitly excluded through separate subvolumes. Subvolumes are created primarily to **exclude** problematic data or enable **independent snapshot management**.

### S1.2.2 System Partition Strategy (/dev/nvme0n1p3)

**Primary Goal**: Clean system snapshots with independent user data management and selective system component exclusion.

| Subvolume | Snapshot Behavior | Strategic Purpose |
| --- | --- | --- |
| @ (root) | **Included** | Core system state (OS, /var/lib, configs) |
| @home | **Independent Snapshots** | Personal data with separate lifecycle |
| @var-log | **Excluded** | Ephemeral log data |
| @var-cache | **Excluded** | Regenerable cache data |
| @var-tmp | **Excluded** | Temporary files |
| @var-spool | **Excluded** | Mail/print queues |
| @var-backups | **Excluded** | System backup files |
| @snapshots | **Excluded** | Prevents recursive snapshots |

**Snapshot Strategy**:

- **System snapshots** capture @ subvolume (includes /var/lib, system configs, installed packages)
- **User snapshots** independently capture @home subvolume (personal files, user configs)
- **Excluded volatile data** prevents bloat from logs, cache, temporary files, and queues
- **Preserved critical /var** maintains package databases (/var/lib), application data, system state

### S1.2.3 ML Development Partition Strategy (/dev/nvme0n1p4)

**Primary Goal**: Comprehensive experiment snapshots with selective exclusion of independently managed systems.

| Subvolume | Snapshot Behavior | Strategic Purpose |
| --- | --- | --- |
| @ml | **Included** | All ML development content by default |
| @ml-docker | **Excluded** | Docker has independent rollback mechanisms |
| @ml-snapshots | **Excluded** | Prevents recursive snapshot inclusion |

**Snapshot Strategy**:

- **Experiment snapshots** capture entire ML filesystem except excluded subvolumes
- **Included by default**: /ml/projects, /ml/services, /ml/models, /ml/cache, /ml/temp
- **Docker exclusion rationale**: Docker provides its own image versioning, tagging, and rollback systems
- **Independent management** leverages Docker's native capabilities rather than duplicating them

## S1.3 Data Organization Strategy (/dev/nvme0n1p5)

### S1.3.1 Append-Only Archive Design

**Primary Goal**: High-performance storage for datasets and completed experiments without snapshot overhead.

**Data Categories**:

- **Base Models**: Foundation models for training (SD1.5, SDXL, Flux)
- **Training Datasets**: Organized by processing state and purpose
- **Experiment Archives**: Completed experiments with full provenance
- **Backup Staging**: Metadata and incremental backup preparation

**Access Patterns**: Sequential reads for training, append-only writes for archival.

## S1.4 Workflow Integration

### S1.4.1 Development Flow

1. **Active Development** occurs in `/ml` (snapshotted BTRFS)
2. **Training Data** sourced from `/data` (high-performance EXT4)
3. **Completed Experiments** archived to `/data` (permanent storage)
4. **System Updates** managed via system snapshots

### S1.4.2 Capacity Allocation

| Storage Domain | Capacity | Usage Pattern |
| --- | --- | --- |
| Active Development | 500GB | Frequent changes, compression benefits |
| Data Archive | 1.2TB | Append-only growth, sequential access |
| System | 200GB | Stable, minimal growth |

### S1.4.3 Integration Benefits

**For Development**: Instant experiment snapshots, quick rollback, environment isolation.

**For Data Management**: High-throughput dataset access, straightforward backup, unlimited archive growth.

**For System Maintenance**: Clean system recovery, update safety, configuration versioning.

## S1.5 Capacity Planning Summary

### S1.5.1 Expected Utilization

**ML Partition (500GB)**:

- Container environments: ~150-200GB
- Active experiments: ~200-250GB
- Working models: ~100-150GB
- Growth buffer: ~50GB

**Data Partition (1.2TB)**:

- Base models: ~100-150GB
- Training datasets: ~400-600GB
- Experiment archives: ~400-600GB
- Future growth: ~200GB

### S1.5.2 Growth Management

**Monthly Growth**: 55-120GB (primarily archived experiments)
**Monitoring Threshold**: 80% utilization
**Cleanup Strategy**: Automated archival of completed experiments

## S1.6 Technology Alignment

### S1.6.1 BTRFS for Development

- **Compression**: 30-50% space savings on code and configurations
- **Snapshots**: Copy-on-write efficiency for experiment versioning
- **Subvolumes**: Granular control over snapshot inclusion

### S1.6.2 EXT4 for Data

- **Performance**: Optimized for large sequential dataset loading
- **Simplicity**: Straightforward backup and archival operations
- **Reliability**: Mature filesystem for critical data storage

### S1.6.3 Strategic Fit

This architecture balances development flexibility with data performance, supporting systematic LoRA training research across multiple base models and experimental variables.

---

**Next Section**: Proceed to **Section S2: Prerequisites & Verification** for pre-installation validation procedures. 