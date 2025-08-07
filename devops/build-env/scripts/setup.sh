#!/bin/bash

# aiailint-dev setup wrapper script
# This script provides a simple interface for setting up the aiailint development environment
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
    
    if [[ ! -f "$ENV_DIR/aiailint-tasks.yml" ]]; then
        log_error "aiailint-tasks.yml not found in environment directory"
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

# Main setup function
run_setup() {
    log_info "Starting aiailint-dev environment setup..."
    
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
    
    # Run setup task
    log_info "Running setup task..."
    if task setup; then
        log_success "aiailint-dev environment setup completed successfully"
    else
        log_error "Setup task failed"
        exit 1
    fi
}

# Help function
show_help() {
    cat << EOF
aiailint-dev Setup Script

Usage: $0 [OPTIONS]

Options:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose output
    --validate      Only validate environment without running setup

Examples:
    $0                    # Run full setup
    $0 --validate        # Only validate environment
    $0 --help           # Show this help

VIBE_CODING Workflow:
    - Validates environment and prerequisites
    - Runs setup task with proper error handling
    - Provides clear success/failure feedback
EOF
}

# Parse command line arguments
VERBOSE=false
VALIDATE_ONLY=false

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
    run_setup
fi
