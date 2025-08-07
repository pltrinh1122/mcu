# aiailint Component-Specific VIBE_CODING Override

## Overview

This document provides component-specific overrides for the aiailint development environment. These instructions extend the global VIBE_CODING.md workflow with aiailint-specific requirements.

**Note**: This document extends, not replaces, the global VIBE_CODING.md workflow.

## Component-Specific Validation Requirements

### **YAML Schema Validation**
- **Required**: All YAML files must validate against `aiai_schema.json`
- **Command**: `python -m jsonschema -i file.yaml aiai_schema.json`
- **Failure Action**: Escalate to Operator for schema validation failures

### **Python Code Quality**
- **Required**: All Python files must pass `pytest` and `mypy` validation
- **Command**: `pytest tests/ && mypy src/`
- **Failure Action**: Auto-fix syntax errors, escalate type errors to Operator

### **Documentation Validation**
- **Required**: All documentation must follow aiailint documentation standards
- **Command**: `markdownlint docs/`
- **Failure Action**: Auto-fix formatting, escalate content issues to Operator

## Component-Specific Testing Requirements

### **Unit Tests**
- **Required**: All new functionality must have corresponding unit tests
- **Location**: `tests/` directory
- **Command**: `pytest tests/`
- **Coverage**: Minimum 80% code coverage for new code

### **Integration Tests**
- **Required**: All validation pipelines must have integration tests
- **Location**: `tests/integration/`
- **Command**: `pytest tests/integration/`
- **Failure Action**: Escalate to Operator for integration test failures

### **Performance Tests**
- **Required**: All validation functions must have performance benchmarks
- **Location**: `tests/performance/`
- **Command**: `pytest tests/performance/ --benchmark-only`
- **Threshold**: No more than 10% performance regression

## Component-Specific File Naming Conventions

### **Python Files**
- **Pattern**: `snake_case.py`
- **Examples**: `aiailint.py`, `validation_result.py`, `error_formatter.py`

### **Test Files**
- **Pattern**: `test_<module_name>.py`
- **Examples**: `test_validator.py`, `test_error_formatter.py`

### **Documentation Files**
- **Pattern**: `UPPER_CASE.md`
- **Examples**: `README.md`, `USAGE.md`, `AIAILINT_SPECIFICATION.md`

## Component-Specific Tool Requirements

### **Required Tools**
- **Python**: 3.8+
- **pytest**: Latest version
- **mypy**: Latest version
- **yamllint**: Latest version
- **markdownlint**: Latest version

### **Optional Tools**
- **pytest-benchmark**: For performance testing
- **pytest-cov**: For coverage reporting
- **black**: For code formatting

## Component-Specific Commit Requirements

### **Commit Message Format**
```
aiailint: <type>(<scope>): <description>

[optional body]

[optional footer]
```

### **Types**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or changes
- `refactor`: Code refactoring
- `perf`: Performance improvements

### **Scopes**
- `validator`: Validation logic changes
- `analyzer`: Analysis logic changes
- `formatter`: Output formatting changes
- `docs`: Documentation changes
- `tests`: Test infrastructure changes

## Component-Specific Error Handling

### **Validation Errors**
- **Schema Errors**: Escalate to Operator immediately
- **Syntax Errors**: Auto-fix when possible, escalate complex issues
- **Type Errors**: Escalate to Operator for review

### **Test Failures**
- **Unit Test Failures**: Escalate to Operator
- **Integration Test Failures**: Escalate to Operator
- **Performance Test Failures**: Escalate to Operator

## Component-Specific Performance Requirements

### **Validation Performance**
- **Target**: < 1 second for typical YAML files
- **Threshold**: Alert Operator if validation takes > 5 seconds
- **Monitoring**: Track validation time for all files

### **Memory Usage**
- **Target**: < 100MB for typical files
- **Threshold**: Alert Operator if memory usage > 500MB
- **Monitoring**: Track memory usage during validation

## Component-Specific Security Requirements

### **Input Validation**
- **Required**: All YAML input must be validated against schema
- **Required**: All file paths must be sanitized
- **Required**: All external data must be validated

### **Output Sanitization**
- **Required**: All error messages must be sanitized
- **Required**: All debug output must be sanitized
- **Required**: No sensitive data in logs

## Component-Specific Documentation Requirements

### **Code Documentation**
- **Required**: All public functions must have docstrings
- **Required**: All classes must have docstrings
- **Required**: All complex logic must have inline comments

### **User Documentation**
- **Required**: All features must be documented in `USAGE.md`
- **Required**: All configuration options must be documented
- **Required**: All error codes must be documented

## Component-Specific Override Conflicts

### **When Conflicts Occur**
1. **Report** the conflict to the Operator
2. **List** the conflicting requirements
3. **Wait** for Operator decision on precedence
4. **Follow** Operator guidance on resolution

### **Common Conflicts**
- **Schema Validation**: Global YAML validation vs aiailint schema validation
- **Testing Requirements**: Global test requirements vs aiailint-specific test requirements
- **Documentation Standards**: Global documentation vs aiailint documentation standards

## Component-Specific Metrics

### **Quality Metrics**
- **Test Coverage**: Minimum 80% for new code
- **Documentation Coverage**: 100% for public APIs
- **Validation Success Rate**: > 95% for valid files

### **Performance Metrics**
- **Validation Time**: < 1 second for typical files
- **Memory Usage**: < 100MB for typical files
- **Error Rate**: < 5% false positives

## Integration with Global Workflow

### **Create Phase**
1. **Check** for aiailint-specific requirements
2. **Follow** aiailint naming conventions
3. **Include** aiailint-specific documentation
4. **Add** aiailint-specific tests

### **Validate Phase**
1. **Run** aiailint-specific validations
2. **Check** schema validation
3. **Verify** code quality standards
4. **Test** documentation standards

### **Test Phase**
1. **Run** aiailint-specific tests
2. **Verify** performance requirements
3. **Check** security requirements
4. **Validate** documentation coverage

### **Commit Phase**
1. **Use** aiailint commit message format
2. **Include** appropriate type and scope
3. **Reference** related issues
4. **Ensure** all validations pass

## Component-Specific Escalation Procedures

### **When to Escalate**
- **Schema validation failures**
- **Performance regression > 10%**
- **Memory usage > 500MB**
- **Test coverage < 80%**
- **Security validation failures**

### **Escalation Format**
```
ESCALATION: aiailint component
ISSUE: [brief description]
IMPACT: [high/medium/low]
RECOMMENDATION: [suggested action]
```

## Component-Specific Success Criteria

### **Validation Success**
- All YAML files pass schema validation
- All Python files pass type checking
- All documentation passes linting
- No security vulnerabilities detected

### **Testing Success**
- All unit tests pass
- All integration tests pass
- Performance benchmarks meet targets
- Code coverage meets minimum requirements

### **Documentation Success**
- All public APIs documented
- All configuration options documented
- All error codes documented
- Documentation passes linting

This component-specific override extends the global VIBE_CODING.md workflow with aiailint-specific requirements while maintaining consistency with the overall project standards.
