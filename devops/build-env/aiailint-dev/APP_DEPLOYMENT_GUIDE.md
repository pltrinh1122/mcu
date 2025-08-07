# aiailint.app Deployment Guide

## Overview

This guide explains how to create and use a **self-contained `aiailint.app`** that bundles all Python dependencies and provides a safe, isolated execution environment.

## Two Deployment Approaches

### 1. **Build Environment Approach** (Current)
- **Location**: `devops/build-env/`
- **Purpose**: Development and testing
- **Usage**: Requires virtual environment activation
- **Safety**: ✅ Isolated but requires setup

### 2. **Self-Contained App Approach** (New)
- **Location**: `devops/build-env/aiailint.app/`
- **Purpose**: Production deployment and distribution
- **Usage**: Direct execution without setup
- **Safety**: ✅ Fully self-contained and isolated

## Creating the Self-Contained App

### Step 1: Build the App
```bash
cd devops/build-env
./scripts/create-app.sh --install
```

This creates:
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
├── data/                  # Data directory
├── install.sh             # Installation script
└── uninstall.sh           # Uninstall script
```

### Step 2: Use the App

#### **Unix/Linux/macOS**
```bash
# Direct execution
./aiailint.app/bin/aiailint validate script.yaml
./aiailint.app/bin/aiailint --help

# Cross-platform Python launcher
python aiailint.app/bin/aiailint.py validate script.yaml
```

#### **Windows**
```cmd
# Windows batch launcher
aiailint.app\bin\aiailint.bat validate script.yaml
aiailint.app\bin\aiailint.bat --help

# Cross-platform Python launcher
python aiailint.app\bin\aiailint.py validate script.yaml
```

## Safety & Containment Features

### ✅ **Complete Isolation**
- **Python Virtual Environment**: All dependencies in `lib/venv/`
- **No System Pollution**: Doesn't affect system Python packages
- **Self-Contained**: Everything needed is in the app directory
- **Portable**: Can be moved to different locations

### ✅ **Cross-Platform Support**
- **Unix Launcher**: `bin/aiailint` (bash script)
- **Windows Launcher**: `bin/aiailint.bat` (batch script)
- **Python Launcher**: `bin/aiailint.py` (cross-platform)

### ✅ **Dependency Management**
- **Isolated Environment**: Virtual environment in `lib/venv/`
- **Version Control**: Dependencies pinned in requirements files
- **No Conflicts**: Won't interfere with other Python projects
- **Reproducible**: Same environment everywhere

## Installation Options

### **Option 1: Portable (Recommended)**
```bash
# Just run directly - no installation needed
./aiailint.app/bin/aiailint --help
```

### **Option 2: System Installation**
```bash
cd aiailint.app
sudo ./install.sh                    # System-wide installation
./install.sh --prefix ~/local/aiai   # User installation
```

### **Option 3: Development Environment**
```bash
cd devops/build-env
./scripts/setup-env.sh
source venv/bin/activate
aiailint --help
```

## Comparison: Build Environment vs Self-Contained App

| Feature | Build Environment | Self-Contained App |
|---------|------------------|-------------------|
| **Setup Required** | ✅ Virtual environment activation | ❌ No setup needed |
| **Portability** | ❌ Tied to build environment | ✅ Fully portable |
| **Dependencies** | ✅ Isolated in venv | ✅ Isolated in app |
| **Cross-Platform** | ✅ Works everywhere | ✅ Multiple launchers |
| **Distribution** | ❌ Requires build env | ✅ Self-contained |
| **User Experience** | ⚠️ Requires technical knowledge | ✅ Simple execution |

## Security Benefits

### **Isolation**
- **No System Dependencies**: All Python packages in app
- **No Path Pollution**: Doesn't modify system PATH
- **No Package Conflicts**: Isolated virtual environment
- **No Permission Issues**: Runs in user space

### **Containment**
- **Self-Contained**: Everything needed is included
- **No Installation**: Just copy and run
- **No Registry Changes**: No system modifications
- **No Side Effects**: Clean execution environment

## Usage Examples

### **Basic Validation**
```bash
# Validate a single file
./aiailint.app/bin/aiailint validate script.yaml

# Validate with verbose output
./aiailint.app/bin/aiailint validate script.yaml --verbose

# Validate entire package
./aiailint.app/bin/aiailint validate --package /path/to/package/
```

### **Help and Information**
```bash
# Get help
./aiailint.app/bin/aiailint --help

# Show version
./aiailint.app/bin/aiailint --version

# List commands
./aiailint.app/bin/aiailint --help
```

### **Different Output Formats**
```bash
# Text output (default)
./aiailint.app/bin/aiailint validate script.yaml

# JSON output
./aiailint.app/bin/aiailint validate script.yaml --format json

# Verbose output
./aiailint.app/bin/aiailint validate script.yaml --verbose
```

## Troubleshooting

### **Permission Issues**
```bash
# Make launcher executable
chmod +x aiailint.app/bin/aiailint

# Check Python in virtual environment
aiailint.app/lib/venv/bin/python --version
```

### **Dependency Issues**
```bash
# Rebuild app with clean dependencies
./scripts/create-app.sh --clean
```

### **Path Issues**
```bash
# Check if Python is found
which python
which python3

# Use explicit Python launcher
python aiailint.app/bin/aiailint.py --help
```

## Development vs Production

### **Development Environment**
- **Location**: `devops/build-env/`
- **Purpose**: Development, testing, debugging
- **Setup**: `./scripts/setup-env.sh`
- **Usage**: `source venv/bin/activate`

### **Production App**
- **Location**: `devops/build-env/aiailint.app/`
- **Purpose**: Distribution, deployment, end users
- **Setup**: `./scripts/create-app.sh`
- **Usage**: `./bin/aiailint --help`

## Best Practices

### **For Developers**
1. Use build environment for development
2. Test with self-contained app before release
3. Keep dependencies updated in requirements files
4. Use version control for app configuration

### **For End Users**
1. Use self-contained app for production
2. Keep app directory intact
3. Don't modify files in `lib/venv/`
4. Use launcher scripts, not direct Python execution

### **For Deployment**
1. Build app on target platform
2. Test app thoroughly before distribution
3. Include documentation in app
4. Provide installation scripts for convenience

---

## Summary

The **self-contained `aiailint.app`** provides:

✅ **Safety**: Complete isolation from system Python  
✅ **Simplicity**: No setup required, just run  
✅ **Portability**: Works anywhere, can be moved  
✅ **Cross-Platform**: Multiple launcher options  
✅ **Distribution**: Easy to package and distribute  

This approach gives you the best of both worlds: a development environment for building and testing, and a self-contained app for deployment and distribution.
