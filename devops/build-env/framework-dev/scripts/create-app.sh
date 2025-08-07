#!/bin/bash

# aiailint Self-Contained App Builder
# This script creates a self-contained aiailint.app directory

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

# Function to create self-contained app
create_self_contained_app() {
    print_status "Creating self-contained aiailint.app"
    
    local app_dir="aiailint.app"
    local aiailint_src="../../../aiailint"
    local requirements_dir="requirements"
    
    # Remove existing app directory
    if [ -d "$app_dir" ]; then
        print_status "Removing existing $app_dir directory"
        rm -rf "$app_dir"
    fi
    
    # Create app directory structure
    print_status "Creating app directory structure"
    mkdir -p "$app_dir"/{bin,lib,src,docs,config,data}
    
    # Copy aiailint source
    print_status "Copying aiailint source code"
    if [ -d "$aiailint_src" ]; then
        cp -r "$aiailint_src"/src/* "$app_dir/src/"
        cp "$aiailint_src"/README.md "$app_dir/" 2>/dev/null || true
        cp "$aiailint_src"/MANIFEST "$app_dir/" 2>/dev/null || true
    else
        print_error "aiailint source directory not found: $aiailint_src"
        return 1
    fi
    
    # Create Python virtual environment in app directory
    print_status "Creating Python virtual environment"
    python3 -m venv "$app_dir/lib/venv"
    
    # Activate virtual environment and install dependencies
    print_status "Installing dependencies"
    source "$app_dir/lib/venv/bin/activate"
    pip install --upgrade pip
    pip install -r "$requirements_dir/requirements.txt"
    
    # Create launcher script
    create_launcher_script "$app_dir"
    
    # Create configuration files
    create_config_files "$app_dir"
    
    # Create documentation
    create_documentation "$app_dir"
    
    # Create data directory structure
    create_data_structure "$app_dir"
    
    # Set permissions
    chmod +x "$app_dir/bin/aiailint"
    chmod +x "$app_dir/bin/aiailint.bat"
    
    print_success "Self-contained app created at: $app_dir"
}

# Function to create launcher script
create_launcher_script() {
    local app_dir="$1"
    
    print_status "Creating launcher scripts"
    
    # Create Unix launcher
    cat > "$app_dir/bin/aiailint" << 'EOF'
#!/bin/bash

# aiailint Self-Contained App Launcher
# This script launches aiailint from the self-contained app directory

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"

# Activate virtual environment
source "$APP_DIR/lib/venv/bin/activate"

# Set Python path to include app source
export PYTHONPATH="$APP_DIR/src:$PYTHONPATH"

# Launch aiailint
exec python "$APP_DIR/src/aiailint.py" "$@"
EOF

    # Create Windows launcher
    cat > "$app_dir/bin/aiailint.bat" << 'EOF'
@echo off
REM aiailint Self-Contained App Launcher for Windows

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set APP_DIR=%SCRIPT_DIR%..

REM Activate virtual environment
call "%APP_DIR%\lib\venv\Scripts\activate.bat"

REM Set Python path to include app source
set PYTHONPATH=%APP_DIR%\src;%PYTHONPATH%

REM Launch aiailint
python "%APP_DIR%\src\aiailint.py" %*
EOF

    # Create Python launcher (cross-platform)
    cat > "$app_dir/bin/aiailint.py" << 'EOF'
#!/usr/bin/env python3
"""
aiailint Self-Contained App Launcher
Cross-platform Python launcher for aiailint
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    app_dir = script_dir.parent
    
    # Set up virtual environment path
    if os.name == 'nt':  # Windows
        venv_python = app_dir / "lib" / "venv" / "Scripts" / "python.exe"
        venv_activate = app_dir / "lib" / "venv" / "Scripts" / "activate.bat"
    else:  # Unix-like
        venv_python = app_dir / "lib" / "venv" / "bin" / "python"
        venv_activate = app_dir / "lib" / "venv" / "bin" / "activate"
    
    # Set Python path
    src_path = app_dir / "src"
    env = os.environ.copy()
    env['PYTHONPATH'] = str(src_path)
    
    # Launch aiailint
    aiailint_script = src_path / "aiailint.py"
    if aiailint_script.exists():
        subprocess.run([str(venv_python), str(aiailint_script)] + sys.argv[1:], env=env)
    else:
        print(f"Error: aiailint.py not found at {aiailint_script}")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

    chmod +x "$app_dir/bin/aiailint.py"
}

# Function to create configuration files
create_config_files() {
    local app_dir="$1"
    
    print_status "Creating configuration files"
    
    # Copy config files
    if [ -d "config" ]; then
        cp -r config/* "$app_dir/config/" 2>/dev/null || true
    fi
    
    # Create app-specific config
    cat > "$app_dir/config/app.conf" << 'EOF'
# aiailint App Configuration
[app]
name = aiailint
version = 1.0.0
description = AIAI Script validation and linting tool

[paths]
src = src/
lib = lib/
docs = docs/
config = config/
data = data/

[python]
venv = lib/venv
requirements = requirements.txt
EOF
}

# Function to create documentation
create_documentation() {
    local app_dir="$1"
    
    print_status "Creating documentation"
    
    # Copy documentation
    cp README.md "$app_dir/docs/" 2>/dev/null || true
    cp QUICK_START.md "$app_dir/docs/" 2>/dev/null || true
    
    # Create app-specific documentation
    cat > "$app_dir/docs/APP_USAGE.md" << 'EOF'
# aiailint.app Usage Guide

## Quick Start

### Unix/Linux/macOS
```bash
./bin/aiailint validate script.yaml
./bin/aiailint --help
```

### Windows
```cmd
bin\aiailint.bat validate script.yaml
bin\aiailint.bat --help
```

### Cross-platform Python
```bash
python bin/aiailint.py validate script.yaml
python bin/aiailint.py --help
```

## App Structure

```
aiailint.app/
├── bin/                    # Launcher scripts
│   ├── aiailint          # Unix launcher
│   ├── aiailint.bat      # Windows launcher
│   └── aiailint.py       # Cross-platform launcher
├── lib/                   # Python virtual environment
│   └── venv/             # Isolated Python environment
├── src/                   # aiailint source code
│   ├── aiailint.py       # Main executable
│   └── ...               # Other source files
├── docs/                  # Documentation
├── config/                # Configuration files
└── data/                  # Data directory
```

## Features

✅ **Self-contained**: All dependencies included
✅ **Cross-platform**: Works on Windows, macOS, Linux
✅ **No installation**: Just run the launcher
✅ **Isolated**: Doesn't affect system Python
✅ **Portable**: Can be moved to different locations

## Examples

```bash
# Validate a single file
./bin/aiailint validate script.yaml

# Validate with verbose output
./bin/aiailint validate script.yaml --verbose

# Validate entire package
./bin/aiailint validate --package /path/to/package/

# Get help
./bin/aiailint --help
```
EOF
}

# Function to create data structure
create_data_structure() {
    local app_dir="$1"
    
    print_status "Creating data directory structure"
    
    # Create data subdirectories
    mkdir -p "$app_dir/data"/{logs,cache,temp,output}
    
    # Create .gitkeep files
    touch "$app_dir/data/logs/.gitkeep"
    touch "$app_dir/data/cache/.gitkeep"
    touch "$app_dir/data/temp/.gitkeep"
    touch "$app_dir/data/output/.gitkeep"
}

# Function to create installation script
create_install_script() {
    local app_dir="$1"
    
    print_status "Creating installation script"
    
    cat > "$app_dir/install.sh" << 'EOF'
#!/bin/bash

# aiailint.app Installation Script
# This script installs aiailint.app to a system location

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Default installation directory
INSTALL_DIR="/opt/aiailint"
BIN_DIR="/usr/local/bin"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --prefix)
            INSTALL_DIR="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --prefix DIR    Installation directory (default: /opt/aiailint)"
            echo "  --help          Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

print_status "Installing aiailint.app to $INSTALL_DIR"

# Check if running as root for system installation
if [ "$EUID" -ne 0 ] && [ "$INSTALL_DIR" = "/opt/aiailint" ]; then
    print_error "System installation requires root privileges"
    print_status "Use --prefix to install to a user directory"
    exit 1
fi

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Copy app files
print_status "Copying app files"
cp -r * "$INSTALL_DIR/"

# Create symlink in bin directory
print_status "Creating symlink"
if [ -w "$BIN_DIR" ]; then
    ln -sf "$INSTALL_DIR/bin/aiailint" "$BIN_DIR/aiailint"
    print_success "Symlink created: $BIN_DIR/aiailint"
else
    print_warning "Cannot create symlink in $BIN_DIR (requires root)"
    print_status "You can create a symlink manually:"
    echo "  sudo ln -sf $INSTALL_DIR/bin/aiailint $BIN_DIR/aiailint"
fi

print_success "Installation completed!"
print_status "You can now run: aiailint --help"
EOF

    chmod +x "$app_dir/install.sh"
}

# Function to create uninstall script
create_uninstall_script() {
    local app_dir="$1"
    
    print_status "Creating uninstall script"
    
    cat > "$app_dir/uninstall.sh" << 'EOF'
#!/bin/bash

# aiailint.app Uninstall Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# Default installation directory
INSTALL_DIR="/opt/aiailint"
BIN_DIR="/usr/local/bin"

print_status "Uninstalling aiailint.app from $INSTALL_DIR"

# Remove symlink
if [ -L "$BIN_DIR/aiailint" ]; then
    rm -f "$BIN_DIR/aiailint"
    print_success "Removed symlink: $BIN_DIR/aiailint"
fi

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    print_success "Removed installation directory: $INSTALL_DIR"
else
    print_warning "Installation directory not found: $INSTALL_DIR"
fi

print_success "Uninstallation completed!"
EOF

    chmod +x "$app_dir/uninstall.sh"
}

# Function to show help
show_help() {
    echo "aiailint Self-Contained App Builder"
    echo
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  --clean         Clean existing app directory before building"
    echo "  --install       Create installation scripts"
    echo
    echo "This script creates a self-contained aiailint.app directory with:"
    echo "  - All Python dependencies in isolated virtual environment"
    echo "  - Cross-platform launcher scripts"
    echo "  - Complete documentation"
    echo "  - Configuration files"
    echo "  - Data directory structure"
    echo
    echo "After creation, you can run:"
    echo "  ./aiailint.app/bin/aiailint --help"
}

# Main function
main() {
    local clean_build=false
    local create_install_scripts=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            --clean)
                clean_build=true
                shift
                ;;
            --install)
                create_install_scripts=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Clean existing app if requested
    if [ "$clean_build" = true ] && [ -d "aiailint.app" ]; then
        print_status "Cleaning existing aiailint.app directory"
        rm -rf aiailint.app
    fi
    
    # Create self-contained app
    create_self_contained_app
    
    # Create installation scripts if requested
    if [ "$create_install_scripts" = true ]; then
        create_install_script "aiailint.app"
        create_uninstall_script "aiailint.app"
    fi
    
    print_success "Self-contained aiailint.app created successfully!"
    echo
    print_status "To use the app:"
    echo "  ./aiailint.app/bin/aiailint --help"
    echo
    print_status "App structure:"
    echo "  aiailint.app/"
    echo "  ├── bin/          # Launcher scripts"
    echo "  ├── lib/          # Python virtual environment"
    echo "  ├── src/          # aiailint source code"
    echo "  ├── docs/         # Documentation"
    echo "  ├── config/       # Configuration files"
    echo "  └── data/         # Data directory"
}

# Run main function
main "$@"
