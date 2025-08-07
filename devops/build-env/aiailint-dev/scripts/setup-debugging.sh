#!/bin/bash

# aiailint Debugging Environment Setup Script
# Optimized for "vibe coding" with strategic asserts and debug logs

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

# Function to create debug utilities
create_debug_utilities() {
    print_status "Creating debug utilities for strategic asserts and logging"
    
    # Create debug utilities module
    cat > "debug_utils.py" << 'EOF'
#!/usr/bin/env python3
"""
aiailint Debug Utilities
Strategic asserts and debug logging for vibe coding
"""

import os
import sys
import logging
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict

# Configure logging for vibe coding
def setup_vibe_logging(level: str = "DEBUG", log_file: str = "vibe_debug.log"):
    """Set up logging optimized for vibe coding workflow"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create vibe logger
    vibe_logger = logging.getLogger('vibe')
    vibe_logger.setLevel(logging.DEBUG)
    
    return vibe_logger

# Strategic assert functions
def vibe_assert(condition: bool, message: str, context: Dict[str, Any] = None):
    """Strategic assert with context for vibe coding"""
    if not condition:
        error_msg = f"VIBE ASSERT FAILED: {message}"
        if context:
            error_msg += f"\nContext: {json.dumps(context, indent=2)}"
        raise AssertionError(error_msg)
    
    # Log successful assert for debugging
    logger = logging.getLogger('vibe')
    logger.debug(f"VIBE ASSERT PASSED: {message}")

def vibe_assert_data_structure(data: Any, expected_type: type, context: str = ""):
    """Assert data structure with detailed logging"""
    vibe_assert(
        isinstance(data, expected_type),
        f"Expected {expected_type.__name__}, got {type(data).__name__}",
        {"context": context, "actual_type": type(data).__name__}
    )

def vibe_assert_file_exists(file_path: Path, context: str = ""):
    """Assert file exists with detailed logging"""
    vibe_assert(
        file_path.exists(),
        f"File does not exist: {file_path}",
        {"context": context, "file_path": str(file_path)}
    )

def vibe_assert_yaml_valid(yaml_data: Dict, context: str = ""):
    """Assert YAML data has required structure"""
    required_keys = ['name', 'version', 'body']
    missing_keys = [key for key in required_keys if key not in yaml_data]
    
    vibe_assert(
        len(missing_keys) == 0,
        f"Missing required keys: {missing_keys}",
        {"context": context, "missing_keys": missing_keys, "available_keys": list(yaml_data.keys())}
    )

# Debug inspection functions
def vibe_inspect(data: Any, label: str = "", max_depth: int = 3):
    """Inspect data structure with vibe logging"""
    logger = logging.getLogger('vibe')
    
    def _inspect_recursive(obj, depth=0, path=""):
        if depth > max_depth:
            return f"<max_depth_reached at {path}>"
        
        if isinstance(obj, dict):
            result = {}
            for k, v in obj.items():
                result[k] = _inspect_recursive(v, depth + 1, f"{path}.{k}")
            return result
        elif isinstance(obj, list):
            return [_inspect_recursive(item, depth + 1, f"{path}[{i}]") for i, item in enumerate(obj)]
        else:
            return f"{type(obj).__name__}: {str(obj)[:100]}"
    
    inspected = _inspect_recursive(data)
    logger.debug(f"VIBE INSPECT {label}: {json.dumps(inspected, indent=2)}")
    return inspected

def vibe_trace_function(func):
    """Decorator to trace function calls with vibe logging"""
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('vibe')
        logger.debug(f"VIBE TRACE: Entering {func.__name__}")
        logger.debug(f"VIBE TRACE: Args: {args}")
        logger.debug(f"VIBE TRACE: Kwargs: {kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"VIBE TRACE: {func.__name__} returned: {type(result).__name__}")
            return result
        except Exception as e:
            logger.error(f"VIBE TRACE: {func.__name__} failed: {e}")
            raise
    
    return wrapper

# Performance tracking
@dataclass
class VibePerformance:
    function_name: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    
    def finish(self):
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time

def vibe_performance_tracker(func):
    """Decorator to track performance with vibe logging"""
    def wrapper(*args, **kwargs):
        import time
        logger = logging.getLogger('vibe')
        
        start_time = time.time()
        logger.debug(f"VIBE PERFORMANCE: Starting {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"VIBE PERFORMANCE: {func.__name__} completed in {duration:.4f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"VIBE PERFORMANCE: {func.__name__} failed after {duration:.4f}s: {e}")
            raise
    
    return wrapper

# Debug state management
class VibeDebugState:
    """Manage debug state for vibe coding sessions"""
    
    def __init__(self):
        self.state = {}
        self.logger = logging.getLogger('vibe')
    
    def set(self, key: str, value: Any):
        """Set debug state"""
        self.state[key] = value
        self.logger.debug(f"VIBE STATE: Set {key} = {value}")
    
    def get(self, key: str, default: Any = None):
        """Get debug state"""
        value = self.state.get(key, default)
        self.logger.debug(f"VIBE STATE: Get {key} = {value}")
        return value
    
    def clear(self):
        """Clear debug state"""
        self.state.clear()
        self.logger.debug("VIBE STATE: Cleared all state")
    
    def dump(self):
        """Dump current debug state"""
        self.logger.debug(f"VIBE STATE: Current state: {json.dumps(self.state, indent=2)}")

# Global debug state instance
vibe_state = VibeDebugState()

# Quick debug helpers
def vibe_log(message: str, level: str = "DEBUG"):
    """Quick vibe logging"""
    logger = logging.getLogger('vibe')
    getattr(logger, level.lower())(f"VIBE: {message}")

def vibe_error(message: str, error: Exception = None):
    """Quick vibe error logging"""
    logger = logging.getLogger('vibe')
    if error:
        logger.error(f"VIBE ERROR: {message} - {error}")
    else:
        logger.error(f"VIBE ERROR: {message}")

def vibe_success(message: str):
    """Quick vibe success logging"""
    logger = logging.getLogger('vibe')
    logger.info(f"VIBE SUCCESS: {message}")

# Initialize vibe logging
vibe_logger = setup_vibe_logging()
EOF

    print_success "Debug utilities created: debug_utils.py"
}

# Function to create test files for debugging
create_test_files() {
    print_status "Creating test files for vibe coding debugging"
    
    # Create test YAML file
    cat > "vibe_test.yaml" << 'EOF'
name: "Vibe Coding Test Script"
version: "1.0"
description: "Test script for vibe coding debugging"

body:
  - type: "command"
    id: "vibe-echo"
    shellCommand: "echo 'Hello from vibe coding!'"
    destructive: false
    
  - type: "validation"
    id: "vibe-validation"
    command: "[ -f /etc/os-release ] && echo 'linux' || echo 'other'"
    expected_output: "linux"
    
  - type: "command"
    id: "vibe-destructive"
    shellCommand: "rm -rf /tmp/vibe-test-file"
    destructive: true
    description: "This should be marked as destructive"
EOF

    # Create invalid YAML file for error debugging
    cat > "vibe_error.yaml" << 'EOF'
name: "Invalid Vibe Test Script"
version: "1.0"
body:
  - type: "command"
    id: "test-command"
    shellCommand: "echo 'test'"
    destructive: false  # This should be true for rm commands
  - type: "invalid_type"
    id: "invalid-element"
    someField: "invalid value"
EOF

    # Create edge case test file
    cat > "vibe_edge_case.yaml" << 'EOF'
name: "Edge Case Test"
version: "1.0"
body:
  - type: "command"
    id: "empty-command"
    shellCommand: ""
    destructive: false
    
  - type: "command"
    id: "very-long-command"
    shellCommand: "echo 'This is a very long command that might cause issues with parsing or validation or other edge cases that we need to test thoroughly'"
    destructive: false
    
  - type: "validation"
    id: "complex-validation"
    command: "python3 -c \"import sys; print('python' + str(sys.version_info[0]))\""
    expected_output: "python3"
EOF

    print_success "Vibe test files created:"
    echo "  - vibe_test.yaml (valid script)"
    echo "  - vibe_error.yaml (invalid script)"
    echo "  - vibe_edge_case.yaml (edge cases)"
}

# Function to set up vibe debugging environment
setup_vibe_debugging_env() {
    print_status "Setting up vibe debugging environment"
    
    # Create .env file for vibe environment variables
    cat > ".env" << 'EOF'
# aiailint Vibe Debug Environment Variables
AIAILINT_DEBUG=1
AIAILINT_DEBUG_LEVEL=DEBUG
VIBE_DEBUG_MODE=1
PYTHONPATH=../../../aiailint/src
PYTHONUNBUFFERED=1
VIBE_LOG_FILE=vibe_debug.log
EOF

    # Create vibe debug configuration file
    cat > "vibe_debug_config.json" << 'EOF'
{
    "vibe_mode": true,
    "debug_level": "DEBUG",
    "log_file": "vibe_debug.log",
    "strategic_asserts": true,
    "performance_tracking": true,
    "state_management": true,
    "test_files": {
        "valid": "vibe_test.yaml",
        "invalid": "vibe_error.yaml",
        "edge_case": "vibe_edge_case.yaml"
    },
    "assert_points": {
        "file_loading": "Ensure YAML files load correctly",
        "validation_start": "Ensure validation pipeline starts",
        "data_structure": "Ensure data structures are correct",
        "error_handling": "Ensure errors are handled properly"
    }
}
EOF

    print_success "Vibe debug environment configured"
}

# Function to create vibe debug helper script
create_vibe_debug_helper() {
    print_status "Creating vibe debug helper script"
    
    cat > "vibe_debug_helper.py" << 'EOF'
#!/usr/bin/env python3
"""
aiailint Vibe Debug Helper
Strategic asserts and debug logging for vibe coding
"""

import os
import sys
import json
from pathlib import Path

# Import our vibe debug utilities
from debug_utils import (
    setup_vibe_logging, vibe_assert, vibe_inspect, 
    vibe_log, vibe_error, vibe_success, vibe_state
)

def setup_vibe_environment():
    """Set up environment for vibe coding debugging"""
    # Add aiailint source to Python path
    aiailint_src = Path(__file__).parent.parent.parent / "aiailint" / "src"
    if aiailint_src.exists():
        sys.path.insert(0, str(aiailint_src))
        vibe_log(f"Added {aiailint_src} to Python path")
    
    # Set vibe debug environment variables
    os.environ['AIAILINT_DEBUG'] = '1'
    os.environ['VIBE_DEBUG_MODE'] = '1'
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    vibe_success("Vibe environment set up")

def load_vibe_test_data():
    """Load test data for vibe debugging"""
    test_files = {
        'valid': 'vibe_test.yaml',
        'invalid': 'vibe_error.yaml',
        'edge_case': 'vibe_edge_case.yaml'
    }
    
    for name, path in test_files.items():
        if Path(path).exists():
            vibe_log(f"Test file available: {name} -> {path}")
        else:
            vibe_error(f"Test file missing: {name} -> {path}")
    
    return test_files

def run_vibe_debug_test():
    """Run a vibe debug test with strategic asserts"""
    try:
        import aiailint
        vibe_success("aiailint module imported successfully")
        
        # Strategic assert: Check module structure
        vibe_assert(hasattr(aiailint, 'AiaiLinter'), "AiaiLinter class should exist")
        vibe_success("AiaiLinter class found")
        
        # Strategic assert: Create linter instance
        linter = aiailint.AiaiLinter()
        vibe_assert(linter is not None, "Linter should be created successfully")
        vibe_success("AiaiLinter created successfully")
        
        # Strategic assert: Check test files
        test_files = load_vibe_test_data()
        vibe_assert(len(test_files) == 3, "Should have 3 test files")
        vibe_success("All test files available")
        
        return True
    except Exception as e:
        vibe_error("Vibe debug test failed", e)
        return False

def vibe_debug_session():
    """Run a complete vibe debugging session"""
    vibe_log("Starting vibe debugging session")
    
    # Set up environment
    setup_vibe_environment()
    
    # Load test data
    test_files = load_vibe_test_data()
    
    # Run debug test
    if run_vibe_debug_test():
        vibe_success("Vibe debug session completed successfully")
    else:
        vibe_error("Vibe debug session failed")
    
    # Dump final state
    vibe_state.dump()

if __name__ == "__main__":
    vibe_debug_session()
EOF

    chmod +x vibe_debug_helper.py
    print_success "Vibe debug helper script created: vibe_debug_helper.py"
}

# Function to show vibe debugging instructions
show_vibe_debugging_instructions() {
    print_status "Vibe Debugging Setup Complete!"
    echo
    echo "🎯 Vibe Coding Debugging Workflow:"
    echo
    echo "1. Strategic Asserts & Debug Logs (No Breakpoints!)"
    echo "   - Use vibe_assert() for validation"
    echo "   - Use vibe_log() for debugging"
    echo "   - Use vibe_inspect() for data inspection"
    echo
    echo "2. Run vibe debug session:"
    echo "   python vibe_debug_helper.py"
    echo
    echo "3. Check vibe debug log:"
    echo "   tail -f vibe_debug.log"
    echo
    echo "4. Use debug utilities in your code:"
    echo "   from debug_utils import vibe_assert, vibe_log, vibe_inspect"
    echo
    echo "📁 Vibe test files created:"
    echo "   - vibe_test.yaml (valid script)"
    echo "   - vibe_error.yaml (invalid script)"
    echo "   - vibe_edge_case.yaml (edge cases)"
    echo
    echo "🔧 Vibe debug utilities:"
    echo "   - debug_utils.py (strategic asserts & logging)"
    echo "   - vibe_debug_helper.py (debug session runner)"
    echo "   - vibe_debug.log (debug output)"
    echo
    echo "💡 Vibe Coding Tips:"
    echo "   - Use strategic asserts instead of breakpoints"
    echo "   - Log everything important with vibe_log()"
    echo "   - Inspect data structures with vibe_inspect()"
    echo "   - Track performance with vibe_performance_tracker()"
    echo "   - Manage debug state with vibe_state"
}

# Function to run vibe debug test
run_vibe_debug_test() {
    print_status "Running vibe debug test"
    
    if python vibe_debug_helper.py; then
        print_success "Vibe debug test passed"
    else
        print_error "Vibe debug test failed"
        return 1
    fi
}

# Main function
main() {
    print_status "Setting up aiailint vibe debugging environment"
    
    # Check virtual environment
    check_venv
    
    # Create debug utilities
    create_debug_utilities
    
    # Create test files
    create_test_files
    
    # Set up vibe debugging environment
    setup_vibe_debugging_env
    
    # Create vibe debug helper
    create_vibe_debug_helper
    
    # Run vibe debug test
    run_vibe_debug_test
    
    # Show instructions
    show_vibe_debugging_instructions
}

# Run main function
main "$@"
