# AIAI Package Design Guidelines

**Document Version:** 1.0  
**Last Modified:** August 5, 2025

---

## Overview

This document provides guidelines for designing AIAI Packages, focusing on the relationship between Scripts and Phases, and how to structure installations for optimal human-AI interaction.

## Core Design Principles

### Scripts vs Phases: Problem-Solution Mapping

**Scripts solve: Atomicity across multiple commands**
- **Problem**: Complex operations require multiple commands that must succeed or fail together
- **Solution**: Scripts provide atomic execution boundaries where either all commands succeed or the entire operation rolls back
- **Focus**: Technical execution, rollback mechanisms, system consistency

**Phases solve: Logical milestones for operator pauses**
- **Problem**: Complex installations need natural breakpoints where operators can pause, assess, and make decisions
- **Solution**: Phases provide logical milestones that group related operations and create natural pause points
- **Focus**: Human decision-making, progress tracking, risk assessment

## Script Design Guidelines

### Script Granularity

**Scripts should be:**
- **Task-Focused**: One specific task or responsibility
- **Reusable**: Can be used in different contexts
- **Testable**: Can be validated independently
- **Atomic**: Either completes entirely or fails cleanly

**Examples of Good Script Granularity:**
```yaml
# Good: Single responsibility
id: "storage-partitioning"
intent: "Create disk partitions for BTRFS installation"
atomic: true
body:
  - command: "Create partition table"
  - command: "Create system partition"
  - command: "Create data partition"

# Good: Reusable component
id: "docker-installation"
intent: "Install and configure Docker"
atomic: true
body:
  - command: "Add Docker repository"
  - command: "Install Docker packages"
  - command: "Configure Docker service"
```

### Script Metadata Structure

```yaml
metadata:
  id: "script-identifier"
  intent: "Human-readable description of what the script accomplishes"
  technicalProficiency: "Beginner|Intermediate|Expert"
  context:
    designPrinciples:
      - "Fail fast and safe"
      - "Preserve existing data"
    dependencies:
      - "Required system state"
      - "Required permissions"
    compatibility:
      - "Supported systems"
      - "Required versions"
```

### Script Execution Patterns

**Sequential Execution:**
```yaml
body:
  - type: "command"
    id: "step-1"
    shellCommand: "command1"
  - type: "command"
    id: "step-2"
    shellCommand: "command2"
  - type: "command"
    id: "step-3"
    shellCommand: "command3"
```

**Conditional Execution:**
```yaml
body:
  - type: "conditional"
    id: "check-requirement"
    condition:
      source: "requirement-check"
      evaluate: "success"
    then:
      - ["proceed-script"]
    else:
      - ["skip-script"]
```

## Phase Design Guidelines

### Phase Composition Flexibility

**Phases can contain:**
- **One script** (when a single script represents a complete logical milestone)
- **Multiple scripts** (when multiple scripts work together to achieve a milestone)
- **Conditional scripts** (when different scripts run based on conditions)

### When to Use Single Script Phases

**Good candidates:**
- **Comprehensive validation** (system validation, hardware checks)
- **Simple installations** (single service, basic configuration)
- **Atomic operations** (partitioning, boot configuration)
- **Reusable components** (standalone functionality)

**Example:**
```yaml
Phase: "System Validation"
Scripts:
  - "comprehensive-system-validation_aiaiScript.yaml"
# Justified: Single comprehensive validation represents a complete milestone
```

### When to Use Multiple Script Phases

**Good candidates:**
- **Complex setups** (multiple components, dependencies)
- **Parallel operations** (independent tasks that can run together)
- **Sequential dependencies** (tasks that must complete in order)
- **Modular designs** (reusable components combined)

**Example:**
```yaml
Phase: "Storage Setup"
Scripts:
  - "disk-partitioning_aiaiScript.yaml"
  - "filesystem-creation_aiaiScript.yaml"
  - "subvolume-setup_aiaiScript.yaml"
# Justified: Multiple related operations to achieve storage milestone
```

### Phase Metadata Structure

```yaml
metadata:
  context:
    phase:
      name: "storage-setup"
      number: 2
      description: "Storage setup and configuration"
      scripts:
        - "storage-partitioning_aiaiScript.yaml"
        - "filesystem-creation_aiaiScript.yaml"
      execution_mode: "sequential"  # or "parallel", "conditional"
      milestone: "Storage ready for installation"
      critical: true
      estimated_duration: "15-20 minutes"
      dependencies:
        - "system-validation-complete"
      validation:
        entry: ["system-validated", "disk-available"]
        exit: ["partitions-created", "filesystems-ready"]
```

## Phase Boundary Guidelines

### Common Phase Boundaries

**System State Changes (Primary Boundaries):**
- **Reboot**: Excellent phase boundary - system state changes completely
- **Shutdown**: Good boundary - clean state transition
- **Live Boot to Installed**: Critical boundary - environment changes

**Filesystem Changes:**
- **Partition Creation**: Critical boundary - destructive operation
- **Filesystem Creation**: Good boundary - new storage structure
- **Mount Point Changes**: Good boundary - access pattern changes

