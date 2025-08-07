# Instruction Document Template

## Context Memory Unit: [UNIT_ID]
- **Created**: [ISO_TIMESTAMP]
- **Updated**: [ISO_TIMESTAMP]
- **Type**: instruction
- **Version**: [VERSION]
- **Project**: AIAI
- **Tool**: [TOOL_NAME]
- **Category**: [CATEGORY]
- **Tags**: [TAG1, TAG2, TAG3]

---

## Executive Summary

**TL;DR**: [One-sentence overview of what this instruction does and why it matters]

**Key Points**:
- [Point 1: Core instruction or behavior]
- [Point 2: Key requirement or constraint]
- [Point 3: Integration with AIAI project]
- [Point 4: When to apply this instruction]
- [Point 5: Expected outcome or result]

---

## Quick Reference

### **Essential Instructions**
```bash
# Basic instruction
[instruction] [parameters] [context]

# Common pattern
[instruction] --option value

# Quick start
[instruction] init
```

### **Core Requirements**
```yaml
# Basic structure
requirement: value
constraint:
  key: value

# Common patterns
pattern1: |
  multi-line
  instruction
pattern2: "{{.VARIABLE}}"
```

### **Immediate Actions**
1. **Understand**: [comprehension requirement]
2. **Apply**: [execution requirement]
3. **Verify**: [validation requirement]
4. **Report**: [feedback requirement]

---

## Detailed Reference

### **Instruction Scope**

#### **What This Instruction Covers**
- [Scope 1]
- [Scope 2]
- [Scope 3]

#### **What This Instruction Does NOT Cover**
- [Exclusion 1]
- [Exclusion 2]
- [Exclusion 3]

### **Core Concepts**

#### **Concept 1: [Name]**
**What it is**: [Brief description]
**Why it matters**: [Relevance to AIAI project]
**How to apply**: [Technical explanation]

#### **Concept 2: [Name]**
**What it is**: [Brief description]
**Why it matters**: [Relevance to AIAI project]
**How to apply**: [Technical explanation]

### **Advanced Requirements**

#### **Requirement 1: [Name]**
```yaml
# Example configuration
requirement1:
  enabled: true
  options:
    - option1
    - option2
```

#### **Requirement 2: [Name]**
```bash
# Example instruction
[instruction] --requirement2-option value
```

---

## AIAI Integration

### **Project-Specific Application**

#### **AIAI Workflow Integration**
```yaml
# AIAI-specific instruction
aiai:
  workflow: instruction
  environment: development
  components:
    - component1
    - component2
```

#### **Common AIAI Use Cases**

**Use Case 1: [Name]**
```bash
# AIAI-specific instruction
[instruction] --aiai-mode --component component1
```

**Use Case 2: [Name]**
```yaml
# AIAI-specific configuration
aiai_workflow:
  step1: [instruction1]
  step2: [instruction2]
  step3: [instruction3]
```

### **Integration Patterns**

#### **Pattern 1: [Name]**
**When to apply**: [Scenario description]
**Implementation**: [Code example]
**Benefits**: [Why this pattern helps AIAI]

#### **Pattern 2: [Name]**
**When to apply**: [Scenario description]
**Implementation**: [Code example]
**Benefits**: [Why this pattern helps AIAI]

---

## Workflow Examples

### **Basic Examples**

#### **Example 1: [Name]**
```yaml
# Working example
version: '3'
instructions:
  basic:
    desc: "Basic instruction example"
    steps:
      - step1: "Execute basic instruction"
      - step2: "Verify compliance"
```

**What it does**: [Explanation]
**When to apply**: [Scenario]
**AIAI context**: [How it fits in our project]

#### **Example 2: [Name]**
```bash
# Working example
[instruction] --option value --flag
```

**What it does**: [Explanation]
**When to apply**: [Scenario]
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
**When to apply**: [Complex scenario]
**AIAI context**: [Advanced integration]

### **Real-World AIAI Examples**

#### **AIAI Workflow Application**
```yaml
# Actual AIAI usage
aiai_workflow:
  setup:
    - instruction: base:setup
    - instruction: python:python-setup
  test:
    - instruction: python:test
    - instruction: python:quality
  build:
    - instruction: python:python-build
    - instruction: docker:docker-build
```

