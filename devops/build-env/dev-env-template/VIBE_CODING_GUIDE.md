# dev-env-template Component-Specific VIBE_CODING Override

## Overview

This document provides component-specific overrides for the development environment template. These instructions extend the global VIBE_CODING.md workflow with template-specific requirements.

**Note**: This document extends, not replaces, the global VIBE_CODING.md workflow.

## Component-Specific Validation Requirements

### **Environment Configuration Validation**
- **Required**: All environment config files must validate against template schema
- **Command**: `python validate_env_config.py`
- **Failure Action**: Escalate to Operator for configuration validation failures

### **Template File Validation**
- **Required**: All template files must pass template validation
- **Command**: `python validate_templates.py`
- **Failure Action**: Escalate to Operator for template validation failures

### **Documentation Validation**
- **Required**: All documentation must follow template documentation standards
- **Command**: `markdownlint docs/`
- **Failure Action**: Auto-fix formatting, escalate content issues to Operator

## Component-Specific Testing Requirements

### **Environment Tests**
- **Required**: All environment configurations must have corresponding tests
- **Location**: `tests/environment/`
- **Command**: `pytest tests/environment/`
- **Coverage**: Minimum 85% environment test coverage

### **Template Tests**
- **Required**: All template changes must have corresponding tests
- **Location**: `tests/templates/`
- **Command**: `pytest tests/templates/`
- **Failure Action**: Escalate to Operator for template test failures

### **Integration Tests**
- **Required**: All environment setups must have integration tests
- **Location**: `tests/integration/`
- **Command**: `pytest tests/integration/`
- **Failure Action**: Escalate to Operator for integration test failures

## Component-Specific File Naming Conventions

### **Environment Files**
- **Pattern**: `env-config.yaml`
- **Examples**: `env-config.yaml`, `env-config-dev.yaml`

### **Template Files**
- **Pattern**: `*_template.*`
- **Examples**: `docker_template.yml`, `script_template.sh`

### **Documentation Files**
- **Pattern**: `UPPER_CASE.md`
- **Examples**: `README.md`, `QUICK_START.md`, `APP_DEPLOYMENT_GUIDE.md`

## Component-Specific Tool Requirements

### **Required Tools**
- **Python**: 3.8+
- **pytest**: Latest version
- **yamllint**: Latest version
- **markdownlint**: Latest version
- **docker**: Latest version

### **Optional Tools**
- **pytest-cov**: For coverage reporting
- **black**: For code formatting
- **shellcheck**: For shell script validation

## Component-Specific Commit Requirements

### **Commit Message Format**
```
template: <type>(<scope>): <description>

[optional body]

[optional footer]
```

### **Types**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or changes
- `refactor`: Code refactoring
- `env`: Environment configuration changes

### **Scopes**
- `env`: Environment configuration changes
- `template`: Template changes
- `docs`: Documentation changes
- `tests`: Test infrastructure changes
- `docker`: Docker configuration changes

## Component-Specific Error Handling

### **Environment Errors**
- **Configuration Errors**: Escalate to Operator immediately
- **Validation Errors**: Auto-fix when possible, escalate complex issues
- **Compatibility Errors**: Escalate to Operator for review

### **Template Errors**
- **Template Syntax Errors**: Escalate to Operator
- **Template Validation Errors**: Escalate to Operator
- **Template Rendering Errors**: Escalate to Operator

## Component-Specific Performance Requirements

### **Environment Setup Performance**
- **Target**: < 30 seconds for typical environment setup
- **Threshold**: Alert Operator if setup takes > 2 minutes
- **Monitoring**: Track setup time for all environments

### **Template Rendering Performance**
- **Target**: < 5 seconds for typical templates
- **Threshold**: Alert Operator if rendering takes > 30 seconds
- **Monitoring**: Track rendering time for all templates

## Component-Specific Security Requirements

### **Environment Security**
- **Required**: All environment configurations must be validated for security
- **Required**: All environment variables must be sanitized
- **Required**: No hardcoded secrets in templates

### **Template Security**
- **Required**: All template inputs must be sanitized
- **Required**: All template outputs must be validated
- **Required**: No code injection in templates

## Component-Specific Documentation Requirements

### **Environment Documentation**
- **Required**: All environment configurations must be documented
- **Required**: All environment variables must be documented
- **Required**: All setup procedures must be documented

### **Template Documentation**
- **Required**: All templates must have usage documentation
- **Required**: All template variables must be documented
- **Required**: All template examples must be provided

## Component-Specific Override Conflicts

### **When Conflicts Occur**
1. **Report** the conflict to the Operator
2. **List** the conflicting requirements
3. **Wait** for Operator decision on precedence
4. **Follow** Operator guidance on resolution

### **Common Conflicts**
- **Environment Validation**: Global YAML validation vs template environment validation
- **Documentation Standards**: Global documentation vs template documentation standards
- **Template Standards**: Global template requirements vs template-specific requirements

## Component-Specific Metrics

### **Quality Metrics**
- **Environment Coverage**: Minimum 85% for environment tests
- **Documentation Coverage**: 100% for all environments and templates
- **Template Success Rate**: > 95% for valid templates

### **Performance Metrics**
- **Environment Setup Time**: < 30 seconds for typical environments
- **Template Rendering Time**: < 5 seconds for typical templates
- **Error Rate**: < 5% false positives

## Integration with Global Workflow

### **Create Phase**
1. **Check** for template-specific requirements
2. **Follow** template naming conventions
3. **Include** template-specific documentation
4. **Add** template-specific tests

### **Validate Phase**
1. **Run** template-specific validations
2. **Check** environment configuration validation
3. **Verify** template validation
4. **Test** documentation standards

### **Test Phase**
1. **Run** template-specific tests
2. **Verify** environment test coverage
3. **Check** template test coverage
4. **Validate** documentation coverage

### **Commit Phase**
1. **Use** template commit message format
2. **Include** appropriate type and scope
3. **Reference** related issues
4. **Ensure** all validations pass

## Component-Specific Escalation Procedures

### **When to Escalate**
- **Environment configuration failures**
- **Template rendering failures**
- **Documentation validation failures**
- **Environment compatibility issues**
- **Template security issues**

### **Escalation Format**
```
ESCALATION: template component
ISSUE: [brief description]
IMPACT: [high/medium/low]
RECOMMENDATION: [suggested action]
```

## Component-Specific Success Criteria

### **Environment Success**
- All environment configurations pass validation
- All environment tests pass
- Environment documentation is complete
- No environment compatibility issues

### **Template Success**
- All template files pass validation
- All template tests pass
- Template documentation is complete
- No template security issues

### **Documentation Success**
- All environments documented
- All templates documented
- All setup procedures documented
- Documentation passes validation

This component-specific override extends the global VIBE_CODING.md workflow with template-specific requirements while maintaining consistency with the overall project standards.
