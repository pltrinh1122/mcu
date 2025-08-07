# AIAI Memory Context Units (MCU)

## Overview

This directory contains the Memory Context Units (MCUs) for the AIAI project, organized according to the CMI (Contextual Memory Intelligence) principles for optimized Operator-AI collaboration.

## Directory Structure

```
aiai/mcu/
├── reference/                    # Reference MCUs for information transfer
│   ├── REFERENCE_SPECIFICATION.md
│   ├── REFERENCE_TEMPLATE.md
│   └── REFERENCE_SPECIFICATION_FAQ.md
└── instruction/                  # Instruction MCUs for behavioral guidance
    ├── INSTRUCTION_TEMPLATE.md   # Base template for all instructions
    └── instruction-agent/        # AI-Agent specific instructions
        ├── INSTRUCTION-AGENT_SPECIFICATION.md
        ├── INSTRUCTION-AGENT_TEMPLATE.md
        └── VIBE_CODING_RESTRUCTURE_PLAN.md
```

## MCU Types

### **Reference MCUs**
- **Purpose**: Information transfer and knowledge sharing
- **Audience**: Both Operators and AI-Agents
- **Content**: Comprehensive documentation, examples, troubleshooting
- **Focus**: Knowledge preservation and transfer

### **Instruction MCUs**
- **Purpose**: Behavioral guidance and workflow instructions
- **Audience**: Primarily AI-Agents (with Operator oversight)
- **Content**: Actionable instructions, compliance requirements
- **Focus**: Execution and compliance

#### **Instruction:Agent MCUs**
- **Purpose**: AI-Agent specific behavioral guidance
- **Audience**: AI-Agent (primary), Operator (secondary)
- **Content**: Dual verification, role-separated governance
- **Focus**: AI-Agent execution with Operator oversight

## Usage

### **Creating New MCUs**
1. **Reference MCUs**: Use `reference/REFERENCE_TEMPLATE.md`
2. **Instruction MCUs**: Use `instruction/INSTRUCTION_TEMPLATE.md`
3. **Instruction:Agent MCUs**: Use `instruction/instruction-agent/INSTRUCTION-AGENT_TEMPLATE.md`

### **Quality Standards**
- **Compliance**: All MCUs must follow their respective specifications
- **Verification**: Dual verification process for Instruction:Agent MCUs
- **Cross-Reference**: TBD - Cross-reference mechanism to be implemented
- **Iteration**: Continuous improvement based on usage and feedback

## Governance

### **Role Separation**
- **AI-Agent**: Routine execution, implicit validation, performance monitoring
- **Operator**: Explicit verification, significant change approval, quality assurance

### **Decision Framework**
- **AI-Agent Autonomous**: Routine implementation, minor adjustments, performance optimization
- **Operator Required**: Major changes, policy updates, conflict resolution, strategic direction

## Related Documents

- **VIBE_CODING.md**: Main workflow instruction (to be restructured as Instruction:Agent MCU)
- **Component VIBE_CODING.md files**: Component-specific workflow overrides
- **Project Documentation**: Integration with overall AIAI project structure

---

*This structure implements CMI Context Memory Unit principles for optimized Operator-AI collaboration within the AIAI project ecosystem.*
