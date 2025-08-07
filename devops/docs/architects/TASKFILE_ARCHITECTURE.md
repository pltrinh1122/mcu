# Configuration Management Design

## Overview

This document describes the Taskfile-based configuration management system for building and deploying development environments. The system provides a tool-agnostic interface through configuration-driven wrapper generation, enabling seamless tool migration without developer retraining.

## Dependencies

### Core Dependencies

#### **Required Dependencies**
- **Task**: Build tool for task execution and dependency management
  - Version: 3.x or later
  - Installation: `sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin`
  - Purpose: Primary build tool for task execution and environment management

- **Python**: Runtime for generator scripts and utilities
  - Version: 3.7 or later
  - Purpose: Execute generator scripts (`generate_taskfile.py`, `generate_wrappers.py`)
  - Required packages: `pyyaml`, `argparse` (built-in), `pathlib` (built-in)

- **Bash**: Shell for wrapper script execution
  - Version: 4.0 or later
  - Purpose: Execute generated wrapper scripts and shell commands
  - Features: Variable expansion, conditional logic, command chaining

- **YAML Parser**: Configuration file processing
  - Package: `PyYAML` (Python)
  - Installation: `pip install pyyaml`
  - Purpose: Parse component configurations and wrapper definitions

#### **Optional Dependencies**

- **yq**: YAML query tool for configuration parsing
  - Purpose: Extract values from YAML configs in shell scripts
  - Installation: `sudo apt install yq` or `go install github.com/mikefarah/yq/v4@latest`
  - Alternative: Can be replaced with `grep`/`sed` for simple extractions

- **Just**: Alternative build tool
  - Purpose: Alternative to Task for build execution
  - Installation: `curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash`
  - Usage: `just setup`, `just test`, `just build`

- **Make**: Traditional build tool
  - Purpose: Alternative to Task for build execution
  - Installation: Usually pre-installed on Unix systems
  - Usage: `make setup`, `make test`, `make build`

- **SSH**: Remote deployment support
  - Purpose: Execute remote commands and file transfers
  - Installation: Usually pre-installed on Unix systems
  - Usage: `ssh user@host command`, `scp file user@host:path`

- **Docker**: Container-based deployment
  - Purpose: Containerized environment and deployment
  - Installation: `sudo apt install docker.io` or Docker Desktop
  - Usage: `docker build`, `docker run`, `docker-compose`

- **Kubernetes**: Orchestrated deployment
  - Purpose: Kubernetes-based deployment and scaling
  - Installation: `kubectl` CLI tool
  - Usage: `kubectl apply`, `kubectl set image`

#### **Development Dependencies**

- **Git**: Version control
  - Purpose: Source code management and deployment tracking
  - Installation: Usually pre-installed on development systems

- **Virtual Environment**: Python isolation
  - Purpose: Isolate Python dependencies per component
  - Usage: `python3 -m venv venv`, `source venv/bin/activate`

- **Code Quality Tools**: Development standards
  - **black**: Code formatting (`pip install black`)
  - **flake8**: Linting (`pip install flake8`)
  - **mypy**: Type checking (`pip install mypy`)
  - **pytest**: Testing (`pip install pytest`)

### Dependency Management

#### **Installation Script**
```bash
#!/bin/bash
# install-dependencies.sh

set -e

echo "Installing Configuration Management Dependencies..."

# Install Task
if ! command -v task &> /dev/null; then
    echo "Installing Task..."
    sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
else
    echo "Task already installed: $(task --version)"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install pyyaml

# Install yq (optional)
if ! command -v yq &> /dev/null; then
    echo "Installing yq..."
    sudo apt install yq -y
else
    echo "yq already installed: $(yq --version)"
fi

# Install Just (optional)
if ! command -v just &> /dev/null; then
    echo "Installing Just..."
    curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash
else
    echo "Just already installed: $(just --version)"
fi

# Verify installations
echo "Verifying installations..."
task --version
python3 --version
bash --version
yq --version
just --version

echo "All dependencies installed successfully!"
```

