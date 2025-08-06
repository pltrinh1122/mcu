# DevOps Automation Usage Guide

## Overview

The DevOps automation component provides comprehensive build, test, and deployment automation for the AIAI ecosystem.

## Features

- **Build Automation**: Automated building of all components
- **Test Automation**: Comprehensive test suites and validation
- **Release Automation**: Automated release creation and asset management
- **CI/CD Pipelines**: GitHub Actions workflows and automation
- **Deployment**: Automated deployment processes

## Installation

```bash
cd devops
pip install -r requirements.txt
```

## Usage

### Build Automation

```bash
# Build all components
./scripts/build/build-all.sh

# Build specific component
./scripts/build/build-component.sh ubuntu-btrfs-aiai

# Build with custom options
./scripts/build/build-all.sh --parallel --clean
```

### Test Automation

```bash
# Run all tests
./scripts/test/test-all.sh

# Test specific components
./scripts/test/test-components.sh framework ubuntu-btrfs-aiai

# Validate AIAI Scripts
./scripts/test/validate-scripts.sh
```

### Release Automation

```bash
# Create a release
./scripts/release/create-release.sh v1.0.0

# Upload release assets
./scripts/release/upload-assets.sh v1.0.0

# Generate changelog
./scripts/release/generate-changelog.sh v1.0.0
```

### Maintenance

```bash
# Cleanup temporary files
./scripts/maintenance/cleanup.sh

# Backup important data
./scripts/maintenance/backup.sh
```

## GitHub Actions Integration

### Build and Test Workflow

```yaml
# .github/workflows/build-components.yml
name: Build and Test AIAI Components

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Build and Test
        run: |
          ./devops/scripts/build/build-all.sh
          ./devops/scripts/test/test-all.sh
```

### Release Workflow

```yaml
# .github/workflows/release-components.yml
name: Release AIAI Components

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Create Release
        run: ./devops/scripts/release/create-release.sh ${{ github.ref_name }}
```

## Configuration

### Build Configuration

```yaml
# devops-config.yaml
build:
  parallel: true
  clean_build: false
  components:
    - framework
    - packages/ubuntu-btrfs-aiai
    - packages/cursor-aiai
    - packages/aiml-aiai
    - aiailint
    - s2m
```

### Test Configuration

```yaml
test:
  framework:
    - unit_tests
    - integration_tests
  packages:
    - installation_tests
    - validation_tests
  tools:
    - functionality_tests
    - integration_tests
```

### Release Configuration

```yaml
release:
  github_token: ${{ secrets.GITHUB_TOKEN }}
  assets:
    - "*.tar.gz"
    - "*.zip"
  changelog:
    format: "markdown"
    include_commits: true
```

## Monitoring and Logging

### Build Logs

```bash
# View build logs
tail -f logs/build.log

# Filter build errors
grep "ERROR" logs/build.log
```

### Test Results

```bash
# Generate test report
./scripts/test/generate-report.sh

# View test coverage
./scripts/test/coverage-report.sh
```

## Troubleshooting

### Common Issues

1. **Build Failures**: Check component dependencies and requirements
2. **Test Failures**: Verify test environment and dependencies
3. **Release Issues**: Ensure GitHub token has proper permissions

### Debug Mode

```bash
# Enable debug logging
export DEBUG=1
./scripts/build/build-all.sh
```

## Contributing

See the main repository documentation for contribution guidelines. 