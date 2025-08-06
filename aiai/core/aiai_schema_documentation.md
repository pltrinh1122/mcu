# AIAI Schema Documentation
Version: 1.2

## Overview

The AIAI (AI Augmented Installation) schema defines the structure for AI-augmented installation scripts that guide human operators through complex installation processes. The schema enforces both structural correctness and semantic constraints for runtime behavior.

## Core Principles

### Runtime Semantics
- Commands are executed sequentially by the human operator
- Conditionals evaluate previous command outputs to determine execution paths
- Scripts can be atomic (all-or-nothing) with rollback capabilities
- Destructive operations require explicit acknowledgment
- Technical proficiency levels determine verbosity of AI guidance

### Security Semantics
- All commands require human execution (no automated execution)
- Destructive operations must be clearly marked
- Elevated privileges (sudo) should be explicitly noted in intent
- Atomic scripts provide rollback safety for system modifications

## Schema Structure

### Root Object
The AIAI script is defined as a root object with two required properties:

- **metadata**: Script metadata that guides AI behavior and operator expectations
- **body**: Ordered list of commands, conditionals, and scripts to execute

## Metadata Section

### Required Properties

#### `id`
- **Type**: String
- **Pattern**: `^[a-zA-Z0-9_-]+$`
- **Description**: Unique identifier for the AIAI script. Used for cross-referencing and state tracking during execution.
- **Examples**: `install-docker-v1`, `setup-ml-environment`, `configure-btrfs`

#### `intent`
- **Type**: String
- **Minimum Length**: 1
- **Description**: Human-readable description of the script's purpose. Guides AI in providing contextual explanations to the operator.
- **Examples**: 
  - `Install Docker container runtime with GPU support`
  - `Configure BTRFS subvolumes for ML development`
  - `Set up Python environment with CUDA`

#### `technicalProficiency`
- **Type**: String
- **Enum**: `["Beginner", "Intermediate", "Expert"]`
- **Description**: Required technical proficiency level for execution. Determines AI verbosity and explanation depth.
- **Examples**:
  - **Beginner**: Detailed step-by-step explanations with rationale
  - **Intermediate**: Summary of key actions with progress updates
  - **Expert**: Minimal output, only errors or when explicitly asked

### Optional Properties

#### `context`
- **Type**: Object
- **Description**: Optional context information that guides AI behavior and operator preparation

##### `context.designPrinciples`
- **Type**: Array of strings
- **Description**: List of design principles followed by this script. Guides AI in explaining rationale and making decisions.
- **Examples**: `["Minimize system modifications", "Fail fast and safe", "Preserve existing data"]`

##### `context.dependencies`
- **Type**: Array of strings
- **Description**: List of system dependencies required. AI uses this for precondition checking and operator guidance.
- **Examples**: `["apt package manager", "NVIDIA GPU drivers", "Internet connection"]`

##### `context.compatibility`
- **Type**: Array of strings
- **Description**: List of compatible systems or environments. AI validates system compatibility before execution.
- **Examples**: `["Ubuntu 20.04+", "Debian 11+", "NVIDIA GPU required"]`

## Body Section

The body contains an ordered array of execution elements. Execution follows strict sequential order unless modified by conditionals.

### Supported Element Types
- `command`: An atomic operation that the human operator executes
- `conditional`: A control-flow element that evaluates conditions and executes different paths
- `script`: A named collection of commands and conditionals

## Command Element

### Description
An atomic operation that the human operator executes. Commands are the fundamental execution units.

### Required Properties

#### `type`
- **Value**: `"command"`
- **Description**: Type identifier for command elements

#### `id`
- **Type**: String
- **Pattern**: `^[a-zA-Z0-9_-]+$`
- **Description**: Unique identifier for the command. Used for cross-referencing in conditionals and state tracking.
- **Examples**: `update-repos`, `install-package`, `verify-installation`

#### `intent`
- **Type**: String
- **Description**: Human-readable description of the command's purpose. AI uses this to explain what the command does and why it's needed.
- **Examples**: `Update package repositories`, `Install Docker container runtime`, `Verify GPU drivers are working`

#### `shellCommand`
- **Type**: String
- **Description**: The shell command to execute. Must be a valid shell command that the operator can run in their terminal.
- **Examples**: `sudo apt update`, `docker --version`, `nvidia-smi`

### Optional Properties

#### `destructive`
- **Type**: Boolean
- **Default**: `false`
- **Description**: Whether this command modifies the system. AI will provide extra warnings and confirmation prompts for destructive operations.
- **Examples**:
  - `true`: Commands that modify system state (install, remove, configure)
  - `false`: Commands that only read information (check, verify, list)

#### `conditional`
- **Type**: Boolean
- **Default**: `false`
- **Description**: Whether this command's output should be evaluated. AI will capture and analyze the output for conditional branching.
- **Examples**:
  - `true`: Commands whose output determines next steps
  - `false`: Commands that are informational or preparatory

#### `retries`
- **Type**: Integer
- **Minimum**: 0
- **Default**: 0
- **Description**: Number of retry attempts on failure. AI will suggest retries and provide alternative approaches if specified.
- **Examples**: `0`, `3`, `5`

