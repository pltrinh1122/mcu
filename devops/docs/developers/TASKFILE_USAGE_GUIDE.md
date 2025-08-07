# Taskfile-Based Configuration Management - Usage Guide

## Overview

This guide provides comprehensive instructions for using the new Taskfile-based configuration management system. The system provides a unified interface for development workflows across all AIAI components with excellent developer experience and VIBE_CODING compliance.

**TL;DR**: Use the three main wrapper scripts (`setup.sh`, `test.sh`, `deploy.sh`) for all development operations. The system provides 50+ tasks across multiple namespaces with comprehensive validation and error handling.

## Quick Start

### **1. Setup Environment**
```bash
cd devops/build-env
./scripts/setup.sh
```

### **2. Run Tests**
```bash
# Run all tests
./scripts/test.sh all

# Run specific test types
./scripts/test.sh unit
./scripts/test.sh integration
./scripts/test.sh quality
```

### **3. Deploy**
```bash
# Build and package
./scripts/deploy.sh build

# Deploy to local environment
./scripts/deploy.sh local

# Full deployment pipeline
./scripts/deploy.sh full
```

## System Architecture

### **Core Components**
```
devops/build-env/
├── templates/                    # Reusable task templates
│   ├── base-tasks.yml           # Base tasks (setup, clean, help)
│   ├── python-tasks.yml         # Python-specific tasks
│   ├── docker-tasks.yml         # Docker-specific tasks
│   └── deploy-tasks.yml         # Deployment tasks
├── environments/
│   └── aiailint-dev/
│       ├── Taskfile.yml         # Master Taskfile with includes
│       ├── aiailint-tasks.yml   # Component-specific overrides
│       └── requirements/         # Component dependencies
└── scripts/                      # Wrapper scripts
    ├── setup.sh                  # Environment setup with validation
    ├── test.sh                   # Comprehensive testing interface
    └── deploy.sh                 # Multi-target deployment interface
```

### **Task Organization**
- **Base Namespace**: Common tasks (setup, clean, help, status)
- **Python Namespace**: Python-specific tasks (install, test, build, quality)
- **Docker Namespace**: Docker tasks (build, run, stop, logs)
- **Deploy Namespace**: Deployment tasks (package, deploy-local, deploy-staging)
- **Component Namespace**: Component-specific tasks (aiailint:lint, aiailint:validate)

## Wrapper Scripts

### **setup.sh - Environment Setup**
```bash
# Basic setup
./scripts/setup.sh

# Setup with verbose output
./scripts/setup.sh --verbose

# Setup with help
./scripts/setup.sh --help
```

**Features**:
- Environment validation and prerequisite checking
- Task availability verification
- Colored output with professional formatting
- Comprehensive error handling
- Help system with usage examples

### **test.sh - Comprehensive Testing**
```bash
# Test types available
./scripts/test.sh unit          # Unit tests
./scripts/test.sh integration   # Integration tests
./scripts/test.sh quality       # Code quality checks
./scripts/test.sh component     # Component-specific tests
./scripts/test.sh validation    # Validation tests
./scripts/test.sh health        # Health checks
./scripts/test.sh all           # All tests
```

**Features**:
- Multiple test types with clear separation
- Automatic test discovery and execution
- Comprehensive error reporting
- Performance monitoring
- Test result aggregation

### **deploy.sh - Multi-Target Deployment**
```bash
# Deployment types available
./scripts/deploy.sh build       # Build and package
./scripts/deploy.sh package     # Create distribution package
./scripts/deploy.sh local       # Deploy to local environment
./scripts/deploy.sh docker      # Deploy using Docker
./scripts/deploy.sh staging     # Deploy to staging environment
./scripts/deploy.sh production  # Deploy to production
./scripts/deploy.sh full        # Complete deployment pipeline
```

**Features**:
- Multi-target deployment support
- Post-deployment health checks
- Comprehensive error handling
- Deployment validation
- Rollback capability