#### **Dependency Verification**
```bash
#!/bin/bash
# verify-dependencies.sh

set -e

echo "Verifying Configuration Management Dependencies..."

# Check required dependencies
required_tools=("task" "python3" "bash" "pip")
for tool in "${required_tools[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        echo "❌ Required tool not found: $tool"
        exit 1
    else
        echo "✅ $tool: $(command -v "$tool")"
    fi
done

# Check Python packages
python3 -c "import yaml" || {
    echo "❌ Python package not found: pyyaml"
    echo "Install with: pip install pyyaml"
    exit 1
}
echo "✅ Python package: pyyaml"

# Check optional dependencies
optional_tools=("yq" "just" "make" "ssh" "docker" "kubectl")
for tool in "${optional_tools[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo "✅ Optional tool available: $tool"
    else
        echo "⚠️  Optional tool not found: $tool"
    fi
done

echo "Dependency verification completed!"
```

### Platform Support

#### **Linux (Ubuntu/Debian)**
- **Primary platform** with full dependency support
- All tools available via package managers
- Native SSH and shell support

#### **macOS**
- **Supported platform** with most dependencies available
- Homebrew installation: `brew install task just yq`
- Native SSH and shell support

#### **Windows**
- **Limited support** via WSL2 or Git Bash
- Task and Just work natively
- Python and Bash available via WSL2
- SSH support via WSL2 or Git Bash

#### **CI/CD Environments**
- **GitHub Actions**: Ubuntu runners with full support
- **GitLab CI**: Docker-based with dependency installation
- **Jenkins**: Agent-based with tool installation
- **Docker**: Containerized environments with all dependencies

### Version Compatibility

#### **Minimum Versions**
- **Task**: 3.0.0+ (for YAML v3 syntax)
- **Python**: 3.7+ (for f-strings and pathlib)
- **Bash**: 4.0+ (for associative arrays and advanced features)
- **PyYAML**: 5.1+ (for safe_load and modern features)

#### **Recommended Versions**
- **Task**: Latest stable (3.x)
- **Python**: 3.9+ (for better type hints and performance)
- **Bash**: 5.0+ (for latest shell features)
- **PyYAML**: 6.0+ (for latest YAML features)

### Dependency Conflicts

#### **Build Tool Conflicts**
- **Task vs Just vs Make**: No conflicts, can coexist
- **Multiple Python versions**: Use virtual environments
- **Shell differences**: Scripts use POSIX-compliant syntax

#### **Resolution Strategies**
- **Tool selection**: Configure via `build-tool.yaml`
- **Python isolation**: Use virtual environments per component
- **Shell compatibility**: Test scripts on target platforms

## Architecture

### Core Components

```
devops/build-env/
├── config/                          # Configuration layer
│   ├── aiailint-config.yaml        # Component-specific configuration
│   ├── wrapper-config.yaml          # Wrapper script definitions
│   └── build-tool.yaml             # Tool selection & configuration
├── scripts/                         # Generated wrapper scripts
│   ├── setup.sh                     # Generated from wrapper-config.yaml
│   ├── test.sh                      # Generated from wrapper-config.yaml
│   ├── build.sh                     # Generated from wrapper-config.yaml
│   └── deploy.sh                    # Generated from wrapper-config.yaml
├── environments/                     # Generated environments
│   └── aiailint-dev/               # Component-specific environment
│       ├── Taskfile.yml             # Generated from component config
│       ├── Justfile                 # Alternative implementation
│       ├── Makefile                 # Alternative implementation
│       └── custom-deploy.py         # Custom implementation
├── generate_taskfile.py             # Taskfile generator
├── generate_wrappers.py             # Wrapper script generator
└── Taskfile.yml                     # Meta-build system
```

