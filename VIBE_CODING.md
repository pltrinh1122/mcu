# Vibe-Coding Workflow

## Overview

This document defines the standard **Vibe-Coding Workflow** for AI-assisted development in the AIAI project. It establishes default behaviors, validation requirements, and quality standards that apply across all components.

## Core Philosophy

### **Rapid Create → Validate → Test → Commit**

✅ **Fast iteration** with AI assistance  
✅ **Quality assurance** through automated validation  
✅ **Consistent standards** across all components  
✅ **Confidence in commits** through comprehensive testing  

## Default Workflow

### **Step 1: Create**
```bash
# Generate code, configs, documentation
# Follow project standards and templates
# Use AI assistance for rapid development
```

**AI Behavior:**
- Create files with proper syntax and structure
- Follow established patterns and conventions
- Use templates when available
- Document decisions and rationale

### **Step 2: Validate**
```bash
# YAML files
yamllint filename.yaml

# JSON files  
jq . filename.json

# Shell scripts
shellcheck script.sh

# Python files
python -m py_compile file.py

# Markdown files
markdownlint filename.md
```

**AI Behavior:**
- **Always run validation** after creating files
- **Fix syntax errors** before proceeding
- **Report validation results** clearly
- **Skip validation only if tool unavailable**

### **Step 3: Test**
```bash
# Unit tests
pytest tests/

# Integration tests
task test

# Manual verification
# Verify functionality works as expected
```

**AI Behavior:**
- **Run relevant tests** for changed components
- **Verify functionality** works as expected
- **Check for regressions** in related areas
- **Report test results** with clear pass/fail status

### **Step 4: Commit**
```bash
# Pre-commit hooks run automatically
git add .
git commit -m "Descriptive commit message"
```

**AI Behavior:**
- **Write descriptive commit messages**
- **Include context and rationale**
- **Reference related issues or components**
- **Ensure all validation passes before commit**

## Validation Requirements

### **YAML Files**
```bash
# Required validation
yamllint filename.yaml

# Common issues to check:
# - Unescaped colons in strings
# - Quote mismatches
# - Indentation errors
# - Invalid YAML structure
```

### **JSON Files**
```bash
# Required validation
jq . filename.json

# Check for:
# - Valid JSON syntax
# - Proper structure
# - Required fields present
```

### **Shell Scripts**
```bash
# Required validation
shellcheck script.sh

# Check for:
# - Shell syntax errors
# - Security issues
# - Best practices
```

### **Python Files**
```bash
# Required validation
python -m py_compile file.py

# Additional checks:
# - mypy for type checking
# - black for formatting
# - flake8 for linting
```

### **Markdown Files**
```bash
# Required validation
markdownlint filename.md

# Check for:
# - Proper markdown syntax
# - Consistent formatting
# - Valid links and references
```

## Quality Standards

### **Code Quality**
- **Syntax**: All files must pass syntax validation
- **Formatting**: Follow project formatting standards
- **Documentation**: Include appropriate documentation
- **Tests**: Add tests for new functionality

### **Commit Quality**
- **Descriptive messages**: Clear what changed and why
- **Atomic commits**: One logical change per commit
- **Validation passing**: All checks must pass
- **Tests passing**: All tests must pass

### **Documentation Quality**
- **Clear structure**: Logical organization
- **Complete coverage**: All important aspects documented
- **Up-to-date**: Reflects current state
- **Actionable**: Provides clear guidance

## AI Assistant Guidelines

### **When Creating Files**
1. **Use templates** when available
2. **Follow established patterns** in the codebase
3. **Include appropriate documentation**
4. **Add validation and tests**
5. **Consider security implications**

### **When Validating**
1. **Run all relevant validators**
2. **Fix issues before proceeding**
3. **Report results clearly**
4. **Explain any skipped validations**

### **When Testing**
1. **Run unit tests** for changed components
2. **Run integration tests** if available
3. **Verify manual functionality**
4. **Check for regressions**

### **When Committing**
1. **Ensure all validation passes**
2. **Write descriptive commit messages**
3. **Include context and rationale**
4. **Reference related issues**

## Component-Specific Overrides

Individual components can override these defaults by including a `VIBE_CODING.md` file in their directory. Component-specific files should:

