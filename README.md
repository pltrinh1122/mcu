# Memory Context Units (MCU)

## Overview

This repository contains the Memory Context Units (MCUs), a standalone component implementing Contextual Memory Intelligence (CMI) principles for optimized Operator-AI collaboration. Originally part of the AIAI project, this component has been extracted to provide focused MCU specifications and templates.

## Directory Structure

```
├── docs/                        # Base MCU specification and documentation
│   ├── MCU_SPECIFICATION.md     # Base specification for all MCU types
│   └── README.md                # MCU documentation overview
├── reference/                    # Reference MCU specifications
│   ├── MCU_REFERENCE_SPECIFICATION.md
│   └── README.md
├── instruction/                  # Instruction MCU specifications
│   ├── MCU_INSTRUCTION_SPECIFICATION.md
│   ├── README.md
│   └── instruction-agent/        # AI-Agent specific instructions
│       ├── MCU_INSTRUCTION-AGENT_SPECIFICATION.md
│       ├── README.md
│       └── vibecoding/          # VIBE_CODING specific instructions
│           ├── MCU_VIBE_CODING_SPECIFICATION.md
│           └── README.md
├── templates/                    # Standardized MCU templates
│   ├── MCU_REFERENCE_TEMPLATE.md
│   ├── MCU_INSTRUCTION_TEMPLATE.md
│   ├── MCU_INSTRUCTION-AGENT_TEMPLATE.md
│   └── README.md
└── tests/                       # Test files and review documents
    ├── MCU_REFERENCE_SPECIFICATION_FAQ.md
    ├── MCU_VIBE_CODING_FAQ.md
    ├── review_2_of_REFERENCE_SPECIFICATON.md
    ├── review_2_of_VIBE_CODING.md
    ├── review_of_REFERENCE_SPECIFICATON.md
    ├── review_of_VIBE_CODING.md
    └── README.md
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
2. **Reference MCUs**: Use `reference/MCU_REFERENCE_TEMPLATE.md`
3. **Instruction MCUs**: Use `instruction/MCU_INSTRUCTION_TEMPLATE.md`
4. **Instruction:Agent MCUs**: Use `instruction/instruction-agent/MCU_INSTRUCTION-AGENT_TEMPLATE.md`
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

## Quick Start

### **Installation**
```bash
git clone git@github.com:your-username/mcu.git
cd mcu
```

### **Usage**
1. **Review Specifications**: Start with `docs/MCU_SPECIFICATION.md`
2. **Choose Template**: Select appropriate template from `templates/` directory
3. **Create MCU**: Follow the template structure and requirements
4. **Validate**: Ensure compliance with specifications

## Related Documents

- **docs/MCU_SPECIFICATION.md**: Base specification for all MCU types
- **templates/**: Standardized templates for all MCU types
  - **MCU_REFERENCE_TEMPLATE.md**: Template for reference MCUs
  - **MCU_INSTRUCTION_TEMPLATE.md**: Template for instruction MCUs
  - **MCU_INSTRUCTION-AGENT_TEMPLATE.md**: Template for AI-Agent instructions
- **tests/**: FAQ and review documents

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*This repository implements CMI Context Memory Unit principles for optimized Operator-AI collaboration.*
