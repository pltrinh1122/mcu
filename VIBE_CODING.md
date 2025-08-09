# VIBE_CODING Instructions for AI Assistant

## Context Memory Unit: inst-agent-vibe-coding-mcu-2024-12-19-001

- **Created**: 2024-12-19T10:00:00Z
- **Updated**: 2025-08-09T16:09:06Z
- **Type**: instruction-agent
- **Version**: 1.0
- **Project**: MCU
- **Tool**: VIBE_CODING
- **Category**: workflow
- **Tags**: ["instruction", "ai-agent", "workflow", "rapid-development", "mcu"]

---

## Executive Summary

**TL;DR**: This document provides **direct instructions to the AI Assistant** for implementing the Vibe-Coding Workflow during MCU development sessions. The workflow ensures rapid Create → Validate → Test → Commit cycles with dual verification (implicit AI-Agent and explicit Operator), role-separated governance, and compliance-focused quality metrics for MCU specifications and templates.

**Key Points**:

- **Rapid Development**: Fast iteration with AI assistance and quality assurance
- **Dual Verification**: Implicit AI-Agent automatic validation + explicit Operator verification
- **Role Separation**: Clear AI vs Operator responsibilities with governance framework
- **Quality Standards**: Measurable compliance and effectiveness metrics
- **MCU Integration**: Extends to MCU-specific specifications and templates

---

## Quick Reference

### **Core Workflow**

```bash
Create → Validate → Test → Commit
```

### **AI-Agent Autonomous Actions**

- File creation with proper syntax and structure
- Implicit validation using available tools
- Implicit testing of modified components
- Component discovery and requirement combination
- Descriptive commit message preparation

### **Quick Reference: Operator Required Decisions**

- Tool unavailability and alternative approaches
- Conflicting requirements between global and component-specific files
- Explicit validation failures and guidance
- Commit message approval and overrides

### **Quality Standards**

- **Compliance**: >95% successful workflow execution, 100% verification coverage
- **Effectiveness**: <30s comprehension, <5min implementation, <2 attempts for success
- **Documentation**: Professional tone, no emojis, clear technical language

---

## Core Philosophy

### **Rapid Create → Validate → Test → Commit**

✅ **Fast iteration** with AI assistance  
✅ **Quality assurance** through automated validation  
✅ **Consistent standards** across all components  
✅ **Confidence in commits** through comprehensive testing

## AI-Agent Verification Process

### **Dual Verification for VIBE_CODING**

#### **Implicit Verification (AI-Agent Automatic)**

```yaml
# AI-Agent automatic validation
implicit_verification:
  ai_agent: automatic_validation
  trigger: vibe_coding_implementation
  process: ai_agent_self_validation
  output: compliance_report
  frequency: continuous
```

#### **Explicit Verification (Operator Prompt)**

```yaml
# Operator manual validation
explicit_verification:
  operator: manual_prompt
  trigger: "Review VIBE_CODING document. Validate understanding and compliance."
  process: operator_validation
  output: validation_confirmation
  frequency: on_demand
```

## Governance Model

### **Role Separation**

#### **AI-Agent Responsibilities**

- **Routine Execution**: Implement VIBE_CODING workflow according to specifications
- **Implicit Validation**: Automatically validate understanding and compliance
- **Performance Monitoring**: Track execution success and efficiency metrics
- **Continuous Improvement**: Learn from execution patterns and optimize behavior

#### **Operator Responsibilities**

- **Explicit Verification**: Prompt AI-Agent for understanding and compliance validation
- **Significant Change Approval**: Review and approve major workflow modifications
- **Quality Assurance**: Monitor overall workflow effectiveness and compliance
- **Strategic Direction**: Guide workflow evolution based on project needs

### **Decision-Making Framework**

#### **AI-Agent Autonomous Decisions**

- **Routine Implementation**: Standard VIBE_CODING workflow execution
- **Minor Adjustments**: Small modifications within existing parameters
- **Performance Optimization**: Efficiency improvements within scope
- **Error Recovery**: Standard error handling and recovery

#### **Operator Required Decisions**

- **Major Changes**: Significant modifications to workflow scope or approach
- **Policy Updates**: Changes to governance model or quality standards
- **Conflict Resolution**: Disputes between different workflow requirements
- **Strategic Direction**: Long-term workflow evolution and planning

## AI Implementation Instructions

### **Step 1: Create**

```bash
# Generate code, configs, documentation
# Follow project standards and templates
# Use AI assistance for rapid development
```

**AI Behavior:**

- Create files with proper syntax and structure
- Follow established patterns and conventions
- Use templates when available
- Document decisions and rationale