### Configuration Layers

#### 1. Component Configuration (`config/aiailint-config.yaml`)
Defines component-specific build parameters, dependencies, and deployment targets.

```yaml
component:
  name: "aiailint"
  type: "tool"
  language: "python"
  description: "AIAI Script validation tool"

dependencies:
  production:
    - "pyyaml>=6.0"
    - "jsonschema>=4.0"
  development:
    - "pytest>=7.0"
    - "black>=23.0"
    - "flake8>=6.0"
    - "mypy>=1.0"

targets:
  setup:
    description: "Setup development environment"
    commands:
      - "python3 -m venv venv"
      - "source venv/bin/activate && pip install -r requirements/requirements-dev.txt"
      - "pip install -e ../../../aiailint/"
  
  test:
    description: "Run tests"
    commands:
      - "source venv/bin/activate && pytest tests/ --cov=aiailint"
    depends_on: ["setup"]
  
  build:
    description: "Build package"
    commands:
      - "source venv/bin/activate && python -m build"
    depends_on: ["test"]
  
  deploy:
    description: "Deploy component"
    commands:
      - "source venv/bin/activate && python setup.py sdist bdist_wheel"
      - "scp dist/*.whl {{.REMOTE_USER}}@{{.REMOTE_HOST}}:{{.REMOTE_PATH}}/"
      - "ssh {{.REMOTE_USER}}@{{.REMOTE_HOST}} 'cd {{.REMOTE_PATH}} && pip install *.whl'"
    depends_on: ["build"]
```

#### 2. Wrapper Configuration (`config/wrapper-config.yaml`)
Defines the tool-agnostic interface and tool-specific mappings.

```yaml
wrappers:
  setup:
    description: "Setup development environment"
    arguments: []
    options:
      component:
        type: "string"
        default: "aiailint"
        description: "Component to setup"
    tool_mappings:
      task:
        command: "task setup"
        args: []
      just:
        command: "just setup"
        args: []
      make:
        command: "make setup"
        args: []

  test:
    description: "Run tests"
    arguments: []
    options:
      component:
        type: "string"
        default: "aiailint"
        description: "Component to test"
      parallel:
        type: "boolean"
        default: false
        description: "Run tests in parallel"
    tool_mappings:
      task:
        command: "task test"
        args: ["{{parallel_flag}}"]
      just:
        command: "just test"
        args: ["{{parallel_flag}}"]
      make:
        command: "make test"
        args: ["{{parallel_flag}}"]

  deploy:
    description: "Deploy component"
    arguments: ["environment"]
    options:
      component:
        type: "string"
        default: "aiailint"
        description: "Component to deploy"
      version:
        type: "string"
        description: "Version to deploy"
    tool_mappings:
      task:
        command: "task deploy"
        args: ["ENVIRONMENT={{environment}}", "VERSION={{version}}"]
      just:
        command: "just deploy"
        args: ["--environment", "{{environment}}", "--version", "{{version}}"]
      make:
        command: "make deploy"
        args: ["ENVIRONMENT={{environment}}", "VERSION={{version}}"]
```

#### 3. Build Tool Configuration (`config/build-tool.yaml`)
Defines which build tool to use and its configuration.

```yaml
build_tool: "task"  # Can be: task, just, make, custom
tool_config:
  task:
    command: "task"
    file: "Taskfile.yml"
  just:
    command: "just"
    file: "Justfile"
  make:
    command: "make"
    file: "Makefile"
  custom:
    command: "python3"
    file: "custom_deploy.py"
```

## Tool Abstraction Benefits

### 1. Developer Interface Consistency
Developers learn one interface that works regardless of the underlying build tool:

```bash
# Same interface regardless of tool
./scripts/setup.sh
./scripts/test.sh
./scripts/build.sh
./scripts/deploy.sh production
```

### 2. Seamless Tool Migration
Tool changes are transparent to developers:

