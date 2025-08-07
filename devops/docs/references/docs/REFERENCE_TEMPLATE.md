# Reference Document Template

## Context Memory Unit: [UNIT_ID]
- **Created**: [ISO_TIMESTAMP]
- **Updated**: [ISO_TIMESTAMP]
- **Type**: reference
- **Version**: [VERSION]
- **Project**: AIAI
- **Tool**: [TOOL_NAME]
- **Category**: [CATEGORY]
- **Tags**: [TAG1, TAG2, TAG3]

---

## Executive Summary

**TL;DR**: [One-sentence overview of what this tool does and why it matters]

**Key Points**:
- [Point 1: Core functionality or benefit]
- [Point 2: Key advantage or feature]
- [Point 3: Integration with AIAI project]
- [Point 4: When to use this tool]
- [Point 5: Main alternative or comparison]

---

## Quick Reference

### **Essential Commands**
```bash
# Basic usage
[command] [options] [arguments]

# Common pattern
[command] --flag value

# Quick start
[command] init
```

### **Core Syntax**
```yaml
# Basic structure
key: value
nested:
  key: value

# Common patterns
pattern1: |
  multi-line
  content
pattern2: "{{.VARIABLE}}"
```

### **Immediate Actions**
1. **Install**: `[installation_command]`
2. **Verify**: `[verification_command]`
3. **Basic Usage**: `[basic_command]`
4. **Get Help**: `[help_command]`

---

## Detailed Reference

### **Installation & Setup**

#### **Prerequisites**
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

#### **Installation Methods**
```bash
# Method 1: Package Manager
[package_manager_command]

# Method 2: Direct Download
[download_command]

# Method 3: Source Build
[build_command]
```

#### **Configuration**
```yaml
# Basic configuration
config:
  setting1: value1
  setting2: value2
```

### **Core Concepts**

#### **Concept 1: [Name]**
**What it is**: [Brief description]
**Why it matters**: [Relevance to AIAI project]
**How it works**: [Technical explanation]

#### **Concept 2: [Name]**
**What it is**: [Brief description]
**Why it matters**: [Relevance to AIAI project]
**How it works**: [Technical explanation]

### **Advanced Features**

#### **Feature 1: [Name]**
```yaml
# Example configuration
feature1:
  enabled: true
  options:
    - option1
    - option2
```

#### **Feature 2: [Name]**
```bash
# Example usage
[command] --feature2-option value
```

---

## AIAI Integration

### **Project-Specific Configuration**

#### **AIAI Build Environment Integration**
```yaml
# AIAI-specific configuration
aiai:
  build_tool: task
  environment: development
  components:
    - aiailint
    - framework
```

#### **Common AIAI Use Cases**

**Use Case 1: [Name]**
```bash
# AIAI-specific command
[command] --aiai-mode --component aiailint
```

**Use Case 2: [Name]**
```yaml
# AIAI-specific configuration
aiai_workflow:
  step1: [command1]
  step2: [command2]
  step3: [command3]
```

### **Integration Patterns**

#### **Pattern 1: [Name]**
**When to use**: [Scenario description]
**Implementation**: [Code example]
**Benefits**: [Why this pattern helps AIAI]

#### **Pattern 2: [Name]**
**When to use**: [Scenario description]
**Implementation**: [Code example]
**Benefits**: [Why this pattern helps AIAI]

---

## Examples & Patterns

### **Basic Examples**

#### **Example 1: [Name]**
```yaml
# Working example
version: '3'
tasks:
  hello:
    desc: "Say hello"
    cmds:
      - echo "Hello, AIAI!"
```

**What it does**: [Explanation]
**When to use**: [Scenario]
**AIAI context**: [How it fits in our project]

#### **Example 2: [Name]**
```bash
# Working example
[command] --option value --flag
```

**What it does**: [Explanation]
**When to use**: [Scenario]
**AIAI context**: [How it fits in our project]

### **Advanced Examples**

#### **Example 3: [Complex Pattern]**
```yaml
# Complex working example
complex_pattern:
  setup:
    - step1
    - step2
  execution:
    - step3
    - step4
  cleanup:
    - step5
```

**What it does**: [Detailed explanation]
**When to use**: [Complex scenario]
**AIAI context**: [Advanced integration]

### **Real-World AIAI Examples**

#### **AIAI Build Workflow**
```yaml
# Actual AIAI usage
aiai_build:
  setup:
    - task: base:setup
    - task: python:python-setup
  test:
    - task: python:test
    - task: python:quality
  build:
    - task: python:python-build
    - task: docker:docker-build
```

**Context**: [When this is used in AIAI]
**Benefits**: [Why this workflow works well]

---

## Troubleshooting

