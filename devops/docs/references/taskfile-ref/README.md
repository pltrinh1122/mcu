# Taskfile References

This directory contains all Taskfile-related documentation and reference materials.

## Files

### Core Reference
- **`TASKFILE_REFERENCE.md`** - Comprehensive Taskfile reference guide with schema, usage examples, and best practices

### Official Documentation
- **`taskfile-schema.json`** - Official JSON schema for Taskfile validation
- **`taskfile-usage.md`** - Official usage documentation from taskfile.dev
- **`taskfile-installation.md`** - Official installation documentation from taskfile.dev
- **`taskfile-readme.md`** - GitHub README with overview and examples

## Usage

These references should be included in the AI context when working on DevOps projects to ensure:

- **Accurate Taskfile syntax and structure**
- **Proper use of includes and namespacing**
- **Best practices for task organization**
- **Effective error handling and debugging**
- **Optimal integration patterns**

## Key Topics Covered

### Schema and Structure
- Taskfile version and format
- Task properties and attributes
- Variable syntax and scope
- Include system and namespacing

### Best Practices
- Task organization patterns
- Template-based architecture
- Variable management strategies
- Error handling approaches
- Conditional execution patterns

### Integration Patterns
- Docker integration
- Python development workflows
- CI/CD pipeline integration
- Shell script integration
- Makefile compatibility

### Troubleshooting
- Common YAML syntax errors
- Task name conflicts
- Variable scope issues
- Include problems
- Debug commands and techniques

## Maintenance

These references should be updated periodically to ensure they reflect the latest versions and best practices of Task.

## Quick Reference

```bash
# List all tasks
task --list

# Show task details
task --list-all

# Run with verbose output
task --verbose task-name

# Dry run (show commands without executing)
task --dry task-name

# Show task dependencies
task --summary task-name
```

## Resources

- [Official Documentation](https://taskfile.dev/)
- [GitHub Repository](https://github.com/go-task/task)
- [Schema Definition](https://taskfile.dev/schema.json)
- [Examples](https://github.com/go-task/task/tree/main/examples)