## Direct Task Usage

### **Task Discovery**
```bash
# List all available tasks
task --list

# List tasks with details
task --list-all

# List tasks in specific namespace
task --list | grep "base:"
task --list | grep "python:"
task --list | grep "aiailint:"
```

### **Common Task Patterns**

#### **Base Tasks**
```bash
# Environment setup
task base:setup

# Clean environment
task base:clean

# Show help
task base:help

# Show status
task base:status
```

#### **Python Tasks**
```bash
# Install dependencies
task python:install

# Run tests
task python:test

# Build package
task python:build

# Code quality checks
task python:quality
```

#### **Component-Specific Tasks**
```bash
# aiailint-specific tasks
task aiailint:lint
task aiailint:validate
task aiailint:test-aiailint
task aiailint:install-aiailint
task aiailint:build-aiailint
task aiailint:docs
task aiailint:clean-aiailint
task aiailint:check
```

#### **Docker Tasks**
```bash
# Build Docker image
task docker:build

# Run container
task docker:run

# Stop container
task docker:stop

# View logs
task docker:logs
```

#### **Deployment Tasks**
```bash
# Package for distribution
task deploy:package

# Deploy to local
task deploy:deploy-local

# Deploy to staging
task deploy:deploy-staging

# Deploy to production
task deploy:deploy-production
```

## Development Workflows

### **New Feature Development**
```bash
# 1. Setup environment
./scripts/setup.sh

# 2. Run tests to ensure clean state
./scripts/test.sh all

# 3. Make changes to code

# 4. Run quality checks
./scripts/test.sh quality

# 5. Run unit tests
./scripts/test.sh unit

# 6. Run integration tests
./scripts/test.sh integration

# 7. Deploy locally for testing
./scripts/deploy.sh local
```

### **Bug Fix Workflow**
```bash
# 1. Identify the issue
./scripts/test.sh all

# 2. Run specific failing tests
./scripts/test.sh unit
./scripts/test.sh integration

# 3. Make fixes

# 4. Validate fixes
./scripts/test.sh all

# 5. Deploy fix
./scripts/deploy.sh local
```

### **Release Preparation**
```bash
# 1. Ensure clean environment
./scripts/setup.sh

# 2. Run comprehensive tests
./scripts/test.sh all

# 3. Build package
./scripts/deploy.sh build

# 4. Deploy to staging
./scripts/deploy.sh staging

# 5. Deploy to production
./scripts/deploy.sh production
```

## Configuration Management

### **Component-Specific Configuration**
Each component can have its own configuration in the `environments/` directory:

```yaml
# environments/aiailint-dev/aiailint-tasks.yml
version: '3'

tasks:
  lint:
    desc: "Run aiailint-specific linting"
    cmds:
      - echo "Running aiailint linting..."
      - python -m aiailint src/

  validate:
    desc: "Run aiailint validation"
    cmds:
      - echo "Running aiailint validation..."
      - python -m aiailint --validate src/
```

### **Template Customization**
Templates can be customized for specific components:

```yaml
# environments/aiailint-dev/Taskfile.yml
version: '3'

includes:
  base: ../templates/base-tasks.yml
  python: ../templates/python-tasks.yml
  docker: ../templates/docker-tasks.yml
  deploy: ../templates/deploy-tasks.yml

# Component-specific overrides
tasks:
  setup:
    desc: "Setup aiailint development environment"
    cmds:
      - task: base:setup
      - echo "Setting up aiailint-specific environment..."
      - pip install -r requirements/requirements.txt
```

## Best Practices

### **Task Organization**
1. **Use namespaces**: Organize tasks by functionality (base, python, docker, deploy)
2. **Component isolation**: Keep component-specific tasks in component namespaces
3. **Template reuse**: Use templates for common patterns
4. **Clear descriptions**: Provide descriptive task descriptions

