#!/bin/bash

# aiailint-dev test wrapper script
# This script provides a simple interface for running tests in the aiailint development environment
# VIBE_CODING: Create -> Validate -> Test -> Commit workflow

set -euo pipefail

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_DIR="$PROJECT_ROOT/environments/aiailint-dev"

# Colors for output (no emojis per VIBE_CODING)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Validation functions
validate_environment() {
    log_info "Validating aiailint-dev environment..."
    
    if [[ ! -d "$ENV_DIR" ]]; then
        log_error "Environment directory not found: $ENV_DIR"
        return 1
    fi
    
    if [[ ! -f "$ENV_DIR/Taskfile.yml" ]]; then
        log_error "Taskfile.yml not found in environment directory"
        return 1
    fi
    
    log_success "Environment validation passed"
    return 0
}

validate_task_availability() {
    log_info "Checking Task availability..."
    
    if ! command -v task &> /dev/null; then
        log_error "Task command not found. Please install Task first."
        log_info "Installation: sh -c \"\$(curl --location https://taskfile.dev/install.sh)\" -- -d -b ~/.local/bin"
        return 1
    fi
    
    log_success "Task command available: $(task --version)"
    return 0
}

# Test execution functions
run_unit_tests() {
    log_info "Running unit tests..."
    if task python:test-unit; then
        log_success "Unit tests completed successfully"
        return 0
    else
        log_error "Unit tests failed"
        return 1
    fi
}

run_integration_tests() {
    log_info "Running integration tests..."
    if task python:test-integration; then
        log_success "Integration tests completed successfully"
        return 0
    else
        log_error "Integration tests failed"
        return 1
    fi
}

run_quality_checks() {
    log_info "Running quality checks..."
    if task python:quality; then
        log_success "Quality checks completed successfully"
        return 0
    else
        log_error "Quality checks failed"
        return 1
    fi
}

run_component_tests() {
    log_info "Running aiailint component tests..."
    if task --taskfile aiailint-tasks.yml test-aiailint; then
        log_success "Component tests completed successfully"
        return 0
    else
        log_error "Component tests failed"
        return 1
    fi
}

run_validation_tests() {
    log_info "Running aiailint validation tests..."
    if task --taskfile aiailint-tasks.yml validate; then
        log_success "Validation tests completed successfully"
        return 0
    else
        log_error "Validation tests failed"
        return 1
    fi
}

run_health_check() {
    log_info "Running aiailint health check..."
    if task --taskfile aiailint-tasks.yml check; then
        log_success "Health check completed successfully"
        return 0
    else
        log_error "Health check failed"
        return 1
    fi
}

# Main test function
run_tests() {
    local test_type="$1"
    local exit_code=0
    
    log_info "Starting aiailint-dev test execution..."
    
    # Validate prerequisites
    if ! validate_task_availability; then
        exit 1
    fi
    
    if ! validate_environment; then
        exit 1
    fi
    
    # Change to environment directory
    log_info "Changing to environment directory: $ENV_DIR"
    cd "$ENV_DIR"
    
    # Run tests based on type
    case "$test_type" in
        "unit")
            run_unit_tests || exit_code=1
            ;;
        "integration")
            run_integration_tests || exit_code=1
            ;;
        "quality")
            run_quality_checks || exit_code=1
            ;;
        "component")
            run_component_tests || exit_code=1
            ;;
        "validation")
            run_validation_tests || exit_code=1
            ;;
        "health")
            run_health_check || exit_code=1
            ;;
        "all")
            log_info "Running comprehensive test suite..."
            run_unit_tests || exit_code=1
            run_integration_tests || exit_code=1
            run_quality_checks || exit_code=1
            run_component_tests || exit_code=1
            run_validation_tests || exit_code=1
            run_health_check || exit_code=1
            ;;
        *)
            log_error "Unknown test type: $test_type"
            show_help
            exit 1
            ;;
    esac
    
    if [[ $exit_code -eq 0 ]]; then
        log_success "All tests completed successfully"
    else
        log_error "Some tests failed"
    fi
    
    return $exit_code
}

# Help function
show_help() {
    cat << EOF
aiailint-dev Test Script

Usage: $0 [OPTIONS] [TEST_TYPE]

Options:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose output
    --validate      Only validate environment without running tests

Test Types:
    unit          Run unit tests only
    integration   Run integration tests only
    quality       Run quality checks only
    component     Run aiailint component tests only
    validation    Run aiailint validation tests only
    health        Run aiailint health check only
    all           Run comprehensive test suite (default)

Examples:
    $0                    # Run all tests
    $0 unit              # Run unit tests only
    $0 --validate        # Only validate environment
    $0 --help           # Show this help

VIBE_CODING Workflow:
    - Validates environment and prerequisites
    - Runs specified test suite with proper error handling
    - Provides clear success/failure feedback
    - Supports different test types for focused testing
EOF
}

# Parse command line arguments
VERBOSE=false
VALIDATE_ONLY=false
TEST_TYPE="all"

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --validate)
            VALIDATE_ONLY=true
            shift
            ;;
        unit|integration|quality|component|validation|health|all)
            TEST_TYPE="$1"
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main execution
if [[ "$VALIDATE_ONLY" == "true" ]]; then
    log_info "Running validation only..."
    validate_task_availability && validate_environment
    exit $?
else
    run_tests "$TEST_TYPE"
fi
