#!/bin/bash
set -e

echo "Running all tests..."

# Test framework
echo "Testing AIAI framework..."
cd framework
python -m pytest tests/
cd ..

# Test packages
echo "Testing AIAI packages..."
cd packages
for package in */; do
    if [ -d "$package/tests" ]; then
        echo "Testing $(basename $package)..."
        cd "$package"
        python -m pytest tests/
        cd ..
    fi
done
cd ..

# Test tools
echo "Testing AIAI tools..."
cd aiailint
python -m pytest tests/
cd ../s2m
python -m pytest tests/
cd ..

echo "All tests passed!" 