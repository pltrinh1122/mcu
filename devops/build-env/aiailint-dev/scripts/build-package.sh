#!/bin/bash

# aiailint Package Building Script
# This script builds distribution packages for aiailint

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

# Function to check if virtual environment is activated
check_venv() {
    if [ -z "$VIRTUAL_ENV" ]; then
        print_warning "Virtual environment not detected"
        print_status "Attempting to activate virtual environment"
        
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        BUILD_ENV_DIR="$(dirname "$SCRIPT_DIR")"
        VENV_DIR="$BUILD_ENV_DIR/venv"
        
        if [ -d "$VENV_DIR" ]; then
            source "$VENV_DIR/bin/activate"
            print_success "Virtual environment activated"
        else
            print_error "Virtual environment not found at $VENV_DIR"
            print_status "Please run ./scripts/setup-env.sh first"
            exit 1
        fi
    else
        print_success "Virtual environment is active: $VIRTUAL_ENV"
    fi
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to clean build artifacts
clean_build() {
    print_status "Cleaning build artifacts"
    
    local build_dir="../../../aiailint"
    
    if [ -d "$build_dir" ]; then
        cd "$build_dir"
        
        # Remove build directories
        rm -rf build/
        rm -rf dist/
        rm -rf *.egg-info/
        
        # Remove Python cache
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -name "*.pyc" -delete 2>/dev/null || true
        find . -name "*.pyo" -delete 2>/dev/null || true
        
        print_success "Build artifacts cleaned"
    else
        print_warning "aiailint directory not found: $build_dir"
    fi
}

# Function to validate package structure
validate_package() {
    print_status "Validating package structure"
    
    local package_dir="../../../aiailint"
    
    if [ -d "$package_dir" ]; then
        cd "$package_dir"
        
        # Check for required files
        local required_files=("src/aiailint.py" "README.md" "MANIFEST")
        local missing_files=()
        
        for file in "${required_files[@]}"; do
            if [ ! -f "$file" ]; then
                missing_files+=("$file")
            fi
        done
        
        if [ ${#missing_files[@]} -eq 0 ]; then
            print_success "Package structure is valid"
            return 0
        else
            print_error "Missing required files: ${missing_files[*]}"
            return 1
        fi
    else
        print_error "aiailint directory not found: $package_dir"
        return 1
    fi
}

# Function to run quality checks before build
run_pre_build_checks() {
    print_status "Running pre-build quality checks"
    
    # Run quality checks
    if ./scripts/quality-check.sh format lint types; then
        print_success "Pre-build quality checks passed"
        return 0
    else
        print_error "Pre-build quality checks failed"
        return 1
    fi
}

# Function to run tests before build
run_pre_build_tests() {
    print_status "Running pre-build tests"
    
    # Run basic tests
    if ./scripts/run-tests.sh unit; then
        print_success "Pre-build tests passed"
        return 0
    else
        print_error "Pre-build tests failed"
        return 1
    fi
}

# Function to build source distribution
build_sdist() {
    print_status "Building source distribution"
    
    local package_dir="../../../aiailint"
    
    if [ -d "$package_dir" ]; then
        cd "$package_dir"
        
        if command_exists python; then
            # Build source distribution
            python setup.py sdist --formats=gztar,zip
            
            # Check if build was successful
            if [ -d "dist" ] && [ "$(ls -1 dist/*.tar.gz 2>/dev/null | wc -l)" -gt 0 ]; then
                print_success "Source distribution built successfully"
                ls -la dist/*.tar.gz
                return 0
            else
                print_error "Source distribution build failed"
                return 1
            fi
        else
            print_error "python command not found"
            return 1
        fi
    else
        print_error "aiailint directory not found: $package_dir"
        return 1
    fi
}

# Function to build wheel distribution
build_wheel() {
    print_status "Building wheel distribution"
    
    local package_dir="../../../aiailint"
    
    if [ -d "$package_dir" ]; then
        cd "$package_dir"
        
        if command_exists python; then
            # Build wheel distribution
            python setup.py bdist_wheel
            
            # Check if build was successful
            if [ -d "dist" ] && [ "$(ls -1 dist/*.whl 2>/dev/null | wc -l)" -gt 0 ]; then
                print_success "Wheel distribution built successfully"
                ls -la dist/*.whl
                return 0
            else
                print_error "Wheel distribution build failed"
                return 1
            fi
        else
            print_error "python command not found"
            return 1
        fi
    else
        print_error "aiailint directory not found: $package_dir"
        return 1
    fi
}

# Function to build using build module
build_with_build_module() {
    print_status "Building with build module"
    
    local package_dir="../../../aiailint"
    
    if [ -d "$package_dir" ]; then
        cd "$package_dir"
        
        if command_exists python; then
            # Install build module if not available
            if ! python -c "import build" 2>/dev/null; then
                print_status "Installing build module"
                pip install build
            fi
            
            # Build using build module
            python -m build
            
            # Check if build was successful
            if [ -d "dist" ] && [ "$(ls -1 dist/* 2>/dev/null | wc -l)" -gt 0 ]; then
                print_success "Build completed successfully"
                ls -la dist/
                return 0
            else
                print_error "Build failed"
                return 1
            fi
        else
            print_error "python command not found"
            return 1
        fi
    else
        print_error "aiailint directory not found: $package_dir"
        return 1
    fi
}

# Function to validate built packages
validate_built_packages() {
    print_status "Validating built packages"
    
    local package_dir="../../../aiailint"
    
    if [ -d "$package_dir" ]; then
        cd "$package_dir"
        
        if [ -d "dist" ]; then
            local packages=($(ls dist/*.tar.gz dist/*.whl 2>/dev/null))
            
            if [ ${#packages[@]} -eq 0 ]; then
                print_error "No packages found in dist directory"
                return 1
            fi
            
            print_status "Found ${#packages[@]} package(s):"
            for package in "${packages[@]}"; do
                echo "  - $(basename "$package") ($(du -h "$package" | cut -f1))"
            done
            
            # Check package structure
            for package in "${packages[@]}"; do
                if [[ "$package" == *.tar.gz ]]; then
                    print_status "Checking source distribution: $(basename "$package")"
                    tar -tzf "$package" | head -10
                elif [[ "$package" == *.whl ]]; then
                    print_status "Checking wheel distribution: $(basename "$package")"
                    unzip -l "$package" | head -10
                fi
            done
            
            print_success "Package validation completed"
            return 0
        else
            print_error "dist directory not found"
            return 1
        fi
    else
        print_error "aiailint directory not found: $package_dir"
        return 1
    fi
}

# Function to install built package for testing
install_built_package() {
    print_status "Installing built package for testing"
    
    local package_dir="../../../aiailint"
    
    if [ -d "$package_dir" ]; then
        cd "$package_dir"
        
        if [ -d "dist" ]; then
            # Find the latest wheel package
            local latest_wheel=$(ls -t dist/*.whl 2>/dev/null | head -1)
            
            if [ -n "$latest_wheel" ]; then
                print_status "Installing: $(basename "$latest_wheel")"
                
                # Install the package
                pip install "$latest_wheel" --force-reinstall
                
                # Test if installation was successful
                if python -c "import aiailint; print('aiailint version:', aiailint.__version__ if hasattr(aiailint, '__version__') else 'unknown')" 2>/dev/null; then
                    print_success "Package installation test passed"
                    return 0
                else
                    print_error "Package installation test failed"
                    return 1
                fi
            else
                print_warning "No wheel package found for testing"
                return 0
            fi
        else
            print_warning "No dist directory found for testing"
            return 0
        fi
    else
        print_error "aiailint directory not found: $package_dir"
        return 1
    fi
}

# Function to generate build report
generate_build_report() {
    print_status "Generating build report"
    
    local package_dir="../../../aiailint"
    local report_dir="build-reports"
    mkdir -p "$report_dir"
    
    if [ -d "$package_dir" ]; then
        cd "$package_dir"
        
        # Generate build summary
        cat > "$report_dir/build-summary.txt" << EOF
aiailint Build Summary
======================
Date: $(date)
Duration: $(($(date +%s) - start_time)) seconds

Build Results:
- Package Validation: $(if [ $validation_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)
- Quality Checks: $(if [ $quality_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)
- Pre-build Tests: $(if [ $tests_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)
- Source Distribution: $(if [ $sdist_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)
- Wheel Distribution: $(if [ $wheel_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)
- Package Validation: $(if [ $package_validation_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)
- Installation Test: $(if [ $install_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)

Built Packages:
$(if [ -d "dist" ]; then ls -la dist/; else echo "No packages found"; fi)

Package Sizes:
$(if [ -d "dist" ]; then du -h dist/*; else echo "No packages found"; fi)
EOF
        
        print_success "Build report generated: $report_dir/build-summary.txt"
    else
        print_error "aiailint directory not found: $package_dir"
    fi
}

# Function to show help
show_help() {
    echo "aiailint Package Builder"
    echo
    echo "Usage: $0 [OPTIONS] [BUILD_TYPE]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -v, --verbose  Enable verbose output"
    echo "  --clean        Clean build artifacts before building"
    echo "  --report       Generate build report"
    echo "  --test         Install and test built package"
    echo "  --skip-checks  Skip pre-build quality checks and tests"
    echo
    echo "Build Types:"
    echo "  sdist          Build source distribution only"
    echo "  wheel          Build wheel distribution only"
    echo "  all            Build all distributions (default)"
    echo
    echo "Examples:"
    echo "  $0                    # Build all distributions"
    echo "  $0 sdist             # Build source distribution only"
    echo "  $0 --clean           # Clean and build all distributions"
    echo "  $0 --test            # Build and test package"
    echo "  $0 --report          # Build and generate report"
}

# Main function
main() {
    local build_type="all"
    local verbose=false
    local clean_build=false
    local generate_report=false
    local test_package=false
    local skip_checks=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            --clean)
                clean_build=true
                shift
                ;;
            --report)
                generate_report=true
                shift
                ;;
            --test)
                test_package=true
                shift
                ;;
            --skip-checks)
                skip_checks=true
                shift
                ;;
            sdist|wheel|all)
                build_type="$1"
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Set start time
    start_time=$(date +%s)
    
    # Check virtual environment
    check_venv
    
    # Initialize failure counters
    validation_failed=0
    quality_failed=0
    tests_failed=0
    sdist_failed=0
    wheel_failed=0
    package_validation_failed=0
    install_failed=0
    
    # Clean build if requested
    if [ "$clean_build" = true ]; then
        clean_build
    fi
    
    # Validate package structure
    if validate_package; then
        print_success "Package validation passed"
    else
        print_error "Package validation failed"
        validation_failed=1
        exit 1
    fi
    
    # Run pre-build checks unless skipped
    if [ "$skip_checks" = false ]; then
        if run_pre_build_checks; then
            print_success "Pre-build quality checks passed"
        else
            print_error "Pre-build quality checks failed"
            quality_failed=1
            if [ "$verbose" = false ]; then
                exit 1
            fi
        fi
        
        if run_pre_build_tests; then
            print_success "Pre-build tests passed"
        else
            print_error "Pre-build tests failed"
            tests_failed=1
            if [ "$verbose" = false ]; then
                exit 1
            fi
        fi
    else
        print_warning "Skipping pre-build checks"
    fi
    
    # Build packages based on type
    case "$build_type" in
        "sdist")
            if build_sdist; then
                print_success "Source distribution build completed"
            else
                print_error "Source distribution build failed"
                sdist_failed=1
                exit 1
            fi
            ;;
        "wheel")
            if build_wheel; then
                print_success "Wheel distribution build completed"
            else
                print_error "Wheel distribution build failed"
                wheel_failed=1
                exit 1
            fi
            ;;
        "all")
            if build_with_build_module; then
                print_success "All distributions built successfully"
            else
                print_error "Build failed"
                sdist_failed=1
                wheel_failed=1
                exit 1
            fi
            ;;
    esac
    
    # Validate built packages
    if validate_built_packages; then
        print_success "Package validation passed"
    else
        print_error "Package validation failed"
        package_validation_failed=1
    fi
    
    # Test package installation if requested
    if [ "$test_package" = true ]; then
        if install_built_package; then
            print_success "Package installation test passed"
        else
            print_error "Package installation test failed"
            install_failed=1
        fi
    fi
    
    # Generate report if requested
    if [ "$generate_report" = true ]; then
        generate_build_report
    fi
    
    # Print summary
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    print_status "Build process completed in ${duration} seconds"
    
    # Return appropriate exit code
    if [ $validation_failed -eq 0 ] && [ $sdist_failed -eq 0 ] && [ $wheel_failed -eq 0 ]; then
        print_success "Build completed successfully!"
        exit 0
    else
        print_error "Build failed!"
        exit 1
    fi
}

# Run main function
main "$@"
