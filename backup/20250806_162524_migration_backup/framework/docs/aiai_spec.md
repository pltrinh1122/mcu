# AIAI (AI Augmented Installation) Specification
Version: 1.4

## Table of Contents

1. [Documentation Scope](#documentation-scope)
2. [Overview](#1-overview)
3. [AIAI Package Deployment](#2-aiai-package-deployment)
   - [Package Structure](#21-package-structure)
   - [Package Components](#22-package-components)
   - [Package Deployment Standards](#23-package-deployment-standards)
   - [Package Distribution](#24-package-distribution)
   - [Package Maintenance](#25-package-maintenance)
4. [Problem Analysis](#3-problem-analysis)
5. [Core Concepts](#4-core-concepts)
   - [The Pair Interaction](#41-the-pair-interaction)
   - [Execution Semantics](#42-execution-semantics)
   - [Script Types and Hierarchy](#43-script-types-and-hierarchy)
6. [Interaction Model](#5-interaction-model)
   - [Session Initialization](#51-session-initialization)
   - [Command Execution Flow](#52-command-execution-flow)
   - [Error Handling](#53-error-handling)
7. [Runtime Behavior](#6-runtime-behavior)
   - [Progress Tracking](#61-progress-tracking)
   - [Security Considerations](#62-security-considerations)
   - [Validation Requirements](#63-validation-requirements)
8. [Glossary](#7-glossary)
9. [Version History](#8-version-history)

## Appendices

A. [Schema Reference](#appendix-a-schema-reference)
B. [Best Practices](#appendix-b-best-practices)
C. [Key Design Decisions](#appendix-c-key-design-decisions)
D. [Package Design Guidelines](#appendix-d-package-design-guidelines)

---

## Documentation Scope

This specification contains implementation guidance, runtime behavior patterns, system architecture details, and high-level schema overview. The detailed schema documentation is maintained in separate files: `aiai_schema.json` (machine-readable) and `aiai_schema_documentation.md` (human-readable). Package design guidelines are provided in `../design/docs/PACKAGE_DESIGN_GUIDELINES.md`. This scope separation ensures the specification remains focused on runtime behavior while providing clear references to structural definitions and design guidance.

## 1. Overview

### 1.1 The Problem

Complex software installations and system configurations present significant challenges that current approaches fail to address adequately:

**Core Challenges:**
- **Expertise Gap**: Installation procedures require deep technical knowledge that may not be available
- **Documentation and Automation Decay**: Step-by-step instructions and automated scripts become quickly outdated as software evolves
- **Safety Risks**: Automated scripts can make irreversible changes without human oversight
- **Error Recovery**: Complex failure scenarios require experience-based judgment and intervention

These dynamic challenges create a need for a new approach that combines human expertise with intelligent guidance.

### 1.2 The AIAI Solution

AIAI (AI Augmented Installation) addresses these challenges through a structured and context-laden script-driven approach that combines human expertise with AI guidance:

**Core Approach:**
- **Human-AI Partnership**: Operator maintains control while AI provides intelligent guidance
- **Context-Rich Scripts**: Define installation procedures with embedded intelligence, branching logic, and safety mechanisms
- **Adaptive Execution**: AI adjusts explanations and recovery strategies based on operator proficiency and system state

**Runtime Behavior:**
The AIAI Specification defines the runtime behavior for AI-augmented installations, focusing on the dynamic interaction between Operator and AI Agent during script execution. The static structure is defined in the separate `aiai_schema.json` file.

## 2. AIAI Package Deployment

### 2.1 Package Structure

An AIAI Package is a complete, deployable installation solution that contains all necessary components for AI-augmented installation execution. Each package follows a standardized structure to ensure consistency and maintainability.

**Standard Package Layout:**
```
package-name/
├── MANIFEST                       # Package manifest file (required)
├── docs/
│   └── OPERATOR_GUIDE.md          # Main operator documentation
├── src/
│   └── aiaiScript/
│       ├── main_script.yaml        # Primary installation script
│       ├── validation_script.yaml  # System validation script
│       └── [additional_scripts].yaml
├── aiai_spec.md                   # AIAI Specification (this document)
├── aiai_schema.json               # Machine-readable schema definition
└── README.md                      # Package overview and quick start
```

**MANIFEST File Format:**
The MANIFEST file is a simple text file that lists all required components and their relative paths within the package. The AI Agent uses this file to validate package completeness and locate components.

**Example MANIFEST:**
```
MANIFEST
docs/OPERATOR_GUIDE.md
src/aiaiScript/btrfs_system_validation_aiaiScript.yaml
src/aiaiScript/btrfs_root_aiaiScript.yaml
src/aiaiScript/btrfs_system_subvolume_creation_aiaiScript.yaml
src/aiaiScript/btrfs_mount_configuration_aiaiScript.yaml
src/aiaiScript/btrfs_boot_configuration_aiaiScript.yaml
src/aiaiScript/btrfs_ml_aiaiScript.yaml
src/aiaiScript/btrfs_data_aiaiScript.yaml
src/aiaiScript/btrfs_data_migration_aiaiScript.yaml
src/aiaiScript/btrfs_pre_reboot_validation_aiaiScript.yaml
src/aiaiScript/btrfs_post_installation_validation_aiaiScript.yaml
src/aiaiScript/docker_aiaiScript.yaml
aiai_spec.md
aiai_schema.json
README.md
```

### 2.2 Package Components

#### 2.2.1 Operator Guide (`docs/OPERATOR_GUIDE.md`)

**Purpose**: Primary documentation for human operators executing the installation.

**Required Content**:
- **Installation Overview**: High-level description of what the installation accomplishes
- **Prerequisites**: System requirements, hardware specifications, and pre-installation setup
- **Quick Start Guide**: Step-by-step instructions for experienced operators
- **Detailed Procedures**: Comprehensive walkthrough for each installation phase
- **Troubleshooting Section**: Common issues, error resolution, and recovery procedures
- **Validation Procedures**: How to verify successful installation completion
- **Post-Installation Configuration**: Additional setup and optimization steps

**Documentation Standards**:
- Use clear, non-technical language for critical safety information
- Include code blocks for all commands with proper syntax highlighting
- Provide context for each step explaining why it's necessary
- Include warnings for destructive operations and system modifications
- Reference specific aiaiScript files for automated execution paths

#### 2.2.2 AIAI Scripts (`src/aiaiScript/*.yaml`)

**Purpose**: Machine-readable installation procedures that define the complete execution flow.

**Required Scripts**:
- **Main Installation Script**: Primary orchestration script that coordinates the entire installation
- **System Validation Script**: Pre-installation validation of system requirements and state
- **Component Scripts**: Individual scripts for specific installation phases or components
- **Recovery Scripts**: Rollback and error recovery procedures

**Script Standards**:
- Follow AIAI Schema specification for structure and validation
- Include comprehensive metadata with clear intent descriptions
- Implement proper error handling and rollback mechanisms
- Use atomic scripts for critical operations that modify system state
- Include validation commands to verify pre/post conditions

#### 2.2.3 AIAI Specification (`aiai_spec.md`)

**Purpose**: Defines the runtime behavior and interaction patterns for AI-augmented installations.

**Content Requirements**:
- Complete specification of AI-Operator interaction model
- Execution semantics and flow control mechanisms
- Error handling and recovery procedures
- Security considerations and validation requirements
- Progress tracking and state management
- Schema reference and best practices

**Deployment Requirements**:
- Must be included in every AIAI Package
- Provides the foundation for AI Agent behavior during execution
- Defines the contract between Operator and AI Agent
- Establishes safety mechanisms and validation procedures

#### 2.2.4 AIAI Schema (`aiai_schema.json`)

**Purpose**: Machine-readable schema definition for validating AIAI Script structure.

**Schema Requirements**:
- Complete JSON Schema specification for all AIAI Script elements
- Validation rules for script structure and content
- Property definitions and constraints for all elements
- Error messages and validation guidance
- Extensibility mechanisms for future enhancements

**Deployment Requirements**:
- Must be included in every AIAI Package
- Used by AI Agents for script validation and parsing
- Provides structural foundation for all AIAI Scripts
- Enables automated validation and error detection

### 2.3 Package Deployment Standards

#### 2.3.1 File Naming Conventions

**Operator Guides**: Use descriptive names with installation target
- Example: `UBUNTU_BTRFS_INSTALLER.md`, `DOCKER_ML_ENVIRONMENT.md`

**AIAI Scripts**: Use descriptive names with script purpose
- Example: `btrfs_system_validation_aiaiScript.yaml`, `docker_installation_aiaiScript.yaml`

**Schema Files**: Use standardized names for consistency
- `aiai_spec.md` - AIAI Specification
- `aiai_schema.json` - Machine-readable schema
- `aiai_schema_documentation.md` - Human-readable schema documentation

#### 2.3.2 Directory Structure Standards

**Required Directories**:
- `docs/` - All operator documentation and guides
- `src/aiaiScript/` - All AIAI Script files
- Root level - Specification and schema files

**Optional Directories**:
- `examples/` - Example scripts and usage demonstrations
- `tests/` - Validation and testing scripts
- `templates/` - Template scripts for common patterns

#### 2.3.3 Package Validation

**Pre-Deployment Checks**:
- MANIFEST file must exist and list all package components
- All files listed in MANIFEST must exist in the package
- All AIAI Scripts must validate against `aiai_schema.json`
- All script references must be resolvable within the package
- All documentation must reference valid script files
- All destructive operations must be clearly marked
- All atomic scripts must have proper rollback mechanisms

**Package Completeness**:
- Must contain MANIFEST file with complete component listing
- Must contain all required components (Guide, Scripts, Spec, Schema)
- Must provide complete installation coverage
- Must include appropriate error handling and recovery procedures
- Must document all prerequisites and system requirements

### 2.4 Package Distribution

#### 2.4.1 Version Management

**Versioning Strategy**:
- Use semantic versioning for package releases
- Track changes across all components (Guide, Scripts, Spec, Schema)
- Maintain backward compatibility within major versions
- Document breaking changes and migration procedures

**Release Process**:
- Validate all components before release
- Test complete installation procedures
- Update documentation to reflect any changes
- Provide migration guidance for existing installations

#### 2.4.2 Distribution Formats

**Source Distribution**:
- Complete package as directory structure
- All files in human-readable formats
- Version control friendly structure
- Easy to modify and customize

**Packaged Distribution**:
- Compressed archive with complete package
- Self-contained with all dependencies
- Includes validation and installation scripts
- Ready for immediate deployment

### 2.5 Package Maintenance

#### 2.5.1 Update Procedures

**Component Updates**:
- Update scripts to reflect software version changes
- Revise documentation for new features or procedures
- Validate schema compatibility for new script features
- Test complete installation procedures after updates

**Backward Compatibility**:
- Maintain compatibility with existing installations
- Provide migration paths for breaking changes
- Document deprecation timelines for removed features
- Support multiple versions during transition periods

#### 2.5.2 Quality Assurance

**Validation Requirements**:
- All scripts must pass schema validation
- All documentation must be current and accurate
- All examples must be tested and verified
- All error handling must be comprehensive

**Testing Procedures**:
- Test complete installation procedures
- Verify error recovery and rollback mechanisms
- Validate operator guide accuracy
- Test AI Agent interaction patterns

## 3. Problem Analysis

### 3.1 Installation Complexity Challenges

**Multi-Domain Expertise Requirements:**
- Modern software installations span multiple technical domains (networking, security, databases, etc.)
- Each domain has its own terminology, best practices, and failure modes
- Cross-domain dependencies create complex interaction patterns
- Domain-specific knowledge becomes outdated rapidly as technologies evolve

**State-Dependent Decision Making:**
- Installation steps depend on current system state (OS version, existing software, hardware capabilities)
- Conditional logic becomes complex and difficult to document
- Error conditions require context-aware recovery strategies
- System state changes during installation affect subsequent steps

**Documentation Maintenance Burden:**
- Installation procedures become outdated as software versions change
- Manual documentation is error-prone and difficult to verify
- Automated scripts become brittle and fail silently
- Different environments require different installation approaches

### 3.2 Human Expertise Limitations

**Knowledge Gap Challenges:**
- Installation procedures require deep technical knowledge that may not be available
- Error recovery and troubleshooting require experience-based judgment
- Complex branching logic is difficult to follow and understand
- Different skill levels need different levels of explanation and guidance

**Cognitive Load Issues:**
- Long installation procedures create mental fatigue and error-prone execution
- Complex state tracking across multiple steps is mentally demanding
- Error conditions require rapid decision-making under pressure
- Progress tracking and rollback planning add cognitive overhead

### 3.3 Safety and Reliability Issues

**Automation Risks:**
- Automated scripts can make irreversible changes without human oversight
- Silent failures in automation can leave systems in inconsistent states
- Rollback mechanisms are often incomplete or non-existent
- System state validation is difficult to implement and maintain

**Human Error Factors:**
- Manual procedures are error-prone and difficult to verify
- Copy-paste errors in command execution are common
- Skipping steps or executing out of order creates inconsistent states
- Lack of validation leads to incomplete or failed installations

## 4. Solution Architecture

### 4.1 Context-Rich Scripts (AIAI Script)

**Core Innovation:**
AIAI Scripts combine structured execution with embedded intelligence, creating context-aware installation procedures that adapt to system state and operator needs.

**Script Components:**
- **aiaIS (AI Augmented Installation Script)**: Named sequences of commands and conditionals with embedded context and adaptive behavior
- **aiaIC (AI Augmented Installation Command)**: Individual atomic operations with context awareness and safety mechanisms
- **BR (Branch Entity)**: Control-flow elements that enable intelligent conditional execution based on system state

**Nested Relationship Hierarchy:**
```
aiaIS (Main Script)
├── aiaIC (Commands)
├── Conditional (BR elements)
│   ├── then: aiaIC or nested aiaIS:
    └── Conditional (BR elements only)
```

**Key Constraints:**
- **Main Scripts** can contain commands, conditionals, and procedure scripts
- **Procedure Scripts** can only contain commands and conditionals (no nested scripts)
- **Commands** are atomic and cannot contain other elements
- **Conditionals** provide branching logic but cannot contain other conditionals directly

**Context-Rich Features:**
- **Embedded Intelligence**: Scripts contain context about system state, operator proficiency, and installation goals
- **Adaptive Behavior**: Execution adapts based on current conditions and operator needs
- **Safety Mechanisms**: Built-in validation, rollback capabilities, and destructive operation warnings
- **State Awareness**: Scripts understand and respond to system state changes

### 4.2 Human-AI Partnership Model

**Core Partnership:**
Each **Installation** is experienced by a **Pair User** (Human Operator and AI Agent working together):

**Human Operator:**
- **Maintains Control**: All critical decisions and command execution remain with the operator
- **Provides Judgment**: Makes decisions based on context, experience, and system state
- **Executes Commands**: Runs the actual installation commands with AI guidance
- **Manages Risk**: Decides when to proceed, pause, or rollback based on AI suggestions

**AI Agent:**
- **Provides Context**: Explains what each command does and why it's needed
- **Offers Guidance**: Suggests next steps, alternatives, and error recovery strategies
- **Adapts Communication**: Adjusts explanation depth based on operator proficiency
- **Monitors State**: Tracks system changes and validates pre/post conditions

**Partnership Benefits:**
- **Human Judgment + AI Intelligence**: Combines human decision-making with AI analysis
- **Safety + Efficiency**: Maintains safety through human oversight while improving efficiency through AI guidance
- **Shared Context**: Both parties understand current state, goals, and constraints
- **Adaptive Interaction**: Communication style adapts to operator needs and system state

### 4.3 Execution Environment (Agentic AI)

**Core Enabler:**
The execution environment provides the intelligent interface that makes the Human-AI partnership possible through agentic AI capabilities.

**Environment Features:**
- **Natural Language Interface**: Chat-based interaction for intuitive human-AI communication
- **Context Management**: Maintains state, history, and shared understanding across sessions
- **Adaptive Interface**: Adjusts verbosity, guidance level, and interaction style based on operator proficiency
- **Intelligent Assistance**: Provides contextual help, error recovery, and progress tracking

**Agentic AI Capabilities:**
- **Context Awareness**: Understands current installation state, operator proficiency, and system conditions
- **Intelligent Guidance**: Provides explanations, suggestions, and alternatives based on context
- **Error Recovery**: Analyzes failures and suggests context-aware recovery strategies
- **Progress Tracking**: Maintains session state and milestone management for complex installations

**Key Innovations:**
- **Context-Rich Scripts**: Scripts with embedded intelligence and adaptive behavior
- **Human-AI Partnership**: Human control with AI guidance, not pure automation
- **Agentic AI Environment**: Intelligent interface that enables the partnership

## 5. Implementation Details

### 5.1 Execution Semantics

#### 5.1.1 Execution Flow Control

**Intra-Script Flow (Commands):**
- Within any individual script, execution always proceeds linearly from one Command `[aiaIC]` to the next
- Commands follow the natural YAML array order
- This linear flow is only modified by internal `BR` elements

**Inter-Script Flow (BR Paths):**
- Each `BR` path contains an array of aiaIS references that define the complete execution sequence
- Scripts in the array are executed in order until completion or failure
- Upon completion of all scripts in a path, control returns to the parent context
- The parent context then evaluates the next element in sequence

**Example: Array-Based aiaIS Sequencing**
```yaml
conditional:
  id: "check-docker"
  condition:
    source: "docker-check"
    evaluate: "success"
  then:
    - ["install-docker", "configure-docker", "verify-docker"]  # Complete path as array
  else:
    - ["skip-docker", "continue-setup"]  # Alternative path as array
```

#### 5.1.2 Atomicity and Rollback
- If the target script is marked `atomic: true` and fails, rollback rules of that script apply before control returns to the parent context
- Rollback mechanisms are script-specific and must be defined in the script metadata
- Atomic scripts ensure system consistency by either completing entirely or rolling back completely

#### 5.1.3 No Inline Commands
- Commands **MUST NOT** appear directly inside `paths`
- Wrap any command sequence that needs conditional execution inside a dedicated script entity and reference that script in `paths`





### 5.2 Complete AIAI Package Execution Process

#### 5.2.1 Package Loading and Validation

**Operator Instructions:**
To initiate an AIAI Package installation session, provide the following prompt to your AI Agent:

```
Assume the role of the AI Agent and execute the installation package located at [PACKAGE_PATH]. Load the package, validate its structure, and execute the installation following the AIAI Specification. Execute shell commands directly with my permission and capture all console output (stdout and stderr) to [PACKAGE_NAME]_installation.txt in the current directory.
```

**Required Actions:**
1. Replace `[PACKAGE_PATH]` with the filesystem path to the AIAI Package directory
2. Replace `[PACKAGE_NAME]` with the package name for output file naming
3. The AI Agent will automatically load and validate the package structure
4. All commands will be executed with operator permission and oversight
5. The AI Agent MUST create the output file `[PACKAGE_NAME]_installation.txt` in the current directory and capture ALL console output (stdout and stderr) from every command execution
6. If the output file doesn't exist after package completion, the AI Agent MUST create it with the complete execution log

**Package Loading Phase:**
1. **Load MANIFEST**: Parse the MANIFEST file to identify all required components
2. **Validate Structure**: Verify all listed files exist in the package directory
3. **Load Specification**: Parse `aiai_spec.md` to understand runtime behavior
4. **Load Schema**: Parse `aiai_schema.json` for script validation
5. **Load Scripts**: Load all AIAI Script files listed in the MANIFEST
6. **Validate Scripts**: Validate all scripts against the AIAI Schema
7. **Abort on Error**: If any validation fails, abort installation and inform operator

**Package Validation Requirements:**
- MANIFEST file must exist and be readable
- All files listed in MANIFEST must exist in the package
- AIAI Specification (`aiai_spec.md`) must be present and valid
- AIAI Schema (`aiai_schema.json`) must be present and valid
- All AIAI Scripts must validate against the schema
- Operator Guide (`docs/OPERATOR_GUIDE.md`) must be present

**Error Handling:**
- If MANIFEST is missing or unreadable → Abort installation
- If any required file is missing → Abort installation
- If any AIAI Script fails schema validation → Abort installation
- If package structure is invalid → Abort installation
- No recovery attempts - leave troubleshooting to the Pair

**Technical Proficiency Adaptation:**
- **Beginner**: Detailed explanations, step-by-step guidance, extra warnings, context for each step
- **Intermediate**: Summarized actions, non-obvious concepts, standard warnings, step relationships
- **Expert**: AI prompts operator for self-assessment and adjusts accordingly
  - **Operator Self-Assessment**: AI prompts for comfort level with target system, familiarity with specific technologies, and preferred interaction verbosity
  - **Dynamic Adaptation**: AI adjusts communication style based on operator's actual needs rather than script assumptions
  - **Respects Operator Autonomy**: Operator can override script's proficiency assumptions with their actual skill level

#### 5.2.2 Session Initialization

**Setup Phase:**
1. **Confirm Package Loaded**: Verify all package components loaded successfully
2. **Identify Main Script**: Determine the primary installation script from the package
3. **Establish Proficiency**: Determine technical proficiency level from script metadata
4. **Operator Assessment**: If proficiency is "Expert", prompt operator for self-assessment
   - Comfort level with target system (Beginner/Intermediate/Expert)
   - Familiarity with specific technologies mentioned in script
   - Preferred interaction verbosity (Minimal/Standard/Detailed)
5. **Confirm Readiness**: Verify terminal access and operator readiness
6. **Initialize State**: Set up execution state tracking and milestone management
7. **Begin Execution**: Start with the main installation script

**Main Script Identification:**
- Look for scripts with names containing "main", "primary", or "installation"
- If multiple candidates, prefer the one with the most comprehensive scope
- If no clear main script, ask operator to specify which script to execute first

#### 5.2.3 Main Execution Loop

**Output File Management:**
- **File Creation**: AI Agent MUST create `[SCRIPT_NAME].txt` at session start
- **Real-time Capture**: All command outputs MUST be captured to the output file
- **Fallback Creation**: If output file doesn't exist after script completion, AI Agent MUST create it with complete execution log
- **File Location**: Output file MUST be created in the current working directory
- **Content Format**: Output file MUST contain timestamp, command, result, and full console output for each step

**For Each Element in Script Body:**

**Step 1: Parse Element**
- **Identify Type**: Determine if element is command, conditional, script, or validation
- **Load Properties**: Extract all relevant properties (id, intent, shellCommand, etc.)
- **Validate References**: Ensure all cross-references are resolvable
- **Check Dependencies**: Verify any required dependencies are available

**Step 2: Prepare and Explain**
- **Assess Requirements**: Check system state and resource availability
- **Explain Context**: Provide explanation appropriate to operator proficiency level
- **Highlight Risks**: Warn about destructive operations or potential issues
- **Set Expectations**: Explain what will happen and expected outcomes

**Step 3: Generate and Present**
- **Generate Command**: Create the shell command or validation command
- **Present to Operator**: Show the command with appropriate context
- **Confirm Understanding**: Ensure operator understands what will be executed
- **Handle Special Cases**: Address sudo requirements, destructive operations, timeouts

**Step 4: Execute and Capture**
- **Wait for Execution**: Let operator run the command
- **Capture Output**: Retain stdout, stderr, and exit code
- **Monitor Progress**: Track execution time and provide feedback
- **Handle Interruptions**: Manage operator questions or interruptions

**Step 5: Validate Results**
- **Check Exit Code**: Verify command completed successfully (0 = success)
- **Analyze Output**: Compare output against expected patterns
- **Validate State**: Confirm system state changed as expected
- **Handle Failures**: If validation fails, proceed to error handling

**Step 6: Progress and Update**
- **Update State**: Record successful execution and new system state
- **Log Progress**: Maintain execution history and milestone tracking
- **Capture Output**: Append command output to `[SCRIPT_NAME].txt` file
- **Determine Next**: Identify next element or handle completion
- **Provide Feedback**: Give operator progress update and next step preview

**Step 7: Output File Verification**
- **Check File Exists**: Verify `[SCRIPT_NAME].txt` exists and is writable
- **Append Results**: Add current command results to output file
- **Handle Failures**: If file creation fails, notify operator and continue
- **Final Verification**: Ensure output file contains complete execution log

#### 5.2.4 Element-Specific Handling

**Command Elements:**
- **Execute**: Present shellCommand to operator for execution
- **Validate**: Check exit code and any conditional output evaluation
- **Handle Timeout**: Monitor execution time against timeout setting
- **Manage Retries**: Implement retry logic if specified

**Validation Elements:**
- **Execute**: Run validation command and capture output
- **Pattern Match**: Compare output against expected_output using specified matching
- **Handle Failure**: Take action based on on_fail setting (abort/retry/skip/branch)
- **Manage Critical**: Treat critical validations as mandatory, non-critical as optional

**Conditional Elements:**
- **Evaluate Condition**: Check source command/script output against criteria
- **Determine Path**: Choose then or else path based on evaluation
- **Execute Branch**: Process elements in the selected path
- **Return Control**: Resume main execution after branch completion

**Script Elements:**
- **Load Nested Script**: Parse the referenced script
- **Execute Recursively**: Apply main execution loop to nested script
- **Handle Atomic**: If atomic=true, implement rollback on failure
- **Return Results**: Pass success/failure status back to parent

#### 5.2.5 Error Handling (Integrated)

**When Any Step Fails:**

**Immediate Analysis:**
- **Analyze Exit Code**: Determine failure type from exit code
- **Parse Error Messages**: Extract key information from stderr
- **Assess Impact**: Determine if failure is critical or recoverable
- **Identify Root Cause**: Find underlying issue (permissions, dependencies, etc.)

**Recovery Decision:**
- **Retry Same**: If appropriate, retry with same parameters
- **Retry Modified**: If appropriate, retry with adjusted parameters
- **Alternative Approach**: Suggest different command or method
- **Manual Intervention**: Guide operator through manual resolution
- **Skip and Continue**: If non-critical, skip and continue
- **Abort Installation**: If critical and unrecoverable, stop execution

**Communication:**
- **Explain Problem**: Provide clear, non-technical description
- **Present Options**: Show recovery options with pros/cons
- **Guide Decision**: Help operator choose best recovery approach
- **Track Progress**: Monitor recovery attempts and outcomes

#### 5.2.6 State Management

**Execution State:**
- **Current Position**: Track script ID, command ID, and step number
- **Execution History**: Maintain log of completed commands with timestamps
- **Success/Failure Status**: Record outcome of each element
- **Branching Decisions**: Log which conditional paths were taken

**Session State:**
- **Chat Context**: Maintain conversation history and operator preferences
- **System State**: Track relevant system information and changes
- **Milestone Points**: Save state at logical checkpoints
- **Resume Capability**: Enable resuming from any saved milestone

**Cross-Reference Management:**
- **Script References**: Validate all script references in BR paths
- **Command References**: Ensure all command references in conditionals exist
- **Dependency Tracking**: Track dependencies between elements
- **Reference Validation**: Verify references at runtime before execution

### 5.3 Runtime Behavior

#### 5.3.1 Progress Tracking

#### 5.3.1.1 State Management
- Track current script and command IDs.
- Record each element's success/failure.
- Log operator decisions for branching history.

**Execution State Tracking:**
- **Current Position**: Track current script ID, command ID, and step number
- **Execution History**: Maintain log of completed commands with timestamps
- **Success/Failure Status**: Record outcome of each command and script
- **Branching Decisions**: Log which conditional paths were taken and why
- **Operator Choices**: Record operator decisions and manual interventions
- **Error History**: Track errors encountered and recovery actions taken

**Session Persistence:**
- **Chat State**: Maintain conversation context and operator preferences
- **Script State**: Track current position in script execution
- **System State**: Record relevant system information and changes
- **Milestone Points**: Save state at logical checkpoints for resumption
- **Resume Capability**: Enable resuming from any saved milestone

**Cross-Reference Resolution:**
- **Script References**: Validate all script references in BR paths are resolvable
- **Command References**: Ensure all command references in conditionals exist
- **Dependency Tracking**: Track dependencies between scripts and commands
- **Reference Validation**: Verify references at runtime before execution
- **Missing Reference Handling**: Provide guidance when references are missing or invalid

#### 5.3.1.2 Milestones
- Prompt operator to save chat at script boundaries.
- Maintain separate installation logs.
- Support resuming via saved state files.

#### 5.3.2 Security Considerations

#### 5.3.2.1 Command Execution
- All commands require explicit operator initiation.
- No direct AI-driven execution.
- Elevated privilege commands (`sudo`) explicitly noted.

#### 5.3.2.2 Destructive Operations
- Mark destructive operations clearly.
- Offer dry-run options.
- Validate pre-execution for critical actions.
- Provide extra warnings and confirmation prompts.

#### 5.3.3 Validation Requirements

#### 5.3.3.1 Execution-Time Validation
AIAI implementations MUST perform runtime validation beyond schema validation:

- **Pre-Execution Validation**: Verify system state before command execution
- **Post-Execution Validation**: Confirm expected outcomes after command execution
- **Cross-Reference Resolution**: Ensure all script and command references are resolvable at runtime
- **Security Compliance**: Validate privilege requirements and destructive operation warnings

#### 5.3.3.2 State Consistency
- **Atomicity Enforcement**: Ensure atomic scripts maintain system consistency
- **Rollback Integrity**: Verify rollback mechanisms preserve system state
- **Progress Persistence**: Maintain execution state across sessions

## 6. Glossary

### Core Terms

**Operator**: The human user who interacts with the AI Agent during installation execution.

**Agent**: The AI system that interprets scripts and guides the Operator through execution.

**Session**: A complete interaction between Operator and Agent for a single installation.

**Atomicity**: The property that ensures a script either completes entirely or rolls back completely.

**Rollback**: The process of reversing changes made by a failed atomic script.

**Milestone**: A checkpoint in execution where the Operator is prompted to save progress.

**Validation**: A dedicated step that checks system state or command outputs against expected patterns.

**Validation Command**: A special command type that executes validation logic and handles failure behavior.

**Dry-Run**: A simulation mode that shows what would happen without making actual changes.

### Schema Terms

**aiaIS**: AI Augmented Installation Script - a named sequence of commands and conditionals.

**aiaIC**: AI Augmented Installation Command - an individual, atomic operation.

**BR**: Branch Entity - control-flow elements to transition between scripts.

**Main Script**: Top-level script that orchestrates installations and can contain procedures.

**Procedure Script**: Atomic, reusable component that can only contain commands and conditionals.

**Technical Proficiency**: Expected operator skill level. For Expert scripts, AI prompts operator for self-assessment to determine actual guidance needs.

## 7. Version History

| Version | Date       | Changes                                                                               |
| ------- | ---------- | ------------------------------------------------------------------------------------- |
| 1.4     | 2025-08-05 | Enhanced technical proficiency behavior for Expert scripts. AI now prompts operators for self-assessment of comfort level, familiarity with target technologies, and preferred interaction verbosity. This enables dynamic adaptation based on actual operator needs rather than script assumptions. |
| 1.3     | 2025-08-05 | Added comprehensive AIAI Package Deployment section defining package structure with MANIFEST-based validation, components, deployment standards, distribution, and maintenance procedures. Updated execution process to support complete package loading and validation. |
| 1.2     | 2025-08-05 | Reorganized specification with cleaner separation of runtime behavior and schema documentation. Consolidated redundant sections and improved navigation. |
| 1.1     | 2025-08-04 | Revised BR entity to restrict `paths` to other scripts and enforce inter-script flow. |
| 1.0     | 2025-06-07 | Initial specification                                                                 |

---

## Appendix A: Schema Reference

### A.1 Quick Reference

The AIAI schema defines the structure for AI-augmented installation scripts written in YAML format.

#### A.1.1 Root Structure
```yaml
metadata:
  id: "script-identifier"
  intent: "Human-readable description"
  technicalProficiency: "Beginner|Intermediate|Expert"
  context: # Optional context information
body:
  # Ordered list of commands, conditionals, and scripts
```

#### A.1.2 Element Types
- **Command**: Atomic operation executed by the operator
- **Conditional**: Control-flow element with branching logic
- **Script**: Named collection of commands and conditionals

#### A.1.3 Key Properties
- **`id`**: Unique identifier (alphanumeric, hyphens, underscores)
- **`intent`**: Human-readable description of purpose
- **`destructive`**: Whether command modifies system (boolean)
- **`atomic`**: Whether script should rollback on failure (boolean)
- **`scriptType`**: "main" or "procedure" for scripts

#### A.1.4 Technical Proficiency Levels
| Level        | Verbosity | Behavior                                |
| ------------ | --------- | --------------------------------------- |
| Beginner     | Verbose   | Explains rationale and steps in detail. |
| Intermediate | Normal    | Summarizes key actions and progress.    |
| Expert       | Silent    | Only reports errors or when asked.      |

**Usage:**
- **Beginner**: Detailed step-by-step explanations with rationale
- **Intermediate**: Summary of key actions and progress updates  
- **Expert**: Minimal output, only errors or when explicitly asked

### A.2 Detailed Schema

For complete schema documentation including:
- Detailed property descriptions and examples
- Validation rules and constraints
- Complete schema structure
- Usage examples

See: `aiai_schema_documentation.md`

For machine-readable JSON Schema for validation:
See: `aiai_schema.json`

---

## Appendix B: Best Practices

### B.1 Error Recovery

- **Graceful Degradation**: Provide alternative execution paths on failure
- **State Restoration**: Ensure system can be restored to known good state
- **User Guidance**: Provide clear next steps when errors occur

### B.2 Performance Optimization

- **Parallel Execution**: Where safe, execute independent commands concurrently
- **Resource Management**: Monitor and manage system resources during execution
- **Timeout Handling**: Implement appropriate timeouts for long-running operations

### B.3 Security Best Practices

- **Explicit Permissions**: Clearly mark commands requiring elevated privileges
- **Dry-Run Options**: Provide simulation modes for destructive operations
- **Validation**: Always validate system state before execution using validation commands
- **Rollback Planning**: Ensure atomic scripts have proper rollback mechanisms

---

## Appendix D: Package Design Guidelines

For comprehensive guidelines on designing AIAI Packages, including Script vs. Phase relationships, phase boundaries, and package design patterns, see: `../design/docs/PACKAGE_DESIGN_GUIDELINES.md`

This document provides:
- Core design principles for Scripts vs. Phases
- Guidelines for script granularity and phase composition
- Common phase boundary patterns and rationale
- Package design patterns and implementation examples
- Quality assurance and best practices for package design

---

## Appendix C: Key Design Decisions

### C.1 Script Body vs. BR Path Structure

AIAI uses two distinct structural approaches based on the content and execution requirements:

**Script Body: Mixed Content with Intrinsic Sequence**
- Contains commands, conditionals, and nested scripts
- Preserves natural YAML array order for mixed content execution
- Requires complex validation for different element types
- Supports direct execution with context switching between types

**BR Path: Script Orchestration with Array Sequencing**
- Contains only script references in arrays
- Uses array order for script execution sequence
- Requires simple validation for script references
- Supports delegation to script execution engines

**Rationale:**
- **Different Abstraction Levels**: Script body handles low-level execution, BR paths handle high-level orchestration
- **Different Execution Semantics**: Script body executes directly, BR paths delegate to other scripts
- **Different Validation Needs**: Script body validates mixed types, BR paths validate script references
- **Preserved Intrinsic Sequence**: Script body maintains natural YAML order for mixed content

**Example:**
```yaml
# Script body - mixed content with intrinsic sequence
body:
  - type: "command"          # Direct execution
    id: "update-repos"
    shellCommand: "sudo apt update"
  - type: "conditional"      # Branching logic
    id: "check-docker"
    then:
      - ["install-docker", "configure-docker"]  # BR path array
    else:
      - ["skip-docker"]
  - type: "script"           # Nested script
    id: "verify-installation"

# BR path - script orchestration only
conditional:
  then:
    - ["install-docker", "configure-docker", "verify-docker"]  # Array of scripts
  else:
    - ["skip-docker", "continue-setup"]
```

This design decision ensures appropriate abstraction levels, execution efficiency, and validation complexity for each use case.

### C.2 Implicit aiaIC Sequencing vs. Linked-List Approach

AIAI uses implicit YAML array order for aiaIC sequencing rather than explicit linked-list references.

**Implicit aiaIC Sequencing:**
- Commands within a script follow the natural array order of the YAML file
- No explicit `next` references are required between commands
- Execution proceeds linearly from one command to the next in array order
- Natural YAML structure provides the necessary sequencing

**Alternative Linked-List Approach:**
```yaml
# Not used - for comparison only
body:
  - type: "command"
    id: "update-repos"
    shellCommand: "sudo apt update"
    next: "install-package"
  - type: "command"
    id: "install-package"
    shellCommand: "sudo apt install docker"
    next: "verify-installation"
  - type: "command"
    id: "verify-installation"
    shellCommand: "docker --version"
    next: null
```

**Why Implicit Sequencing Was Chosen:**

1. **Simplicity and Reliability**
   - No risk of broken `next` references or circular dependencies
   - No complex validation rules for chain integrity
   - Natural YAML array order is intuitive and reliable

2. **Maintainability**
   - Easy to add, remove, or reorder commands without updating references
   - No need to track and update multiple `next` pointers
   - Simple insertion and deletion operations

3. **Human Readability**
   - Execution flow is immediately obvious from YAML structure
   - No need to trace through `next` references to understand sequence
   - Natural for both humans and AI to understand

4. **Performance**
   - No runtime overhead for following `next` references
   - Direct array iteration is more efficient
   - Simpler state management during execution

5. **Error Handling**
   - No risk of infinite loops from circular references
   - Simpler error recovery when commands fail
   - Clear execution boundaries

**Example of Current Approach:**
```yaml
body:
  - type: "command"
    id: "update-repos"
    shellCommand: "sudo apt update"
  - type: "command"
    id: "install-package"
    shellCommand: "sudo apt install docker"
  - type: "command"
    id: "verify-installation"
    shellCommand: "docker --version"
```

**Trade-offs Considered:**

**Advantages of Implicit Sequencing:**
- **Simplicity**: Leverages YAML's natural array ordering
- **Reliability**: No risk of broken references or cycles
- **Maintainability**: Easy to modify command sequences
- **Performance**: Direct array iteration without reference overhead
- **Readability**: Clear execution flow from YAML structure

**Disadvantages of Implicit Sequencing:**
- **Limited Flexibility**: Cannot support complex branching within command sequences
- **No Dynamic Routing**: Cannot change next command based on runtime conditions
- **Fixed Order**: Commands must execute in array order

**When Linked-List Might Be Beneficial:**
- Complex branching logic within command sequences
- Dynamic command routing based on runtime state
- Parallel execution paths
- Plugin-based command insertion

**Why BR Paths Use Array Sequencing (Different from aiaIC):**

While aiaIC uses implicit sequencing, BR paths use explicit array sequencing for script orchestration. This difference reflects the distinct requirements of each use case:

**BR Path Requirements:**
- **Script Orchestration**: BR paths orchestrate high-level script execution
- **Complex Branching**: Multiple execution paths with different script sequences
- **Delegation Model**: BR paths delegate execution to other scripts
- **Orchestration Logic**: Need to define complete execution paths upfront

**aiaIC Requirements:**
- **Direct Execution**: Commands execute directly within script context
- **Linear Flow**: Simple sequential execution is the common case
- **Mixed Content**: Commands are mixed with conditionals and nested scripts
- **Intrinsic Sequence**: Natural YAML order provides necessary sequencing

**Reference to BR Design Decision:**
For detailed explanation of BR path array sequencing, see section 2.2.2 "Inter-Script Flow Control" which documents the design decision for array-based aiaIS sequencing in BR paths.

**Unified Design Philosophy:**
Both approaches leverage YAML's strengths while serving different purposes:
- **aiaIC**: Implicit array order for simple, linear command execution
- **BR Paths**: Explicit array sequences for complex script orchestration

**Conclusion:**
For AIAI's use case, this hybrid approach provides the optimal balance of simplicity for common cases (aiaIC) with flexibility for complex orchestration (BR paths). The different sequencing approaches reflect the different abstraction levels and execution requirements of each entity type.