#### `timeout`
- **Type**: Integer
- **Minimum**: 1
- **Default**: 300
- **Description**: Timeout in seconds for command execution. AI will warn operator if command takes longer than expected.
- **Examples**: `60`, `300`, `1800`

#### `args`
- **Type**: Array of strings
- **Description**: Optional command arguments. Used for parameterized commands that need dynamic values.
- **Examples**: `[["--yes", "--force"], ["-y", "package-name"]]`

## Conditional Element

### Description
A control-flow element that evaluates conditions and executes different paths based on results. Enables adaptive installation logic.

### Required Properties

#### `type`
- **Value**: `"conditional"`
- **Description**: Type identifier for conditional elements

#### `id`
- **Type**: String
- **Pattern**: `^[a-zA-Z0-9_-]+$`
- **Description**: Unique identifier for the conditional. Used for state tracking and debugging.
- **Examples**: `check-existing`, `verify-gpu`, `detect-os`

#### `intent`
- **Type**: String
- **Description**: Human-readable description of the conditional's purpose. AI uses this to explain the branching logic to the operator.
- **Examples**: `Check if package already installed`, `Verify GPU drivers are working`, `Detect operating system type`

#### `condition`
- **Type**: Object
- **Description**: Condition evaluation criteria. Defines how to evaluate the source command or script output.

##### `condition.source`
- **Type**: String
- **Description**: ID of command or script to evaluate. Must reference a previous command or script in the execution sequence.
- **Examples**: `check-installed`, `verify-gpu`, `detect-os`

##### `condition.evaluate`
- **Type**: String
- **Enum**: `["success", "failure", "output", "exists"]`
- **Description**: What aspect of the source to evaluate. Determines the evaluation method.
- **Examples**:
  - `success`: Command completed successfully (exit code 0)
  - `failure`: Command failed (non-zero exit code)
  - `output`: Command output content for pattern matching
  - `exists`: File or resource exists on system

##### `condition.value`
- **Type**: String
- **Description**: Optional comparison value for evaluation. Used with 'output' evaluation for pattern matching.
- **Examples**: `ubuntu`, `active`, `nvidia`

##### `condition.operator`
- **Type**: String
- **Enum**: `["equals", "contains", "starts_with", "ends_with", "regex"]`
- **Description**: Optional comparison operator. Defines how to compare the source output with the value.
- **Examples**:
  - `equals`: Exact string match
  - `contains`: Substring search
  - `regex`: Regular expression pattern matching

#### `then`
- **Type**: Array
- **Description**: Elements to execute when condition is true. These commands/scripts run if the condition evaluates to true.
- **Items**: One of `command` or `script`

#### `else`
- **Type**: Array
- **Description**: Elements to execute when condition is false. These commands/scripts run if the condition evaluates to false.
- **Items**: One of `command` or `script`

## Script Element

### Description
A named collection of commands and conditionals. Scripts provide modularity and reusability in installation procedures.

### Required Properties

#### `type`
- **Value**: `"script"`
- **Description**: Type identifier for script elements

#### `scriptType`
- **Type**: String
- **Enum**: `["main", "procedure"]`
- **Description**: Type of script - main can contain procedures, procedures are atomic. Defines the script's role in the hierarchy.
- **Examples**:
  - `main`: Top-level script that orchestrates the installation
  - `procedure`: Reusable component that performs a specific task

#### `id`
- **Type**: String
- **Pattern**: `^[a-zA-Z0-9_-]+$`
- **Description**: Unique identifier for the script. Used for cross-referencing and state tracking.
- **Examples**: `install-docker`, `setup-gpu`, `configure-environment`

#### `intent`
- **Type**: String
- **Description**: Human-readable description of the script's purpose. AI uses this to explain the script's role to the operator.
- **Examples**: `Install Docker container runtime`, `Configure GPU drivers`, `Set up development environment`

#### `body`
- **Type**: Array
- **Description**: Ordered list of commands, conditionals, and nested scripts. Execution follows the order defined in this array.

### Optional Properties

#### `atomic`
- **Type**: Boolean
- **Default**: `false`
- **Description**: Whether this script should be executed atomically with rollback on failure. Provides safety for complex operations.
- **Examples**:
  - `true`: Script that modifies system state and needs rollback capability
  - `false`: Script that only reads information or performs safe operations

### Script Type Constraints

#### Main Scripts (`scriptType: "main"`)
- Can contain any combination of `command`, `conditional`, and `procedure_script` elements
- Serve as top-level orchestrators for installations

#### Procedure Scripts (`scriptType: "procedure"`)
- Can only contain `command` and `conditional` elements
- Provide modular, reusable components
- Are atomic units that perform specific tasks

## Procedure Script Element

### Description
A nested script that can only contain commands and conditionals. Provides modularity without complex nesting.

### Required Properties

#### `type`
- **Value**: `"script"`
- **Description**: Type identifier for procedure script elements

