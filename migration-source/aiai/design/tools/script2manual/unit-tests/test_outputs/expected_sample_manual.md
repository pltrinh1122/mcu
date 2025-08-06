# Manual Installation Instructions

*This document was automatically generated from aiaiScript files.*

## Source Scripts

This manual was generated from the following aiaiScript files:

- `sample_aiaiScript.yaml`

## Overview

This manual provides step-by-step instructions for manual installation.
Each step includes the command to execute, its purpose, and expected outcomes.

## Phase 1: System Validation

**Source**: `sample_aiaiScript.yaml`
**Purpose**: Validate system prerequisites

### Step 1: Verify running from live boot environment

**Purpose**: Verify running from live boot environment  
**Critical**: Yes - must pass to continue  
**On Failure**: abort  

**Verification**:

```bash
# Run the command and check output
df / | grep -q '^/dev/loop' && echo 'live_boot_detected'

# Expected:
live_boot_detected
```

### Step 2: Check if running with sudo privileges

**Purpose**: Check if running with sudo privileges  

```bash
[ -n "$SUDO_USER" ] && echo 'sudo_active' || echo 'no_sudo'
```

### Step 3: Verify disk capacity meets requirements

**Purpose**: Verify disk capacity meets requirements  
**Critical**: Yes - must pass to continue  
**On Failure**: abort  

**Verification**:

```bash
# Run the command and check output
lsblk -b -d -o SIZE /dev/nvme0n1 | tail -1 | awk '{print int($1/1024/1024/1024)}' | awk '{if($1>=1400) print "sufficient_capacity"; else print "insufficient_capacity"}'`

# Expected:
sufficient_capacity
```

### Step 4: Get disk model and capacity information

**Purpose**: Get disk model and capacity information  

```bash
lsblk -d -o MODEL,SIZE /dev/nvme0n1 | tail -1
```

---

## Troubleshooting

### Common Issues

**Command fails with permission error**:
- Ensure you're running with sudo privileges
- Check if the command requires elevated permissions

**Validation step fails**:
- Verify the system meets the requirements
- Check if all prerequisites are installed
- Review the expected output format

**Destructive operation warnings**:
- Double-check the target before proceeding
- Ensure you have backups if needed
- Verify you're working on the correct system 