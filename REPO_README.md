# AIAI Packages Repository

A comprehensive collection of AIAI (AI Augmented Installation) packages, tools, and framework components for automated system installation and configuration.

## Repository Structure

```
aiai/
├── framework/                    # AIAI Framework Core
│   ├── docs/                    # Framework documentation
│   ├── src/                     # Framework source code
│   ├── templates/               # AIAI Script templates
│   └── tests/                   # Framework test suites
├── packages/                    # AIAI Package Collection
│   ├── ubuntu-btrfs-aiai/       # Ubuntu BTRFS Installation Package
│   │   ├── docs/                # Package documentation
│   │   ├── src/                 # AIAI Scripts for Ubuntu-BTRFS
│   │   └── tests/               # Package test suites
│   ├── cursor-aiai/             # Cursor AIAI Integration Package
│   │   ├── docs/                # Package documentation
│   │   ├── src/                 # AIAI Scripts for Cursor
│   │   └── tests/               # Package test suites
│   └── aiml-aiai/               # AI/ML AIAI Components Package
│       ├── docs/                # Package documentation
│       ├── src/                 # AIAI Scripts for ML workflows
│       └── tests/               # Package test suites
├── aiailint/                    # AIAI Script Linter
│   ├── docs/                    # Linter documentation
│   ├── src/                     # Linter source code
│   └── tests/                   # Linter test suites
├── s2m/                         # Script to Manual Converter
│   ├── docs/                    # Converter documentation
│   ├── src/                     # Converter source code
│   └── tests/                   # Converter test suites
└── devops/                      # DevOps automation component
    ├── docs/                    # DevOps documentation
    ├── src/                     # DevOps automation code
    ├── workflows/               # CI/CD workflow definitions
    ├── scripts/                 # Build/deployment scripts
    └── tests/                   # DevOps automation tests
```

## Components Overview

### Framework (`aiai/framework/`)
The core AIAI framework providing the foundation for all AIAI packages and tools.

**Purpose:** Core framework, templates, and shared components for AIAI development.

**Key Features:**
- AIAI Script specification and validation
- Template system for common installation patterns
- Shared utilities and components
- Framework documentation and guides

### Packages (`aiai/packages/`)
**Purpose:** Collection of AIAI packages for different installation and automation scenarios.

#### Ubuntu BTRFS AIAI (`packages/ubuntu-btrfs-aiai/`)
**Purpose:** Automated Ubuntu installation with BTRFS filesystem configuration.

**Features:**
- Complete Ubuntu installation automation
- BTRFS subvolume management
- System partitioning and configuration
- Boot loader setup and validation

#### Cursor AIAI (`packages/cursor-aiai/`)
**Purpose:** AIAI integration with Cursor IDE for enhanced development workflows.

**Features:**
- Cursor IDE integration scripts
- Development environment automation
- Code generation and validation
- IDE-specific AIAI Scripts

#### AIML AIAI (`packages/aiml-aiai/`)
**Purpose:** AI/ML workflow automation and model deployment scripts.

**Features:**
- ML model deployment automation
- Data pipeline configuration
- Model validation and testing
- ML infrastructure setup

### AIAI Linter (`aiai/aiailint/`)
**Purpose:** Validation and linting tool for AIAI Scripts.

**Features:**
- AIAI Script syntax validation
- Best practices enforcement
- Error detection and reporting
- Integration with CI/CD pipelines

### Script to Manual (`aiai/s2m/`)
**Purpose:** Convert AIAI Scripts to human-readable documentation.

**Features:**
- Automated documentation generation
- Installation manual creation
- Step-by-step guide generation
- Documentation templates

### DevOps (`aiai/devops/`)
**Purpose:** DevOps automation and CI/CD processes for the AIAI ecosystem.

**Features:**
- Build automation for all components
- Test automation and validation
- Release automation and asset management
- CI/CD pipeline configuration
- Deployment automation

## Getting Started

### Prerequisites
- Python 3.11+
- Git
- Basic understanding of AIAI Scripts

