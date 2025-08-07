#!/bin/bash

# aiailint Quality Check Script
# This script runs code quality checks including formatting, linting, and type checking

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

# Function to run code formatting check
run_format_check() {
    print_status "Running code formatting check with black"
    
    local source_dir="../../../aiailint/src"
    
    if [ -d "$source_dir" ]; then
        if command_exists black; then
            # Check if code is properly formatted
            if black --check --diff "$source_dir" 2>/dev/null; then
                print_success "Code formatting is correct"
                return 0
            else
                print_error "Code formatting issues found"
                print_status "Run 'black $source_dir' to fix formatting"
                return 1
            fi
        else
            print_warning "black not found, skipping format check"
            return 0
        fi
    else
        print_warning "Source directory not found: $source_dir"
        return 0
    fi
}

# Function to run code formatting
run_format() {
    print_status "Running code formatting with black"
    
    local source_dir="../../../aiailint/src"
    
    if [ -d "$source_dir" ]; then
        if command_exists black; then
            black "$source_dir"
            print_success "Code formatting completed"
        else
            print_warning "black not found, skipping format"
        fi
    else
        print_warning "Source directory not found: $source_dir"
    fi
}

# Function to run import sorting
run_import_sort() {
    print_status "Running import sorting with isort"
    
    local source_dir="../../../aiailint/src"
    
    if [ -d "$source_dir" ]; then
        if command_exists isort; then
            isort "$source_dir"
            print_success "Import sorting completed"
        else
            print_warning "isort not found, skipping import sort"
        fi
    else
        print_warning "Source directory not found: $source_dir"
    fi
}

# Function to run linting check
run_lint_check() {
    print_status "Running linting check with flake8"
    
    local source_dir="../../../aiailint/src"
    
    if [ -d "$source_dir" ]; then
        if command_exists flake8; then
            if flake8 "$source_dir" --count --show-source --statistics; then
                print_success "Linting check passed"
                return 0
            else
                print_error "Linting issues found"
                return 1
            fi
        else
            print_warning "flake8 not found, skipping lint check"
            return 0
        fi
    else
        print_warning "Source directory not found: $source_dir"
        return 0
    fi
}

# Function to run type checking
run_type_check() {
    print_status "Running type checking with mypy"
    
    local source_dir="../../../aiailint/src"
    
    if [ -d "$source_dir" ]; then
        if command_exists mypy; then
            if mypy "$source_dir" --ignore-missing-imports --no-strict-optional; then
                print_success "Type checking passed"
                return 0
            else
                print_error "Type checking issues found"
                return 1
            fi
        else
            print_warning "mypy not found, skipping type check"
            return 0
        fi
    else
        print_warning "Source directory not found: $source_dir"
        return 0
    fi
}

# Function to run security analysis
run_security_check() {
    print_status "Running security analysis with bandit"
    
    local source_dir="../../../aiailint/src"
    
    if [ -d "$source_dir" ]; then
        if command_exists bandit; then
            if bandit -r "$source_dir" -f json -o bandit-report.json; then
                print_success "Security analysis completed"
                return 0
            else
                print_warning "Security issues found (see bandit-report.json)"
                return 1
            fi
        else
            print_warning "bandit not found, skipping security check"
            return 0
        fi
    else
        print_warning "Source directory not found: $source_dir"
        return 0
    fi
}

# Function to run complexity analysis
run_complexity_check() {
    print_status "Running complexity analysis"
    
    local source_dir="../../../aiailint/src"
    
    if [ -d "$source_dir" ]; then
        if command_exists radon; then
            print_status "Cyclomatic complexity analysis:"
            radon cc "$source_dir" -a
            
            print_status "Maintainability index:"
            radon mi "$source_dir"
            
            print_success "Complexity analysis completed"
        else
            print_warning "radon not found, skipping complexity analysis"
        fi
    else
        print_warning "Source directory not found: $source_dir"
    fi
}

# Function to run dependency check
run_dependency_check() {
    print_status "Running dependency vulnerability check with safety"
    
    if command_exists safety; then
        if safety check --json --output safety-report.json; then
            print_success "Dependency check completed"
            return 0
        else
            print_warning "Vulnerable dependencies found (see safety-report.json)"
            return 1
        fi
    else
        print_warning "safety not found, skipping dependency check"
        return 0
    fi
}