**User Environment Changes:**
- **User Creation**: Good boundary - access control changes
- **Service Installation**: Good boundary - new capabilities available
- **Configuration Changes**: Moderate boundary - behavior changes

### Why Reboot Makes an Excellent Phase Boundary

**System State Reset:**
- Memory is cleared
- Kernel modules are reloaded
- Services are restarted
- Hardware detection runs again

**Validation Opportunity:**
- Can verify boot configuration worked
- Can test new kernel parameters
- Can confirm filesystem mounting
- Can validate service startup

**Rollback Safety:**
- If boot fails, previous state is preserved
- Can boot from rescue media to fix issues
- Clear failure point for troubleshooting

**Cognitive Break:**
- Operator can pause and assess
- Natural checkpoint for documentation
- Time to verify system state

## Package Design Patterns

### Pattern 1: Sequential Dependencies

```yaml
Phase: "Storage Setup"
Scripts:
  - storage_partitioning_aiaiScript.yaml  # Must complete first
  - filesystem_creation_aiaiScript.yaml   # Depends on partitioning
  - subvolume_setup_aiaiScript.yaml      # Depends on filesystem
```

### Pattern 2: Parallel Execution

```yaml
Phase: "Environment Setup"
Scripts:
  - docker_installation_aiaiScript.yaml   # Can run in parallel
  - python_environment_aiaiScript.yaml    # Can run in parallel
  - ml_frameworks_aiaiScript.yaml        # Can run in parallel
```

### Pattern 3: Conditional Execution

```yaml
Phase: "Hardware Optimization"
Scripts:
  - gpu_detection_aiaiScript.yaml        # Always run
  - gpu_driver_install_aiaiScript.yaml   # Only if GPU detected
  - gpu_optimization_aiaiScript.yaml     # Only if drivers installed
```

## Implementation Guidelines

### Main Script Phase Orchestration

```yaml
body:
  - type: "script"
    scriptType: "procedure"
    id: "phase-1-system-validation"
    intent: "Phase 1: System validation and prerequisites"
    atomic: true
    body:
      - type: "script"
        scriptType: "procedure"
        id: "system-validation-main"
        # Orchestrates validation scripts
        
  - type: "script"
    scriptType: "procedure"
    id: "phase-2-storage-setup"
    intent: "Phase 2: Storage partitioning and configuration"
    atomic: true
    body:
      - type: "script"
        scriptType: "procedure"
        id: "storage-partitioning"
        # Partitioning script
      - type: "script"
        scriptType: "procedure"
        id: "filesystem-creation"
        # Filesystem script
      - type: "script"
        scriptType: "procedure"
        id: "subvolume-setup"
        # Subvolume script
```

### AI Agent Phase Communication

**Phase Start:**
```
"Starting Phase 2 of 7: Storage Partitioning
This phase will create the disk partitions needed for your BTRFS installation.
Estimated time: 10-15 minutes
This is a critical phase that will modify your disk layout."
```

**Phase Progress:**
```
"Phase 2 Progress: 3 of 8 commands completed
Creating EFI partition... ✓
Creating system partition... ✓
Creating ML partition... ⏳"
```

**Phase Completion:**
```
"Phase 2 Complete: Storage Partitioning
✓ All partitions created successfully
✓ Filesystems initialized
✓ Mount points configured
Ready to proceed to Phase 3: Subvolume Setup"
```

## Quality Assurance Guidelines

### Script Validation

**Pre-Deployment Checks:**
- All scripts must pass schema validation
- All script references must be resolvable
- All destructive operations must be clearly marked
- All atomic scripts must have proper rollback mechanisms

### Phase Validation

**Phase Completeness:**
- Each phase must have clear entry and exit criteria
- Each phase must represent a logical milestone
- Each phase must provide operator decision points
- Each phase must have appropriate risk assessment

### Package Validation

**Package Completeness:**
- Must contain all required components (Guide, Scripts, Spec, Schema)
- Must provide complete installation coverage
- Must include appropriate error handling and recovery procedures
- Must document all prerequisites and system requirements

## Best Practices

### Script Design Best Practices

1. **Keep scripts focused**: One responsibility per script
2. **Make scripts reusable**: Design for multiple contexts
3. **Ensure atomicity**: All-or-nothing execution
4. **Provide clear rollback**: Define rollback mechanisms
5. **Include validation**: Validate pre/post conditions

### Phase Design Best Practices

1. **Create logical milestones**: Each phase should represent a complete logical unit
2. **Provide operator decision points**: Natural pauses for human assessment
3. **Align with risk boundaries**: Higher-risk operations in separate phases
4. **Include validation points**: Clear entry and exit criteria
5. **Consider cognitive load**: Optimal duration (5-30 minutes)

### Package Design Best Practices

1. **Start simple**: Begin with single script phases, add complexity as needed
2. **Plan for reuse**: Design scripts that can be used across packages
3. **Document thoroughly**: Clear operator guides and technical documentation
4. **Test comprehensively**: Validate complete installation procedures
5. **Maintain flexibility**: Allow for different execution patterns

---

*These guidelines ensure that AIAI Packages provide optimal human-AI interaction while maintaining technical safety and operational flexibility.* 