### Installation
```bash
# Clone the repository
git clone https://github.com/your-org/aiai-packages.git
cd aiai-packages

# Install framework dependencies
cd aiai/framework
pip install -r requirements.txt

# Install linter
cd ../aiailint
pip install -r requirements.txt

# Install script-to-manual converter
cd ../s2m
pip install -r requirements.txt
```

### Quick Start
```bash
# Validate an AIAI Script
cd aiai/aiailint
python src/aiailint.py ../packages/ubuntu-btrfs-aiai/scripts/*.yaml

# Generate documentation
cd ../s2m
python src/s2m.py ../packages/ubuntu-btrfs-aiai/scripts/installation.yaml

# Run framework tests
cd ../framework
python -m pytest tests/
```

## Development Guidelines

### Directory Structure Standards
Every directory contains:
- `README.md` - Directory-specific documentation
- `docs/` - Component documentation
- `tests/` - Test suites
- `src/` or `scripts/` - Source code or AIAI Scripts

### AIAI Script Standards
- Follow AIAI Script specification (see `aiai/framework/docs/`)
- Include comprehensive validation
- Provide clear documentation
- Include test coverage

### Contributing
1. Fork the repository
2. Create a feature branch
3. Follow the coding standards
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

## Package Development

### Creating a New Package
```bash
# Use the template system
cd framework/templates
python create_package.py --name "my-new-package" --type "installation"
```

### Package Structure Template
```
packages/my-new-package/
├── README.md                   # Package overview
├── MANIFEST                    # Package manifest
├── docs/
│   ├── OPERATOR_GUIDE.md      # Usage guide
│   └── INSTALLATION.md         # Installation instructions
├── src/
│   ├── main_installation.yaml  # Main AIAI Script
│   ├── validation.yaml         # Validation scripts
│   └── cleanup.yaml           # Cleanup scripts
└── tests/
    ├── test_installation.py    # Installation tests
    ├── test_validation.py      # Validation tests
    └── test_data/             # Test data files
```

## Testing Strategy

### Component Tests (`component/tests/`)
**Purpose:** Testing the component's core functionality and business logic

**Framework Tests (`framework/tests/`)**
- Unit tests for core components
- Integration tests for framework features
- Template validation tests

**Package Tests (`package/tests/`)**
- Installation validation
- AIAI Script syntax checking
- End-to-end installation tests
- Cross-platform compatibility
- Target system integration (e.g., Ubuntu/BTRFS for ubuntu-btrfs-aiai)

**Tool Tests (`tool/tests/`)**
- Linter functionality tests
- Script validation accuracy
- Documentation generation tests
- Tool integration tests

### DevOps Tests (`devops/tests/`)
**Purpose:** Testing the DevOps automation and CI/CD processes

**Build Automation Tests**
- Build script functionality
- Component build processes
- Artifact creation and validation
- Build environment configuration

**Release Automation Tests**
- Release script functionality
- GitHub release creation
- Asset upload processes
- Version management

**CI/CD Pipeline Tests**
- GitHub Actions workflow validation
- Pipeline configuration tests
- Automation reliability tests
- Deployment process validation

### Test Environment Differences

**Component Tests:**
- **Target system simulation** - Ubuntu/BTRFS environment for ubuntu-btrfs-aiai
- **AIAI Script execution** - Real script execution in target environment
- **Business logic validation** - Does the component meet user requirements?

**DevOps Tests:**
- **Automation environment** - Build/test/deploy environment
- **Script execution** - DevOps script execution and validation
- **Pipeline validation** - CI/CD pipeline functionality and reliability

### Example Test Scopes

**Component Test Example (ubuntu-btrfs-aiai/tests/):**
```python
def test_btrfs_subvolume_creation():
    """Test BTRFS subvolume creation AIAI Script"""
    script = load_aiai_script("scripts/create_subvolumes.yaml")
    result = execute_aiai_script(script)
    
    assert result.subvolumes_created
    assert result.mount_points_configured
    assert result.permissions_set_correctly
```

**DevOps Test Example (devops/tests/):**
```python
def test_build_ubuntu_package():
    """Test build automation for Ubuntu package"""
    result = run_build_script("scripts/build/build-component.sh ubuntu-btrfs-aiai")
    
    assert result.build_successful
    assert result.package_archive_created
    assert result.validation_passed
    assert result.artifacts_uploaded
```
a
## GitHub Configuration and Automation