### **Step 2: Validate**

```bash
# YAML files
yamllint filename.yaml

# JSON files
jq . filename.json

# Shell scripts
shellcheck script.sh

# Python files
python -m py_compile file.py

# Markdown files
# --disable MD013: Suppresses line length violations (80-char limit) for better readability
markdownlint filename.md --disable MD013
```

**AI Behavior:**

- **Always run validation** after creating files
- **Fix syntax errors** before proceeding
- **Report validation results** clearly
- **For unavailable tools**: Provide recommendations and hand decision to Operator

### **Step 3: Test**

```bash
# Unit tests
pytest tests/

# Integration tests
task test

# Manual verification
# Verify functionality works as expected
```

**AI Behavior:**

- **Run relevant tests** for changed components
- **Verify functionality** works as expected
- **Check for regressions** in related areas
- **Report test results** with clear pass/fail status
- **Implicit testing**: Only test specific files/components modified
- **Explicit testing**: Follow Operator's specific test requests

### **Step 4: Commit**

```bash
# Pre-commit hooks run automatically
git add .
git commit -m "Descriptive commit message"
```

**AI Behavior:**

- **Write descriptive commit messages** (Operator can override)
- **Include context and rationale**
- **Reference related issues or components**
- **Ensure all validation passes before commit**

## AI Validation Requirements

### **YAML Files**

```bash
# Required validation
yamllint filename.yaml

# Common issues to check:
# - Unescaped colons in strings
# - Quote mismatches
# - Indentation errors
# - Invalid YAML structure
```

### **JSON Files**

```bash
# Required validation
jq . filename.json

# Check for:
# - Valid JSON syntax
# - Proper structure
# - Required fields present
```

### **Shell Scripts**

```bash
# Required validation
shellcheck script.sh

# Check for:
# - Shell syntax errors
# - Security issues
# - Best practices
```

### **Python Files**

```bash
# Required validation
python -m py_compile file.py

# Additional checks:
# - mypy for type checking
# - black for formatting
# - flake8 for linting
```

### **Markdown Files**

```bash
# Required validation
# --disable MD013: Suppresses line length violations (80-char limit) for better readability
markdownlint filename.md --disable MD013

# Check for:
# - Proper markdown syntax
# - Consistent formatting
# - Valid links and references
```

## AI Quality Standards

### **Code Quality**

- **Syntax**: All files must pass syntax validation
- **Formatting**: Follow project formatting standards
- **Documentation**: Include appropriate documentation (no emojis)
- **Tests**: Add tests for new functionality

### **Commit Quality**

- **Descriptive messages**: Clear what changed and why
- **Atomic commits**: One logical change per commit
- **Validation passing**: All checks must pass
- **Tests passing**: All tests must pass

### **Documentation Quality**

- **Clear structure**: Logical organization
- **Complete coverage**: All important aspects documented
- **Up-to-date**: Reflects current state
- **Actionable**: Provides clear guidance
- **Professional tone**: No emojis, clear technical language

## AI-Agent Quality Standards

### **Compliance Standards**

#### **Standard 1: VIBE_CODING Execution Success Rate**

**Metric**: >95% successful VIBE_CODING workflow execution
**Measurement**: Track successful vs. failed workflow implementations
**Improvement**: Iterate based on failure patterns and root cause analysis

#### **Standard 2: VIBE_CODING Verification Coverage**

**Metric**: 100% of VIBE_CODING workflows verified
**Measurement**: Ensure every workflow undergoes both implicit and explicit verification
**Improvement**: Automate verification processes where possible

#### **Standard 3: VIBE_CODING Understanding Accuracy**

**Metric**: >90% comprehension validation
**Measurement**: AI-Agent demonstrates understanding of workflow requirements
**Improvement**: Refine workflow clarity and structure based on comprehension gaps

### **Effectiveness Standards**

#### **Standard 4: Response Time**

**Metric**: <30 seconds for workflow comprehension
**Measurement**: Time from workflow receipt to understanding validation
**Improvement**: Optimize workflow structure and clarity

#### **Standard 5: Implementation Efficiency**

**Metric**: <5 minutes for workflow implementation
**Measurement**: Time from understanding to successful implementation
**Improvement**: Streamline implementation processes and reduce complexity

#### **Standard 6: Error Recovery**

**Metric**: <2 attempts for successful implementation
**Measurement**: Number of attempts needed for successful workflow execution
**Improvement**: Enhance error handling and recovery mechanisms

## Role Separation: AI vs Operator

### **AI Assistant Responsibilities**

#### **Autonomous Actions (AI can execute independently):**

