# aiailint Build Environment

## Overview

This directory contains the build environment configuration for developing and testing the `aiailint` tool. The build environment provides an isolated Python environment with all necessary dependencies for development, testing, and deployment.

## Purpose

- **Isolated Development**: Provides a clean Python environment for aiailint development
- **Dependency Management**: Manages all required Python packages and their versions
- **Testing Framework**: Includes test runners and validation tools
- **CI/CD Integration**: Supports automated testing and deployment
- **Cross-Platform**: Works on Linux, macOS, and Windows

## Structure

```
build-env/
├── README.md                    # This file
├── requirements/                 # Python dependency specifications
│   ├── requirements.txt         # Production dependencies
│   ├── requirements-dev.txt     # Development dependencies
│   └── requirements-test.txt    # Testing dependencies
├── scripts/                     # Build and deployment scripts
│   ├── setup-env.sh            # Environment setup script
│   ├── run-tests.sh            # Test runner script
│   ├── build-package.sh        # Package building script
│   └── install-local.sh        # Local installation script
├── config/                      # Configuration files
│   ├── pyproject.toml          # Python project configuration
│   ├── setup.cfg               # Setup configuration
│   └── tox.ini                 # Tox testing configuration
├── docker/                      # Docker support
│   ├── Dockerfile              # Development container
│   └── docker-compose.yml      # Multi-service setup
└── ci/                         # CI/CD configuration
    ├── github-actions.yml      # GitHub Actions workflow
    └── gitlab-ci.yml          # GitLab CI configuration
```

## Quick Start

### 1. Setup Environment

```bash
# Navigate to build environment
cd devops/build-env

# Setup Python virtual environment
./scripts/setup-env.sh

# Activate environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

### 2. Install Dependencies

```bash
# Install all dependencies
pip install -r requirements/requirements-dev.txt

# Or install specific sets
pip install -r requirements/requirements.txt        # Production
pip install -r requirements/requirements-test.txt   # Testing
```

### 3. Run Tests

```bash
# Run all tests
./scripts/run-tests.sh

# Or run specific test suites
python -m pytest tests/ -v
python -m tox
```

### 4. Build Package

```bash
# Build distribution package
./scripts/build-package.sh

# Install locally
./scripts/install-local.sh
```

## Dependencies

### Production Dependencies
- `pyyaml>=6.0` - YAML parsing and processing
- `jsonschema>=4.0` - JSON Schema validation
- `bashlex>=0.16` - Bash command parsing (recommended)
- `bashparser>=0.1` - Alternative bash parser
- `libbash>=0.1` - Direct bash integration

### Development Dependencies
- `pytest>=7.0` - Testing framework
- `pytest-cov>=4.0` - Coverage reporting
- `black>=23.0` - Code formatting
- `flake8>=6.0` - Linting
- `mypy>=1.0` - Type checking
- `tox>=4.0` - Multi-environment testing

### Testing Dependencies
- `pytest-mock>=3.0` - Mocking support
- `pytest-xdist>=3.0` - Parallel test execution
- `coverage>=7.0` - Code coverage analysis

## Environment Setup

### Prerequisites

1. **Python 3.8+**: Required for modern Python features
2. **pip**: Package installer
3. **virtualenv**: Virtual environment management
4. **git**: Version control

### Automated Setup

The `setup-env.sh` script automates the entire setup process:

```bash
./scripts/setup-env.sh
```

This script:
- Creates a Python virtual environment
- Installs all dependencies
- Sets up pre-commit hooks
- Configures development tools
- Validates the setup

### Manual Setup

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements/requirements-dev.txt

# Install aiailint in development mode
pip install -e ../../aiailint/
```

## Testing

### Test Structure

```
tests/
├── unit/                      # Unit tests
│   ├── test_validators/      # Validator tests
│   ├── test_analyzers/       # Analyzer tests
│   └── test_utils/           # Utility tests
├── integration/               # Integration tests
│   ├── test_scripts/         # Script validation tests
│   └── test_packages/        # Package validation tests
├── functional/                # Functional tests
│   ├── test_cli/             # CLI interface tests
│   └── test_output/          # Output format tests
└── fixtures/                  # Test data
    ├── valid_scripts/        # Valid AIAI Scripts
    ├── invalid_scripts/      # Invalid AIAI Scripts
    └── packages/             # Test packages
```