# Function to run all quality checks
run_all_checks() {
    print_status "Running all quality checks"
    
    local start_time=$(date +%s)
    local failed_checks=0
    
    # Run different quality checks
    if run_format_check; then
        print_success "Format check passed"
    else
        print_error "Format check failed"
        ((failed_checks++))
    fi
    
    if run_lint_check; then
        print_success "Lint check passed"
    else
        print_error "Lint check failed"
        ((failed_checks++))
    fi
    
    if run_type_check; then
        print_success "Type check passed"
    else
        print_error "Type check failed"
        ((failed_checks++))
    fi
    
    # Run security and dependency checks (don't fail the build)
    run_security_check
    run_dependency_check
    run_complexity_check
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    print_status "Quality checks completed in ${duration} seconds"
    
    if [ $failed_checks -eq 0 ]; then
        print_success "All quality checks passed!"
        return 0
    else
        print_error "$failed_checks quality check(s) failed"
        return 1
    fi
}

# Function to run specific quality check
run_specific_check() {
    local check_type="$1"
    
    case "$check_type" in
        "format")
            run_format_check
            ;;
        "format-fix")
            run_format
            ;;
        "imports")
            run_import_sort
            ;;
        "lint")
            run_lint_check
            ;;
        "types")
            run_type_check
            ;;
        "security")
            run_security_check
            ;;
        "dependencies")
            run_dependency_check
            ;;
        "complexity")
            run_complexity_check
            ;;
        *)
            print_error "Unknown check type: $check_type"
            print_status "Available check types: format, format-fix, imports, lint, types, security, dependencies, complexity"
            exit 1
            ;;
    esac
}

# Function to generate quality report
generate_quality_report() {
    print_status "Generating quality report"
    
    local report_dir="quality-reports"
    mkdir -p "$report_dir"
    
    # Generate quality summary
    cat > "$report_dir/quality-summary.txt" << EOF
aiailint Quality Check Summary
==============================
Date: $(date)
Duration: $(($(date +%s) - start_time)) seconds

Quality Check Results:
- Format Check: $(if [ $format_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)
- Lint Check: $(if [ $lint_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)
- Type Check: $(if [ $type_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)
- Security Check: $(if [ $security_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)
- Dependency Check: $(if [ $dependency_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)

Files Checked:
$(find ../../../aiailint/src -name "*.py" | wc -l) Python files
$(find ../../../aiailint/src -name "*.py" -exec wc -l {} + | tail -1 | awk '{print $1}') total lines of code
EOF
    
    print_success "Quality report generated: $report_dir/quality-summary.txt"
}

# Function to show help
show_help() {
    echo "aiailint Quality Check"
    echo
    echo "Usage: $0 [OPTIONS] [CHECK_TYPE]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -v, --verbose  Enable verbose output"
    echo "  --report       Generate quality report"
    echo "  --fix          Auto-fix issues where possible"
    echo
    echo "Check Types:"
    echo "  format         Check code formatting"
    echo "  format-fix     Fix code formatting"
    echo "  imports        Sort imports"
    echo "  lint           Run linting checks"
    echo "  types          Run type checking"
    echo "  security       Run security analysis"
    echo "  dependencies   Check dependency vulnerabilities"
    echo "  complexity     Analyze code complexity"
    echo "  all            Run all checks (default)"
    echo
    echo "Examples:"
    echo "  $0                    # Run all quality checks"
    echo "  $0 format            # Check code formatting"
    echo "  $0 --fix             # Run all checks with auto-fix"
    echo "  $0 --report          # Run all checks and generate report"
}

# Main function
main() {
    local check_type="all"
    local verbose=false
    local generate_report=false
    local auto_fix=false
    
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
            --report)
                generate_report=true
                shift
                ;;
            --fix)
                auto_fix=true
                shift
                ;;
            format|format-fix|imports|lint|types|security|dependencies|complexity|all)
                check_type="$1"
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
    
    # Set environment variables
    if [ "$verbose" = true ]; then
        export PYTHONPATH="../../../aiailint/src:$PYTHONPATH"
    fi
    
    # Run checks based on type
    if [ "$check_type" = "all" ]; then
        if [ "$auto_fix" = true ]; then
            print_status "Running all quality checks with auto-fix"
            run_format
            run_import_sort
        fi
        run_all_checks
    else
        if [ "$auto_fix" = true ] && [ "$check_type" = "format" ]; then
            run_specific_check "format-fix"
        else
            run_specific_check "$check_type"
        fi
    fi
    
    # Generate report if requested
    if [ "$generate_report" = true ]; then
        generate_quality_report
    fi
    
    # Print summary
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    print_status "Quality checks completed in ${duration} seconds"
}

# Run main function
main "$@"