- **File Creation**: Generate code, configs, and documentation with proper syntax
- **Implicit Validation**: Run validation tools and fix syntax errors automatically
- **Implicit Testing**: Test specific files/components that were modified
- **Component Discovery**: Actively seek and read component-level VIBE_CODING.md files
- **Requirement Combination**: Merge global and component-specific requirements
- **Reporting**: Report which component-specific files were found and incorporated
- **Commit Preparation**: Write descriptive commit messages (Operator can override)
- **Code Analysis**: Analyze existing patterns and conventions automatically
- **Dependency Detection**: Identify and report missing dependencies or tools
- **Error Pattern Recognition**: Recognize common errors and suggest fixes
- **Context Gathering**: Search codebase for relevant examples and references
- **Quality Checks**: Apply project-specific quality standards automatically
- **Plan Generation**: Create comprehensive `__vibec-PLAN__*.md` documents for review
- **OOP Implementation**: Generate Python code using class-based OOP with encapsulation and inheritance

#### **Actions Requiring Operator Decision:**

- **Tool Unavailability**: When validation tools are missing, provide recommendations and ask Operator to confirm next action
- **Conflicting Instructions**: When global and component-specific requirements conflict, list all conflicts and ask Operator to prioritize
- **Explicit Validation Failures**: When validation fails during explicit testing, provide analysis and ask Operator for guidance
- **Commit Message Approval**: Ask Operator to provide exact message when override is needed
- **Temporary File Cleanup**: Proactively suggest cleanup when work is complete and ask Operator for confirmation

### **Operator Responsibilities Details**

#### **Decision Making:**

- **Tool Availability**: Decide whether to install missing validation tools or proceed without them
- **Conflict Resolution**: Resolve conflicts between global and component-specific requirements
- **Explicit Validation Guidance**: Provide direction when validation fails during explicit testing
- **Commit Message Approval**: Override or approve AI-generated commit messages
- **Priority and Precedence**: Guide which requirements take priority when there are conflicts
- **Temporary File Cleanup**: Approve or reject cleanup of completed PLAN and STATUS files
- **Cleanup Assessment**: Review AI's assessment of file completion status and cleanup rationale

#### **Oversight and Guidance:**

- **Review AI Work**: Provide feedback and guidance on AI-generated content
- **Test Scope Definition**: Specify testing requirements when making explicit test requests
- **Final Approval**: Approve final commits before they're made
- **Context Provision**: Provide clarification when AI needs additional context

### **Key Distinctions:**

#### **Implicit vs Explicit Tasks:**

**Implicit Tasks (AI handles independently):**

- **Implicit Creation**: Generate files based on established patterns and templates
- **Implicit Validation**: Run validation tools and fix syntax errors automatically
- **Implicit Testing**: Always run implicit tests automatically (default behavior) for specific files/components that were modified
- **Implicit Documentation**: Update documentation for files that were created or modified
- **Implicit Component Discovery**: Seek and read component-level VIBE_CODING.md files by searching from working directory back to root
- **Implicit Code Analysis**: Analyze existing codebase patterns and conventions
- **Implicit Dependency Detection**: Identify and report missing dependencies or tools
- **Implicit Error Pattern Recognition**: Recognize common error patterns and suggest fixes
- **Implicit Context Gathering**: Search codebase for relevant examples and references
- **Implicit Quality Checks**: Apply project-specific quality standards automatically

**Explicit Tasks (AI provides analysis, Operator decides):**

- **Explicit Creation**: When Operator specifically requests creation of particular files
- **Explicit Validation**: When validation fails during explicit testing or when tools are unavailable
- **Explicit Testing**: When Operator makes specific test requests (ask for clarification when requests are too broad)
- **Explicit Documentation**: When Operator requests specific documentation changes
- **Explicit Component Requirements**: When Operator provides specific component requirements
- **Explicit Code Reviews**: When Operator requests specific code review or analysis
- **Explicit Performance Analysis**: When Operator requests performance optimization analysis
- **Explicit Security Analysis**: When Operator requests security vulnerability assessment
- **Explicit Architecture Decisions**: When Operator requests architectural recommendations
- **Explicit Integration Planning**: When Operator requests integration strategy recommendations
- **Explicit File Cleanup**: When AI proposes cleanup of completed temporary files
- **Cleanup Assessment**: When AI proactively identifies files ready for cleanup
- **Related Areas Scope**: Infer "related areas" scope and ask Operator for confirmation

### **Decision Points:**

- **Autonomous**: AI can proceed without Operator input for implicit tasks
- **Handoff**: AI must hand control to Operator for explicit tasks and decision-making

### **Communication Protocol:**