### Running Tests

```bash
# Run all tests
./scripts/run-tests.sh

# Run specific test categories
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/functional/ -v

# Run with coverage
pytest --cov=aiailint tests/

# Run with specific markers
pytest -m "not slow" tests/
pytest -m "destructive" tests/
```

### Test Configuration

The test configuration is defined in:
- `pytest.ini` - Pytest configuration
- `tox.ini` - Multi-environment testing
- `setup.cfg` - Coverage and linting configuration

## Development Workflow

### 1. Code Quality

```bash
# Format code
black aiailint/

# Lint code
flake8 aiailint/

# Type checking
mypy aiailint/

# Run all quality checks
./scripts/quality-check.sh
```

### 2. Testing

```bash
# Run tests before committing
./scripts/run-tests.sh

# Run specific test suites
pytest tests/unit/test_validators/ -v
pytest tests/integration/test_scripts/ -v
```

### 3. Building

```bash
# Build package
./scripts/build-package.sh

# Install locally for testing
./scripts/install-local.sh
```

## Docker Support

### Development Container

```bash
# Build development container
docker build -f docker/Dockerfile -t aiailint-dev .

# Run container
docker run -it --rm -v $(pwd):/workspace aiailint-dev

# Or use docker-compose
docker-compose -f docker/docker-compose.yml up
```

### Multi-Stage Build

The Dockerfile includes:
- Development stage with all tools
- Testing stage for CI/CD
- Production stage for deployment

## CI/CD Integration

### GitHub Actions

The workflow in `ci/github-actions.yml` provides:
- Automated testing on multiple Python versions
- Code quality checks
- Coverage reporting
- Package building and publishing

### GitLab CI

The configuration in `ci/gitlab-ci.yml` includes:
- Multi-stage pipeline
- Docker-based testing
- Artifact management
- Deployment automation

## Configuration Files

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "aiailint"
version = "1.0.0"
description = "AIAI Script validation and linting tool"
authors = [{name = "AIAI Team"}]
license = {text = "MIT"}
requires-python = ">=3.8"
dependencies = [
    "pyyaml>=6.0",
    "jsonschema>=4.0",
    "bashlex>=0.16",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=23.0",
    "flake8>=6.0",
    "mypy>=1.0",
]
test = [
    "pytest-cov>=4.0",
    "pytest-mock>=3.0",
    "tox>=4.0",
]

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
```

### tox.ini

```ini
[tox]
envlist = py38, py39, py310, py311, py312
isolated_build = True

[testenv]
deps =
    pytest>=7.0
    pytest-cov>=4.0
    pytest-mock>=3.0
commands =
    pytest {posargs:tests/} --cov=aiailint --cov-report=term-missing
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated
2. **Permission Errors**: Check file permissions on scripts
3. **Dependency Conflicts**: Use `pip install --force-reinstall`
4. **Test Failures**: Check test data and fixtures

### Debug Mode

```bash
# Enable debug output
export AIAILINT_DEBUG=1
./scripts/run-tests.sh

# Verbose pytest output
pytest -v -s tests/
```

### Environment Validation

```bash
# Validate environment setup
./scripts/validate-env.sh
```

## Contributing

### Development Guidelines

1. **Environment Setup**: Always use the provided build environment
2. **Testing**: Write tests for all new functionality
3. **Code Quality**: Run quality checks before committing
4. **Documentation**: Update docs for new features

### Adding Dependencies

1. **Update requirements files**: Add to appropriate requirements file
2. **Update pyproject.toml**: Add to dependencies section
3. **Test installation**: Verify in clean environment
4. **Update documentation**: Document new dependencies

## License

This build environment follows the same license as the main AIAI project.

---

**Last Updated**: 2025-01-27  
**Version**: 1.0.0  
**Status**: Production Ready
