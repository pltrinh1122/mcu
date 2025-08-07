#!/bin/bash

# aiailint-dev deploy wrapper script
# This script provides a simple interface for deploying the aiailint development environment
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

# Deployment functions
run_build() {
    log_info "Building aiailint application..."
    if task build; then
        log_success "Build completed successfully"
        return 0
    else
        log_error "Build failed"
        return 1
    fi
}

run_package() {
    log_info "Creating deployment package..."
    if task deploy:package; then
        log_success "Package created successfully"
        return 0
    else
        log_error "Package creation failed"
        return 1
    fi
}

run_local_deploy() {
    log_info "Deploying to local environment..."
    if task deploy:deploy-local; then
        log_success "Local deployment completed successfully"
        return 0
    else
        log_error "Local deployment failed"
        return 1
    fi
}

run_docker_deploy() {
    log_info "Deploying with Docker..."
    if task docker:docker-build && task docker:docker-run; then
        log_success "Docker deployment completed successfully"
        return 0
    else
        log_error "Docker deployment failed"
        return 1
    fi
}

run_staging_deploy() {
    log_info "Deploying to staging environment..."
    if task deploy:deploy-staging; then
        log_success "Staging deployment completed successfully"
        return 0
    else
        log_error "Staging deployment failed"
        return 1
    fi
}

run_production_deploy() {
    log_info "Deploying to production environment..."
    if task deploy:deploy-production; then
        log_success "Production deployment completed successfully"
        return 0
    else
        log_error "Production deployment failed"
        return 1
    fi
}

run_health_check() {
    log_info "Running post-deployment health check..."
    if task deploy:health-check; then
        log_success "Health check passed"
        return 0
    else
        log_error "Health check failed"
        return 1
    fi
}

# Main deploy function
run_deploy() {
    local deploy_type="$1"
    local exit_code=0
    
    log_info "Starting aiailint-dev deployment..."
    
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
    
    # Run deployment based on type
    case "$deploy_type" in
        "build")
            run_build || exit_code=1
            ;;
        "package")
            run_package || exit_code=1
            ;;
        "local")
            run_build || exit_code=1
            run_local_deploy || exit_code=1
            ;;
        "docker")
            run_build || exit_code=1
            run_docker_deploy || exit_code=1
            ;;
        "staging")
            run_build || exit_code=1
            run_package || exit_code=1
            run_staging_deploy || exit_code=1
            run_health_check || exit_code=1
            ;;
        "production")
            run_build || exit_code=1
            run_package || exit_code=1
            run_production_deploy || exit_code=1
            run_health_check || exit_code=1
            ;;
        "full")
            log_info "Running full deployment pipeline..."
            run_build || exit_code=1
            run_package || exit_code=1
            run_local_deploy || exit_code=1
            run_docker_deploy || exit_code=1
            run_health_check || exit_code=1
            ;;
        *)
            log_error "Unknown deployment type: $deploy_type"
            show_help
            exit 1
            ;;
    esac
    
    if [[ $exit_code -eq 0 ]]; then
        log_success "Deployment completed successfully"
    else
        log_error "Deployment failed"
    fi
    
    return $exit_code
}

# Help function
show_help() {
    cat << EOF
aiailint-dev Deploy Script

Usage: $0 [OPTIONS] [DEPLOY_TYPE]

Options:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose output
    --validate      Only validate environment without deploying

Deploy Types:
    build       Build application only
    package     Create deployment package only
    local       Deploy to local environment
    docker      Deploy with Docker
    staging     Deploy to staging environment
    production  Deploy to production environment
    full        Run full deployment pipeline (default)

Examples:
    $0                    # Run full deployment
    $0 local              # Deploy to local environment
    $0 --validate        # Only validate environment
    $0 --help           # Show this help

VIBE_CODING Workflow:
    - Validates environment and prerequisites
    - Runs deployment pipeline with proper error handling
    - Provides clear success/failure feedback
    - Supports different deployment targets
    - Includes post-deployment health checks
EOF
}

# Parse command line arguments
VERBOSE=false
VALIDATE_ONLY=false
DEPLOY_TYPE="full"

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
        build|package|local|docker|staging|production|full)
            DEPLOY_TYPE="$1"
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
    run_deploy "$DEPLOY_TYPE"
fi
