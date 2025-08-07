# aiailint Development Container
# Multi-stage Dockerfile for development, testing, and production

# Base stage with Python and system dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash aiai
WORKDIR /workspace

# Development stage
FROM base as development

# Install development dependencies
COPY requirements/requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt

# Install aiailint in development mode
COPY ../../../aiailint /workspace/aiailint
WORKDIR /workspace/aiailint
RUN pip install -e .

# Set up development environment
RUN mkdir -p /workspace/build-env
WORKDIR /workspace/build-env

# Copy build environment files
COPY . /workspace/build-env/

# Set permissions
RUN chown -R aiai:aiai /workspace
USER aiai

# Expose ports for development tools
EXPOSE 8000 8080

# Default command for development
CMD ["bash"]

# Testing stage
FROM base as testing

# Install testing dependencies
COPY requirements/requirements-test.txt /tmp/requirements-test.txt
RUN pip install --no-cache-dir -r /tmp/requirements-test.txt

# Install aiailint
COPY ../../../aiailint /workspace/aiailint
WORKDIR /workspace/aiailint
RUN pip install .

# Set up testing environment
RUN mkdir -p /workspace/build-env
WORKDIR /workspace/build-env

# Copy build environment files
COPY . /workspace/build-env/

# Set permissions
RUN chown -R aiai:aiai /workspace
USER aiai

# Default command for testing
CMD ["pytest", "../../../aiailint/tests/", "-v"]

# Production stage
FROM base as production

# Install production dependencies
COPY requirements/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install aiailint
COPY ../../../aiailint /workspace/aiailint
WORKDIR /workspace/aiailint
RUN pip install .

# Set up production environment
RUN mkdir -p /workspace/build-env
WORKDIR /workspace/build-env

# Copy build environment files
COPY . /workspace/build-env/

# Set permissions
RUN chown -R aiai:aiai /workspace
USER aiai

# Default command for production
CMD ["aiailint", "--help"]

# CI/CD stage
FROM base as ci

# Install CI/CD dependencies
COPY requirements/requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt

# Install aiailint
COPY ../../../aiailint /workspace/aiailint
WORKDIR /workspace/aiailint
RUN pip install -e .

# Set up CI/CD environment
RUN mkdir -p /workspace/build-env
WORKDIR /workspace/build-env

# Copy build environment files
COPY . /workspace/build-env/

# Set permissions
RUN chown -R aiai:aiai /workspace
USER aiai

# Default command for CI/CD
CMD ["./scripts/run-tests.sh", "--coverage", "--report"]
