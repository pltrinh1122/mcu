# AIAI Memory Context Units (MCU)

## Overview

This directory contains the Memory Context Units (MCUs) for the AIAI project, organized according to the CMI (Contextual Memory Intelligence) principles for optimized Operator-AI collaboration.

## Directory Structure

```
mcu/
├── docs/                        # Base MCU specification and documentation
│   ├── MCU_SPECIFICATION.md     # Base specification for all MCU types
│   └── README.md                # MCU documentation overview
├── reference/                    # Reference MCUs for information transfer
│   ├── REFERENCE_SPECIFICATION.md
│   └── REFERENCE_TEMPLATE.md
├── instruction/                  # Instruction MCUs for behavioral guidance
│   ├── INSTRUCTION_TEMPLATE.md   # Base template for all instructions
│   └── instruction-agent/        # AI-Agent specific instructions
│       ├── INSTRUCTION-AGENT_SPECIFICATION.md
│       ├── INSTRUCTION-AGENT_TEMPLATE.md
│       └── vibecoding/          # VIBE_CODING specific instructions
│           └── VIBE_CODING_RESTRUCTURE_PLAN.md
└── tests/                       # Test files and review documents
    ├── REFERENCE_SPECIFICATION_FAQ.md
    ├── review_of_REFERENCE_SPECIFICATON.md
    ├── review_2_of_REFERENCE_SPECIFICATON.md
    ├── review_of_VIBE_CODING.md
    └── review_2_of_VIBE_CODING.md
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
1. **Base Specification**: Inherit from `docs/MCU_SPECIFICATION.md`
2. **Reference MCUs**: Use `reference/REFERENCE_TEMPLATE.md`
3. **Instruction MCUs**: Use `instruction/INSTRUCTION_TEMPLATE.md`
4. **Instruction:Agent MCUs**: Use `instruction/instruction-agent/INSTRUCTION-AGENT_TEMPLATE.md`
5. **VIBE_CODING MCUs**: Use `instruction/instruction-agent/vibecoding/` for VIBE_CODING specific instructions

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

- **docs/MCU_SPECIFICATION.md**: Base specification for all MCU types
- **VIBE_CODING.md**: Main workflow instruction (to be restructured as Instruction:Agent MCU)
- **Component VIBE_CODING.md files**: Component-specific workflow overrides
- **Project Documentation**: Integration with overall AIAI project structure
- **Test Files**: FAQ and review documents in `tests/` directory

---

*This structure implements CMI Context Memory Unit principles for optimized Operator-AI collaboration within the AIAI project ecosystem.*