#### `scriptType`
- **Value**: `"procedure"`
- **Description**: Procedure script type - can only contain commands and conditionals

#### `id`
- **Type**: String
- **Pattern**: `^[a-zA-Z0-9_-]+$`
- **Description**: Unique identifier for the procedure script. Used for cross-referencing and state tracking.
- **Examples**: `install-package`, `verify-service`, `configure-service`

#### `intent`
- **Type**: String
- **Description**: Human-readable description of the procedure's purpose. AI uses this to explain the procedure's role.
- **Examples**: `Install specific package`, `Verify service is running`, `Configure service settings`

#### `body`
- **Type**: Array
- **Description**: Ordered list of commands and conditionals only. Procedures are atomic units that perform specific tasks.
- **Items**: One of `command` or `conditional`

### Optional Properties

#### `atomic`
- **Type**: Boolean
- **Default**: `false`
- **Description**: Whether this procedure should be executed atomically with rollback on failure. Provides safety for procedure execution.
- **Examples**:
  - `true`: Procedure that modifies system state
  - `false`: Procedure that only reads information

## Additional Entity Types

### Cleanup Element

#### Description
Scripts designed to reverse or remove installed components post-installation. Provides uninstall and rollback capabilities.

#### Required Properties
- `id`: Unique identifier for the cleanup
- `type`: Must be `"cleanup"`
- `commands`: List of command IDs to execute for cleanup. References commands that perform uninstall operations.
- `atomic`: Whether cleanup should be executed atomically. Ensures cleanup either completes entirely or not at all.

### Notification Element

#### Description
Hooks that alert operators or systems about key installation events. Provides monitoring and alerting capabilities.

#### Required Properties
- `id`: Unique identifier for the notification
- `type`: Must be `"notification"`
- `channel`: Notification channel (e.g., email, slack). Defines how the notification is delivered.
- `messageTemplate`: Template for the notification message. Supports variable substitution for dynamic content.
- `triggers`: List of BR_ID or aiaIC_ID that trigger this notification. Defines when notifications are sent.

### Extension Element

#### Description
Extension points for custom integrations and modular functionality. Enables plugin architecture for installations.

#### Required Properties
- `id`: Unique identifier for the extension
- `type`: Must be `"extension"`
- `hookPoint`: Hook point for the extension (e.g., pre-install, post-install). Defines when the extension is executed.
- `module`: Module or script location for the extension. References the extension implementation.

## Validation Rules

### Structural Validation
- All required properties must be present
- String patterns must match specified regex patterns
- Enum values must be from the allowed set
- Numeric values must meet minimum requirements

### Semantic Validation
- Cross-references must be resolvable (IDs must exist)
- Script type constraints must be enforced
- Conditional source references must be valid
- Body arrays must contain valid element types

### Runtime Validation
- Commands must be executable by the operator
- Destructive operations must be clearly marked
- Atomic scripts must have rollback mechanisms
- Timeouts must be reasonable for the operation type

## Best Practices

### Naming Conventions
- Use kebab-case for IDs (e.g., `install-docker`, `verify-gpu`)
- Make intent descriptions clear and actionable
- Use descriptive names that indicate purpose

### Structure Guidelines
- Keep scripts modular and focused on single tasks
- Use procedures for reusable components
- Mark destructive operations explicitly
- Provide appropriate timeouts and retry values

### Security Considerations
- Always mark destructive operations with `destructive: true`
- Include sudo commands in intent descriptions
- Provide clear explanations for privileged operations
- Use atomic scripts for system modifications

### AI Interaction
- Write clear, descriptive intent strings
- Include context information for better AI guidance
- Specify appropriate technical proficiency levels
- Provide examples and alternatives in descriptions

## Example Usage

```yaml
metadata:
  id: "install-docker-gpu"
  intent: "Install Docker with GPU support for ML development"
  technicalProficiency: "Intermediate"
  context:
    designPrinciples:
      - "Minimize system modifications"
      - "Fail fast and safe"
    dependencies:
      - "apt package manager"
      - "NVIDIA GPU drivers"
    compatibility:
      - "Ubuntu 20.04+"
      - "NVIDIA GPU required"

body:
  - type: "command"
    id: "update-repos"
    intent: "Update package repositories"
    shellCommand: "sudo apt update"
    destructive: false

  - type: "conditional"
    id: "check-docker"
    intent: "Check if Docker is already installed"
    condition:
      source: "check-docker-installed"
      evaluate: "success"
    then:
      - type: "command"
        id: "docker-already-installed"
        shellCommand: "echo 'Docker already installed'"
    else:
      - type: "script"
        scriptType: "procedure"
        id: "install-docker"
        intent: "Install Docker container runtime"
        body:
          - type: "command"
            id: "install-docker-packages"
            shellCommand: "sudo apt install -y docker.io"
            destructive: true

  - type: "command"
    id: "check-docker-installed"
    intent: "Check if Docker is installed"
    shellCommand: "docker --version"
    conditional: true
```

This documentation provides a comprehensive reference for understanding and implementing the AIAI schema, focusing on both structural requirements and semantic behavior. 