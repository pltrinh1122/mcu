#!/bin/bash

# Prepare Distribution Version Script
# Converts development version (with soft links) to distribution version (with actual files)

set -e

PACKAGE_DIR="ubuntu-btrfs-aiai"
SOURCE_DIR="aiai"

echo "Preparing Ubuntu-BTRFS AIAI Package for distribution..."

# Check if we're in the right directory
if [ ! -d "$PACKAGE_DIR" ]; then
    echo "Error: $PACKAGE_DIR directory not found"
    exit 1
fi

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: $SOURCE_DIR directory not found"
    exit 1
fi

# Check if files are currently soft links
if [ -L "$PACKAGE_DIR/aiai_spec.md" ] && [ -L "$PACKAGE_DIR/aiai_schema.json" ]; then
    echo "Detected development version with soft links"
    
    # Remove soft links
    echo "Removing soft links..."
    rm "$PACKAGE_DIR/aiai_spec.md"
    rm "$PACKAGE_DIR/aiai_schema.json"
    
    # Copy actual files
    echo "Copying actual files..."
    cp "$SOURCE_DIR/aiai_spec.md" "$PACKAGE_DIR/"
    cp "$SOURCE_DIR/aiai_schema.json" "$PACKAGE_DIR/"
    
    echo "Distribution version prepared successfully!"
    echo "Files are now actual copies, not soft links"
    
elif [ -f "$PACKAGE_DIR/aiai_spec.md" ] && [ -f "$PACKAGE_DIR/aiai_schema.json" ] && [ ! -L "$PACKAGE_DIR/aiai_spec.md" ] && [ ! -L "$PACKAGE_DIR/aiai_schema.json" ]; then
    echo "Detected distribution version with actual files"
    echo "No conversion needed"
    
else
    echo "Error: Unexpected file state detected"
    echo "Please check the package structure manually"
    exit 1
fi

echo "Package is ready for distribution!" 