### **Error Handling**
1. **Validate prerequisites**: Check for required tools and dependencies
2. **Provide clear error messages**: Use descriptive error messages
3. **Include help information**: Add `--help` options to wrapper scripts
4. **Graceful degradation**: Handle missing tools gracefully

### **Performance Optimization**
1. **Parallel execution**: Use Task's parallel execution where safe
2. **Caching**: Leverage Task's caching for expensive operations
3. **Selective testing**: Run only relevant tests for changes
4. **Incremental builds**: Use incremental build patterns

### **Security Considerations**
1. **Validate inputs**: Check all user inputs and parameters
2. **Safe defaults**: Provide safe default values
3. **Permission checks**: Verify required permissions before operations
4. **Audit trails**: Log important operations for audit purposes

## Troubleshooting

### **Common Issues**

#### **Task Not Found**
```bash
# Check if task exists
task --list | grep "task-name"

# Check namespace
task --list | grep "namespace:"

# Verify Taskfile syntax
task --dry task-name
```

#### **Template Inclusion Issues**
```bash
# Check template file exists
ls templates/template-name.yml

# Verify include syntax
cat environments/component/Taskfile.yml

# Test template inclusion
task --list | grep "template:"
```

#### **Wrapper Script Errors**
```bash
# Check script permissions
ls -la scripts/

# Run with verbose output
./scripts/script-name.sh --verbose

# Check for missing dependencies
./scripts/script-name.sh --help
```

### **Debugging Commands**
```bash
# Show task details
task --list-all

# Dry run (show commands without executing)
task --dry task-name

# Verbose output
task --verbose task-name

# Show task dependencies
task --summary task-name
```

## Integration with VIBE_CODING

### **Validation Compliance**
- **YAML validation**: All Taskfiles validated with proper syntax
- **Shell validation**: All wrapper scripts validated with shellcheck
- **Template validation**: Template inclusion functionality tested
- **Component validation**: Component-specific tasks validated

### **Testing Compliance**
- **Unit tests**: Component-specific unit tests available
- **Integration tests**: Cross-component integration testing
- **Quality tests**: Code quality and style checking
- **Health tests**: System health and functionality verification

### **Documentation Compliance**
- **Professional tone**: No emojis, clear technical language
- **Comprehensive coverage**: All aspects documented
- **Actionable content**: Clear instructions and examples
- **Structured format**: Consistent organization and formatting

## Future Enhancements

### **Planned Features**
1. **Additional component environments**: framework-dev, s2m-dev, package-dev
2. **CI/CD integration**: GitHub Actions and other CI/CD platforms
3. **Performance monitoring**: Execution time tracking and optimization
4. **Advanced templating**: More sophisticated template customization

### **Extension Points**
1. **Custom task templates**: Create new task templates for specific patterns
2. **Component-specific overrides**: Add component-specific task overrides
3. **Wrapper script extensions**: Extend wrapper scripts with additional functionality
4. **Integration patterns**: Add integration with external tools and services

## Support and Resources

### **Documentation**
- **This guide**: Comprehensive usage instructions
- **../architects/TASKFILE_PROGRESS.md**: System development status and history
- **../architects/TASKFILE_ARCHITECTURE.md**: System design and architecture
- **TASKFILE_TRAINING.md**: Comprehensive training program
- **Component-specific docs**: Individual component documentation

### **Help Resources**
```bash
# Get help for wrapper scripts
./scripts/setup.sh --help
./scripts/test.sh --help
./scripts/deploy.sh --help

# Get help for tasks
task base:help
task python:help
task aiailint:help
```

### **Community and Support**
- **Issue tracking**: Report issues through project issue tracker
- **Documentation updates**: Keep documentation current with system changes
- **Best practices**: Share and document best practices
- **Training materials**: Create training materials for new team members

---

*This usage guide provides comprehensive instructions for the Taskfile-based configuration management system. For technical details and architecture information, see ../architects/TASKFILE_ARCHITECTURE.md. For system status and progress, see ../architects/TASKFILE_PROGRESS.md.*