**Context**: [When this is used in AIAI]
**Benefits**: [Why this workflow works well]

---

## Compliance Issues

### **Common Problems**

#### **Issue 1: [Compliance Problem]**
**Symptoms**: [How to recognize the issue]
**Causes**: [Why it happens]
**Solutions**:
```bash
# Solution 1
[instruction] --fix-option

# Solution 2
[alternative_approach]
```

**Prevention**: [How to avoid this issue]

#### **Issue 2: [Compliance Problem]**
**Symptoms**: [How to recognize the issue]
**Causes**: [Why it happens]
**Solutions**:
```bash
# Solution 1
[instruction] --fix-option

# Solution 2
[alternative_approach]
```

**Prevention**: [How to avoid this issue]

### **Verification Techniques**

#### **Verification Method 1: [Name]**
```bash
# Verification command
[instruction] --verify --verbose
```

**What it shows**: [Output explanation]
**How to interpret**: [Analysis guidance]

#### **Verification Method 2: [Name]**
```bash
# Verification command
[instruction] --dry-run
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
- **✅ Understanding**: Tested on [platform] with [version]
- **✅ Application**: All examples verified working
- **✅ AIAI Integration**: Tested in our environment
- **✅ Advanced Requirements**: [Status of advanced testing]

### **Last Verified**
- **Date**: [ISO_DATE]
- **Tool Version**: [VERSION]
- **Platform**: [PLATFORM]
- **Verification Script**: [SCRIPT_NAME]

---

## Cross-Reference Integration

**TBD - Cross-reference mechanism to be implemented as we learn optimal integration patterns**

### **Related Instructions**
- **[Related Instruction 1]**: [LINK] - [Relationship description]
- **[Related Instruction 2]**: [LINK] - [Relationship description]
- **[Related Instruction 3]**: [LINK] - [Relationship description]

### **Related References**
- **[Reference 1]**: [LINK] - [How it relates]
- **[Reference 2]**: [LINK] - [How it relates]

### **Related Integrations**
- **[Integration 1]**: [LINK] - [Integration context]
- **[Integration 2]**: [LINK] - [Integration context]

---

## Template Usage Instructions

### **How to Use This Template**

1. **Copy the template** to your instruction document location
2. **Replace placeholders** with actual content:
   - `[UNIT_ID]` → Unique identifier (e.g., `inst-taskfile-2024-08-07-001`)
   - `[TOOL_NAME]` → Actual tool name
   - `[CATEGORY]` → Tool category
   - `[TAG1, TAG2, TAG3]` → Relevant tags
   - `[ISO_TIMESTAMP]` → Current timestamp
   - `[VERSION]` → Document version

3. **Fill in each section** with actual content:
   - **Executive Summary**: 2-3 sentence overview
   - **Quick Reference**: Essential instructions and requirements
   - **Detailed Reference**: Comprehensive coverage
   - **AIAI Integration**: Project-specific examples
   - **Workflow Examples**: Working examples
   - **Compliance Issues**: Common problems and solutions
   - **Sources & Verification**: Attribution and verification status
   - **Cross-Reference Integration**: Links to related documents

4. **Verify accuracy** using the verification strategy
5. **Test all examples** in the AIAI environment
6. **Update metadata** when making changes

### **Template Customization**

#### **For Different Instruction Types**
- **Behavioral Instructions**: Emphasize actions and outcomes
- **Process Instructions**: Focus on workflow and steps
- **Quality Instructions**: Prioritize standards and validation
- **Integration Instructions**: Highlight connections and dependencies

#### **For Different Audiences**
- **Operator-Focused**: More step-by-step instructions
- **AI-Focused**: More structured data and relationships
- **Both**: Balanced approach with clear sections

### **Quality Checklist**

- [ ] All placeholders replaced with actual content
- [ ] Examples tested and working
- [ ] AIAI integration examples included
- [ ] Compliance issues section complete
- [ ] Sources properly attributed
- [ ] Cross-reference integration linked
- [ ] Verification status current
- [ ] Metadata fields complete
- [ ] Progressive disclosure implemented
- [ ] Digestible chunks created

---

*This template implements the Instruction Specification and CMI Context Memory Unit principles for optimized Operator-AI collaboration.*
