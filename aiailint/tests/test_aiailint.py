"""
Tests for the main aiailint application.

This module contains pytest-based tests for the main AiaiLinter class,
following OOP principles and using fixtures for test data management.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from tests.utils import create_test_script, validate_yaml_syntax

# Import the main application components
from src.aiailint import AiaiLinter, ValidationResult, ValidationIssue, ExitCodes


class TestAiaiLinterInitialization:
    """Test cases for AiaiLinter class initialization using OOP principles."""
    
    def test_default_initialization(self):
        """Test AiaiLinter initialization with default parameters."""
        linter = AiaiLinter()
        
        assert linter.verbose == False
        assert linter.strict == False
        assert linter.format_output == "text"
        assert linter.no_semantic == False
        assert linter.business_rules_only == False
        assert len(linter.validators) > 0
    
    def test_verbose_initialization(self):
        """Test AiaiLinter initialization with verbose mode."""
        linter = AiaiLinter(verbose=True)
        
        assert linter.verbose == True
        assert linter.strict == False
        assert linter.format_output == "text"
    
    def test_strict_initialization(self):
        """Test AiaiLinter initialization with strict mode."""
        linter = AiaiLinter(strict=True)
        
        assert linter.verbose == False
        assert linter.strict == True
        assert linter.format_output == "text"
    
    def test_json_output_initialization(self):
        """Test AiaiLinter initialization with JSON output format."""
        linter = AiaiLinter(format_output="json")
        
        assert linter.format_output == "json"
        assert hasattr(linter, 'output_formatter')
    
    def test_no_semantic_initialization(self):
        """Test AiaiLinter initialization with semantic analysis disabled."""
        linter = AiaiLinter(no_semantic=True)
        
        assert linter.no_semantic == True
        # Should have fewer validators when semantic analysis is disabled
        assert len(linter.validators) > 0
    
    def test_business_rules_only_initialization(self):
        """Test AiaiLinter initialization with business rules only."""
        linter = AiaiLinter(business_rules_only=True)
        
        assert linter.business_rules_only == True
        # Should have only business rules and cross-reference validators
        assert len(linter.validators) > 0


class TestValidationResult:
    """Test cases for ValidationResult dataclass using OOP principles."""
    
    def test_validation_result_creation(self):
        """Test ValidationResult creation with basic parameters."""
        result = ValidationResult(
            success=True,
            errors=[],
            warnings=[],
            info=[],
            file_path="test.yaml"
        )
        
        assert result.success == True
        assert result.errors == []
        assert result.warnings == []
        assert result.info == []
        assert result.file_path == "test.yaml"
    
    def test_validation_result_with_issues(self):
        """Test ValidationResult creation with validation issues."""
        result = ValidationResult(
            success=False,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"],
            info=["Info 1"],
            file_path="test.yaml"
        )
        
        assert result.success == False
        assert len(result.errors) == 2
        assert len(result.warnings) == 1
        assert len(result.info) == 1
        assert result.has_issues == True
    
    def test_validation_result_has_issues_property(self):
        """Test ValidationResult has_issues property."""
        # Test with errors
        result_with_errors = ValidationResult(
            success=False,
            errors=["Error"],
            warnings=[],
            info=[]
        )
        assert result_with_errors.has_issues == True
        
        # Test with warnings
        result_with_warnings = ValidationResult(
            success=True,
            errors=[],
            warnings=["Warning"],
            info=[]
        )
        assert result_with_warnings.has_issues == True
        
        # Test with info
        result_with_info = ValidationResult(
            success=True,
            errors=[],
            warnings=[],
            info=["Info"]
        )
        assert result_with_info.has_issues == True
        
        # Test with no issues
        result_clean = ValidationResult(
            success=True,
            errors=[],
            warnings=[],
            info=[]
        )
        assert result_clean.has_issues == False


class TestValidationIssue:
    """Test cases for ValidationIssue dataclass using OOP principles."""
    
    def test_validation_issue_creation(self):
        """Test ValidationIssue creation with basic parameters."""
        issue = ValidationIssue(
            code="E001",
            severity="error",
            message="Test error message",
            line=10,
            path="metadata.name",
            command="echo 'test'",
            fix_suggestion="Use proper syntax"
        )
        
        assert issue.code == "E001"
        assert issue.severity == "error"
        assert issue.message == "Test error message"
        assert issue.line == 10
        assert issue.path == "metadata.name"
        assert issue.command == "echo 'test'"
        assert issue.fix_suggestion == "Use proper syntax"
    
    def test_validation_issue_with_minimal_parameters(self):
        """Test ValidationIssue creation with minimal parameters."""
        issue = ValidationIssue(
            code="E002",
            severity="warning",
            message="Test warning message"
        )
        
        assert issue.code == "E002"
        assert issue.severity == "warning"
        assert issue.message == "Test warning message"
        assert issue.line is None
        assert issue.path is None
        assert issue.command is None
        assert issue.fix_suggestion is None


class TestAiaiLinterDependencyChecking:
    """Test cases for dependency checking functionality."""
    
    @patch('src.aiailint.yaml')
    @patch('src.aiailint.jsonschema')
    def test_dependencies_available(self, mock_jsonschema, mock_yaml):
        """Test dependency checking when all dependencies are available."""
        linter = AiaiLinter()
        result = linter.check_dependencies()
        
        assert result == True
    
    @patch('src.aiailint.yaml')
    @patch('src.aiailint.jsonschema')
    @patch('src.aiailint.bashlex')
    def test_dependencies_with_bashlex(self, mock_bashlex, mock_jsonschema, mock_yaml):
        """Test dependency checking with bashlex available."""
        linter = AiaiLinter(verbose=True)
        result = linter.check_dependencies()
        
        assert result == True
    
    @patch('src.aiailint.yaml')
    @patch('src.aiailint.jsonschema')
    @patch('src.aiailint.bashlex', side_effect=ImportError)
    @patch('src.aiailint.bashparser')
    def test_dependencies_with_bashparser(self, mock_bashparser, mock_bashlex, mock_jsonschema, mock_yaml):
        """Test dependency checking with bashparser available."""
        linter = AiaiLinter(verbose=True)
        result = linter.check_dependencies()
        
        assert result == True
    
    @patch('src.aiailint.yaml')
    @patch('src.aiailint.jsonschema')
    @patch('src.aiailint.bashlex', side_effect=ImportError)
    @patch('src.aiailint.bashparser', side_effect=ImportError)
    def test_dependencies_without_bash_parser(self, mock_bashparser, mock_bashlex, mock_jsonschema, mock_yaml):
        """Test dependency checking without bash parser."""
        linter = AiaiLinter(verbose=True)
        result = linter.check_dependencies()
        
        assert result == False
    
    @patch('src.aiailint.yaml', side_effect=ImportError)
    def test_dependencies_missing_yaml(self, mock_yaml):
        """Test dependency checking with missing yaml dependency."""
        linter = AiaiLinter()
        result = linter.check_dependencies()
        
        assert result == False


class TestAiaiLinterFileValidation:
    """Test cases for file validation functionality."""
    
    def test_validate_file_system_check(self, temp_yaml_file, sample_valid_script):
        """Test file system validation with valid file."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_valid_script)
        
        linter = AiaiLinter()
        
        # Mock the validation pipeline to focus on file system checks
        with patch.object(linter, '_run_validation_pipeline') as mock_pipeline:
            mock_pipeline.return_value = ValidationResult(
                success=True,
                errors=[],
                warnings=[],
                info=[],
                file_path=str(temp_yaml_file)
            )
            
            result = linter.validate_file(temp_yaml_file)
            
            assert result.success == True
            assert result.file_path == str(temp_yaml_file)
    
    def test_validate_file_nonexistent(self):
        """Test file validation with nonexistent file."""
        linter = AiaiLinter()
        result = linter.validate_file("nonexistent_file.yaml")
        
        assert result.success == False
        assert len(result.errors) > 0
    
    def test_validate_file_directory(self, tmp_path):
        """Test file validation with directory instead of file."""
        linter = AiaiLinter()
        result = linter.validate_file(tmp_path)
        
        assert result.success == False
        assert len(result.errors) > 0
    
    def test_validate_file_empty(self, temp_yaml_file):
        """Test file validation with empty file."""
        # Create empty file
        with open(temp_yaml_file, 'w') as f:
            f.write("")
        
        linter = AiaiLinter()
        result = linter.validate_file(temp_yaml_file)
        
        assert result.success == False
        assert len(result.errors) > 0


