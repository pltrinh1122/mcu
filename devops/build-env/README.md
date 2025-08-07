# Build Environments

This directory contains specific build environments for different components of the AIAI ecosystem. Each subdirectory represents a dedicated build environment for a particular component or tool.

## Architecture

```
build-env/
├── README.md                    # This file
├── aiailint-dev/               # aiailint development environment
│   ├── README.md               # aiailint-specific documentation
│   ├── requirements/            # Python dependencies
│   ├── scripts/                # Build and test scripts
│   ├── config/                 # Configuration files
│   ├── docker/                 # Docker support
│   ├── ci/                     # CI/CD configuration
│   └── .vscode/               # IDE integration
├── framework-dev/              # Framework development environment (future)
├── s2m-dev/                   # Script2Manual development environment (future)
└── package-dev/               # Package development environment (future)
```

## Purpose

Each build environment provides:
- **Isolated Development**: Clean, isolated environment for specific components
- **Dependency Management**: Component-specific dependencies and versions
- **Testing Framework**: Dedicated testing tools and configurations
- **CI/CD Integration**: Component-specific automation
- **Documentation**: Component-specific guides and tutorials

## Available Environments

### aiailint-dev
**Purpose**: Development environment for the aiailint validation tool
**Features**:
- Python virtual environment with aiailint dependencies
- Comprehensive testing suite (unit, integration, functional)
- Code quality tools (black, flake8, mypy)
- Docker containerization support
- CI/CD pipeline with GitHub Actions
- Vibe coding debugging workflow
- Self-contained app distribution

**Quick Start**:
```bash
cd build-env/aiailint-dev
./scripts/setup-env.sh
```

## Adding New Environments

To add a new build environment:

1. **Create Environment Directory**:
   ```bash
   mkdir build-env/[component-name]-dev
   ```

2. **Copy Template Structure**:
   ```bash
   cp -r build-env/aiailint-dev/* build-env/[component-name]-dev/
   ```

3. **Customize for Component**:
   - Update requirements for component-specific dependencies
   - Modify scripts for component-specific build processes
   - Update documentation for component-specific usage
   - Adjust CI/CD configuration for component needs

4. **Update This README**:
   - Add new environment to the list
   - Document component-specific features
   - Provide quick start instructions

## Environment Standards

All build environments follow these standards:

### Directory Structure
```
[component]-dev/
├── README.md                    # Component-specific documentation
├── requirements/                # Dependency specifications
│   ├── requirements.txt        # Production dependencies
│   ├── requirements-dev.txt    # Development dependencies
│   └── requirements-test.txt   # Testing dependencies
├── scripts/                    # Build and deployment scripts
│   ├── setup-env.sh           # Environment setup
│   ├── run-tests.sh           # Test execution
│   ├── quality-check.sh       # Code quality checks
│   └── build-package.sh       # Package building
├── config/                     # Configuration files
│   ├── pyproject.toml         # Python project config
│   └── tox.ini                # Multi-environment testing
├── docker/                     # Docker support
│   ├── Dockerfile             # Container definition
│   └── docker-compose.yml     # Multi-service setup
├── ci/                        # CI/CD configuration
│   └── github-actions.yml     # GitHub Actions workflow
└── .vscode/                   # IDE integration
    ├── launch.json            # Debug configurations
    ├── settings.json          # Workspace settings
    └── tasks.json             # Custom tasks
```

### Required Scripts
- `setup-env.sh` - Environment setup and dependency installation
- `run-tests.sh` - Comprehensive testing suite
- `quality-check.sh` - Code quality and security analysis
- `build-package.sh` - Package building and distribution

### Required Documentation
- `README.md` - Comprehensive environment guide
- `QUICK_START.md` - Quick setup instructions
- Component-specific guides as needed

### Required Configuration
- `pyproject.toml` - Python project configuration
- `tox.ini` - Multi-environment testing
- GitHub Actions workflow for CI/CD

## Environment Isolation

Each environment is completely isolated:
- **Separate Virtual Environments**: Each component has its own Python environment
- **Component-Specific Dependencies**: Dependencies are tailored to each component
- **Isolated Testing**: Tests run in component-specific environments
- **Independent CI/CD**: Each component has its own automation pipeline

## Cross-Environment Development

For development involving multiple components:

1. **Set up each environment**:
   ```bash
   cd build-env/aiailint-dev && ./scripts/setup-env.sh
   cd ../framework-dev && ./scripts/setup-env.sh
   ```

2. **Use environment-specific commands**:
   ```bash
   # aiailint development
   cd build-env/aiailint-dev
   ./scripts/run-tests.sh
   
   # Framework development
   cd build-env/framework-dev
   ./scripts/run-tests.sh
   ```

3. **Cross-component testing** (when needed):
   ```bash
   # Test aiailint with framework changes
   cd build-env/aiailint-dev
   ./scripts/test-integration.sh ../framework-dev/
   ```

## Best Practices

### Environment Management
- **Always use virtual environments**: Never install dependencies globally
- **Pin dependency versions**: Use exact versions in requirements files
- **Test in clean environments**: Verify setup works in fresh environments
- **Document environment requirements**: Clearly specify prerequisites

### Development Workflow
- **Activate correct environment**: Always activate the right environment for your component
- **Run tests before committing**: Ensure all tests pass in the component environment
- **Update documentation**: Keep component-specific docs current
- **Use component-specific tools**: Use the tools and scripts provided for each environment

### CI/CD Integration
- **Environment-specific workflows**: Each component has its own CI/CD pipeline
- **Isolated testing**: Tests run in component-specific environments
- **Component-specific artifacts**: Build and deploy artifacts per component
- **Cross-component integration**: Test integration between components when needed

## Troubleshooting

### Common Issues

1. **Environment Conflicts**: Ensure you're in the correct environment directory
2. **Dependency Issues**: Use component-specific requirements files
3. **Script Permissions**: Make scripts executable with `chmod +x scripts/*.sh`
4. **Path Issues**: Use relative paths within each environment

### Environment Validation

```bash
# Validate environment setup
cd build-env/[component]-dev
./scripts/validate-env.sh
```

### Cross-Environment Debugging

```bash
# Debug environment interactions
cd build-env/aiailint-dev
./scripts/debug-integration.sh ../framework-dev/
```

## Contributing

When adding new build environments:

1. **Follow the standard structure**: Use the established directory and file structure
2. **Include all required scripts**: Ensure all standard scripts are present
3. **Update this README**: Add new environments to the documentation
4. **Test the environment**: Verify the environment works correctly
5. **Document component specifics**: Add component-specific documentation

## License

This build environment structure follows the same license as the main AIAI project.

---

**Last Updated**: 2025-01-27  
**Version**: 1.0.0  
**Status**: Production Ready
