# Development Environment Generator Makefile
# This Makefile provides commands to generate new development environments

.PHONY: help create-env list-envs clean-env validate-env

# Default target
help:
	@echo "Development Environment Generator"
	@echo "================================"
	@echo ""
	@echo "Available commands:"
	@echo "  make create-env COMPONENT=<name>     - Create new development environment"
	@echo "  make list-envs                       - List existing environments"
	@echo "  make clean-env COMPONENT=<name>      - Remove development environment"
	@echo "  make validate-env COMPONENT=<name>   - Validate environment setup"
	@echo "  make template-env COMPONENT=<name>   - Create environment from template"
	@echo "  make update-template                 - Update template from existing env"
	@echo ""

# Check if COMPONENT is provided
check-component:
	@if [ -z "$(COMPONENT)" ]; then \
		echo "Error: COMPONENT variable is required"; \
		echo "Usage: make create-env COMPONENT=<component-name>"; \
		exit 1; \
	fi

# Create new development environment
create-env: check-component
	@echo "Creating development environment for $(COMPONENT)..."
	@mkdir -p $(COMPONENT)-dev
	@cp -r dev-env-template/* $(COMPONENT)-dev/
	@echo "Environment created: $(COMPONENT)-dev/"
	@echo "Next steps:"
	@echo "  1. cd $(COMPONENT)-dev"
	@echo "  2. Edit env-config.yaml with your component details"
	@echo "  3. python generate_env.py create --component $(COMPONENT)"

# Generate environment from configuration
generate-env: check-component
	@echo "Generating environment from configuration..."
	@cd $(COMPONENT)-dev && python3 generate_env.py create --component $(COMPONENT)

# List existing environments
list-envs:
	@echo "Existing development environments:"
	@for env in */; do \
		if [ -d "$$env" ] && [ "$$env" != "dev-env-template/" ]; then \
			echo "  - $$env"; \
		fi; \
	done

# Clean environment
clean-env: check-component
	@echo "Removing development environment for $(COMPONENT)..."
	@if [ -d "$(COMPONENT)-dev" ]; then \
		rm -rf "$(COMPONENT)-dev"; \
		echo "Environment removed: $(COMPONENT)-dev/"; \
	else \
		echo "Environment not found: $(COMPONENT)-dev/"; \
	fi

# Validate environment setup
validate-env: check-component
	@echo "Validating environment for $(COMPONENT)..."
	@if [ -d "$(COMPONENT)-dev" ]; then \
		echo "✓ Environment directory exists"; \
		if [ -f "$(COMPONENT)-dev/env-config.yaml" ]; then \
			echo "✓ Configuration file exists"; \
		else \
			echo "✗ Configuration file missing"; \
		fi; \
		if [ -f "$(COMPONENT)-dev/scripts/setup-env.sh" ]; then \
			echo "✓ Setup script exists"; \
		else \
			echo "✗ Setup script missing"; \
		fi; \
		if [ -f "$(COMPONENT)-dev/README.md" ]; then \
			echo "✓ Documentation exists"; \
		else \
			echo "✗ Documentation missing"; \
		fi; \
	else \
		echo "✗ Environment directory not found: $(COMPONENT)-dev/"; \
	fi

# Create environment from template with configuration
template-env: check-component
	@echo "Creating environment from template for $(COMPONENT)..."
	@mkdir -p $(COMPONENT)-dev
	@cp -r dev-env-template/* $(COMPONENT)-dev/
	@echo "Template copied to $(COMPONENT)-dev/"
	@echo "Please edit $(COMPONENT)-dev/env-config.yaml with your component details"
	@echo "Then run: python generate_env.py create --component $(COMPONENT)"

# Update template from existing environment
update-template: check-component
	@echo "Updating template from $(COMPONENT)-dev..."
	@if [ -d "$(COMPONENT)-dev" ]; then \
		rm -rf dev-env-template/*; \
		cp -r $(COMPONENT)-dev/* dev-env-template/; \
		echo "Template updated from $(COMPONENT)-dev/"; \
	else \
		echo "Environment not found: $(COMPONENT)-dev/"; \
	fi

# Quick environment creation with defaults
quick-env: check-component
	@echo "Creating quick environment for $(COMPONENT)..."
	@mkdir -p $(COMPONENT)-dev
	@cp -r dev-env-template/* $(COMPONENT)-dev/
	@cd $(COMPONENT)-dev && sed -i "s/{{COMPONENT_NAME}}/$(COMPONENT)/g" env-config.yaml
	@cd $(COMPONENT)-dev && sed -i "s/{{COMPONENT_FULL_NAME}}/$(COMPONENT)/g" env-config.yaml
	@cd $(COMPONENT)-dev && sed -i "s/{{COMPONENT_DESCRIPTION}}/$(COMPONENT) component/g" env-config.yaml
	@echo "Quick environment created: $(COMPONENT)-dev/"
	@echo "Edit $(COMPONENT)-dev/env-config.yaml to customize"

# Show environment info
info-env: check-component
	@echo "Environment information for $(COMPONENT):"
	@if [ -d "$(COMPONENT)-dev" ]; then \
		echo "Files:"; \
		find $(COMPONENT)-dev -type f -name "*.md" -o -name "*.sh" -o -name "*.yaml" | head -10; \
	else \
		echo "Environment not found: $(COMPONENT)-dev/"; \
	fi

# Install dependencies for environment
install-env: check-component
	@echo "Installing dependencies for $(COMPONENT)..."
	@if [ -d "$(COMPONENT)-dev" ]; then \
		cd $(COMPONENT)-dev && ./scripts/setup-env.sh; \
	else \
		echo "Environment not found: $(COMPONENT)-dev/"; \
	fi

# Run tests for environment
test-env: check-component
	@echo "Running tests for $(COMPONENT)..."
	@if [ -d "$(COMPONENT)-dev" ]; then \
		cd $(COMPONENT)-dev && ./scripts/run-tests.sh; \
	else \
		echo "Environment not found: $(COMPONENT)-dev/"; \
	fi

# Quality check for environment
quality-env: check-component
	@echo "Running quality checks for $(COMPONENT)..."
	@if [ -d "$(COMPONENT)-dev" ]; then \
		cd $(COMPONENT)-dev && ./scripts/quality-check.sh; \
	else \
		echo "Environment not found: $(COMPONENT)-dev/"; \
	fi
