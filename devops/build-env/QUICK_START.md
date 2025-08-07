# aiailint Build Environment - Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- Git
- Bash shell

## Quick Setup (5 minutes)

### 1. Navigate to Build Environment

```bash
cd devops/build-env
```

### 2. Run Setup Script

```bash
./scripts/setup-env.sh
```

This script will:
- ✅ Create a Python virtual environment
- ✅ Install all dependencies
- ✅ Set up pre-commit hooks
- ✅ Configure development tools
- ✅ Validate the setup

### 3. Activate Environment

```bash
source venv/bin/activate
```

### 4. Verify Installation

```bash
# Check if aiailint is available
aiailint --help

# Run a quick test
./scripts/run-tests.sh unit
```

## Common Commands

### Development Workflow

```bash
# Run quality checks
./scripts/quality-check.sh

# Run all tests
./scripts/run-tests.sh

# Build package
./scripts/build-package.sh
```

### Docker Development

```bash
# Start development container
docker-compose --profile dev up

# Run tests in container
docker-compose --profile test up

# Run quality checks in container
docker-compose --profile quality up
```

### CI/CD Integration

The build environment includes:
- GitHub Actions workflow
- Multi-environment testing with tox
- Docker containerization
- Automated quality checks

## Troubleshooting

### Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf venv/
./scripts/setup-env.sh
```

### Dependency Issues

```bash
# Reinstall dependencies
pip install -r requirements/requirements-dev.txt --force-reinstall
```

### Permission Issues

```bash
# Make scripts executable
chmod +x scripts/*.sh
```

## Next Steps

1. **Explore the codebase**: Check out `aiailint/src/` for the main tool
2. **Run tests**: Use `./scripts/run-tests.sh` to run different test suites
3. **Quality checks**: Use `./scripts/quality-check.sh` for code quality
4. **Build packages**: Use `./scripts/build-package.sh` to create distributions
5. **Docker development**: Use `docker-compose` for containerized development

## Support

- **Documentation**: See `README.md` for detailed documentation
- **Issues**: Check the main project repository for known issues
- **Development**: Follow the development guidelines in the main README

---

**Ready to develop!** 🚀
