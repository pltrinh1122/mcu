#!/bin/bash

# aiailint Test Runner Script
# This script runs all tests for the aiailint project

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

# Function to run unit tests
run_unit_tests() {
    print_status "Running unit tests"
    
    local test_dir="../../../aiailint/tests"
    local coverage_file=".coverage.unit"
    
    if [ -d "$test_dir" ]; then
        python -m pytest "$test_dir" \
            --cov=aiailint \
            --cov-report=term-missing \
            --cov-report=html:htmlcov/unit \
            --cov-report=xml:coverage.xml \
            --cov-fail-under=80 \
            -v \
            --tb=short \
            --maxfail=10 \
            --durations=10
        print_success "Unit tests completed"
    else
        print_warning "Unit test directory not found: $test_dir"
    fi
}

# Function to run integration tests
run_integration_tests() {
    print_status "Running integration tests"
    
    local test_dir="../../../aiailint/tests"
    
    if [ -d "$test_dir" ]; then
        python -m pytest "$test_dir" \
            -m "integration" \
            -v \
            --tb=short \
            --maxfail=5 \
            --durations=10
        print_success "Integration tests completed"
    else
        print_warning "Integration test directory not found: $test_dir"
    fi
}

# Function to run functional tests
run_functional_tests() {
    print_status "Running functional tests"
    
    local test_dir="../../../aiailint/tests"
    
    if [ -d "$test_dir" ]; then
        python -m pytest "$test_dir" \
            -m "functional" \
            -v \
            --tb=short \
            --maxfail=5 \
            --durations=10
        print_success "Functional tests completed"
    else
        print_warning "Functional test directory not found: $test_dir"
    fi
}

# Function to run performance tests
run_performance_tests() {
    print_status "Running performance tests"
    
    local test_dir="../../../aiailint/tests"
    
    if [ -d "$test_dir" ]; then
        python -m pytest "$test_dir" \
            --benchmark-only \
            --benchmark-skip \
            -v \
            --tb=short
        print_success "Performance tests completed"
    else
        print_warning "Performance test directory not found: $test_dir"
    fi
}

# Function to run security tests
run_security_tests() {
    print_status "Running security tests"
    
    # Run bandit security analysis
    if command -v bandit >/dev/null 2>&1; then
        print_status "Running bandit security analysis"
        bandit -r ../../../aiailint/src/ -f json -o bandit-report.json || true
        bandit -r ../../../aiailint/src/ -f txt -o bandit-report.txt || true
        print_success "Bandit security analysis completed"
    else
        print_warning "bandit not found, skipping security analysis"
    fi
    
    # Run safety check
    if command -v safety >/dev/null 2>&1; then
        print_status "Running safety vulnerability check"
        safety check --json --output safety-report.json || true
        safety check --text --output safety-report.txt || true
        print_success "Safety vulnerability check completed"
    else
        print_warning "safety not found, skipping vulnerability check"
    fi
}

# Function to run aiailint self-validation
run_self_validation() {
    print_status "Running aiailint self-validation"
    
    local aiailint_dir="../../../aiailint"
    
    if [ -d "$aiailint_dir" ]; then
        # Test aiailint on its own source files
        if command -v aiailint >/dev/null 2>&1; then
            print_status "Validating aiailint source files"
            aiailint validate "$aiailint_dir/src/" --format json --verbose || true
            print_success "Self-validation completed"
        else
            print_warning "aiailint command not found"
        fi
    else
        print_warning "aiailint directory not found: $aiailint_dir"
    fi
}

# Function to run all tests
run_all_tests() {
    print_status "Running all test suites"
    
    local start_time=$(date +%s)
    local failed_tests=0
    
    # Run different test categories
    if run_unit_tests; then
        print_success "Unit tests passed"
    else
        print_error "Unit tests failed"
        ((failed_tests++))
    fi
    
    if run_integration_tests; then
        print_success "Integration tests passed"
    else
        print_error "Integration tests failed"
        ((failed_tests++))
    fi
    
    if run_functional_tests; then
        print_success "Functional tests passed"
    else
        print_error "Functional tests failed"
        ((failed_tests++))
    fi
    
    if run_performance_tests; then
        print_success "Performance tests passed"
    else
        print_error "Performance tests failed"
        ((failed_tests++))
    fi
    
    # Run security tests (don't fail the build)
    run_security_tests
    
    # Run self-validation (don't fail the build)
    run_self_validation
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    print_status "Test execution completed in ${duration} seconds"
    
    if [ $failed_tests -eq 0 ]; then
        print_success "All tests passed!"
        return 0
    else
        print_error "$failed_tests test suite(s) failed"
        return 1
    fi
}

