# framework-dev Component-Specific VIBE_CODING Override

## Overview

This document provides component-specific overrides for the framework development environment. These instructions extend the global VIBE_CODING.md workflow with framework-specific requirements.

**Note**: This document extends, not replaces, the global VIBE_CODING.md workflow.

## Component-Specific Validation Requirements

### **Schema Validation**
- **Required**: All schema files must validate against JSON Schema standard
- **Command**: `python -m jsonschema -i schema.json meta-schema.json`
- **Failure Action**: Escalate to Operator for schema validation failures

### **Documentation Validation**
- **Required**: All documentation must follow framework documentation standards
- **Command**: `markdownlint docs/`
- **Failure Action**: Auto-fix formatting, escalate content issues to Operator

### **Template Validation**
- **Required**: All template files must pass template validation
- **Command**: `python validate_templates.py`
- **Failure Action**: Escalate to Operator for template validation failures

## Component-Specific Testing Requirements

### **Schema Tests**
- **Required**: All schema changes must have corresponding tests
- **Location**: `tests/schema/`
- **Command**: `pytest tests/schema/`
- **Coverage**: Minimum 90% schema test coverage

### **Template Tests**
- **Required**: All template changes must have corresponding tests
- **Location**: `tests/templates/`
- **Command**: `pytest tests/templates/`
- **Failure Action**: Escalate to Operator for template test failures

### **Documentation Tests**
- **Required**: All documentation changes must have link validation
- **Location**: `tests/docs/`
- **Command**: `pytest tests/docs/`
- **Failure Action**: Escalate to Operator for documentation test failures

## Component-Specific File Naming Conventions

### **Schema Files**
- **Pattern**: `*_schema.json`
- **Examples**: `aiai_schema.json`, `template_schema.json`

### **Template Files**
- **Pattern**: `*_template.md`
- **Examples**: `operator_guide_template.md`, `package_template.md`

### **Documentation Files**
- **Pattern**: `UPPER_CASE.md`
- **Examples**: `README.md`, `DESIGN_README.md`, `PACKAGE_DESIGN_GUIDELINES.md`

## Component-Specific Tool Requirements

### **Required Tools**
- **Python**: 3.8+
- **pytest**: Latest version
- **jsonschema**: Latest version
- **markdownlint**: Latest version

### **Optional Tools**
- **pytest-cov**: For coverage reporting
- **black**: For code formatting
- **yamllint**: For YAML validation

## Component-Specific Commit Requirements

### **Commit Message Format**
```
framework: <type>(<scope>): <description>

[optional body]

[optional footer]
```

### **Types**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or changes
- `refactor`: Code refactoring
- `schema`: Schema changes

### **Scopes**
- `schema`: Schema definition changes
- `template`: Template changes
- `docs`: Documentation changes
- `tests`: Test infrastructure changes
- `design`: Design document changes

## Component-Specific Error Handling

### **Schema Errors**
- **Schema Validation Errors**: Escalate to Operator immediately
- **Schema Syntax Errors**: Auto-fix when possible, escalate complex issues
- **Schema Compatibility Errors**: Escalate to Operator for review

### **Template Errors**
- **Template Syntax Errors**: Escalate to Operator
- **Template Validation Errors**: Escalate to Operator
- **Template Rendering Errors**: Escalate to Operator

## Component-Specific Performance Requirements

### **Schema Validation Performance**
- **Target**: < 500ms for typical schema files
- **Threshold**: Alert Operator if validation takes > 2 seconds
- **Monitoring**: Track validation time for all schema files

### **Template Rendering Performance**
- **Target**: < 1 second for typical templates
- **Threshold**: Alert Operator if rendering takes > 5 seconds
- **Monitoring**: Track rendering time for all templates

## Component-Specific Security Requirements

### **Schema Security**
- **Required**: All schema files must be validated for security
- **Required**: All schema references must be sanitized
- **Required**: No external schema references without validation

### **Template Security**
- **Required**: All template inputs must be sanitized
- **Required**: All template outputs must be validated
- **Required**: No code injection in templates

## Component-Specific Documentation Requirements

### **Schema Documentation**
- **Required**: All schema fields must be documented
- **Required**: All schema constraints must be documented
- **Required**: All schema examples must be provided

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
- **Schema Validation**: Global JSON validation vs framework schema validation
- **Documentation Standards**: Global documentation vs framework documentation standards
- **Template Standards**: Global template requirements vs framework template requirements

## Component-Specific Metrics

### **Quality Metrics**
- **Schema Coverage**: Minimum 90% for schema tests
- **Documentation Coverage**: 100% for all schemas and templates
- **Template Success Rate**: > 95% for valid templates

### **Performance Metrics**
- **Schema Validation Time**: < 500ms for typical schemas
- **Template Rendering Time**: < 1 second for typical templates
- **Error Rate**: < 5% false positives

## Integration with Global Workflow

### **Create Phase**
1. **Check** for framework-specific requirements
2. **Follow** framework naming conventions
3. **Include** framework-specific documentation
4. **Add** framework-specific tests

### **Validate Phase**
1. **Run** framework-specific validations
2. **Check** schema validation
3. **Verify** template validation
4. **Test** documentation standards

### **Test Phase**
1. **Run** framework-specific tests
2. **Verify** schema test coverage
3. **Check** template test coverage
4. **Validate** documentation coverage

### **Commit Phase**
1. **Use** framework commit message format
2. **Include** appropriate type and scope
3. **Reference** related issues
4. **Ensure** all validations pass

## Component-Specific Escalation Procedures

### **When to Escalate**
- **Schema validation failures**
- **Template rendering failures**
- **Documentation validation failures**
- **Schema compatibility issues**
- **Template security issues**

### **Escalation Format**
```
ESCALATION: framework component
ISSUE: [brief description]
IMPACT: [high/medium/low]
RECOMMENDATION: [suggested action]
```

## Component-Specific Success Criteria

### **Schema Success**
- All schema files pass validation
- All schema tests pass
- Schema documentation is complete
- No schema compatibility issues

### **Template Success**
- All template files pass validation
- All template tests pass
- Template documentation is complete
- No template security issues

### **Documentation Success**
- All schemas documented
- All templates documented
- All design documents complete
- Documentation passes validation

This component-specific override extends the global VIBE_CODING.md workflow with framework-specific requirements while maintaining consistency with the overall project standards.
