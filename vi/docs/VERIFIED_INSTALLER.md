# Verified Installer (VI)

## Overview

The Verified Installer (VI) is a comprehensive, parameterized system for verifying various types of installations. It provides a standardized approach to installation validation while maintaining flexibility for different installation types and requirements.

## Key Features

### 1. **Generic Installation Type Support**
- **Any Installation Type**: The framework accepts any installation type defined in viScript files
- **BTRFS Root**: Root partition filesystem and subvolume verification
- **BTRFS ML**: Machine learning partition verification and optimization
- **BTRFS Data**: Data storage partition verification and backup testing
- **Docker**: Container platform verification
- **Custom**: User-defined installation types

### 2. **Flexible viScript System**
- JSON-based viScript files with strict schema validation
- Parameterized verification phases
- Simplified severity system (critical/informational)
- Conditional execution logic
- Test mode support

### 3. **Text Output Format**
- **Text**: Simple success/failed/warning messages
- **Verbose**: Detailed logging and output
- **Log Files**: Comprehensive logging to timestamped log files

### 4. **Advanced Features**
- Test mode (dry-run) support
- Strict viScript schema validation
- viScript validation with error reporting
- Dependency checking
- Comprehensive logging

## Architecture

### Core Components

```
Verified Installer (VI)
├── Main Script (verified_installer.sh)
├── viScript Files (*_viScript.json)
└── Generic viScript-driven verification
```

### viScript Structure

```json
{
  "installation_type": "btrfs_root",
  "version": "1.0",
  "description": "Installation description",
  "phases": [
    {
      "name": "phase_name",
      "description": "Phase description",
      "checks": [
        {
          "name": "check_name",
          "description": "Check description",
          "command": "command_to_execute",
          "validation_type": "return_value|output_pattern|both|none",
          "expected_return": 0,
          "expected_pattern": "expected_output_pattern",
          "severity": "critical|informational",
          "optional": true/false
        }
      ]
    }
  ],
  "next_step": "next_viscript_filename.json"
}
```

## Usage Examples

### Basic Usage

```bash
# System validation
sudo ./verified_installer.sh system_validation_viScript.json

# BTRFS installation verification with verbose output
sudo ./verified_installer.sh btrfs_root_viScript.json --verbose

# Docker installation with test mode
sudo ./verified_installer.sh ../ubuntu-btrfs-installer/src/docker_viScript.json --test

# Custom installation verification
sudo ./verified_installer.sh custom_viScript.json

# Generate text report using shell redirection
sudo ./verified_installer.sh btrfs_root_viScript.json > report.txt
```

### Advanced Usage

```bash
# Test mode with verbose output
sudo ./verified_installer.sh btrfs_root_viScript.json --test --verbose

# Verbose mode for detailed logging
sudo ./verified_installer.sh ../ubuntu-btrfs-installer/src/docker_viScript.json --verbose

# Help display
sudo ./verified_installer.sh --help
```

## viScript File Examples

### BTRFS Root Partition viScript (btrfs_root_viScript.json)

```json
{
  "installation_type": "btrfs_root",
  "version": "1.0",
  "description": "BTRFS Root Partition Installation Verification",
  "phases": [
    {
      "name": "boot_verification",
      "description": "Verify system booted successfully from BTRFS root subvolumes",
      "checks": [
        {
          "name": "root_filesystem",
          "description": "Root filesystem running from BTRFS subvolumes",
          "command": "mount | grep 'on / '",
          "validation_type": "output_pattern",
          "expected_pattern": "btrfs.*subvol=/@",
          "severity": "critical"
        }
      ]
    }
  ]
}
```

### BTRFS ML Partition viScript (btrfs_ml_viScript.json)

```json
{
  "installation_type": "btrfs_ml",
  "version": "1.0",
  "description": "BTRFS ML Partition Installation Verification",
  "phases": [
    {
      "name": "mount_verification",
      "description": "Verify ML partition is properly mounted",
      "checks": [
        {
          "name": "ml_mount",
          "description": "/ml partition mounted as BTRFS",
          "command": "mount | grep 'on /ml '",
          "validation_type": "output_pattern",
          "expected_pattern": "btrfs",
          "severity": "critical"
        }
      ]
    }
  ]
}
```

### BTRFS Data Partition viScript (btrfs_data_viScript.json)

```json
{
  "installation_type": "btrfs_data",
  "version": "1.0",
  "description": "BTRFS Data Partition Installation Verification",
  "phases": [
    {
      "name": "mount_verification",
      "description": "Verify data partition is properly mounted",
      "checks": [
        {
          "name": "data_mount",
          "description": "/data partition mounted as BTRFS",
          "command": "mount | grep 'on /data '",
          "validation_type": "output_pattern",
          "expected_pattern": "btrfs",
          "severity": "critical"
        }
      ]
    }
  ]
}
```

### Docker viScript (docker_viScript.json)

```json
{
  "installation_type": "docker",
  "version": "1.0",
  "description": "Docker Installation Verification",
  "phases": [
    {
      "name": "service_verification",
      "description": "Verify Docker service is running",
      "checks": [
        {
          "name": "docker_service",
          "description": "Docker service is active",
          "command": "systemctl is-active docker",
          "validation_type": "output_pattern",
          "expected_pattern": "active",
          "severity": "critical"
        }
      ]
    }
  ]
}
```