```bash
# Before migration (using Task)
./scripts/setup.sh
./scripts/deploy.sh production

# After migration (using Just) - same interface!
./scripts/setup.sh
./scripts/deploy.sh production

# Only configuration changes, no retraining needed
echo 'build_tool: "just"' > config/build-tool.yaml
task generate-wrappers
```

### 3. Tool Evaluation & Testing
Test different tools without developer impact:

```bash
# Test different tools
BUILD_TOOL=task ./scripts/test.sh
BUILD_TOOL=just ./scripts/test.sh
BUILD_TOOL=make ./scripts/test.sh
```

### 4. Environment-Specific Tools
Use different tools for different contexts:

```bash
# Development: Task (fast iteration)
BUILD_TOOL=task ./scripts/test.sh

# Production: Make (proven stability)
BUILD_TOOL=make ./scripts/deploy.sh production

# CI/CD: Just (simpler syntax)
BUILD_TOOL=just ./scripts/ci-deploy.sh
```

## Meta-Build System

### Taskfile for Environment Management
The system uses Task itself to manage the build environment generation:

```yaml
# Taskfile.yml
version: '3'

vars:
  CONFIG_DIR: "config"
  SCRIPTS_DIR: "scripts"

tasks:
  generate-wrappers:
    desc: Generate wrapper scripts from configuration
    cmds:
      - python3 generate_wrappers.py --config {{.CONFIG_DIR}}/wrapper-config.yaml --output {{.SCRIPTS_DIR}}
    sources:
      - {{.CONFIG_DIR}}/wrapper-config.yaml
      - generate_wrappers.py
    generates:
      - {{.SCRIPTS_DIR}}/setup.sh
      - {{.SCRIPTS_DIR}}/test.sh
      - {{.SCRIPTS_DIR}}/build.sh
      - {{.SCRIPTS_DIR}}/deploy.sh

  generate-taskfile:
    desc: Generate Taskfile from component configuration
    cmds:
      - python3 generate_taskfile.py --config {{.CONFIG_DIR}}/aiailint-config.yaml --output Taskfile.yml
    sources:
      - {{.CONFIG_DIR}}/aiailint-config.yaml
      - generate_taskfile.py
    generates:
      - Taskfile.yml

  setup-environment:
    desc: Setup complete development environment
    deps: [generate-wrappers, generate-taskfile]
    cmds:
      - task setup

  # Tool migration tasks
  migrate-to-task:
    desc: Migrate from current tool to Task
    cmds:
      - echo "Migrating to Task..."
      - echo 'build_tool: "task"' > {{.CONFIG_DIR}}/build-tool.yaml
      - task generate-wrappers

  migrate-to-just:
    desc: Migrate from current tool to Just
    cmds:
      - echo "Migrating to Just..."
      - echo 'build_tool: "just"' > {{.CONFIG_DIR}}/build-tool.yaml
      - task generate-wrappers
```

## Generator Scripts

### 1. Taskfile Generator (`generate_taskfile.py`)
Converts component configuration into Taskfile.yml:

```python
#!/usr/bin/env python3
import yaml
import argparse

def generate_taskfile(config_file: str, output_file: str):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    taskfile_content = f"""version: '3'

vars:
  COMPONENT_NAME: "{config['component']['name']}"
  COMPONENT_TYPE: "{config['component']['type']}"
  VENV_DIR: "venv"

tasks:
"""
    
    for target_name, target_config in config['targets'].items():
        taskfile_content += f"""  {target_name}:
    desc: {target_config['description']}
    cmds:
"""
        for command in target_config['commands']:
            taskfile_content += f"      - {command}\n"
        
        if 'depends_on' in target_config:
            deps = ", ".join([f'"{dep}"' for dep in target_config['depends_on']])
            taskfile_content += f"    deps: [{deps}]\n"
        
        taskfile_content += "\n"
    
    with open(output_file, 'w') as f:
        f.write(taskfile_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Component config file")
    parser.add_argument("--output", required=True, help="Output Taskfile.yml")
    args = parser.parse_args()
    
    generate_taskfile(args.config, args.output)
```

