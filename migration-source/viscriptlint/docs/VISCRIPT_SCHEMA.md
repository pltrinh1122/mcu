# viScript Schema Documentation

## Overview

The viScript schema defines the structure for Verified Installer (VI) configuration files. This schema ensures consistency and provides validation for viScript files used by the `verified_installer.py` framework.

## Schema File

- **Schema**: `viscript_schema.json`
- **Version**: Draft-07 JSON Schema
- **Format**: JSON Schema specification

## Quick Start

### Basic viScript Structure

```json
{
  "installation_type": "system_validation",
  "version": "2.0",
  "description": "System validation for Ubuntu installation",
  "phases": [
    {
      "name": "hardware_check",
      "description": "Verify hardware requirements",
      "checks": [
        {
          "name": "memory_check",
          "description": "Check available RAM",
          "command": "free -h",
          "validation_type": "output_pattern",
          "expected_pattern": "\\d+G",
          "severity": "critical"
        }
      ]
    }
  ],
  "next_step": "btrfs_system_subvolume_creation_viScript.json"
}
```

## Schema Reference

### Top-Level Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `installation_type` | string | ✅ | Type of installation (e.g., "system_validation", "btrfs_root") |
| `version` | string | ✅ | Schema version (format: "X.Y") |
| `description` | string | ❌ | Human-readable description |
| `author` | string | ❌ | Author of the viScript |
| `created_date` | string | ❌ | Creation date (YYYY-MM-DD) |
| `phases` | array | ✅ | Array of verification phases |
| `next_step` | string | ❌ | Next viScript filename |
| `prerequisites` | object | ❌ | Prerequisites configuration |

### Phase Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | ✅ | Unique phase identifier |
| `description` | string | ✅ | Phase description |
| `checks` | array | ✅ | Array of verification checks |

### Check Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | ✅ | Unique check identifier |
| `description` | string | ✅ | Check description |
| `command` | string | ✅ | Shell command to execute |
| `validation_type` | string | ✅ | Validation method |
| `expected_return` | integer | ❌ | Expected exit code |
| `expected_pattern` | string | ❌ | Expected output pattern |
| `severity` | string | ✅ | Check importance |
| `optional` | boolean | ❌ | Whether check is optional |

## Validation Types

### `return_value`
Validates that the command returns the expected exit code.

**Required fields**: `expected_return`

```json
{
  "name": "service_check",
  "description": "Check if service is running",
  "command": "systemctl is-active docker",
  "validation_type": "return_value",
  "expected_return": 0,
  "severity": "critical"
}
```

### `output_pattern`
Validates that command output matches a regex pattern.

**Required fields**: `expected_pattern`

```json
{
  "name": "disk_check",
  "description": "Check available disk space",
  "command": "df -h /",
  "validation_type": "output_pattern",
  "expected_pattern": "\\d+%",
  "severity": "critical"
}
```

### `both`
Validates both return value and output pattern.

**Required fields**: `expected_return`, `expected_pattern`

```json
{
  "name": "comprehensive_check",
  "description": "Check both exit code and output",
  "command": "echo 'success'",
  "validation_type": "both",
  "expected_return": 0,
  "expected_pattern": "success",
  "severity": "critical"
}
```

### `none`
Executes command without validation (always succeeds if command runs).

```json
{
  "name": "info_check",
  "description": "Display system information",
  "command": "uname -a",
  "validation_type": "none",
  "severity": "informational"
}
```

## Severity Levels

### `critical`
- Failure causes overall verification to fail
- Weight: 3 points
- Used for essential system requirements

### `informational`
- Failure creates warning but doesn't fail overall verification
- Weight: 1 point
- Used for optional checks and information gathering

## Installation Types

Common installation types include:

- `system_validation`: Pre-installation system checks
- `btrfs_root`: BTRFS root partition verification
- `btrfs_ml`: BTRFS ML partition verification
- `btrfs_data`: BTRFS data partition verification
- `docker`: Docker installation verification

## Validation Tools

### viscriptlint
Primary validation tool with comprehensive checks:

```bash
./viscriptlint system_validation_viScript.json --verbose
```

### JSON Schema Validation
Formal schema validation using ajv:

```bash
# Install ajv
npm install -g ajv-cli

# Validate against schema
ajv validate -s viscript_schema.json -d system_validation_viScript.json
```

### Online Validation
Use online JSON Schema validators with `viscript_schema.json`.

## Best Practices

### 1. Naming Conventions
- Use descriptive, lowercase names with underscores
- Phase names: `hardware_check`, `network_validation`
- Check names: `memory_check`, `disk_space_validation`

### 2. Command Design
- Use idempotent commands where possible
- Include proper error handling
- Test commands in isolation before adding to viScript

### 3. Validation Patterns
- Use specific patterns rather than generic ones
- Test patterns against actual command output
- Consider edge cases and error conditions

### 4. Severity Assignment
- Use `critical` for essential system requirements
- Use `informational` for optional checks and information
- Consider the impact of failure on the overall installation

### 5. Documentation
- Provide clear, descriptive names and descriptions
- Include context about what each check verifies
- Document any special requirements or dependencies

## Migration Guide

### From Legacy Schema
If migrating from older viScript files:

1. **Remove deprecated fields**:
   - `critical` → use `severity: "critical"`
   - `weight` → use `severity` (weight is calculated automatically)

2. **Remove unsupported fields**:
   - `test_mode` (not implemented in verified_installer.py)
- `conditional` (not implemented in verified_installer.py)

3. **Remove removed top-level fields**:
   - `mount_points`, `services`, `filesystems`
   - `test_operations`, `dependencies`
   - `post_verification` → use `next_step`

4. **Update validation types**:
   - Ensure all checks have `severity` field
   - Use proper validation type enums

## Examples

### Complete Example
See `system_validation_viScript.json` for a complete working example.

### Minimal Example
```json
{
  "installation_type": "minimal_test",
  "version": "2.0",
  "description": "Minimal viScript example",
  "phases": [
    {
      "name": "basic_check",
      "description": "Basic system check",
      "checks": [
        {
          "name": "echo_test",
          "description": "Simple echo test",
          "command": "echo 'hello world'",
          "validation_type": "output_pattern",
          "expected_pattern": "hello world",
          "severity": "informational"
        }
      ]
    }
  ]
}
```

## Troubleshooting

### Common Issues

1. **Missing required fields**: Ensure all required fields are present
2. **Invalid validation types**: Use only supported validation types
3. **Missing severity**: All checks must have severity field
4. **Invalid patterns**: Test regex patterns against actual output
5. **Schema validation errors**: Use ajv for detailed schema validation

### Debugging

1. **Use verbose mode**: `./viscriptlint file.json --verbose`
2. **Check JSON syntax**: `jq empty file.json`
3. **Validate schema**: `ajv validate -s viscript_schema.json -d file.json`
4. **Test commands**: Run commands manually to verify output

## Version History

- **v2.0**: Current schema with removed unsupported attributes
- **v1.0**: Legacy schema (deprecated)

## References

- [JSON Schema Specification](https://json-schema.org/)
- [Verified Installer Documentation](../verified-installer/docs/VERIFIED_INSTALLER.md)
- [System Readiness Checklist](../ubuntu-btrfs-installer/docs/S2_SYSTEM_READINESS_CHECKLIST.md) 