## viScript Validation

### Strict Schema Validation

The VI framework enforces strict validation of viScript files to ensure consistency and reliability:

- **Required Fields**: All checks must have `severity` field
- **Deprecated Fields**: `critical` and `weight` fields are no longer supported
- **Valid Severity Values**: Only `"critical"` or `"informational"` are allowed
- **Schema Validation**: JSON structure and required fields are validated
- **Error Reporting**: Detailed error messages guide users to fix issues

### Removed Attributes

The following attributes were removed from the schema as they are not supported by the actual implementation:

**Top-level attributes (removed):**
- `mount_points`: Removed as unnecessary for pre-installation validation
- `services`: Removed as unnecessary for pre-installation validation
- `filesystems`: Removed as unnecessary for pre-installation validation
- `test_operations`: Removed as unnecessary for pre-installation validation
- `dependencies`: Removed as commands fail naturally if dependencies aren't met
- `post_verification`: Replaced with `next_step` attribute

**Check-level attributes (not supported):**
- `test_mode`: Documented but not actually implemented in verified_installer.sh
- `conditional`: Documented but not actually implemented in verified_installer.sh

**New attributes:**
- `next_step`: Single string providing guidance to the next viScript to execute

### Validation Error Examples

```bash
# Deprecated field error
[error] viScript contains deprecated field 'critical'. Use 'severity' instead.

# Missing severity error  
[error] viScript contains checks without required 'severity' field:
[error]   - check_name
[error] All checks must have 'severity' field set to 'critical' or 'informational'

# Invalid severity error
[error] viScript contains checks with invalid severity values:
[error]   - check_name (severity: invalid_value)
[error] Severity must be 'critical' or 'informational'

# Unsupported attribute warning
[warning] Found unsupported attributes: test_mode, conditional
[info] These attributes are documented but not actually supported by verified_installer.sh
[info] They will be ignored during execution

# Removed field warning
[warning] Found removed top-level fields: mount_points, dependencies
[info] These fields were removed from the schema and will be ignored
[info] Consider removing them from your viScript for cleaner code
```

## Check Types and Parameters

### Standard Check Parameters

- **name**: Unique identifier for the check
- **description**: Human-readable description
- **command**: Shell command to execute
- **validation_type**: Type of validation (return_value|output_pattern|both|none)
- **expected_return**: Expected return code (for return_value validation)
- **expected_pattern**: Regex pattern for expected output (for output_pattern validation)
- **severity**: Check importance (critical|informational)
- **optional**: Whether the check is optional

### Check Categories

1. **Service Checks**: Verify system services are running
2. **Mount Checks**: Verify filesystem mounts
3. **Command Checks**: Verify commands are available and working
4. **Pattern Checks**: Verify output matches expected patterns
5. **Test Checks**: Perform actual operations (with cleanup)

## Output Formats

### Text Output (Default)
```
=== Verified Installer (VI) v5.0 ===
Timestamp: Sat Aug  2 06:42:18 PM PDT 2025
Installation Type: btrfs_root
viScript File: btrfs_root_viScript.json
TEST MODE: Running in dry-run mode
Log file: /tmp/verified_installer_20250802-184218.log

=== Phase: boot_verification ===
Description: Verify system booted successfully from BTRFS root subvolumes
SUCCESS: Root filesystem running from BTRFS subvolumes - Expected pattern 'btrfs.*subvol=/@' found
SUCCESS: Create test system snapshot - Command executed (return: 0)
FAILED: Docker service is active - Expected pattern 'active' not found (CRITICAL)

=== VERIFICATION SUMMARY ===
Timestamp: Sat Aug  2 06:42:18 PM PDT 2025
Installation Type: btrfs_root
Total Checks: 15
Successful: 14
Failed: 1
Warnings: 0
Success Rate: 93%
Status: FAILED
Installation verification failed - review required
```

### Verbose Output
When using `--verbose` flag, additional debug information is displayed:
```
[2025-08-02 18:42:18] [debug] Validating return value: return_value_test (expected: 0)
[2025-08-02 18:42:18] [info] TEST MODE: Validating return value: return_value_test
success
SUCCESS: Test return value validation - command succeeds with expected return code - Return value 0 matches expected 0 (test mode)
```

## Command Line Interface

### Usage
```bash
sudo ./verified_installer.sh <viScript_file> [OPTIONS]
```

### Arguments
- **<viScript_file>**: Mandatory viScript file (e.g., system_validation_viScript.json)

### Options
- **--test**: Run in test mode (includes viScript validation, dry-run where possible)
- **--verbose**: Show detailed output and debug information
- **--help, -h**: Show help message

### Examples
```bash
# Basic usage
sudo ./verified_installer.sh system_validation_viScript.json

# Test mode
sudo ./verified_installer.sh btrfs_root_viScript.json --test

# Verbose output
sudo ./verified_installer.sh ../ubuntu-btrfs-installer/src/docker_viScript.json --verbose

# Test mode with verbose output
sudo ./verified_installer.sh custom_viScript.json --test --verbose

# Redirect output to file
sudo ./verified_installer.sh btrfs_root_viScript.json > report.txt
```

