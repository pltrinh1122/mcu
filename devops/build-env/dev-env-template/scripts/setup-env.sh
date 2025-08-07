#!/bin/bash

# aiailint Build Environment Setup Script
# This script sets up a complete development environment for aiailint

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    local python_cmd="$1"
    local version
    
    if command_exists "$python_cmd"; then
        version=$("$python_cmd" --version 2>&1 | cut -d' ' -f2)
        print_status "Found $python_cmd version $version"
        
        # Extract major and minor version
        local major=$(echo "$version" | cut -d'.' -f1)
        local minor=$(echo "$version" | cut -d'.' -f2)
        
        if [ "$major" -ge 3 ] && [ "$minor" -ge 8 ]; then
            print_success "Python version $version is compatible"
            return 0
        else
            print_error "Python version $version is too old. Need Python 3.8+"
            return 1
        fi
    else
        print_error "$python_cmd not found"
        return 1
    fi
}

# Function to create virtual environment
create_venv() {
    local python_cmd="$1"
    local venv_dir="$2"
    
    print_status "Creating virtual environment in $venv_dir"
    
    if [ -d "$venv_dir" ]; then
        print_warning "Virtual environment already exists at $venv_dir"
        read -p "Do you want to recreate it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Removing existing virtual environment"
            rm -rf "$venv_dir"
        else
            print_status "Using existing virtual environment"
            return 0
        fi
    fi
    
    "$python_cmd" -m venv "$venv_dir"
    print_success "Virtual environment created"
}

# Function to install dependencies
install_dependencies() {
    local venv_dir="$1"
    local requirements_dir="$2"
    
    print_status "Installing dependencies"
    
    # Activate virtual environment
    source "$venv_dir/bin/activate"
    
    # Upgrade pip
    print_status "Upgrading pip"
    pip install --upgrade pip
    
    # Install production dependencies
    print_status "Installing production dependencies"
    pip install -r "$requirements_dir/requirements.txt"
    
    # Install development dependencies
    print_status "Installing development dependencies"
    pip install -r "$requirements_dir/requirements-dev.txt"
    
    # Install aiailint in development mode
    print_status "Installing aiailint in development mode"
    pip install -e ../../../aiailint/
    
    print_success "Dependencies installed successfully"
}

# Function to setup pre-commit hooks
setup_pre_commit() {
    local venv_dir="$1"
    
    print_status "Setting up pre-commit hooks"
    
    # Activate virtual environment
    source "$venv_dir/bin/activate"
    
    # Install pre-commit
    pip install pre-commit
    
    # Setup pre-commit hooks
    pre-commit install
    
    print_success "Pre-commit hooks configured"
}

# Function to validate setup
validate_setup() {
    local venv_dir="$1"
    
    print_status "Validating setup"
    
    # Activate virtual environment
    source "$venv_dir/bin/activate"
    
    # Check if aiailint is available
    if command_exists aiailint; then
        print_success "aiailint command is available"
    else
        print_error "aiailint command not found"
        return 1
    fi
    
    # Check if pytest is available
    if command_exists pytest; then
        print_success "pytest is available"
    else
        print_error "pytest not found"
        return 1
    fi
    
    # Check if black is available
    if command_exists black; then
        print_success "black is available"
    else
        print_error "black not found"
        return 1
    fi
    
    # Run basic test
    print_status "Running basic validation test"
    if python -c "import aiailint; print('aiailint module imported successfully')" 2>/dev/null; then
        print_success "aiailint module can be imported"
    else
        print_error "Failed to import aiailint module"
        return 1
    fi
    
    print_success "Setup validation completed"
}

# Function to create configuration files
create_config_files() {
    local config_dir="$1"
    
    print_status "Creating configuration files"
    
    # Create config directory if it doesn't exist
    mkdir -p "$config_dir"
    
    # Create pytest.ini if it doesn't exist
    if [ ! -f "$config_dir/pytest.ini" ]; then
        cat > "$config_dir/pytest.ini" << 'EOF'
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    destructive: marks tests that may be destructive
EOF
        print_success "Created pytest.ini"
    fi
    
    # Create .flake8 if it doesn't exist
    if [ ! -f "$config_dir/.flake8" ]; then
        cat > "$config_dir/.flake8" << 'EOF'
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = 
    .git,
    __pycache__,
    .venv,
    venv,
    build,
    dist,
    *.egg-info
EOF
        print_success "Created .flake8"
    fi
    
    # Create .coveragerc if it doesn't exist
    if [ ! -f "$config_dir/.coveragerc" ]; then
        cat > "$config_dir/.coveragerc" << 'EOF'
[run]
source = aiailint
omit = 
    */tests/*
    */test_*
    */__pycache__/*
    */venv/*
    */.venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod
EOF
        print_success "Created .coveragerc"
    fi
}

# Main function
main() {
    print_status "Starting aiailint build environment setup"
    
    # Get script directory
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    BUILD_ENV_DIR="$(dirname "$SCRIPT_DIR")"
    REQUIREMENTS_DIR="$BUILD_ENV_DIR/requirements"
    CONFIG_DIR="$BUILD_ENV_DIR/config"
    VENV_DIR="$BUILD_ENV_DIR/venv"
    
    # Check if we're in the right directory
    if [ ! -f "$REQUIREMENTS_DIR/requirements.txt" ]; then
        print_error "requirements.txt not found. Please run this script from the build-env directory."
        exit 1
    fi
    
    print_status "Build environment directory: $BUILD_ENV_DIR"
    
    # Check Python availability
    PYTHON_CMD=""
    for cmd in python3 python; do
        if check_python_version "$cmd"; then
            PYTHON_CMD="$cmd"
            break
        fi
    done
    
    if [ -z "$PYTHON_CMD" ]; then
        print_error "No compatible Python version found. Please install Python 3.8+"
        exit 1
    fi
    
    # Create virtual environment
    create_venv "$PYTHON_CMD" "$VENV_DIR"
    
    # Install dependencies
    install_dependencies "$VENV_DIR" "$REQUIREMENTS_DIR"
    
    # Setup pre-commit hooks
    setup_pre_commit "$VENV_DIR"
    
    # Create configuration files
    create_config_files "$CONFIG_DIR"
    
    # Validate setup
    validate_setup "$VENV_DIR"
    
    print_success "aiailint build environment setup completed successfully!"
    echo
    print_status "To activate the environment, run:"
    echo "  source $VENV_DIR/bin/activate"
    echo
    print_status "To run tests, use:"
    echo "  ./scripts/run-tests.sh"
    echo
    print_status "To run quality checks, use:"
    echo "  ./scripts/quality-check.sh"
    echo
    print_status "To build the package, use:"
    echo "  ./scripts/build-package.sh"
}

# Run main function
main "$@"