### Repository Structure
```
aiai/
├── .github/                     # GitHub-specific configuration
│   ├── workflows/               # GitHub Actions workflows
│   │   ├── build-packages.yml   # Package build automation
│   │   ├── test-packages.yml    # Test automation
│   │   ├── release-packages.yml # Release automation
│   │   ├── lint-aiai-scripts.yml # AIAI Script validation
│   │   └── security-scan.yml    # Security scanning
│   ├── ISSUE_TEMPLATE/          # Issue templates
│   │   ├── bug_report.md        # Bug report template
│   │   ├── feature_request.md   # Feature request template
│   │   └── package_request.md   # New package request
│   ├── PULL_REQUEST_TEMPLATE.md # PR template
│   └── dependabot.yml           # Dependency updates
├── devops/                      # DevOps automation component
│   ├── docs/                    # DevOps documentation
│   ├── src/                     # DevOps automation code
│   ├── workflows/               # CI/CD workflow definitions
│   ├── scripts/                 # Build/deployment scripts
│   │   ├── build/
│   │   │   ├── build-all.sh     # Build all components
│   │   │   ├── build-component.sh # Build specific component
│   │   │   └── build-docs.sh    # Build documentation
│   │   ├── test/
│   │   │   ├── test-all.sh      # Run all tests
│   │   │   ├── test-components.sh # Test components
│   │   │   └── validate-scripts.sh # Validate AIAI Scripts
│   │   ├── release/
│   │   │   ├── create-release.sh # Create GitHub release
│   │   │   ├── upload-assets.sh  # Upload release assets
│   │   │   └── generate-changelog.sh # Generate changelog
│   │   └── maintenance/
│   │       ├── cleanup.sh       # Cleanup temporary files
│   │       └── backup.sh        # Backup important data
│   └── tests/                   # DevOps automation tests
```

### GitHub Actions Workflows

#### Build and Test Workflow (`.github/workflows/build-packages.yml`)
```yaml
name: Build and Test AIAI Components

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        component: [framework, packages/ubuntu-btrfs-aiai, packages/cursor-aiai, packages/aiml-aiai, aiailint, s2m]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r ${{ matrix.component }}/requirements.txt
      
      - name: Build ${{ matrix.component }}
        run: |
          ./devops/scripts/build/build-component.sh ${{ matrix.component }}
      
      - name: Test ${{ matrix.component }}
        run: |
          ./devops/scripts/test/test-components.sh ${{ matrix.component }}
      
      - name: Validate AIAI Scripts
        run: |
          ./devops/scripts/test/validate-scripts.sh ${{ matrix.component }}
```

#### Release Workflow (`.github/workflows/release-packages.yml`)
```yaml
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
      
      - name: Build all components
        run: ./devops/scripts/build/build-all.sh
      
      - name: Run all tests
        run: ./devops/scripts/test/test-all.sh
      
      - name: Generate documentation
        run: ./devops/scripts/build/build-docs.sh
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: AIAI Components Release ${{ github.ref }}
          body: |
            ## AIAI Components Release ${{ github.ref }}
            
            ### Components Included:
            - Framework
            - Ubuntu BTRFS AIAI Package
            - Cursor AIAI Package
            - AIML AIAI Package
            - AIAI Linter
            - Script to Manual Converter
            
            ### Changes:
            ${{ github.event.head_commit.message }}
          draft: false
          prerelease: false
      
      - name: Upload Component Assets
        run: ./devops/scripts/release/upload-assets.sh
```

#### Lint AIAI Scripts Workflow (`.github/workflows/lint-aiai-scripts.yml`)
```yaml
name: Lint AIAI Scripts

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install aiailint
        run: |
          cd aiailint
          pip install -r requirements.txt
      
      - name: Lint AIAI Scripts
        run: |
          python aiailint/src/aiailint.py \
            */scripts/*.yaml
```

### Automation Scripts

#### Build Scripts (`devops/scripts/build/`)

