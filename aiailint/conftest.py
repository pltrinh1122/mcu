"""
Shared fixtures for aiailint tests.

This module provides common fixtures used across all aiailint test modules.
"""

import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_yaml_file():
    """Fixture providing a temporary YAML file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def sample_valid_script():
    """Fixture providing a sample valid AIAI script"""
    return """
metadata:
  name: "test-script"
  version: "1.0.0"
  description: "Test script"

steps:
  - name: "test-step"
    command: "echo 'test'"
    """


@pytest.fixture
def sample_invalid_script():
    """Fixture providing a sample invalid AIAI script"""
    return """
# Missing metadata and steps
invalid: "content"
    """


@pytest.fixture
def sample_complex_script():
    """Fixture providing a sample complex AIAI script with multiple steps"""
    return """
metadata:
  name: "complex-test-script"
  version: "2.0.0"
  description: "Complex test script with multiple steps"

steps:
  - name: "step-1"
    command: "echo 'Step 1'"
    description: "First step"
    
  - name: "step-2"
    command: "echo 'Step 2'"
    description: "Second step"
    
  - name: "step-3"
    command: "echo 'Step 3'"
    description: "Third step"
    """


@pytest.fixture
def sample_script_with_metadata():
    """Fixture providing a sample AIAI script with full metadata"""
    return """
metadata:
  name: "metadata-test-script"
  version: "1.0.0"
  description: "Test script with full metadata"
  author: "Test Author"
  created: "2024-01-01"
  tags: ["test", "validation"]

steps:
  - name: "metadata-step"
    command: "echo 'Testing metadata'"
    """
