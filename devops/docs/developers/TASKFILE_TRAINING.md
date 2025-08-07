# Training Materials - Taskfile-Based Configuration Management

## Overview

This document provides structured training materials for the development team to learn and effectively use the new Taskfile-based configuration management system. The training is designed to be self-paced with practical exercises and real-world scenarios.

## Training Objectives

By the end of this training, participants will be able to:
1. **Understand the system architecture** and component relationships
2. **Use wrapper scripts effectively** for common development tasks
3. **Navigate the task namespace system** and find appropriate tasks
4. **Create and customize component environments** for new projects
5. **Troubleshoot common issues** and understand error messages
6. **Follow VIBE_CODING compliance** in all development activities

## Prerequisites

### **Required Knowledge**
- Basic command line usage (bash, shell commands)
- Understanding of YAML syntax
- Familiarity with Python development workflows
- Basic understanding of Docker concepts

### **Required Tools**
- Task 3.44.1 or later
- Python 3.x
- Git
- Text editor (VS Code, Vim, etc.)

### **System Access**
- Access to the `devops/build-env` directory
- Permission to execute wrapper scripts
- Ability to create and modify Taskfiles

## Training Modules

### **Module 1: System Overview and Architecture**

#### **Learning Objectives**
- Understand the overall system design
- Identify key components and their relationships
- Recognize the benefits of the Taskfile-based approach

#### **Key Concepts**
1. **Template System**: Reusable task templates for common patterns
2. **Component Isolation**: Separate environments for different components
3. **Namespace Organization**: Logical grouping of related tasks
4. **Wrapper Scripts**: Simplified interface for common operations

#### **Practical Exercise**
```bash
# Explore the system structure
cd devops/build-env
ls -la
tree -L 3

# Examine template files
cat templates/base-tasks.yml
cat templates/python-tasks.yml

# Explore component environment
ls -la environments/aiailint-dev/
cat environments/aiailint-dev/Taskfile.yml
```

#### **Discussion Questions**
1. How does the template system reduce duplication?
2. What are the benefits of component isolation?
3. How does the namespace system improve organization?

### **Module 2: Wrapper Scripts and Basic Operations**

#### **Learning Objectives**
- Use wrapper scripts for common development tasks
- Understand script options and help systems
- Handle errors and troubleshoot issues

#### **Core Scripts**
1. **setup.sh**: Environment setup and validation
2. **test.sh**: Comprehensive testing interface
3. **deploy.sh**: Multi-target deployment

#### **Practical Exercise**
```bash
# Setup environment
./scripts/setup.sh --help
./scripts/setup.sh

# Run tests
./scripts/test.sh --help
./scripts/test.sh all

# Deploy locally
./scripts/deploy.sh --help
./scripts/deploy.sh local
```

#### **Error Handling Exercise**
```bash
# Simulate missing Task
export PATH="/tmp:$PATH"
./scripts/setup.sh

# Simulate test failure
# (Create a failing test and observe error handling)

# Simulate deployment issues
# (Create deployment problems and observe error messages)
```

#### **Discussion Questions**
1. How do wrapper scripts improve developer experience?
2. What error handling patterns are most effective?
3. How can script output be customized for different needs?

### **Module 3: Task Discovery and Direct Usage**

#### **Learning Objectives**
- Discover available tasks using Task commands
- Understand task namespaces and organization
- Use tasks directly for advanced operations

#### **Task Discovery Commands**
```bash
# List all tasks
task --list

# List with details
task --list-all

# Filter by namespace
task --list | grep "base:"
task --list | grep "python:"
task --list | grep "aiailint:"
```

#### **Practical Exercise**
```bash
# Explore base tasks
task base:help
task base:status

# Explore Python tasks
task python:install
task python:test
task python:quality

# Explore component tasks
task aiailint:lint
task aiailint:validate
task aiailint:docs
```

#### **Advanced Task Usage**
```bash
# Dry run (show commands without executing)
task --dry python:build

# Verbose output
task --verbose aiailint:test-aiailint

# Show task dependencies
task --summary deploy:deploy-production
```

#### **Discussion Questions**
1. When should you use wrapper scripts vs direct task execution?
2. How does the namespace system help with task organization?
3. What are the benefits of dry-run and verbose modes?

### **Module 4: Component Environment Creation**

#### **Learning Objectives**
- Create new component environments
- Customize templates for specific needs
- Understand the master + override pattern

