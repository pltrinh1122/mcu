# Developers Documentation

This directory contains documentation specifically for application developers working with the AIAI ecosystem.

## Contents

### **TASKFILE_USAGE_GUIDE.md**
Comprehensive guide for the Taskfile-based configuration management system:
- System architecture and component relationships
- Wrapper scripts for common development tasks
- Task discovery and direct usage patterns
- Development workflows and best practices
- Troubleshooting and debugging techniques

### **TASKFILE_TRAINING.md**
Comprehensive training program with 7 modules:
- System overview and architecture
- Wrapper scripts and basic operations
- Task discovery and direct usage
- Component environment creation
- Development workflows
- Troubleshooting and debugging
- VIBE_CODING compliance

## Quick Start

```bash
# View usage guide
cat TASKFILE_USAGE_GUIDE.md

# Access training materials
cat TASKFILE_TRAINING.md

# Setup development environment
cd ../../build-env
./scripts/setup.sh

# Run tests
./scripts/test.sh all

# Deploy locally
./scripts/deploy.sh local
```

## Key Development Areas

### **Taskfile-Based Configuration Management**
- 50+ tasks across multiple namespaces
- Template system for reusable patterns
- Component-specific environments
- Wrapper scripts for simplified interface

### **Development Workflows**
- Feature development workflow
- Bug fix workflow
- Release preparation workflow
- Quality assurance processes

### **Component Development**
- Creating new component environments
- Customizing templates for specific needs
- Component-specific task overrides
- Requirements management

### **Testing and Validation**
- Unit testing strategies
- Integration testing approaches
- Quality checks and linting
- Performance testing

## Development Standards

### **VIBE_CODING Compliance**
- Professional communication without emojis
- Comprehensive validation and error handling
- Component discovery and requirement incorporation
- Clear, actionable documentation

### **Code Quality**
- Syntax validation for all file types
- Comprehensive testing before commits
- Professional documentation standards
- Error handling and graceful degradation

## Related Documentation

- **../devops/**: DevOps automation and infrastructure
- **../architects/**: System architecture and design
- **../operators/**: User profiles and role definitions
- **../references/**: Technical specifications and schemas

---

*This documentation supports developers in building and maintaining AIAI ecosystem components with high quality and consistency.*