# Function to run specific test category
run_specific_tests() {
    local test_type="$1"
    
    case "$test_type" in
        "unit")
            run_unit_tests
            ;;
        "integration")
            run_integration_tests
            ;;
        "functional")
            run_functional_tests
            ;;
        "performance")
            run_performance_tests
            ;;
        "security")
            run_security_tests
            ;;
        "self")
            run_self_validation
            ;;
        *)
            print_error "Unknown test type: $test_type"
            print_status "Available test types: unit, integration, functional, performance, security, self"
            exit 1
            ;;
    esac
}

# Function to generate test report
generate_report() {
    print_status "Generating test report"
    
    local report_dir="test-reports"
    mkdir -p "$report_dir"
    
    # Generate HTML coverage report
    if [ -f ".coverage" ]; then
        python -m coverage html --directory="$report_dir/htmlcov"
        print_success "HTML coverage report generated: $report_dir/htmlcov/index.html"
    fi
    
    # Generate XML coverage report
    if [ -f ".coverage" ]; then
        python -m coverage xml -o "$report_dir/coverage.xml"
        print_success "XML coverage report generated: $report_dir/coverage.xml"
    fi
    
    # Generate test summary
    cat > "$report_dir/test-summary.txt" << EOF
aiailint Test Summary
====================
Date: $(date)
Duration: $(($(date +%s) - start_time)) seconds

Test Results:
- Unit Tests: $(if [ $unit_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)
- Integration Tests: $(if [ $integration_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)
- Functional Tests: $(if [ $functional_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)
- Performance Tests: $(if [ $performance_failed -eq 0 ]; then echo "PASSED"; else echo "FAILED"; fi)

Coverage: $(python -m coverage report --show-missing | tail -1 | awk '{print $4}')
EOF
    
    print_success "Test report generated: $report_dir/test-summary.txt"
}

# Function to show help
show_help() {
    echo "aiailint Test Runner"
    echo
    echo "Usage: $0 [OPTIONS] [TEST_TYPE]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -v, --verbose  Enable verbose output"
    echo "  --report       Generate test report"
    echo "  --coverage     Run with coverage analysis"
    echo
    echo "Test Types:"
    echo "  unit           Run unit tests only"
    echo "  integration    Run integration tests only"
    echo "  functional     Run functional tests only"
    echo "  performance    Run performance tests only"
    echo "  security       Run security tests only"
    echo "  self           Run self-validation only"
    echo "  all            Run all tests (default)"
    echo
    echo "Examples:"
    echo "  $0                    # Run all tests"
    echo "  $0 unit              # Run unit tests only"
    echo "  $0 --coverage        # Run all tests with coverage"
    echo "  $0 --report          # Run all tests and generate report"
}

# Main function
main() {
    local test_type="all"
    local verbose=false
    local generate_report=false
    local with_coverage=false
    
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
            --coverage)
                with_coverage=true
                shift
                ;;
            unit|integration|functional|performance|security|self|all)
                test_type="$1"
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
        export PYTEST_ADDOPTS="-v -s"
    fi
    
    if [ "$with_coverage" = true ]; then
        export PYTEST_ADDOPTS="$PYTEST_ADDOPTS --cov=aiailint --cov-report=term-missing"
    fi
    
    # Run tests based on type
    if [ "$test_type" = "all" ]; then
        run_all_tests
    else
        run_specific_tests "$test_type"
    fi
    
    # Generate report if requested
    if [ "$generate_report" = true ]; then
        generate_report
    fi
    
    # Print summary
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    print_status "Test execution completed in ${duration} seconds"
}

# Run main function
main "$@"