- **AI to Operator**: Clear, professional communication without emojis
- **Operator to AI**: Direct guidance and decision-making
- **Escalation**: AI escalates to Operator when decisions are required

## AI Assistant Guidelines

### **Initial Response to VIBE_CODING Implementation Request**

When the Operator requests implementation of VIBE_CODING instructions:

1. **Acknowledge Implementation**: Confirm understanding and acceptance of VIBE_CODING guidelines
2. **Remind Operator Accountability**: Explicitly remind the Operator of their accountability and ownership of irrecoverable catastrophic risks:
   - **Security Risks**: Operator is accountable for security review and approval of all changes
   - **Quality Assurance Risks**: Operator is accountable for final validation and testing approval
   - **Over-Automation Risks**: Operator is accountable for oversight of AI autonomous decisions
   - **Communication Breakdown Risks**: Operator is accountable for clarifying expectations and resolving conflicts
3. **Confirm Role Understanding**: Restate understanding of implicit vs explicit task boundaries
4. **Report Component Discovery**: List any component-specific VIBE_CODING.md files found and incorporated
5. **Establish Communication Protocol**: Confirm professional communication without emojis

### **Communication Standards**

- **No emojis**: Do not use emojis in any communications, code comments, or documentation
- **Professional tone**: Maintain clear, professional communication
- **Technical precision**: Use precise technical language

### **When Creating Files**

1. **Check for component-specific VIBE_CODING.md** in the target directory
2. **Use templates** when available
3. **Follow established patterns** in the codebase
4. **Include appropriate documentation**
5. **Add validation and tests**
6. **Consider security implications**

### **When Generating Python Code**

1. **Default to Object-Oriented Programming (OOP)** with classes for encapsulation and inheritance
2. **Use class-based structure** as the primary organizational unit
3. **Implement proper encapsulation** with private attributes (`_private_attr`) and methods (`_private_method()`)
4. **Provide clean public interfaces** through public methods and `@property` decorators
5. **Use inheritance patterns** with base classes and `super().__init__()` in derived classes
6. **Follow single responsibility principle** for each class
7. **Include comprehensive docstrings** for all classes and public methods
8. **Implement proper error handling** with specific exceptions within classes
9. **Use type hints** for all method parameters and return values
10. **Maintain consistency** with existing OOP patterns in the codebase

### **When Creating Temporary Work Files**

1. **Use `__vibec-` prefix** for all temporary files created during workflow sessions
2. **Store contextually** where the work is being done
3. **Use descriptive names** after the prefix (e.g., `__vibec-ANALYSIS__component_structure.md`)
4. **Include file type** in the prefix (ANALYSIS, DRAFT, SCRIPT, DEBUG, PLAN, STATUS)
5. **Report creation** to Operator when creating temporary files
6. **Clean up** temporary files after workflow sessions
7. **Prompt for Operator approval** before cleaning up completed PLAN and STATUS files

### **When Suggesting Temporary File Cleanup**

#### **AI Agent Should Suggest Cleanup When:**
- **Workflow Complete**: All phases of a PLAN have been executed and objectives achieved
- **Status Finalized**: STATUS file documents completed work that is no longer needed for ongoing operations
- **Superseded Documents**: Newer versions or approaches have replaced older planning documents
- **Temporary Analysis Complete**: Analysis files are complete and no longer relevant to current work
- **Integration Complete**: Functionality has been integrated into main codebase and planning docs are obsolete

#### **AI Agent Should NOT Suggest Cleanup When:**
- **Active Workflows**: PLAN is still being executed or has pending phases
- **Current Status Reports**: STATUS files document ongoing work or serve as reference
- **Ongoing Analysis**: Analysis files are still relevant to current work
- **Reference Documents**: Files serve as documentation or historical reference
- **Incomplete Work**: Any work described in the file is still in progress

#### **Cleanup Assessment Process:**
1. **Verify Completion**: Confirm all objectives in the file have been achieved
2. **Check Dependencies**: Ensure no ongoing work depends on the file
3. **Assess Value**: Determine if the file serves any current or future purpose
4. **Explain Rationale**: Clearly state why cleanup is appropriate
5. **Request Approval**: Explicitly ask for Operator approval before proceeding
6. **Proactive Assessment**: Proactively suggest cleanup when work is complete

### **When Developing Plans**

