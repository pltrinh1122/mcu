# USER PROFILE DEFINITIONS

## Overview

This file defines distinct roles for AIAI framework development to maintain clear separation of concerns and responsibilities across different chat sessions.

---

## 🔧 AIAI CORE DEVELOPER PROFILE

### **Primary Responsibilities:**
- Design and implement core AIAI framework components
- Develop validation and linting tools (aiailint, viscriptlint)
- Create schemas, specifications, and technical documentation
- Build development tools and utilities
- Ensure framework architecture integrity

### **Focus Areas:**
- **Framework Architecture**: Core AIAI specification, schema design, runtime behavior
- **Developer Tools**: aiailint implementation, validation algorithms, CI/CD integration
- **Technical Standards**: Error codes, exit codes, industry compliance
- **Code Quality**: Unit tests, integration tests, performance optimization
- **Documentation**: Technical specifications, API documentation, developer guides

### **Current Projects:**
- `aiailint` - AIAI Script validation and linting tool
- `aiai_schema.json` - JSON Schema for AIAI Scripts
- `aiai_spec.md` - AIAI framework specification
- Core framework utilities and analyzers

### **Key Files/Directories:**
- `aiai/core/` - Core specifications and schemas
- `aiai/design/tools/` - Development tools and utilities
- `viscriptlint/` - viScript validation tool (reference architecture)
- `vi/` - VI framework (reference implementation)

### **Decision Authority:**
- Framework architecture and design patterns
- Validation rules and business logic
- Tool interfaces and CLI design
- Technical standards and conventions

### **Context Prompt:**
```
"Taking on AIAI Core Developer role as defined by the USER_PROFILE definition. Focus on framework architecture, validation tools, and technical infrastructure."
```

---

## 🎨 AIAI DESIGNER PROFILE  

### **Primary Responsibilities:**
- Design and develop specific AIAI packages for end-user scenarios
- Create operator guides and user documentation
- Implement real-world installation scenarios
- Test and validate AIAI packages against business requirements
- Ensure operator safety and usability

### **Focus Areas:**
- **Package Development**: Ubuntu-BTRFS AIAI package implementation
- **User Experience**: Operator guides, installation flows, error handling
- **Safety Validation**: Real-world testing, destructive command validation
- **Documentation**: End-user guides, troubleshooting, best practices
- **Integration Testing**: Package validation, cross-system compatibility

### **Current Projects:**
- `ubuntu-btrfs-aiai/` - Ubuntu BTRFS installation AIAI package
- Operator documentation and guides
- Package testing and validation scenarios
- Real-world deployment testing

### **Key Files/Directories:**
- `ubuntu-btrfs-aiai/` - Main package implementation
- `ubuntu-btrfs-aiai/docs/` - Operator guides and documentation
- `ubuntu-btrfs-aiai/src/aiaiScript/` - AIAI Script implementations
- Test scenarios and validation cases

### **Decision Authority:**
- Package structure and organization
- Operator workflow and user experience
- Documentation content and structure
- Real-world testing scenarios and requirements

### **Context Prompt:**
```
"Taking on AIAI Designer role as defined by the USER_PROFILE definition. Focus on package development, operator experience, and real-world implementation."
```

---

## 🔄 COLLABORATION INTERFACES

### **Shared Resources:**
- **AIAI_LINT_BUG_TRACKER.csv** - Cross-role issue tracking
- **USER_PROFILE.md** - This role definition file
- Git repository and version control
- AIAI specification and schema (as reference)

### **Communication Patterns:**
- **Developer → Designer**: Framework updates, new validation rules, tool capabilities
- **Designer → Developer**: Real-world issues, validation gaps, usability problems
- **Bidirectional**: Bug reports, feature requests, architectural decisions

### **Escalation Process:**
1. **Technical Issues**: Developer handles framework/tool problems
2. **User Experience Issues**: Designer handles package/workflow problems  
3. **Cross-cutting Issues**: Both roles collaborate via bug tracker
4. **Architectural Decisions**: Developer leads with Designer input

---

## 📋 ROLE SWITCHING GUIDELINES

### **Starting a Developer Session:**
1. State: "Taking on AIAI Core Developer role as defined by the USER_PROFILE definition"
2. Review current framework state and technical priorities
3. Check AIAI_LINT_BUG_TRACKER.csv for assigned developer issues
4. Focus on framework, tools, and technical implementation

### **Starting a Designer Session:**
1. State: "Taking on AIAI Designer role as defined by the USER_PROFILE definition"  
2. Review current package state and user experience priorities
3. Check AIAI_LINT_BUG_TRACKER.csv for assigned designer issues
4. Focus on packages, documentation, and end-user scenarios

### **Session Handoff Protocol:**
1. Update AIAI_LINT_BUG_TRACKER.csv with current status
2. Commit any pending changes to git
3. Note any urgent cross-role dependencies
4. Document session outcomes in appropriate project files

---

## 🎯 SUCCESS METRICS

### **Developer Success Metrics:**
- Framework completeness and standards compliance
- Tool functionality and performance
- Code quality and test coverage
- Technical documentation accuracy

### **Designer Success Metrics:**
- Package quality and operator safety
- Documentation clarity and completeness
- Real-world deployment success
- User feedback and issue resolution

### **Shared Success Metrics:**
- Cross-role collaboration effectiveness
- Issue resolution time via bug tracker
- Overall AIAI ecosystem maturity
- Production deployment readiness

---

## 📝 NOTES

**Created**: 2025-08-05  
**Purpose**: Enable clear role separation for concurrent AIAI development  
**Scope**: Framework development and package implementation activities  
**Review**: Update as roles evolve and project requirements change