### 2. Wrapper Generator (`generate_wrappers.py`)
Generates tool-agnostic wrapper scripts from configuration:

```python
#!/usr/bin/env python3
import yaml
import argparse
from pathlib import Path

class WrapperGenerator:
    def __init__(self, config_file: str):
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self):
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def generate_wrapper_script(self, wrapper_name: str, config: dict) -> str:
        """Generate a wrapper script from configuration"""
        script_content = f"""#!/bin/bash
# Generated wrapper script for {wrapper_name}
set -e

# Load build tool configuration
BUILD_TOOL=${{BUILD_TOOL:-$(yq e '.build_tool' config/build-tool.yaml 2>/dev/null || echo 'task')}}
BUILD_COMMAND=${{BUILD_COMMAND:-$(yq e ".tool_config.$BUILD_TOOL.command" config/build-tool.yaml 2>/dev/null || echo 'task')}}

# Parse arguments and options
{self._generate_argument_parsing(wrapper_name, config)}

# Execute tool-specific command
case "$BUILD_TOOL" in
{self._generate_tool_mappings(wrapper_name, config)}
    *)
        echo "Unknown build tool: $BUILD_TOOL"
        echo "Supported tools: {', '.join(config['tool_mappings'].keys())}"
        exit 1
        ;;
esac

echo "{config['description']} completed!"
"""
        return script_content
    
    def generate_all_wrappers(self, output_dir: str):
        """Generate all wrapper scripts"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        for wrapper_name, config in self.config['wrappers'].items():
            script_content = self.generate_wrapper_script(wrapper_name, config)
            script_file = output_path / f"{wrapper_name}.sh"
            
            with open(script_file, 'w') as f:
                f.write(script_content)
            
            script_file.chmod(0o755)
            print(f"Generated: {script_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Wrapper configuration file")
    parser.add_argument("--output", required=True, help="Output directory for scripts")
    args = parser.parse_args()
    
    generator = WrapperGenerator(args.config)
    generator.generate_all_wrappers(args.output)
```

## Workflow

### 1. Initial Setup
```bash
# Generate wrapper scripts
task generate-wrappers

# Generate component Taskfile
task generate-taskfile

# Setup environment
task setup-environment
```

### 2. Developer Usage
```bash
# Use generated interface
./scripts/setup.sh
./scripts/test.sh
./scripts/build.sh
./scripts/deploy.sh production
```

### 3. Tool Migration
```bash
# Change build tool
echo 'build_tool: "just"' > config/build-tool.yaml

# Regenerate wrappers
task generate-wrappers

# Interface unchanged for developers
./scripts/setup.sh  # Now uses Just
```

## Benefits

### 1. Configuration-Driven
- All build logic defined in YAML configuration
- No manual script writing required
- Easy to maintain and modify

### 2. Tool Agnostic
- Support for Task, Just, Make, and custom tools
- Seamless tool migration without retraining
- Consistent developer interface

### 3. Meta-Build System
- Task generates its own abstraction layer
- Self-documenting configuration
- Automated script generation

### 4. Future-Proof
- Easy to add new tools
- Easy to modify build logic
- Easy to extend functionality

## Migration Path

### From Current System
1. **Phase 1**: Implement configuration-driven system alongside existing
2. **Phase 2**: Migrate components one by one
3. **Phase 3**: Remove old system once migration complete

### To New Tools
1. **Add tool support** to wrapper-config.yaml
2. **Regenerate wrappers** with task generate-wrappers
3. **Update build-tool.yaml** to use new tool
4. **No developer retraining** required

This design provides a robust, flexible, and maintainable configuration management system that can evolve with changing requirements while maintaining developer productivity.