**build-all.sh:**
```bash
#!/bin/bash
set -e

echo "Building all AIAI components..."

# Build framework
echo "Building AIAI framework..."
cd aiai/framework
./scripts/build.sh
cd ..

# Build framework
echo "Building AIAI framework..."
cd framework
./scripts/build.sh
cd ..

# Build packages
echo "Building AIAI packages..."
cd packages
for package in */; do
    if [ -f "$package/scripts/build.sh" ]; then
        echo "Building $(basename $package)..."
        cd "$package"
        ./scripts/build.sh
        cd ..
    fi
done
cd ..

# Build tools
echo "Building AIAI tools..."
cd aiailint
./scripts/build.sh
cd ../s2m
./scripts/build.sh
cd ..

echo "All components built successfully!"
```

**build-component.sh:**
```bash
#!/bin/bash
set -e

COMPONENT_NAME=$1

if [ -z "$COMPONENT_NAME" ]; then
    echo "Usage: $0 <component-name>"
    exit 1
fi

COMPONENT_DIR="aiai/$COMPONENT_NAME"

if [ ! -d "$COMPONENT_DIR" ]; then
    echo "Component $COMPONENT_NAME not found"
    exit 1
fi

echo "Building component: $COMPONENT_NAME"

cd "$COMPONENT_DIR"

# Validate AIAI Scripts if they exist
if [ -d "scripts" ]; then
    python -m aiai.validator scripts/*.yaml
fi

# Create component archive
VERSION=$(git describe --tags --always)
ARCHIVE_NAME="${COMPONENT_NAME}-${VERSION}.tar.gz"

tar -czf "$ARCHIVE_NAME" \
    src/ \
    docs/ \
    tests/ \
    scripts/ \
    README.md \
    MANIFEST

echo "Component built: $ARCHIVE_NAME"
```

#### Test Scripts (`devops/scripts/test/`)

**test-all.sh:**
```bash
#!/bin/bash
set -e

echo "Running all tests..."

# Test framework
echo "Testing AIAI framework..."
cd aiai/framework
python -m pytest tests/
cd ..

# Test framework
echo "Testing AIAI framework..."
cd framework
python -m pytest tests/
cd ..

# Test packages
echo "Testing AIAI packages..."
cd packages
for package in */; do
    if [ -d "$package/tests" ]; then
        echo "Testing $(basename $package)..."
        cd "$package"
        python -m pytest tests/
        cd ..
    fi
done
cd ..

# Test tools
echo "Testing AIAI tools..."
cd aiailint
python -m pytest tests/
cd ../s2m
python -m pytest tests/
cd ..

echo "All tests passed!"
```

**validate-scripts.sh:**
```bash
#!/bin/bash
set -e

COMPONENT_NAME=$1

if [ -z "$COMPONENT_NAME" ]; then
    echo "Validating all AIAI Scripts..."
    # Validate framework scripts
    find framework/src/ -name "*.yaml" -exec python -m aiai.validator {} \;
    # Validate package scripts
    find packages/*/src/ -name "*.yaml" -exec python -m aiai.validator {} \;
else
    echo "Validating AIAI Scripts for $COMPONENT_NAME..."
    if [[ "$COMPONENT_NAME" == packages/* ]]; then
        python -m aiai.validator "$COMPONENT_NAME/src/"*.yaml
    else
        python -m aiai.validator "$COMPONENT_NAME/src/"*.yaml
    fi
fi
```

#### Release Scripts (`devops/scripts/release/`)

**create-release.sh:**
```bash
#!/bin/bash
set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: $0 <version>"
    exit 1
fi

echo "Creating release for version: $VERSION"

# Build all packages
./devops/scripts/build/build-all.sh

# Run all tests
./devops/scripts/test/test-all.sh

# Generate changelog
./devops/scripts/release/generate-changelog.sh "$VERSION"

# Create GitHub release
gh release create "$VERSION" \
    --title "AIAI Packages Release $VERSION" \
    --notes-file CHANGELOG.md \
    --draft

echo "Release created: $VERSION"
```