1. **Extend** the default workflow, not replace it
2. **Add** component-specific validation requirements
3. **Customize** testing procedures for the component
4. **Document** component-specific conventions

### **Example Component Override**
```markdown
# Component-Specific Vibe-Coding

## Additional Validation
- **Schema validation**: `python -m jsonschema -i file.json schema.json`
- **API testing**: `pytest tests/api/`

## Component-Specific Tests
- **Integration tests**: `task test:integration`
- **Performance tests**: `task test:performance`

## Component Conventions
- **Naming**: Use `component_` prefix for all files
- **Structure**: Follow component-specific directory layout
```

## Error Handling

### **Validation Failures**
1. **Identify the issue** clearly
2. **Fix the problem** before proceeding
3. **Re-run validation** to confirm fix
4. **Document the issue** if it's a common pattern

### **Test Failures**
1. **Understand the failure** (read error messages)
2. **Fix the underlying issue**
3. **Re-run tests** to confirm fix
4. **Check for regressions** in related areas

### **Tool Unavailability**
1. **Report missing tools** clearly
2. **Provide installation instructions**
3. **Skip validation** only if tool unavailable
4. **Note in commit message** that validation was skipped

## Success Metrics

### **Quality Metrics**
- **Validation pass rate**: 100% of files pass validation
- **Test pass rate**: 100% of tests pass
- **Commit quality**: Descriptive, atomic commits
- **Documentation coverage**: All components documented

### **Efficiency Metrics**
- **Rapid iteration**: Quick create → validate → test cycles
- **Confidence in commits**: No broken code committed
- **Reduced debugging**: Issues caught early in workflow
- **Consistent standards**: Uniform quality across components

## Tools and Dependencies

### **Required Tools**
```bash
# YAML validation
pip install yamllint

# JSON validation  
# jq (usually pre-installed)

# Shell validation
# shellcheck (install via package manager)

# Markdown validation
npm install -g markdownlint-cli

# Python validation
pip install black flake8 mypy
```

### **Optional Tools**
```bash
# Additional validation
pip install jsonschema  # JSON schema validation
pip install yamale      # YAML schema validation

# Performance testing
pip install pytest-benchmark

# Security scanning
pip install bandit safety
```

## Integration with Existing Workflows

### **Git Hooks**
- **Pre-commit**: Automatic validation before commits
- **Post-commit**: Success notifications
- **Pre-push**: Final validation before pushing

### **CI/CD Integration**
- **Validation**: All files validated in CI
- **Testing**: All tests run in CI
- **Quality**: Code quality checks in CI
- **Documentation**: Documentation validation in CI

### **IDE Integration**
- **Real-time validation**: Show errors as you type
- **Auto-formatting**: Format code on save
- **Linting**: Show linting errors in editor
- **Testing**: Run tests from IDE

## Troubleshooting

### **Common Issues**

**YAML Validation Failures**
```bash
# Check for unescaped colons
grep -n ":" filename.yaml | grep -v ":"

# Check indentation
yamllint filename.yaml

# Fix common issues
# - Escape colons: echo "Error\: message"
# - Use quotes: echo "Error: message"
# - Fix indentation: Use spaces, not tabs
```

**JSON Validation Failures**
```bash
# Check JSON syntax
jq . filename.json

# Fix common issues
# - Missing commas
# - Unclosed brackets/braces
# - Invalid escape sequences
```

**Shell Validation Failures**
```bash
# Check shell syntax
shellcheck script.sh

# Fix common issues
# - Quote variables: "$var" not $var
# - Use [[ ]] for tests
# - Handle errors properly
```

### **Getting Help**
1. **Check tool documentation** for specific errors
2. **Review project conventions** for patterns
3. **Ask for clarification** if unsure about requirements
4. **Document solutions** for future reference

## Conclusion

The Vibe-Coding Workflow ensures **rapid, high-quality development** with AI assistance while maintaining **consistent standards** across all components. By following this workflow, we achieve:

✅ **Fast iteration** with confidence  
✅ **Quality assurance** through validation  
✅ **Consistent standards** across components  
✅ **Reduced debugging** through early error detection  
✅ **Maintainable code** through proper testing  

This workflow scales from individual components to the entire project, providing a foundation for collaborative AI-assisted development.
