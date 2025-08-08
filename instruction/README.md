# Instruction Memory Context Units

## Overview

This directory contains Instruction Memory Context Units (MCUs) designed for behavioral guidance and workflow instructions. These MCUs provide structured guidance for human-AI collaboration and autonomous AI execution.

## Structure

- **INSTRUCTION_SPECIFICATION.md**: Base specification for all instruction MCUs (Operator-AI collaboration)
- **MCU_INSTRUCTION_TEMPLATE.md**: Base template for all instruction MCUs
- **instruction-agent/**: AI-Agent specific instruction MCUs (autonomous AI execution)

## Purpose

Instruction MCUs serve as actionable guidance that:
- **Define Behavior**: Specify how AI-Agents should act and respond
- **Establish Workflows**: Create structured processes for execution
- **Ensure Compliance**: Set standards and verification requirements
- **Enable Governance**: Provide role separation and decision frameworks

## Directory Structure

```
instruction/
├── MCU_INSTRUCTION_TEMPLATE.md           # Base template for all instructions
└── instruction-agent/                # AI-Agent specific instructions
    ├── INSTRUCTION-AGENT_SPECIFICATION.md
    ├── MCU_INSTRUCTION-AGENT_TEMPLATE.md
    └── VIBE_CODING_RESTRUCTURE_PLAN.md
```

## MCU Types

### **Base Instruction MCUs**
- **Purpose**: General behavioral guidance and workflow instructions
- **Audience**: Both Operators and AI-Agents
- **Content**: Workflow instructions, process guidance, quality standards
- **Focus**: Actionable guidance for execution

### **Instruction:Agent MCUs**
- **Purpose**: AI-Agent specific behavioral guidance
- **Audience**: AI-Agent (primary), Operator (secondary)
- **Content**: Dual verification, role-separated governance, compliance metrics
- **Focus**: AI-Agent execution with Operator oversight

## Documents

### **MCU_INSTRUCTION_TEMPLATE.md**
- **Purpose**: Base template for creating all instruction MCUs
- **Content**: Standard structure with instruction-specific sections
- **Audience**: Anyone creating instruction documentation
- **Inheritance**: Inherited by specialized instruction templates

### **instruction-agent/INSTRUCTION-AGENT_SPECIFICATION.md**
- **Purpose**: Defines standards for Instruction:Agent MCUs
- **Content**: Quality standards, governance model, verification process
- **Audience**: Document creators and maintainers
- **Focus**: AI-Agent specific requirements

### **instruction-agent/MCU_INSTRUCTION-AGENT_TEMPLATE.md**
- **Purpose**: Template for creating Instruction:Agent MCUs
- **Content**: AI-Agent specific structure and requirements
- **Audience**: Anyone creating AI-Agent instruction documentation
- **Inheritance**: Inherits from base MCU_INSTRUCTION_TEMPLATE.md

### **instruction-agent/VIBE_CODING_RESTRUCTURE_PLAN.md**
- **Purpose**: Plan for restructuring VIBE_CODING.md as Instruction:Agent MCU
- **Content**: Implementation plan, governance integration, quality enhancement
- **Audience**: Project maintainers and implementers

## Usage

### **Creating Instruction MCUs**
1. **Base Instructions**: Use `MCU_INSTRUCTION_TEMPLATE.md`
2. **AI-Agent Instructions**: Use `instruction-agent/MCU_INSTRUCTION-AGENT_TEMPLATE.md`
3. **Follow Specifications**: Implement requirements from respective specifications
4. **Add Content**: Fill in all sections with actionable guidance
5. **Verify Compliance**: Ensure dual verification and governance requirements

### **Quality Standards**
- **Compliance**: All instructions must follow their respective specifications
- **Verification**: Dual verification process for Instruction:Agent MCUs
- **Governance**: Clear role separation and decision frameworks
- **Effectiveness**: Measurable compliance and performance metrics

## Governance Model

### **Role Separation**
- **AI-Agent**: Routine execution, implicit validation, performance monitoring
- **Operator**: Explicit verification, significant change approval, quality assurance

### **Decision Framework**
- **AI-Agent Autonomous**: Routine implementation, minor adjustments, performance optimization
- **Operator Required**: Major changes, policy updates, conflict resolution, strategic direction

### **Verification Process**
- **Implicit Verification**: AI-Agent automatic validation during execution
- **Explicit Verification**: Operator prompt for understanding and compliance validation

## Structure

### **Standard Sections**
1. **Executive Summary**: 2-3 sentence overview
2. **Quick Reference**: Essential instructions and requirements
3. **Detailed Reference**: Comprehensive coverage
4. **AIAI Integration**: Project-specific examples
5. **Workflow Examples**: Working examples and patterns
6. **Compliance Issues**: Common problems and solutions
7. **Sources & Verification**: Attribution and verification status
8. **Cross-Reference Integration**: Links to related documents

### **Instruction:Agent Specific Sections**
- **AI-Agent Verification Process**: Dual verification implementation
- **AI-Agent Compliance Standards**: Measurable compliance metrics
- **Governance Model**: Role separation and decision framework

## Integration

### **Cross-Reference**
- **Related Instructions**: Link to other instruction MCUs
- **Related References**: Link to reference MCUs
- **Related Integrations**: Link to integration MCUs

### **Verification**
- **Dual Verification**: Both implicit and explicit validation
- **Compliance Metrics**: Measurable standards and performance tracking
- **Governance Oversight**: Role separation and decision frameworks
- **Continuous Improvement**: Iterative refinement based on feedback

---

*Instruction MCUs implement CMI Context Memory Unit principles for optimized behavioral guidance and workflow execution.*