**upload-assets.sh:**
```bash
#!/bin/bash
set -e

VERSION=$(git describe --tags --always)

echo "Uploading assets for version: $VERSION"

# Upload framework archive
FRAMEWORK_ARCHIVE="framework-${VERSION}.tar.gz"
if [ -f "framework/$FRAMEWORK_ARCHIVE" ]; then
    echo "Uploading $FRAMEWORK_ARCHIVE..."
    gh release upload "$VERSION" "framework/$FRAMEWORK_ARCHIVE"
fi

# Upload package archives
cd packages
for package in */; do
    PACKAGE_NAME=$(basename $package)
    ARCHIVE_NAME="${PACKAGE_NAME}-${VERSION}.tar.gz"
    
    if [ -f "$package/$ARCHIVE_NAME" ]; then
        echo "Uploading $ARCHIVE_NAME..."
        gh release upload "$VERSION" "packages/$package/$ARCHIVE_NAME"
    fi
done
cd ..

# Upload tool archives
for tool in aiailint s2m; do
    TOOL_ARCHIVE="${tool}-${VERSION}.tar.gz"
    if [ -f "$tool/$TOOL_ARCHIVE" ]; then
        echo "Uploading $TOOL_ARCHIVE..."
        gh release upload "$VERSION" "$tool/$TOOL_ARCHIVE"
    fi
done

echo "All assets uploaded successfully!"
```

### GitHub Configuration Files

#### Issue Templates (`.github/ISSUE_TEMPLATE/`)

**bug_report.md:**
```markdown
---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: ['bug']
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment:**
 - OS: [e.g. Ubuntu 22.04]
 - AIAI Framework Version: [e.g. 1.0.0]
 - Package Version: [e.g. ubuntu-btrfs-aiai 1.0.0]

**Additional context**
Add any other context about the problem here.
```

**feature_request.md:**
```markdown
---
name: Feature Request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: ['enhancement']
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

#### Pull Request Template (`.github/PULL_REQUEST_TEMPLATE.md`)
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] AIAI Scripts validated
- [ ] Documentation updated

## Checklist
- [ ] Code follows the project's style guidelines
- [ ] Self-review of code completed
- [ ] Code is commented, particularly in hard-to-understand areas
- [ ] Corresponding changes to documentation made
- [ ] No new warnings generated
- [ ] Tests added that prove fix is effective or feature works
```

#### Dependabot Configuration (`.github/dependabot.yml`)
```yaml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5

  # Python dependencies for packages
  - package-ecosystem: "pip"
    directory: "/aiai/framework"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5

  - package-ecosystem: "pip"
    directory: "/aiai/aiailint"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

## Release Process

### Versioning
- Semantic versioning (MAJOR.MINOR.PATCH)
- Framework and packages versioned independently
- Release notes for each component

### Release Automation
```bash
# Create a release
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions will automatically:
# 1. Build all packages
# 2. Run test suites
# 3. Validate AIAI Scripts
# 4. Generate documentation
# 5. Create GitHub release
# 6. Upload package artifacts
```

## Documentation

### Framework Documentation
- `aiai/framework/docs/` - Core framework documentation
- API reference and usage guides
- Template system documentation

### Package Documentation
- Each package includes comprehensive documentation
- Installation guides and operator manuals
- Troubleshooting and FAQ sections

### Tool Documentation
- `aiai/aiailint/docs/` - Linter usage and configuration
- `aiai/s2m/docs/` - Documentation generation guide

## Community and Support

### Issues and Bug Reports
- Use GitHub Issues for bug reports
- Include detailed reproduction steps
- Provide environment information

### Feature Requests
- Submit feature requests via GitHub Issues
- Include use case and benefit description
- Consider implementation complexity

### Contributing Guidelines
- Follow the established coding standards
- Include tests for new functionality
- Update documentation for changes
- Review existing issues and PRs

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- AIAI Script specification contributors
- Ubuntu BTRFS community
- Cursor IDE team
- Open source contributors

---

**Note:** This repository follows the AIAI (AI Augmented Installation) specification and best practices. For more information about AIAI Scripts, see the framework documentation in `aiai/framework/docs/`. 