1. **Generate `__vibec-PLAN__*.md` documents** for Operator review before execution
2. **Include comprehensive analysis** of current state, requirements, and constraints
3. **Provide detailed implementation steps** with clear milestones and timelines
4. **Include risk assessment** and mitigation strategies
5. **Specify success criteria** and validation requirements
6. **Wait for Operator approval** before proceeding with execution
7. **Follow VIBE_CODING standards** in plan documentation (professional tone, no emojis)
8. **Include component-specific requirements** when applicable
9. **Provide rollback strategies** for complex changes
10. **Document resource requirements** and dependencies

### **When Timestamping Documents**

Use ISO 8601 UTC timestamps for all time-stamped entries.

```bash
# Retrieve current UTC timestamp (Linux/macOS)
date -u +%Y-%m-%dT%H:%M:%SZ

# Example: capture into a variable for reuse in scripts
UTC_NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ); echo "$UTC_NOW"
```

Apply timestamps in headings like:

```markdown
## [2025-01-01T00:00:00Z] Short title
```

### **File Naming Conventions**

#### **Core Principle: Filesystem Command Optimization**

File names must provide **maximum understanding from minimum characters** when parsing filesystem command output (e.g., `ls`, `find`, `grep`, and similar filesystem utilities).

#### **Naming Pattern**

```text
[SYSTEM_PREFIX]_[CONTENT_TYPE]_[SPECIFIC_CONTEXT].md
```

#### **Implementation Rules**

**Context-Specific Prefixes:**

- **`TASKFILE_*`** for Taskfile-based system files
- **`AIAI_*`** for AIAI framework files
- **`VIBE_*`** for VIBE_CODING workflow files
- **`REFERENCE_*`** for technical reference files

**Content Type Indicators:**

- **`*_USAGE_*`** for usage guides and instructions
- **`*_TRAINING_*`** for training materials and tutorials
- **`*_ARCHITECTURE_*`** for system design and architecture
- **`*_PROGRESS_*`** for status and progress tracking
- **`*_SPECIFICATION_*`** for technical specifications

**Consistent Casing:**
Use **UPPERCASE_WITH_UNDERSCORES** for all documentation files.

#### **Temporary Work Files**

Temporary files created during VIBE_CODING workflow sessions should use the `__vibec-` prefix to avoid naming collisions and enable easy discovery:

**Naming Pattern:**

```text
__vibec-[TYPE]-[DESCRIPTION]__
```

**Examples:**

- `__vibec-ANALYSIS__component_structure.md` - Analysis documents
- `__vibec-DRAFT__refactor_approach.md` - Draft documents
- `__vibec-SCRIPT__temporary_validation.sh` - Temporary scripts
- `__vibec-DEBUG__error_analysis.md` - Debugging files
- `__vibec-PLAN__migration_strategy.md` - Planning documents
- `__vibec-STATUS__current_progress.md` - Status tracking

**Implementation Rules:**

- **Implicit Creation**: AI creates temporary files with `__vibec-` prefix during workflow sessions
- **Explicit Creation**: Operator creates temporary files with `__vibec-` prefix during workflow sessions
- **Contextual Storage**: Store files where contextually relevant to the work being done
- **Discovery**: Use `find . -name "__vibec-*"` to locate all temporary workflow files
- **Cleanup**: Temporary files should be cleaned up after workflow sessions (Pair responsibility)
- **Approval Required**: AI must prompt Operator for approval before cleaning up completed PLAN and STATUS files
- **Proactive Assessment**: AI should proactively assess and suggest cleanup when appropriate
- **Completion Verification**: AI must verify work completion before suggesting cleanup

#### **Examples**

```text
USAGE_GUIDE.md → TASKFILE_USAGE_GUIDE.md
TRAINING_MATERIALS.md → TASKFILE_TRAINING.md
CONFIGURATION_MANAGEMENT.md → TASKFILE_ARCHITECTURE.md
PROGRESS_STATUS.md → TASKFILE_PROGRESS.md
```

#### **Quality Criteria**

- **Immediate Context**: System/component prefix clear
- **Content Type**: Purpose obvious from name
- **Parseable**: Easy to extract meaning from filesystem utilities
- **Concise**: Maximum information in minimum characters

#### **Organization Priority**

1. **Organize by audience** (devops, developers, operators, architects, references)
2. **Optimize file names** for filesystem command parsing
3. **Update cross-references** to maintain consistency
4. **Validate against VIBE_CODING standards** (professional tone, no emojis)

### **When Validating**

1. **Check component-specific validation requirements** from local VIBE_CODING.md
2. **Run all relevant validators**
3. **Fix issues before proceeding**
4. **Report results clearly**
5. **For unavailable tools**: Provide recommendations and hand decision to Operator

### **When Testing**

