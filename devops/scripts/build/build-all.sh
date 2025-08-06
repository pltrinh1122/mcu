#!/bin/bash
set -e

echo "Building all AIAI components..."

# Build framework
echo "Building AIAI framework..."
cd framework
./scripts/build.sh
cd ..

# Build packages
echo "Building AIAI packages..."
cd packages
for package in */; do
    if [ -f "$package/scripts/build.sh" ]; then
        echo "Building $(basename $package)..."
        cd "$package"
        ./scripts/build.sh
        cd ..
    fi
done
cd ..

# Build tools
echo "Building AIAI tools..."
cd aiailint
./scripts/build.sh
cd ../s2m
./scripts/build.sh
cd ..

echo "All components built successfully!" 