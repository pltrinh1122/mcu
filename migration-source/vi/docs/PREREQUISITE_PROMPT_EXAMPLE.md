# Prerequisite Prompt System Example

## **Simplified Enforcement System**

The new prerequisite prompt system provides a simple, user-friendly way to enforce sequential execution of viScripts without complex dependency resolution.

## **Example Prompts**

### **1. First viScript (No Prerequisites)**

When executing the first viScript in a sequence:

```
=== viScript Execution Confirmation ===
viScript: system_validation_viScript.json
Type: system_validation
Prerequisites: None (first viScript in sequence)

Ready to execute this viScript? (Y/N)
Confirm execution: 
```

### **2. Subsequent viScript (With Prerequisites)**

When executing a viScript that has prerequisites:

```
=== viScript Prerequisite Confirmation ===
viScript: btrfs_data_migration_viScript.json
Type: btrfs_data_migration

Prerequisites that must be completed:
  - btrfs_subvolume_creation_viScript.json

Warnings:
  ⚠️  This operation migrates live system data - ensure system backup exists
  ⚠️  Migration involves rsync operations on critical system directories
  ⚠️  Verify sufficient disk space before proceeding
  ⚠️  System backup snapshot will be created automatically

Please confirm that ALL prerequisite viScripts have been completed successfully.
This viScript will modify system configuration and cannot be safely undone.

Confirm prerequisites completed and ready to proceed? (Y/N): 
```

### **3. Critical viScript (High Risk)**

When executing a critical viScript like boot configuration:

```
=== viScript Prerequisite Confirmation ===
viScript: btrfs_boot_configuration_viScript.json
Type: btrfs_boot_configuration

Prerequisites that must be completed:
  - btrfs_subvolume_creation_viScript.json
  - btrfs_data_migration_viScript.json
  - btrfs_mount_configuration_viScript.json

Warnings:
  ⚠️  This operation modifies critical boot configuration files
  ⚠️  System bootability depends on correct configuration
  ⚠️  Interactive verification checkpoints will be required
  ⚠️  This is the POINT OF NO RETURN for BTRFS subvolume boot
  ⚠️  Complete pre-reboot validation before proceeding

Please confirm that ALL prerequisite viScripts have been completed successfully.
This viScript will modify system configuration and cannot be safely undone.

Confirm prerequisites completed and ready to proceed? (Y/N): 
```

## **Usage Examples**

### **Individual viScript Execution**

```bash
# Execute with prerequisite confirmation
sudo ./verified_installer.sh --type btrfs_data_migration --viScript btrfs_data_migration_viScript.json --verbose

# Execute in test mode (skips confirmation)
sudo ./verified_installer.sh --type btrfs_data_migration --viScript btrfs_data_migration_viScript.json --test --verbose
```

### **Batch Execution**

```bash
# Execute batch with interactive confirmations
./verified_installer.sh system_validation_viScript.json --verbose

# Execute batch with auto-confirm (skips prompts)
./verified_installer.sh system_validation_viScript.json --verbose

# Execute specific phase with confirmations
./verified_installer.sh btrfs_root_viScript.json --verbose
```

## **Benefits of Simplified System**

### **1. User-Friendly**
- **Clear Prompts**: Easy-to-understand confirmation messages
- **Position Awareness**: Shows current viScript position in sequence
- **Prerequisite List**: Clearly lists what must be completed first
- **Warning Display**: Shows important warnings before execution

### **2. Flexible**
- **Test Mode**: Skip confirmations in test/dry-run mode
- **Auto-Confirm**: Option to skip all prompts for automated execution
- **Individual Execution**: Works for both individual and batch execution
- **Validation Mode**: Skip confirmations in validation-only mode

### **3. Safe**
- **Explicit Confirmation**: User must explicitly confirm prerequisites
- **Warning Display**: Shows all relevant warnings before execution
- **Cancellation Option**: User can cancel at any time
- **Logging**: All confirmations and cancellations are logged

### **4. Maintainable**
- **Simple Logic**: No complex dependency resolution
- **Clear Messages**: Self-documenting prompt messages
- **Consistent Interface**: Same prompt system across all viScripts
- **Easy to Extend**: Simple to add new confirmation types

## **Execution Flow**

### **Individual viScript Execution**
```
1. Load viScript
2. Display viScript information
3. Check for prerequisites
4. If prerequisites exist:
   - Display prerequisite list
   - Display warnings
   - Prompt for confirmation
5. If no prerequisites:
   - Display simple confirmation
6. Execute viScript or cancel
```

### **Batch Execution**
```
1. Load batch configuration
2. Display execution plan
3. For each viScript:
   - Show position (e.g., "2-of-5")
   - Display prerequisites
   - Prompt for confirmation
   - Execute viScript
4. Continue to next viScript
```

## 🛡️ **Safety Features**

### **1. Clear Communication**
- **Position Awareness**: User knows exactly where they are in the sequence
- **Prerequisite List**: Clear list of what must be completed first
- **Warning Display**: Important warnings are prominently displayed
- **Risk Communication**: Clear indication of what the viScript will do

### **2. User Control**
- **Explicit Confirmation**: User must type 'Y' to proceed
- **Cancellation Option**: User can type 'N' to cancel
- **Test Mode**: Skip confirmations for testing
- **Auto-Confirm**: Skip confirmations for automated execution

### **3. Logging**
- **Confirmation Logging**: All confirmations are logged
- **Cancellation Logging**: All cancellations are logged
- **Error Logging**: All errors are logged with context
- **Progress Tracking**: Execution progress is tracked

## **Conclusion**

The simplified prerequisite prompt system provides:

1. **Clear Communication**: Users know exactly what prerequisites are required
2. **User Control**: Users can confirm or cancel at any point
3. **Safety**: Multiple layers of confirmation and warning display
4. **Flexibility**: Works for individual and batch execution
5. **Simplicity**: No complex dependency resolution, just clear prompts

This system ensures that users understand the sequence requirements and can make informed decisions about when to proceed with each viScript execution. 