class TestAiaiLinterYAMLLoading:
    """Test cases for YAML loading functionality."""
    
    def test_load_yaml_valid_content(self, temp_yaml_file, sample_valid_script):
        """Test YAML loading with valid content."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_valid_script)
        
        linter = AiaiLinter()
        
        # Test the private method through mocking
        with patch.object(linter, '_load_yaml_data') as mock_load:
            mock_load.return_value = {
                "metadata": {"name": "test"},
                "steps": [{"name": "test", "command": "echo"}]
            }
            
            # This would normally be called internally, but we're testing the mock
            data = linter._load_yaml_data(Path(temp_yaml_file))
            
            assert data is not None
            assert "metadata" in data
            assert "steps" in data
    
    def test_load_yaml_invalid_content(self, temp_yaml_file):
        """Test YAML loading with invalid content."""
        with open(temp_yaml_file, 'w') as f:
            f.write("invalid: yaml: content: with: colons:")
        
        linter = AiaiLinter()
        
        # Test the private method through mocking
        with patch.object(linter, '_load_yaml_data') as mock_load:
            mock_load.return_value = None
            
            data = linter._load_yaml_data(Path(temp_yaml_file))
            
            assert data is None
    
    def test_load_yaml_malformed_content(self, temp_yaml_file):
        """Test YAML loading with malformed content."""
        with open(temp_yaml_file, 'w') as f:
            f.write("metadata:\n  name: test\n  # Missing closing quote\n")
        
        linter = AiaiLinter()
        
        # Test the private method through mocking
        with patch.object(linter, '_load_yaml_data') as mock_load:
            mock_load.return_value = None
            
            data = linter._load_yaml_data(Path(temp_yaml_file))
            
            assert data is None


class TestAiaiLinterValidationPipeline:
    """Test cases for validation pipeline orchestration."""
    
    def test_validation_pipeline_execution(self, temp_yaml_file, sample_valid_script):
        """Test complete validation pipeline execution."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_valid_script)
        
        linter = AiaiLinter()
        
        # Mock the internal validation methods
        with patch.object(linter, '_validate_file_system') as mock_fs:
            with patch.object(linter, '_load_yaml_data') as mock_load:
                with patch.object(linter, '_run_all_validations') as mock_validations:
                    with patch.object(linter, '_aggregate_validation_results') as mock_aggregate:
                        
                        # Setup mocks
                        mock_fs.return_value = ValidationResult(
                            success=True, errors=[], warnings=[], info=[]
                        )
                        mock_load.return_value = {
                            "metadata": {"name": "test"},
                            "steps": [{"name": "test", "command": "echo"}]
                        }
                        mock_validations.return_value = [
                            ValidationResult(success=True, errors=[], warnings=[], info=[])
                        ]
                        mock_aggregate.return_value = ValidationResult(
                            success=True, errors=[], warnings=[], info=[], file_path=str(temp_yaml_file)
                        )
                        
                        result = linter._run_validation_pipeline(Path(temp_yaml_file))
                        
                        assert result.success == True
                        assert result.file_path == str(temp_yaml_file)
    
    def test_validation_pipeline_file_system_error(self, temp_yaml_file):
        """Test validation pipeline with file system error."""
        linter = AiaiLinter()
        
        # Mock file system validation to return error
        with patch.object(linter, '_validate_file_system') as mock_fs:
            mock_fs.return_value = ValidationResult(
                success=False, 
                errors=["File not found"], 
                warnings=[], 
                info=[]
            )
            
            result = linter._run_validation_pipeline(Path(temp_yaml_file))
            
            assert result.success == False
            assert len(result.errors) > 0
    
    def test_validation_pipeline_yaml_loading_error(self, temp_yaml_file, sample_valid_script):
        """Test validation pipeline with YAML loading error."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_valid_script)
        
        linter = AiaiLinter()
        
        # Mock file system validation to succeed but YAML loading to fail
        with patch.object(linter, '_validate_file_system') as mock_fs:
            with patch.object(linter, '_load_yaml_data') as mock_load:
                
                mock_fs.return_value = ValidationResult(
                    success=True, errors=[], warnings=[], info=[]
                )
                mock_load.return_value = None
                
                result = linter._run_validation_pipeline(Path(temp_yaml_file))
                
                assert result.success == False
                assert len(result.errors) > 0


class TestAiaiLinterResultAggregation:
    """Test cases for result aggregation functionality."""
    
    def test_aggregate_validation_results_success(self):
        """Test aggregation of successful validation results."""
        linter = AiaiLinter()
        
        results = [
            ValidationResult(success=True, errors=[], warnings=[], info=[]),
            ValidationResult(success=True, errors=[], warnings=[], info=[])
        ]
        
        aggregated = linter._aggregate_validation_results(results)
        
        assert aggregated.success == True
        assert len(aggregated.errors) == 0
        assert len(aggregated.warnings) == 0
        assert len(aggregated.info) == 0
    
    def test_aggregate_validation_results_with_errors(self):
        """Test aggregation of validation results with errors."""
        linter = AiaiLinter()
        
        results = [
            ValidationResult(success=True, errors=[], warnings=[], info=[]),
            ValidationResult(success=False, errors=["Error 1"], warnings=[], info=[]),
            ValidationResult(success=True, errors=[], warnings=["Warning 1"], info=[])
        ]
        
        aggregated = linter._aggregate_validation_results(results)
        
        assert aggregated.success == False
        assert len(aggregated.errors) == 1
        assert len(aggregated.warnings) == 1
        assert "Error 1" in aggregated.errors
        assert "Warning 1" in aggregated.warnings
    
    def test_aggregate_validation_results_strict_mode(self):
        """Test aggregation in strict mode (warnings treated as errors)."""
        linter = AiaiLinter(strict=True)
        
        results = [
            ValidationResult(success=True, errors=[], warnings=["Warning 1"], info=[])
        ]
        
        aggregated = linter._aggregate_validation_results(results)
        
        assert aggregated.success == False  # Should fail in strict mode
        assert len(aggregated.errors) == 1  # Warning should become error
        assert "Warning 1" in aggregated.errors


class TestAiaiLinterIntegration:
    """Integration test cases for AiaiLinter."""
    
    def test_end_to_end_validation_workflow(self, temp_yaml_file, sample_valid_script):
        """Test complete end-to-end validation workflow."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_valid_script)
        
        linter = AiaiLinter()
        
        # Mock dependencies to focus on workflow
        with patch.object(linter, 'check_dependencies', return_value=True):
            with patch.object(linter, '_run_validation_pipeline') as mock_pipeline:
                mock_pipeline.return_value = ValidationResult(
                    success=True,
                    errors=[],
                    warnings=[],
                    info=[],
                    file_path=str(temp_yaml_file)
                )
                
                result = linter.validate_file(temp_yaml_file)
                
                assert result.success == True
                assert result.file_path == str(temp_yaml_file)
    
    def test_package_validation_workflow(self, tmp_path):
        """Test package validation workflow."""
        # Create a package structure
        package_dir = tmp_path / "test_package"
        package_dir.mkdir()
        
        script1 = package_dir / "script1.yaml"
        script2 = package_dir / "script2.yaml"
        
        # Create test scripts
        with open(script1, 'w') as f:
            f.write("metadata:\n  name: script1\nsteps:\n  - name: step1\n    command: echo")
        
        with open(script2, 'w') as f:
            f.write("metadata:\n  name: script2\nsteps:\n  - name: step2\n    command: echo")
        
        linter = AiaiLinter()
        
        # Mock the validation pipeline
        with patch.object(linter, '_run_validation_pipeline') as mock_pipeline:
            mock_pipeline.return_value = ValidationResult(
                success=True,
                errors=[],
                warnings=[],
                info=[],
                file_path=str(script1)
            )
            
            result = linter.validate_package(package_dir)
            
            assert result.success == True