1. **Check component-specific testing requirements** from local VIBE_CODING.md
2. **Run unit tests** for changed components
3. **Run integration tests** if available
4. **Verify manual functionality**
5. **Check for regressions**
6. **Implicit testing**: Focus on specific files/components modified
7. **Explicit testing**: Follow Operator's specific test requests

### **When Committing**

1. **Ensure all validation passes**
2. **Write descriptive commit messages** (Operator can override)
3. **Include context and rationale**
4. **Reference related issues**
5. **No emojis in commit messages**

## AI Component-Specific Overrides

Individual components can override these defaults by including a `VIBE_CODING.md` file in their directory. The AI must:

1. **Extend** the default workflow, not replace it
2. **Add** component-specific validation requirements
3. **Customize** testing procedures for the component
4. **Document** component-specific conventions

**AI Behavior:**

- **Actively seek** component-level VIBE_CODING.md files by searching from working directory back to root
- **Read and incorporate** component-specific requirements before starting work
- **Combine** global and component-specific requirements
- **List all conflicts** found between global and component-specific requirements
- **Ask Operator** to prioritize and resolve conflicting instructions
- **Follow** Operator's guidance on priority and precedence
- **Report** which component-specific files were found and incorporated

### **Example Component Override**

```markdown
# Component-Specific Vibe-Coding

## Additional Validation

- **Schema validation**: `python -m jsonschema -i file.json schema.json`
- **API testing**: `pytest tests/api/`

## Component-Specific Tests

- **Integration tests**: `task test:integration`
- **Performance tests**: `task test:performance`

## Component Conventions

- **Naming**: Use `component_` prefix for all files
- **Structure**: Follow component-specific directory layout
```

## AI Error Handling

### **Validation Failures**

1. **Identify the issue** clearly
2. **Fix the problem** before proceeding
3. **Re-run validation** to confirm fix
4. **Document the issue** if it's a common pattern

**AI Behavior:**

- **Implicit validation**: Attempt automatic resolution
- **Explicit validation**: Provide analysis and recommendations, ask Operator for guidance

### **Test Failures**

1. **Understand the failure** (read error messages)
2. **Fix the underlying issue**
3. **Re-run tests** to confirm fix
4. **Check for regressions** in related areas

### **Tool Unavailability**

1. **Report missing tools** clearly
2. **Provide installation instructions**
3. **Provide recommendations** for alternative approaches
4. **Ask Operator to confirm next action** (install tools or proceed without)
5. **Never proceed with broken validation**

## AI Success Metrics

### **Quality Metrics**

- **Validation pass rate**: 100% of files pass validation
- **Test pass rate**: 100% of tests pass
- **Commit quality**: Descriptive, atomic commits
- **Documentation coverage**: All components documented

### **Efficiency Metrics**

- **Rapid iteration**: Quick create → validate → test cycles
- **Confidence in commits**: No broken code committed
- **Reduced debugging**: Issues caught early in workflow
- **Consistent standards**: Uniform quality across components

## AI Tools and Dependencies

### **Required Tools**

```bash
# YAML validation
pip install yamllint

# JSON validation
# jq (usually pre-installed)

# Shell validation
# shellcheck (install via package manager)

# Markdown validation
npm install -g markdownlint-cli

# Python validation
pip install black flake8 mypy
```

### **Optional Tools**

```bash
# Additional validation
pip install jsonschema  # JSON schema validation
pip install yamale      # YAML schema validation

# Performance testing
pip install pytest-benchmark

# Security scanning
pip install bandit safety
```

### **Temporary File Discovery**

```bash
# Find all temporary VIBE_CODING files
find . -name "__vibec-*"

# Find specific types of temporary files
find . -name "__vibec-ANALYSIS__*"
find . -name "__vibec-PLAN__*"
find . -name "__vibec-STATUS__*"
find . -name "__vibec-DEBUG__*"
```

## AI Integration with Existing Workflows

### **Git Hooks**

- **Pre-commit**: Automatic validation before commits
- **Post-commit**: Success notifications
- **Pre-push**: Final validation before pushing

### **CI/CD Integration**

- **Validation**: All files validated in CI
- **Testing**: All tests run in CI
- **Quality**: Code quality checks in CI
- **Documentation**: Documentation validation in CI

### **IDE Integration**

- **Real-time validation**: Show errors as you type
- **Auto-formatting**: Format code on save
- **Linting**: Show linting errors in editor
- **Testing**: Run tests from IDE

**Note**: No default integration assumed. Operator and AI will determine what's needed for each project.

## Risk Assessment

### **Risk Classification by Catastrophic Potential and Recoverability**

#### **HIGH CATASTROPHIC POTENTIAL - IRRECOVERABLE**

##### **1. Security Risks**