## Extending the Framework

### Adding New Installation Types

1. **Create viScript File**
   ```json
   {
     "installation_type": "new_type",
     "version": "1.0",
     "description": "New Installation Type",
     "phases": [...]
   }
   ```

2. **Use Generic Framework**
   ```bash
   sudo ./verified_installer.sh new_type_viScript.json
   ```

### Adding Custom Phases

```json
{
  "phases": [
    {
      "name": "custom_phase",
      "description": "Custom verification phase",
      "checks": [...]
    }
  ]
}
```

### Adding Custom Checks

```json
{
  "checks": [
    {
      "name": "custom_check",
      "description": "Custom verification check",
      "command": "custom_command",
      "validation_type": "output_pattern",
      "expected_pattern": "expected_output",
      "severity": "critical"
    }
  ]
}
```

## Best Practices

### 1. **viScript Design**
- Use descriptive names and descriptions
- Group related checks into logical phases
- Set appropriate severity levels for critical vs. non-critical checks
- Include cleanup operations for test checks

### 2. **Command Design**
- Use idempotent commands where possible
- Include proper error handling
- Test commands in isolation before adding to viScript
- Use conditional checks for optional features

### 3. **Output Design**
- Provide clear success/failure messages
- Include relevant context in descriptions
- Use appropriate log levels
- Generate comprehensive reports for troubleshooting

### 4. **Testing**
- Test viScripts in isolation
- Use test mode for destructive operations
- Validate JSON syntax before deployment
- Test with verbose mode for debugging

## Troubleshooting

### Common Issues

1. **viScript File Not Found**
   ```
   Error: viScript file 'viScript.json' not found
   Solution: Ensure viScript file exists and path is correct
   ```

2. **Invalid JSON**
   ```
   Error: Invalid JSON in viScript file
   Solution: Validate JSON syntax using jq or online validator
   ```

3. **Missing Dependencies**
   ```
   Warning: Required command 'btrfs' not found
   Solution: Install required packages before running verification
   ```

4. **Permission Issues**
   ```
   Error: Permission denied
   Solution: Run with sudo or appropriate permissions
   ```

### Debug Mode

```bash
# Enable verbose logging
sudo ./verified_installer.sh btrfs_root_viScript.json --verbose

# Test mode with validation only
sudo ./verified_installer.sh btrfs_root_viScript.json --test
```

## Integration Examples

### CI/CD Pipeline Integration

```yaml
# GitHub Actions
- name: Verify Installation
  run: |
    sudo ./verified_installer.sh \
      btrfs_root_viScript.json > verification_results.txt

- name: Check Results
  run: |
    if grep -q "FAILED" verification_results.txt; then
      echo "Installation verification failed"
      exit 1
    fi
```

### Ansible Integration

```yaml
- name: Run installation verification
  shell: |
    sudo ./verified_installer.sh \
      "{{ viScript_file }}" > "{{ report_file }}"
  register: verification_result

- name: Parse verification results
  set_fact:
    verification_passed: "{{ 'FAILED' not in verification_result.stdout }}"
```

## Future Enhancements

### Planned Features

1. **viScript Versioning**: Version-aware viScript processing with migration tools
2. **Plugin System**: Modular plugin architecture for custom verification logic
3. **Remote Verification**: Support for remote system verification
4. **Database Integration**: Store verification results in databases
5. **Web Interface**: Web-based viScript configuration and result viewing
6. **Scheduled Verification**: Automated periodic verification
7. **Alerting System**: Integration with monitoring systems
8. **Performance Metrics**: Detailed performance analysis
9. **Compliance Reporting**: Generate compliance reports

### **Output Format Enhancements**
- **JSON Output**: Structured JSON format for programmatic analysis and CI/CD integration
- **XML Output**: Standardized XML format for enterprise reporting systems
- **HTML Reports**: Professional HTML reports with styling and interactive elements
- **CSV Export**: Comma-separated values for spreadsheet analysis
- **PDF Reports**: Portable Document Format for formal documentation
- **Markdown Reports**: Lightweight markdown format for documentation systems

### **Lightweight JSON Parser**
- **Built-in JSON Parser**: Develop a lightweight, native JSON parser to eliminate dependency on external `jq` package
- **Minimal Footprint**: Parser optimized for small memory footprint and fast execution
- **Core Functionality**: Support for essential JSON operations (parsing, querying, validation)
- **Fallback Support**: Maintain compatibility with `jq` while providing native alternative
- **Performance Optimization**: Faster execution for simple JSON operations compared to external tools

### Contributing

1. **Fork the repository**
2. **Create feature branch**
3. **Add tests for new functionality**
4. **Update documentation**
5. **Submit pull request**

## License

This framework is provided as-is for educational and operational purposes. Please ensure compliance with your organization's policies when using this framework.

---

**Version**: 5.0  
**Last Updated**: 2025-08-02  
**Author**: Verified Installer Team 