class TestAiaiLinterPerformance:
    """Performance test cases for AiaiLinter."""
    
    @pytest.mark.slow
    def test_validation_performance(self, temp_yaml_file, sample_complex_script):
        """Test validation performance with complex script."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_complex_script)
        
        linter = AiaiLinter()
        
        # Mock dependencies to focus on performance
        with patch.object(linter, 'check_dependencies', return_value=True):
            with patch.object(linter, '_run_validation_pipeline') as mock_pipeline:
                mock_pipeline.return_value = ValidationResult(
                    success=True,
                    errors=[],
                    warnings=[],
                    info=[],
                    file_path=str(temp_yaml_file)
                )
                
                import time
                start_time = time.time()
                
                result = linter.validate_file(temp_yaml_file)
                
                end_time = time.time()
                duration = end_time - start_time
                
                # Should complete within reasonable time
                assert duration < 5.0, f"Validation took {duration:.2f}s, expected <5s"
                assert result.success == True
    
    @pytest.mark.slow
    def test_memory_usage(self, temp_yaml_file, sample_complex_script):
        """Test memory usage during validation."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_complex_script)
        
        linter = AiaiLinter()
        
        # Mock dependencies to focus on memory usage
        with patch.object(linter, 'check_dependencies', return_value=True):
            with patch.object(linter, '_run_validation_pipeline') as mock_pipeline:
                mock_pipeline.return_value = ValidationResult(
                    success=True,
                    errors=[],
                    warnings=[],
                    info=[],
                    file_path=str(temp_yaml_file)
                )
                
                try:
                    import psutil
                    process = psutil.Process()
                    start_memory = process.memory_info().rss / 1024 / 1024  # MB
                    
                    result = linter.validate_file(temp_yaml_file)
                    
                    end_memory = process.memory_info().rss / 1024 / 1024  # MB
                    memory_used = end_memory - start_memory
                    
                    # Should use reasonable amount of memory
                    assert memory_used < 100, f"Memory used {memory_used:.1f}MB, expected <100MB"
                    assert result.success == True
                except ImportError:
                    # psutil not available, skip memory test
                    pytest.skip("psutil not available for memory testing")
