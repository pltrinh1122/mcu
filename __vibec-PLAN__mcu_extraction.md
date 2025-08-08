# __vibec-PLAN__: MCU Component Extraction

## Context Memory Unit: plan-mcu-extraction-2024-12-19-001

**Date**: 2024-12-19  
**Tool**: PLAN  
**Type**: Component Extraction  
**Status**: Pending Operator Review  

---

## Executive Summary

This plan outlines the comprehensive extraction of the `mcu/` component from the AIAI monorepo into a separate, standalone repository called "mcu". The MCU (Memory Context Units) component implements Contextual Memory Intelligence (CMI) principles and serves as the foundation for optimized Operator-AI collaboration.

## Current State Analysis

### **Component Structure**
```
mcu/
├── docs/                        # Base MCU specification and documentation
│   ├── MCU_SPECIFICATION.md     # Base specification for all MCU types
│   └── README.md                # MCU documentation overview
├── reference/                    # Reference MCUs for information transfer
│   ├── MCU_REFERENCE_SPECIFICATION.md
│   ├── MCU_REFERENCE_TEMPLATE.md
│   └── README.md
├── instruction/                  # Instruction MCUs for behavioral guidance
│   ├── MCU_INSTRUCTION_SPECIFICATION.md
│   ├── MCU_INSTRUCTION_TEMPLATE.md
│   ├── README.md
│   └── instruction-agent/        # AI-Agent specific instructions
│       ├── MCU_INSTRUCTION-AGENT_SPECIFICATION.md
│       ├── MCU_INSTRUCTION-AGENT_TEMPLATE.md
│       ├── README.md
│       └── vibecoding/          # VIBE_CODING specific instructions
│           ├── MCU_VIBE_CODING_SPECIFICATION.md
│           └── README.md
└── tests/                       # Test files and review documents
    ├── MCU_REFERENCE_SPECIFICATION_FAQ.md
    ├── MCU_VIBE_CODING_FAQ.md
    ├── review_2_of_REFERENCE_SPECIFICATON.md
    ├── review_2_of_VIBE_CODING.md
    ├── review_of_REFERENCE_SPECIFICATON.md
    ├── review_of_VIBE_CODING.md
    └── README.md
```

### **Dependencies Identified**
- **VIBE_CODING.md**: References MCU specifications and templates
- **Internal Cross-References**: Multiple MCU files reference each other
- **Documentation Integration**: MCU principles integrated into main project docs

## Extraction Strategy

### **Phase 1: Repository Setup and Structure**
1. **Create New Repository**
   - Initialize "mcu" repository on GitHub/GitLab
   - Set up branch protection rules
   - Configure CI/CD pipeline for documentation validation

2. **Establish Repository Structure**
   ```
   mcu/
   ├── .github/                   # GitHub workflows and templates
   ├── docs/                      # Base MCU specification
   ├── reference/                 # Reference MCU specifications
   ├── instruction/               # Instruction MCU specifications
   ├── templates/                 # MCU templates
   ├── tests/                     # Test files and reviews
   ├── examples/                  # Example MCU implementations
   ├── scripts/                   # Utility scripts
   ├── README.md                  # Main repository documentation
   ├── LICENSE                    # License file
   ├── CONTRIBUTING.md           # Contribution guidelines
   ├── CHANGELOG.md              # Version history
   └── pyproject.toml            # Python project configuration
   ```

### **Phase 2: Content Migration**
1. **Core Documentation Migration**
   - Migrate `docs/` directory with base specifications
   - Migrate `reference/` directory with reference MCU specs
   - Migrate `instruction/` directory with instruction MCU specs
   - Migrate `tests/` directory with test files and reviews

2. **Template Standardization**
   - Create `templates/` directory for reusable MCU templates
   - Standardize template structure and metadata
   - Add template validation scripts

3. **Example Implementations**
   - Create `examples/` directory with sample MCU implementations
   - Include real-world usage examples
   - Add documentation for each example

### **Phase 3: Repository Infrastructure**
1. **Documentation Framework**
   - Set up MkDocs or similar for documentation site
   - Configure automatic documentation generation
   - Set up documentation validation pipeline

2. **Quality Assurance**
   - Implement YAML validation for MCU files
   - Add link checking for cross-references
   - Set up automated testing for MCU structure compliance

3. **Development Tools**
   - Add pre-commit hooks for MCU validation
   - Create MCU generation and validation scripts
   - Set up automated testing pipeline

### **Phase 4: Integration and Dependencies**
1. **Update AIAI Repository**
   - Remove `mcu/` directory from AIAI monorepo
   - Update `VIBE_CODING.md` to reference external MCU repository
   - Update any internal references to MCU specifications

2. **Cross-Repository Integration**
   - Set up submodule or dependency reference to MCU repository
   - Configure automated synchronization if needed
   - Update documentation to reflect new structure

3. **Backward Compatibility**
   - Maintain API compatibility for existing MCU references
   - Provide migration guide for existing implementations
   - Support gradual migration timeline

## Implementation Plan

### **Step 1: Repository Creation and History Preservation (Day 1)**
- [ ] Create backup branch: `git branch backup-mcu-extraction`
- [ ] Document current state and dependencies
- [ ] Execute Git subtree extraction: `git subtree split --prefix=mcu --onto=empty-branch -b mcu-extraction`
- [ ] Create "mcu" repository on GitHub
- [ ] Push extracted history to new repository
- [ ] Verify history preservation and commit integrity
- [ ] Set up initial repository structure
- [ ] Configure branch protection and CI/CD
- [ ] Add license and contribution guidelines