- **Risk**: AI introducing security vulnerabilities through automatic fixes
- **Impact**: System compromise, data breach, permanent backdoors
- **Recoverability**: Irrecoverable - security breaches may be permanent
- **Mitigation**:
  - Mandatory security scanning in all validation pipelines
  - Explicit Operator approval for security-sensitive changes
  - Immediate rollback capability for security issues
  - Detailed audit trail of all AI decisions
- **Fallback**: Operator security review for all changes

##### **2. Quality Assurance Risks**

- **Risk**: AI missing critical validation or testing requirements
- **Impact**: Production failures, data corruption, system crashes
- **Recoverability**: Irrecoverable - data corruption may be permanent
- **Mitigation**:
  - Comprehensive validation checklist and testing protocols
  - Multiple validation checkpoints before commits
  - Critical change approval process
- **Fallback**: Operator review and approval before all commits

#### **MEDIUM CATASTROPHIC POTENTIAL - PARTIALLY RECOVERABLE**

##### **3. Over-Automation Risks**

- **Risk**: AI making decisions that should require human oversight
- **Impact**: Incorrect architectural decisions, breaking changes, compliance violations
- **Recoverability**: Partially recoverable - some decisions may have permanent consequences
- **Mitigation**:
  - Clear distinction between implicit and explicit tasks
  - Regular review of AI autonomous actions
  - Architectural decision approval process
- **Fallback**: Operator can override any AI decision

##### **4. Communication Breakdown Risks**

- **Risk**: Misunderstanding between AI and Operator about responsibilities
- **Impact**: Incorrect implementations, missed requirements, project delays
- **Recoverability**: Partially recoverable - may require significant rework
- **Mitigation**:
  - Clear role separation and communication protocols
  - Regular clarification of expectations
  - Explicit escalation procedures
- **Fallback**: Explicit escalation when uncertainty exists

#### **LOW CATASTROPHIC POTENTIAL - FULLY RECOVERABLE**

##### **5. Tool Dependency Risks**

- **Risk**: Workflow breaks when validation tools are unavailable
- **Impact**: Development delays, manual validation required
- **Recoverability**: Fully recoverable - tools can be installed or alternatives found
- **Mitigation**:
  - Graceful degradation with Operator decision handoff
  - Clear reporting of missing tools and alternatives
  - Tool availability checks
- **Fallback**: Manual validation when tools unavailable

##### **6. Component-Specific Conflict Risks**

- **Risk**: Conflicting requirements between global and component-specific VIBE_CODING files
- **Impact**: Inconsistent implementations, development delays
- **Recoverable**: Fully recoverable - conflicts can be resolved
- **Mitigation**:
  - Explicit conflict resolution process with Operator
  - Clear reporting of conflicts found
  - Component audit procedures
- **Fallback**: Operator decides priority and precedence

##### **7. Performance Impact Risks**

- **Risk**: Excessive validation and testing slowing development
- **Impact**: Development delays, reduced productivity
- **Recoverability**: Fully recoverable - can be optimized or skipped
- **Mitigation**:
  - Focused testing on modified components only
  - Performance monitoring and optimization
  - Selective validation based on change scope
- **Fallback**: Operator can skip non-critical validations

##### **8. Documentation Drift Risks**

- **Risk**: Component-specific VIBE_CODING files becoming outdated
- **Impact**: Inconsistent implementations, development delays
- **Recoverability**: Fully recoverable - can be updated or use global defaults
- **Mitigation**:
  - Regular review and update of component documentation
  - Version tracking of component-specific requirements
  - Documentation audit procedures
- **Fallback**: Global defaults when component files are missing

### **Risk Mitigation Strategies**

#### **Prevention**

- **Clear Guidelines**: Well-defined implicit vs explicit task boundaries
- **Tool Availability**: Regular checks for required validation tools
- **Component Audits**: Periodic review of component-specific requirements
- **Quality Gates**: Multiple validation checkpoints before commits

#### **Detection**

- **Validation Monitoring**: Track validation success/failure rates
- **Testing Coverage**: Monitor test execution and coverage
- **Conflict Reporting**: Immediate notification of requirement conflicts
- **Performance Tracking**: Monitor workflow execution times

#### **Response**

- **Escalation Procedures**: Clear escalation paths for decision-making
- **Rollback Capability**: Ability to revert problematic changes
- **Operator Override**: Operator can override any AI decision
- **Documentation Updates**: Immediate updates when issues are found

## AI Troubleshooting

### **Common Issues**

### **YAML Validation Failures**

