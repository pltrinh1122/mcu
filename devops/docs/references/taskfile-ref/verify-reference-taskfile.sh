#!/bin/bash

# Taskfile Reference Verification Script
# This script verifies that our curated reference is accurate

set -e

# Capture script directory early
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔍 Verifying Taskfile Reference Accuracy..."
echo "=========================================="
echo "Script directory: $SCRIPT_DIR"

# 1. Check if Task is installed and working
echo "1. Verifying Task installation..."
if command -v task >/dev/null 2>&1; then
    TASK_VERSION=$(task --version)
    echo "✅ Task installed: $TASK_VERSION"
else
    echo "❌ Task not found in PATH"
    exit 1
fi

# 2. Verify basic Taskfile syntax
echo ""
echo "2. Testing basic Taskfile syntax..."
cat > /tmp/test-taskfile.yml << 'EOF'
version: '3'
tasks:
  test:
    desc: "Test task"
    cmds:
      - echo "Hello from Task!"
EOF

if task --taskfile /tmp/test-taskfile.yml --list >/dev/null 2>&1; then
    echo "✅ Basic Taskfile syntax is correct"
else
    echo "❌ Basic Taskfile syntax failed"
    exit 1
fi

# 3. Test our documented features
echo ""
echo "3. Testing documented features..."

# Test includes
cat > /tmp/base-tasks.yml << 'EOF'
version: '3'
tasks:
  setup:
    desc: "Base setup"
    cmds:
      - echo "Base setup"
EOF

cat > /tmp/main-taskfile.yml << 'EOF'
version: '3'
includes:
  base:
    taskfile: ./base-tasks.yml
tasks:
  test:
    desc: "Test task"
    cmds:
      - task: base:setup
EOF

cd /tmp
if task --taskfile main-taskfile.yml --list >/dev/null 2>&1; then
    echo "✅ Include system works as documented"
else
    echo "❌ Include system failed"
fi
cd "$SCRIPT_DIR"

# 4. Verify schema against official schema
echo ""
echo "4. Verifying schema information..."
if [ -f "$SCRIPT_DIR/taskfile-schema.json" ]; then
    echo "✅ Official schema file exists"
    SCHEMA_SIZE=$(wc -c < "$SCRIPT_DIR/taskfile-schema.json")
    echo "   Schema size: $SCHEMA_SIZE bytes"
else
    echo "❌ Official schema file missing"
    echo "   Looking for: $SCRIPT_DIR/taskfile-schema.json"
    ls -la "$SCRIPT_DIR/" | grep schema || echo "   No schema files found"
fi

# 5. Test documented commands
echo ""
echo "5. Testing documented commands..."
COMMANDS=("--help" "--version")
for cmd in "${COMMANDS[@]}"; do
    if task $cmd >/dev/null 2>&1; then
        echo "✅ Command '$cmd' works"
    else
        echo "❌ Command '$cmd' failed"
    fi
done

# Test commands that need a Taskfile
cd /tmp
cat > test-taskfile.yml << 'EOF'
version: '3'
tasks:
  test:
    desc: "Test task"
    cmds:
      - echo "Test"
EOF

if task --taskfile test-taskfile.yml --list >/dev/null 2>&1; then
    echo "✅ Command '--list' works with Taskfile"
else
    echo "❌ Command '--list' failed"
fi

if task --taskfile test-taskfile.yml --dry test >/dev/null 2>&1; then
    echo "✅ Command '--dry' works with Taskfile"
else
    echo "❌ Command '--dry' failed"
fi

if task --taskfile test-taskfile.yml --verbose test >/dev/null 2>&1; then
    echo "✅ Command '--verbose' works with Taskfile"
else
    echo "❌ Command '--verbose' failed"
fi
cd "$SCRIPT_DIR"

# 6. Verify our reference file exists and is readable
echo ""
echo "6. Checking reference file..."
if [ -f "$SCRIPT_DIR/TASKFILE_REFERENCE.md" ]; then
    echo "✅ Reference file exists"
    REF_SIZE=$(wc -l < "$SCRIPT_DIR/TASKFILE_REFERENCE.md")
    echo "   Reference lines: $REF_SIZE"
else
    echo "❌ Reference file missing"
    echo "   Looking for: $SCRIPT_DIR/TASKFILE_REFERENCE.md"
    ls -la "$SCRIPT_DIR/" | grep REFERENCE || echo "   No reference files found"
fi

# 7. Check for common issues mentioned in our reference
echo ""
echo "7. Testing common issues mentioned in reference..."

# Test YAML syntax with colons (should work)
cat > /tmp/colon-test.yml << 'EOF'
version: '3'
tasks:
  test:
    desc: "Test with colon: in description"
    cmds:
      - echo "Testing colon handling"
EOF

if task --taskfile /tmp/colon-test.yml --list >/dev/null 2>&1; then
    echo "✅ Colon handling works correctly"
else
    echo "❌ Colon handling failed"
fi

# Cleanup
rm -f /tmp/test-taskfile.yml /tmp/base-tasks.yml /tmp/main-taskfile.yml /tmp/colon-test.yml

echo ""
echo "🎉 Verification complete!"
echo "If all checks passed, our reference should be accurate."
