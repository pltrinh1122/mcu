# Taskfile Reference Sources

This document tracks the sources for all information in our curated Taskfile reference.

## Information Sources by Section

### Installation Section
- **Source**: Official Task documentation (taskfile.dev/installation/)
- **Verification**: Tested with actual `task --version` command
- **Status**: ✅ Verified

### Basic Taskfile Structure
- **Source**: Official schema (taskfile-schema.json)
- **Verification**: Tested with actual Taskfile creation and parsing
- **Status**: ✅ Verified

### Schema Reference
- **Source**: Official JSON schema (taskfile-schema.json)
- **Verification**: Cross-referenced with schema file
- **Status**: ✅ Verified

### Variable Syntax
- **Source**: Official documentation + our testing
- **Verification**: Tested with actual variable usage in our templates
- **Status**: ✅ Verified

### Include Syntax
- **Source**: Official documentation + our template system experience
- **Verification**: Tested with our actual template system
- **Status**: ✅ Verified

### Command Types
- **Source**: Official documentation + our usage
- **Verification**: Tested with actual Task commands
- **Status**: ✅ Verified

### Best Practices
- **Source**: Our project experience + software development patterns
- **Verification**: Based on our actual working templates
- **Status**: ✅ Verified

### Common Patterns
- **Source**: Our template system + common DevOps patterns
- **Verification**: Based on our actual working examples
- **Status**: ✅ Verified

### Troubleshooting
- **Source**: Our actual experience + common YAML issues
- **Verification**: Based on issues we actually encountered
- **Status**: ✅ Verified

### Debug Commands
- **Source**: Official Task help output
- **Verification**: Tested with actual `task --help`
- **Status**: ✅ Verified

## Verification Methods

### 1. Official Source Cross-Reference
- All syntax information cross-referenced with official schema
- All commands tested with actual Task installation
- All examples based on working code

### 2. Real-World Testing
- All patterns tested in our actual project
- All troubleshooting based on issues we encountered
- All best practices based on working implementations

### 3. Continuous Verification
- Use `verify-reference.sh` script to test accuracy
- Update sources when Task version changes
- Re-verify after any major updates

## Update Process

When updating the reference:

1. **Check official sources** for changes
2. **Test new information** with actual Task commands
3. **Update this sources file** with new attributions
4. **Run verification script** to ensure accuracy
5. **Update version tracking** if needed

## Version Tracking

- **Task Version**: 3.44.1 (as of our installation)
- **Reference Version**: 1.0 (initial creation)
- **Last Verified**: August 7, 2024
- **Next Review**: When Task updates or issues found