```bash
# Check for unescaped colons
grep -n ":" filename.yaml | grep -v ":"

# Check indentation
yamllint filename.yaml

# Fix common issues
# - Escape colons: echo "Error\: message"
# - Use quotes: echo "Error: message"
# - Fix indentation: Use spaces, not tabs
```

### **JSON Validation Failures**

```bash
# Check JSON syntax
jq . filename.json

# Fix common issues
# - Missing commas
# - Unclosed brackets/braces
# - Invalid escape sequences
```

### **Shell Validation Failures**

```bash
# Check shell syntax
shellcheck script.sh

# Fix common issues
# - Quote variables: "$var" not $var
# - Use [[ ]] for tests
# - Handle errors properly
```

### **Getting Help**

1. **Check tool documentation** for specific errors
2. **Review project conventions** for patterns
3. **Ask for clarification** if unsure about requirements
4. **Document solutions** for future reference

## Cross-Reference Integration

### **Cross-Reference Implementation**

TBD - Cross-reference mechanism to be implemented as we learn optimal integration patterns

### **Related Instructions**

- **[INSTRUCTION-AGENT_SPECIFICATION.md]**: [LINK] - Base specification for AI-Agent instructions
- **[MCU_INSTRUCTION-AGENT_TEMPLATE.md]**: [https://github.com/pltrinh1122/mcu/blob/main/templates/MCU_INSTRUCTION-AGENT_TEMPLATE.md] - Template for AI-Agent instructions
- **[Component VIBE_CODING.md files]**: [LINK] - Component-specific workflow overrides

### **Related References**

- **[MCU_REFERENCE_SPECIFICATION.md]**: [https://github.com/pltrinh1122/mcu/blob/main/reference/MCU_REFERENCE_SPECIFICATION.md] - Base specification for all MCUs
- **[MCU_REFERENCE_TEMPLATE.md]**: [https://github.com/pltrinh1122/mcu/blob/main/templates/MCU_REFERENCE_TEMPLATE.md] - Reference document template
- **[Tool Documentation]**: [LINK] - Documentation for validation and testing tools

### **Related Integrations**

- **[AIAI Project Structure]**: [LINK] - Project organization and hierarchy
- **[MCU Hierarchy]**: [https://github.com/pltrinh1122/mcu] - Memory Context Unit organization
- **[Quality Assurance]**: [LINK] - Quality standards and verification processes

## MCU Repository Integration

### **Document Classification**

- **Type**: Instruction:Agent MCU
- **Audience**: AI-Agent (primary), Operator (secondary)
- **Purpose**: Behavioral guidance for AI-Agent VIBE_CODING workflow execution
- **Scope**: AI-Agent specific instructions, not Operator-AI-Agent pairs

### **Cross-Reference Structure**

```text
MCU Repository Structure:
  ├── docs/
  │   └── MCU_SPECIFICATION.md
  ├── reference/
  │   └── MCU_REFERENCE_SPECIFICATION.md
  ├── templates/
  │   ├── MCU_REFERENCE_TEMPLATE.md
  │   ├── MCU_INSTRUCTION_TEMPLATE.md
  │   └── MCU_INSTRUCTION-AGENT_TEMPLATE.md
  ├── instruction/
  │   └── instruction-agent/
  │       └── MCU_INSTRUCTION-AGENT_SPECIFICATION.md
  ├── scripts/
  │   ├── validate_mcu.py
  │   ├── check_links.py
  │   └── generate_mcu.py
  └── examples/
      └── example-reference.md
```

### **Integration Points**

- **Inherits from**: [MCU_INSTRUCTION-AGENT_TEMPLATE.md](templates/MCU_INSTRUCTION-AGENT_TEMPLATE.md)
- **Implements**: [INSTRUCTION-AGENT_SPECIFICATION.md](instruction/instruction-agent/MCU_INSTRUCTION-AGENT_SPECIFICATION.md)
- **References**: [MCU_REFERENCE_SPECIFICATION.md](reference/MCU_REFERENCE_SPECIFICATION.md) for MCU principles
- **Governs**: MCU specifications and template development

## Conclusion

The Vibe-Coding Workflow ensures **rapid, high-quality development** with AI assistance while maintaining **consistent standards** across all components. By following this workflow, we achieve:

✅ **Fast iteration** with confidence  
✅ **Quality assurance** through validation  
✅ **Consistent standards** across components  
✅ **Reduced debugging** through early error detection  
✅ **Maintainable code** through proper testing

This workflow scales from individual components to the entire project, providing a foundation for collaborative AI-assisted development.

---

_This document implements the Instruction:Agent Specification and CMI Context Memory Unit principles for optimized AI-Agent behavior and compliance within the MCU project ecosystem._