#### **Component Creation Process**
```bash
# Create new component environment
mkdir -p environments/new-component
cd environments/new-component

# Create master Taskfile
cat > Taskfile.yml << 'EOF'
version: '3'

includes:
  base: ../templates/base-tasks.yml
  python: ../templates/python-tasks.yml
  docker: ../templates/docker-tasks.yml
  deploy: ../templates/deploy-tasks.yml

tasks:
  setup:
    desc: "Setup new-component development environment"
    cmds:
      - task: base:setup
      - echo "Setting up new-component environment..."
      - pip install -r requirements/requirements.txt
EOF

# Create component-specific tasks
cat > new-component-tasks.yml << 'EOF'
version: '3'

tasks:
  component-specific:
    desc: "Run component-specific operations"
    cmds:
      - echo "Running component-specific task..."
EOF

# Create requirements
mkdir requirements
cat > requirements/requirements.txt << 'EOF'
# Component-specific dependencies
component-library==1.0.0
EOF
```

#### **Template Customization Exercise**
```bash
# Customize Python tasks for component
cat > python-override.yml << 'EOF'
version: '3'

tasks:
  test:
    desc: "Run component-specific tests"
    cmds:
      - echo "Running component tests..."
      - python -m pytest tests/component/
EOF
```

#### **Discussion Questions**
1. What considerations go into designing component-specific tasks?
2. How do you decide when to override vs extend templates?
3. What are the trade-offs of component isolation vs shared functionality?

### **Module 5: Development Workflows**

#### **Learning Objectives**
- Follow established development workflows
- Integrate the system with existing development practices
- Optimize workflows for team productivity

#### **Feature Development Workflow**
```bash
# 1. Setup environment
./scripts/setup.sh

# 2. Verify clean state
./scripts/test.sh all

# 3. Create feature branch
git checkout -b feature/new-feature

# 4. Make changes
# (Edit code files)

# 5. Run quality checks
./scripts/test.sh quality

# 6. Run tests
./scripts/test.sh unit
./scripts/test.sh integration

# 7. Deploy for testing
./scripts/deploy.sh local

# 8. Commit changes
git add .
git commit -m "Add new feature with comprehensive testing"
```

#### **Bug Fix Workflow**
```bash
# 1. Identify issue
./scripts/test.sh all

# 2. Create fix branch
git checkout -b fix/bug-description

# 3. Isolate failing tests
./scripts/test.sh unit
./scripts/test.sh integration

# 4. Implement fix
# (Make necessary code changes)

# 5. Verify fix
./scripts/test.sh all

# 6. Deploy fix
./scripts/deploy.sh local

# 7. Commit fix
git commit -m "Fix bug with comprehensive testing"
```

#### **Release Preparation Workflow**
```bash
# 1. Ensure clean environment
./scripts/setup.sh

# 2. Run comprehensive tests
./scripts/test.sh all

# 3. Build release package
./scripts/deploy.sh build

# 4. Deploy to staging
./scripts/deploy.sh staging

# 5. Verify staging deployment
./scripts/test.sh health

# 6. Deploy to production
./scripts/deploy.sh production
```

#### **Discussion Questions**
1. How do these workflows improve development efficiency?
2. What are the key quality gates in each workflow?
3. How can workflows be customized for different team needs?

### **Module 6: Troubleshooting and Debugging**

#### **Learning Objectives**
- Identify and resolve common issues
- Use debugging tools and techniques
- Understand error messages and logs

#### **Common Issues and Solutions**

**Issue 1: Task Not Found**
```bash
# Problem: task command not found
# Solution: Install Task
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin

# Problem: specific task not found
# Solution: Check task list and namespaces
task --list | grep "task-name"
```

**Issue 2: Template Inclusion Problems**
```bash
# Problem: template file not found
# Solution: Check file paths and syntax
ls templates/template-name.yml
cat environments/component/Taskfile.yml

# Problem: namespace conflicts
# Solution: Check task names and namespaces
task --list-all | grep "conflicting-task"
```

**Issue 3: Wrapper Script Errors**
```bash
# Problem: permission denied
# Solution: Check script permissions
ls -la scripts/
chmod +x scripts/script-name.sh

# Problem: missing dependencies
# Solution: Check system requirements
./scripts/script-name.sh --help
```

#### **Debugging Techniques**
```bash
# Enable verbose output
./scripts/script-name.sh --verbose
task --verbose task-name

# Dry run to see commands
task --dry task-name

# Check task dependencies
task --summary task-name

# Validate YAML syntax
yamllint Taskfile.yml
```