### **Common Issues**

#### **Issue 1: [Error Message]**
**Symptoms**: [How to recognize the issue]
**Causes**: [Why it happens]
**Solutions**:
```bash
# Solution 1
[command] --fix-option

# Solution 2
[alternative_approach]
```

**Prevention**: [How to avoid this issue]

#### **Issue 2: [Error Message]**
**Symptoms**: [How to recognize the issue]
**Causes**: [Why it happens]
**Solutions**:
```bash
# Solution 1
[command] --fix-option

# Solution 2
[alternative_approach]
```

**Prevention**: [How to avoid this issue]

### **Debugging Techniques**

#### **Debug Method 1: [Name]**
```bash
# Debug command
[command] --debug --verbose
```

**What it shows**: [Output explanation]
**How to interpret**: [Analysis guidance]

#### **Debug Method 2: [Name]**
```bash
# Debug command
[command] --dry-run
```

**What it shows**: [Output explanation]
**How to interpret**: [Analysis guidance]

### **AIAI-Specific Issues**

#### **AIAI Issue 1: [Name]**
**Context**: [When this happens in AIAI]
**Symptoms**: [How to recognize]
**Solution**: [AIAI-specific fix]

#### **AIAI Issue 2: [Name]**
**Context**: [When this happens in AIAI]
**Symptoms**: [How to recognize]
**Solution**: [AIAI-specific fix]

---

## Sources & Verification

### **Information Sources**
- **Official Documentation**: [URL] - [Date accessed]
- **Schema Definition**: [URL] - [Date accessed]
- **Community Examples**: [URL] - [Date accessed]
- **AIAI Testing**: [Date] - [Test results]

### **Verification Status**
- **✅ Installation**: Tested on [platform] with [version]
- **✅ Basic Commands**: All examples verified working
- **✅ AIAI Integration**: Tested in our environment
- **✅ Advanced Features**: [Status of advanced testing]

### **Last Verified**
- **Date**: [ISO_DATE]
- **Tool Version**: [VERSION]
- **Platform**: [PLATFORM]
- **Verification Script**: [SCRIPT_NAME]

---

## Related Context Units

### **Related References**
- **[Related Tool 1]**: [LINK] - [Relationship description]
- **[Related Tool 2]**: [LINK] - [Relationship description]
- **[Related Tool 3]**: [LINK] - [Relationship description]

### **Related Instructions**
- **[Instruction 1]**: [LINK] - [How it relates]
- **[Instruction 2]**: [LINK] - [How it relates]

### **Related Integrations**
- **[Integration 1]**: [LINK] - [Integration context]
- **[Integration 2]**: [LINK] - [Integration context]

---

## Template Usage Instructions

### **How to Use This Template**

1. **Copy the template** to your reference document location
2. **Replace placeholders** with actual content:
   - `[UNIT_ID]` → Unique identifier (e.g., `ref-taskfile-2024-08-07-001`)
   - `[TOOL_NAME]` → Actual tool name
   - `[CATEGORY]` → Tool category
   - `[TAG1, TAG2, TAG3]` → Relevant tags
   - `[ISO_TIMESTAMP]` → Current timestamp
   - `[VERSION]` → Document version

3. **Fill in each section** with actual content:
   - **Executive Summary**: 2-3 sentence overview
   - **Quick Reference**: Essential commands and syntax
   - **Detailed Reference**: Comprehensive coverage
   - **AIAI Integration**: Project-specific examples
   - **Examples & Patterns**: Working examples
   - **Troubleshooting**: Common issues and solutions
   - **Sources & Verification**: Attribution and verification status
   - **Related Context Units**: Links to related documents

4. **Verify accuracy** using the verification strategy
5. **Test all examples** in the AIAI environment
6. **Update metadata** when making changes

### **Template Customization**

#### **For Different Tool Types**
- **Build Tools**: Emphasize configuration and automation
- **Development Tools**: Focus on workflow integration
- **Infrastructure Tools**: Highlight deployment and scaling
- **Testing Tools**: Prioritize quality and validation

#### **For Different Audiences**
- **Operator-Focused**: More step-by-step instructions
- **AI-Focused**: More structured data and relationships
- **Both**: Balanced approach with clear sections

### **Quality Checklist**

- [ ] All placeholders replaced with actual content
- [ ] Examples tested and working
- [ ] AIAI integration examples included
- [ ] Troubleshooting section complete
- [ ] Sources properly attributed
- [ ] Related context units linked
- [ ] Verification status current
- [ ] Metadata fields complete
- [ ] Progressive disclosure implemented
- [ ] Digestible chunks created

---

*This template implements the Reference Specification and CMI Context Memory Unit principles for optimized Operator-AI collaboration.*
