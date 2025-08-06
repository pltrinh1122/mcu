#!/bin/bash

# aiailint runner script
# Activates the virtual environment and runs aiailint with provided arguments

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Path to the virtual environment
VENV_PATH="$SCRIPT_DIR/../../../../aiailint_env"

# Path to the aiailint tool
AIAILINT_PATH="$SCRIPT_DIR/src/aiailint.py"

# Check if virtual environment exists
if [ ! -f "$VENV_PATH/bin/activate" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    echo "Please run: python3 -m venv aiailint_env && source aiailint_env/bin/activate && pip install pyyaml jsonschema bashlex"
    exit 1
fi

# Activate virtual environment and run aiailint
source "$VENV_PATH/bin/activate"
python3 "$AIAILINT_PATH" "$@" 