### **Step 2: Content Migration (Days 2-3)**
- [ ] Migrate core documentation files
- [ ] Standardize file structure and naming
- [ ] Update internal cross-references
- [ ] Create template directory structure

### **Step 3: Infrastructure Setup (Days 4-5)**
- [ ] Set up documentation framework
- [ ] Configure validation scripts
- [ ] Add development tools and hooks
- [ ] Create example implementations

### **Step 4: Integration and Testing (Days 6-7)**
- [ ] Update AIAI repository references
- [ ] Test cross-repository integration
- [ ] Validate all links and references
- [ ] Verify Git history preservation and commit integrity
- [ ] Perform comprehensive testing

### **Step 5: Documentation and Release (Day 8)**
- [ ] Complete documentation updates
- [ ] Create migration guide
- [ ] Release initial version
- [ ] Announce extraction completion

## Risk Assessment

### **High Risk**
- **Breaking References**: Internal cross-references may break during migration
- **Documentation Gaps**: Some documentation may reference MCU files without updates
- **Integration Complexity**: Cross-repository integration may introduce complexity

### **Medium Risk**
- **Template Compatibility**: Existing MCU templates may need updates
- **Validation Pipeline**: New validation requirements may conflict with existing processes
- **User Adoption**: Users may need time to adapt to new repository structure

### **Low Risk**
- **Content Loss**: All content will be preserved during migration
- **Version Control**: Git history can be preserved through careful migration

## Git History Preservation Strategy

### **Repository Extraction Methods**
1. **Git Subtree Extraction** (Recommended)
   - Use `git subtree split` to extract MCU directory with full history
   - Command: `git subtree split --prefix=mcu --onto=empty-branch -b mcu-extraction`
   - Preserves all commits, authors, timestamps, and commit messages
   - Maintains complete development history

2. **Git Filter-Repo Alternative**
   - Use `git filter-repo` for more complex history manipulation
   - Allows selective history preservation with custom filtering
   - Useful if additional cleanup is needed during extraction

### **History Preservation Steps**
1. **Pre-Extraction Preparation**
   - Create backup branch: `git branch backup-mcu-extraction`
   - Document current state and dependencies
   - Tag current version for rollback capability

2. **Extraction Process**
   - Execute subtree split with full history preservation
   - Verify all commits are transferred correctly
   - Validate author attribution and timestamps

3. **Post-Extraction Verification**
   - Compare commit hashes and timestamps
   - Verify all file changes are preserved
   - Test repository integrity and functionality

### **Cross-Repository History Linking**
- Maintain reference to original AIAI repository
- Document extraction commit hash for future reference
- Create bidirectional links between repositories

## Mitigation Strategies

### **Reference Management**
- Implement comprehensive link checking
- Create redirects for old references
- Provide clear migration documentation

### **Testing Strategy**
- Automated validation of all MCU files
- Cross-reference verification
- Integration testing with AIAI repository

### **User Communication**
- Clear announcement of extraction
- Detailed migration guide
- Support for gradual transition

## Success Criteria

### **Technical Success**
- [ ] All MCU files successfully migrated
- [ ] Complete Git history preserved with all commits, authors, and timestamps
- [ ] No broken cross-references
- [ ] Automated validation pipeline working
- [ ] Documentation site functional

### **Integration Success**
- [ ] AIAI repository updated to reference external MCU
- [ ] Cross-repository integration working
- [ ] Backward compatibility maintained
- [ ] Migration guide completed

### **Quality Success**
- [ ] All MCU files pass validation
- [ ] Documentation is comprehensive and accurate
- [ ] Examples are functional and well-documented
- [ ] Templates are standardized and reusable

## Resource Requirements

### **Time Allocation**
- **Repository Setup**: 1 day
- **Content Migration**: 2 days
- **Infrastructure Setup**: 2 days
- **Integration and Testing**: 2 days
- **Documentation and Release**: 1 day
- **Total Estimated Time**: 8 days

### **Skills Required**
- Git repository management
- Documentation framework setup
- YAML validation and processing
- Cross-repository integration
- Technical writing and documentation

### **Tools Needed**
- Git for version control
- MkDocs or similar for documentation
- Python for validation scripts
- GitHub Actions for CI/CD
- Link checking tools

## Post-Extraction Maintenance

### **Ongoing Responsibilities**
- Maintain MCU specifications and templates
- Update documentation as needed
- Provide support for MCU implementations
- Coordinate with AIAI repository for integration

### **Version Management**
- Semantic versioning for MCU specifications
- Changelog maintenance
- Release notes for significant changes
- Backward compatibility considerations

### **Community Engagement**
- Issue tracking and resolution
- Pull request review and merging
- Documentation improvements
- Example implementation contributions

---

## Approval Required

This plan requires Operator review and approval before execution. The extraction involves significant changes to the AIAI project structure and may impact existing workflows and documentation.

**Next Steps**:
1. Operator review and approval of this plan
2. Repository creation and initial setup
3. Content migration and validation
4. Integration testing and documentation updates
5. Final release and announcement

---

*This plan implements systematic component extraction following VIBE_CODING principles for safe and controlled repository separation.*