#### **Log Analysis**
```bash
# Check script logs
./scripts/test.sh all 2>&1 | tee test.log

# Analyze error patterns
grep -i error test.log
grep -i fail test.log

# Check system resources
top
df -h
free -h
```

#### **Discussion Questions**
1. What are the most common troubleshooting scenarios?
2. How can debugging be made more efficient?
3. What logging and monitoring would be most helpful?

### **Module 7: VIBE_CODING Compliance**

#### **Learning Objectives**
- Understand VIBE_CODING principles and requirements
- Apply compliance standards to development activities
- Maintain quality and consistency across the team

#### **VIBE_CODING Principles**
1. **Rapid Create → Validate → Test → Commit**: Fast iteration with quality assurance
2. **Professional Communication**: Clear, technical language without emojis
3. **Component Discovery**: Active seeking of component-specific requirements
4. **Error Handling**: Comprehensive validation and graceful degradation
5. **Documentation Standards**: Complete, actionable documentation

#### **Compliance Checklist**
- [ ] All files pass syntax validation
- [ ] All tests pass before commits
- [ ] Documentation is complete and professional
- [ ] Error handling is comprehensive
- [ ] Component-specific requirements are incorporated
- [ ] No emojis in code, comments, or documentation

#### **Practical Exercise**
```bash
# Validate YAML files
yamllint templates/*.yml
yamllint environments/*/Taskfile.yml

# Validate shell scripts
shellcheck scripts/*.sh

# Run comprehensive tests
./scripts/test.sh all

# Check documentation quality
# (Review documentation for completeness and professionalism)
```

#### **Discussion Questions**
1. How does VIBE_CODING improve development quality?
2. What are the key compliance challenges?
3. How can compliance be maintained as the team grows?

## Assessment and Certification

### **Knowledge Assessment**
Participants should be able to:
1. **Explain system architecture** and component relationships
2. **Use wrapper scripts effectively** for common tasks
3. **Navigate task namespaces** and find appropriate tasks
4. **Create component environments** with proper customization
5. **Troubleshoot common issues** using appropriate techniques
6. **Follow VIBE_CODING compliance** in all activities

### **Practical Assessment**
Complete the following exercises:
1. **Setup Exercise**: Successfully setup a new development environment
2. **Testing Exercise**: Run comprehensive tests and interpret results
3. **Deployment Exercise**: Deploy a component to local environment
4. **Customization Exercise**: Create a new component environment
5. **Troubleshooting Exercise**: Resolve common issues independently

### **Certification Criteria**
- Complete all training modules
- Pass knowledge assessment with 80% or higher
- Successfully complete all practical exercises
- Demonstrate VIBE_CODING compliance
- Contribute to team documentation or best practices

## Resources and References

### **Documentation**
- **TASKFILE_USAGE_GUIDE.md**: Comprehensive usage instructions
- **../architects/TASKFILE_PROGRESS.md**: System development history
- **../architects/TASKFILE_ARCHITECTURE.md**: System architecture
- **VIBE_CODING.md**: Development workflow standards

### **External Resources**
- **Task Documentation**: https://taskfile.dev/
- **YAML Reference**: https://yaml.org/spec/
- **Shell Scripting**: https://www.gnu.org/software/bash/
- **Python Development**: https://docs.python.org/

### **Team Resources**
- **Issue Tracker**: Report problems and request features
- **Code Repository**: Access to all source code and configurations
- **Team Chat**: Real-time support and collaboration
- **Knowledge Base**: Shared documentation and best practices

## Training Schedule

### **Recommended Timeline**
- **Week 1**: Modules 1-2 (System Overview, Wrapper Scripts)
- **Week 2**: Modules 3-4 (Task Discovery, Component Creation)
- **Week 3**: Modules 5-6 (Workflows, Troubleshooting)
- **Week 4**: Module 7 (VIBE_CODING Compliance) and Assessment

### **Training Format**
- **Self-paced learning**: Complete modules at your own pace
- **Practical exercises**: Hands-on experience with real scenarios
- **Team discussions**: Share experiences and best practices
- **Mentor support**: Available for questions and guidance

### **Follow-up Activities**
- **Regular reviews**: Monthly system usage reviews
- **Best practice sharing**: Team presentations on effective usage
- **Continuous improvement**: Feedback and system enhancements
- **Advanced training**: Specialized topics as needed

---

*This training program provides comprehensive instruction for the Taskfile-based configuration management system. For additional support or questions, contact the development team or refer to the documentation resources listed above.*
