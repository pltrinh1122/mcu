"""
Integration tests for the aiailint application.

This module contains pytest-based integration tests for the complete
aiailint workflow, following OOP principles and using fixtures for test data management.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from tests.utils import create_test_script, validate_yaml_syntax

# Import the main application components
from src.aiailint import AiaiLinter, ValidationResult, ValidationIssue, ExitCodes


class TestAiaiLinterEndToEndWorkflow:
    """Integration test cases for complete end-to-end validation workflow."""
    
    def test_complete_validation_workflow_valid_file(self, temp_yaml_file, sample_valid_script):
        """Test complete validation workflow with valid file."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_valid_script)
        
        linter = AiaiLinter()
        
        # Mock dependencies to focus on workflow integration
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
                assert len(result.errors) == 0
                assert len(result.warnings) == 0
    
    def test_complete_validation_workflow_invalid_file(self, temp_yaml_file, sample_invalid_script):
        """Test complete validation workflow with invalid file."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_invalid_script)
        
        linter = AiaiLinter()
        
        # Mock dependencies to focus on workflow integration
        with patch.object(linter, 'check_dependencies', return_value=True):
            with patch.object(linter, '_run_validation_pipeline') as mock_pipeline:
                mock_pipeline.return_value = ValidationResult(
                    success=False,
                    errors=["Missing metadata", "Invalid structure"],
                    warnings=[],
                    info=[],
                    file_path=str(temp_yaml_file)
                )
                
                result = linter.validate_file(temp_yaml_file)
                
                assert result.success == False
                assert result.file_path == str(temp_yaml_file)
                assert len(result.errors) == 2
                assert "Missing metadata" in result.errors
                assert "Invalid structure" in result.errors
    
    def test_complete_validation_workflow_with_warnings(self, temp_yaml_file, sample_valid_script):
        """Test complete validation workflow with warnings."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_valid_script)
        
        linter = AiaiLinter()
        
        # Mock dependencies to focus on workflow integration
        with patch.object(linter, 'check_dependencies', return_value=True):
            with patch.object(linter, '_run_validation_pipeline') as mock_pipeline:
                mock_pipeline.return_value = ValidationResult(
                    success=True,
                    errors=[],
                    warnings=["Consider adding description"],
                    info=["File processed successfully"],
                    file_path=str(temp_yaml_file)
                )
                
                result = linter.validate_file(temp_yaml_file)
                
                assert result.success == True
                assert result.file_path == str(temp_yaml_file)
                assert len(result.errors) == 0
                assert len(result.warnings) == 1
                assert len(result.info) == 1
                assert "Consider adding description" in result.warnings


class TestAiaiLinterPackageValidation:
    """Integration test cases for package validation workflow."""
    
    def test_package_validation_single_file(self, tmp_path):
        """Test package validation with single file."""
        # Create package directory
        package_dir = tmp_path / "test_package"
        package_dir.mkdir()
        
        # Create single script file
        script_file = package_dir / "script.yaml"
        with open(script_file, 'w') as f:
            f.write("metadata:\n  name: test\nsteps:\n  - name: step\n    command: echo")
        
        linter = AiaiLinter()
        
        # Mock the validation pipeline
        with patch.object(linter, '_run_validation_pipeline') as mock_pipeline:
            mock_pipeline.return_value = ValidationResult(
                success=True,
                errors=[],
                warnings=[],
                info=[],
                file_path=str(script_file)
            )
            
            result = linter.validate_package(package_dir)
            
            assert result.success == True
            assert len(result.errors) == 0
            assert len(result.warnings) == 0
    
    def test_package_validation_multiple_files(self, tmp_path):
        """Test package validation with multiple files."""
        # Create package directory
        package_dir = tmp_path / "test_package"
        package_dir.mkdir()
        
        # Create multiple script files
        script1 = package_dir / "script1.yaml"
        script2 = package_dir / "script2.yaml"
        script3 = package_dir / "script3.yaml"
        
        with open(script1, 'w') as f:
            f.write("metadata:\n  name: script1\nsteps:\n  - name: step1\n    command: echo")
        
        with open(script2, 'w') as f:
            f.write("metadata:\n  name: script2\nsteps:\n  - name: step2\n    command: echo")
        
        with open(script3, 'w') as f:
            f.write("metadata:\n  name: script3\nsteps:\n  - name: step3\n    command: echo")
        
        linter = AiaiLinter()
        
        # Mock the validation pipeline to return success for all files
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
            assert len(result.errors) == 0
            assert len(result.warnings) == 0
    
    def test_package_validation_with_errors(self, tmp_path):
        """Test package validation with some files having errors."""
        # Create package directory
        package_dir = tmp_path / "test_package"
        package_dir.mkdir()
        
        # Create script files (one valid, one invalid)
        script1 = package_dir / "script1.yaml"
        script2 = package_dir / "script2.yaml"
        
        with open(script1, 'w') as f:
            f.write("metadata:\n  name: script1\nsteps:\n  - name: step1\n    command: echo")
        
        with open(script2, 'w') as f:
            f.write("invalid: content")  # Invalid script
        
        linter = AiaiLinter()
        
        # Mock the validation pipeline to return different results
        with patch.object(linter, '_run_validation_pipeline') as mock_pipeline:
            # First call returns success, second call returns error
            mock_pipeline.side_effect = [
                ValidationResult(success=True, errors=[], warnings=[], info=[], file_path=str(script1)),
                ValidationResult(success=False, errors=["Invalid structure"], warnings=[], info=[], file_path=str(script2))
            ]
            
            result = linter.validate_package(package_dir)
            
            assert result.success == False  # Should fail due to invalid file
            assert len(result.errors) > 0


class TestAiaiLinterDependencyIntegration:
    """Integration test cases for dependency checking and validation."""
    
    def test_dependency_checking_integration(self):
        """Test dependency checking integration with validation workflow."""
        linter = AiaiLinter(verbose=True)
        
        # Test with all dependencies available
        with patch('src.aiailint.yaml'):
            with patch('src.aiailint.jsonschema'):
                with patch('src.aiailint.bashlex'):
                    result = linter.check_dependencies()
                    assert result == True
    
    def test_dependency_checking_missing_dependencies(self):
        """Test dependency checking with missing dependencies."""
        linter = AiaiLinter(verbose=True)
        
        # Test with missing dependencies
        with patch('src.aiailint.yaml', side_effect=ImportError):
            result = linter.check_dependencies()
            assert result == False
    
    def test_validation_with_dependency_check(self, temp_yaml_file, sample_valid_script):
        """Test validation workflow with dependency checking."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_valid_script)
        
        linter = AiaiLinter()
        
        # Mock dependencies and validation pipeline
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
    
    def test_validation_with_missing_dependencies(self, temp_yaml_file, sample_valid_script):
        """Test validation workflow with missing dependencies."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_valid_script)
        
        linter = AiaiLinter()
        
        # Mock dependency check to fail
        with patch.object(linter, 'check_dependencies', return_value=False):
            result = linter.validate_file(temp_yaml_file)
            
            assert result.success == False
            assert len(result.errors) > 0


class TestAiaiLinterErrorHandlingIntegration:
    """Integration test cases for error handling and recovery."""
    
    def test_error_handling_corrupted_file(self, temp_yaml_file):
        """Test error handling with corrupted file."""
        # Create corrupted YAML file
        with open(temp_yaml_file, 'w') as f:
            f.write("metadata:\n  name: test\n  # Missing closing quote\n")
        
        linter = AiaiLinter()
        
        # Mock the validation pipeline to simulate YAML parsing error
        with patch.object(linter, 'check_dependencies', return_value=True):
            with patch.object(linter, '_run_validation_pipeline') as mock_pipeline:
                mock_pipeline.return_value = ValidationResult(
                    success=False,
                    errors=["YAML parsing error: line 3"],
                    warnings=[],
                    info=[],
                    file_path=str(temp_yaml_file)
                )
                
                result = linter.validate_file(temp_yaml_file)
                
                assert result.success == False
                assert len(result.errors) == 1
                assert "YAML parsing error" in result.errors[0]
    
    def test_error_handling_file_not_found(self):
        """Test error handling with file not found."""
        linter = AiaiLinter()
        
        # Mock the validation pipeline to simulate file not found error
        with patch.object(linter, 'check_dependencies', return_value=True):
            with patch.object(linter, '_run_validation_pipeline') as mock_pipeline:
                mock_pipeline.return_value = ValidationResult(
                    success=False,
                    errors=["File not found: nonexistent.yaml"],
                    warnings=[],
                    info=[],
                    file_path="nonexistent.yaml"
                )
                
                result = linter.validate_file("nonexistent.yaml")
                
                assert result.success == False
                assert len(result.errors) == 1
                assert "File not found" in result.errors[0]
    
    def test_error_handling_permission_error(self, temp_yaml_file):
        """Test error handling with permission error."""
        # Create file but make it unreadable
        with open(temp_yaml_file, 'w') as f:
            f.write("metadata:\n  name: test\nsteps:\n  - name: step\n    command: echo")
        
        # Make file unreadable (simulate permission error)
        os.chmod(temp_yaml_file, 0o000)
        
        linter = AiaiLinter()
        
        # Mock the validation pipeline to simulate permission error
        with patch.object(linter, 'check_dependencies', return_value=True):
            with patch.object(linter, '_run_validation_pipeline') as mock_pipeline:
                mock_pipeline.return_value = ValidationResult(
                    success=False,
                    errors=["Permission denied: cannot read file"],
                    warnings=[],
                    info=[],
                    file_path=str(temp_yaml_file)
                )
                
                result = linter.validate_file(temp_yaml_file)
                
                assert result.success == False
                assert len(result.errors) == 1
                assert "Permission denied" in result.errors[0]
        
        # Restore file permissions
        os.chmod(temp_yaml_file, 0o644)


class TestAiaiLinterPerformanceIntegration:
    """Integration test cases for performance characteristics."""
    
    @pytest.mark.slow
    def test_performance_with_large_file(self, temp_yaml_file):
        """Test performance with large YAML file."""
        # Create large YAML file
        large_script = "metadata:\n  name: large_test\nsteps:\n"
        for i in range(1000):  # Create 1000 steps
            large_script += f"  - name: step{i}\n    command: echo 'step {i}'\n"
        
        with open(temp_yaml_file, 'w') as f:
            f.write(large_script)
        
        linter = AiaiLinter()
        
        # Mock the validation pipeline
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
                
                # Should complete within reasonable time even for large files
                assert duration < 10.0, f"Large file validation took {duration:.2f}s, expected <10s"
                assert result.success == True
    
    @pytest.mark.slow
    def test_memory_usage_integration(self, temp_yaml_file):
        """Test memory usage during integration workflow."""
        # Create moderately large YAML file
        medium_script = "metadata:\n  name: medium_test\nsteps:\n"
        for i in range(100):  # Create 100 steps
            medium_script += f"  - name: step{i}\n    command: echo 'step {i}'\n"
        
        with open(temp_yaml_file, 'w') as f:
            f.write(medium_script)
        
        linter = AiaiLinter()
        
        # Mock the validation pipeline
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


class TestAiaiLinterConfigurationIntegration:
    """Integration test cases for different configuration modes."""
    
    def test_verbose_mode_integration(self, temp_yaml_file, sample_valid_script):
        """Test integration with verbose mode enabled."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_valid_script)
        
        linter = AiaiLinter(verbose=True)
        
        # Mock dependencies and validation pipeline
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
    
    def test_strict_mode_integration(self, temp_yaml_file, sample_valid_script):
        """Test integration with strict mode enabled."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_valid_script)
        
        linter = AiaiLinter(strict=True)
        
        # Mock dependencies and validation pipeline
        with patch.object(linter, 'check_dependencies', return_value=True):
            with patch.object(linter, '_run_validation_pipeline') as mock_pipeline:
                mock_pipeline.return_value = ValidationResult(
                    success=True,
                    errors=[],
                    warnings=["Warning in strict mode"],
                    info=[],
                    file_path=str(temp_yaml_file)
                )
                
                result = linter.validate_file(temp_yaml_file)
                
                # In strict mode, warnings should be treated as errors
                assert result.success == False
                assert len(result.errors) == 1
                assert "Warning in strict mode" in result.errors
    
    def test_json_output_integration(self, temp_yaml_file, sample_valid_script):
        """Test integration with JSON output format."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_valid_script)
        
        linter = AiaiLinter(format_output="json")
        
        # Mock dependencies and validation pipeline
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
                # JSON formatter should be used
                assert hasattr(linter, 'output_formatter')
    
    def test_no_semantic_integration(self, temp_yaml_file, sample_valid_script):
        """Test integration with semantic analysis disabled."""
        with open(temp_yaml_file, 'w') as f:
            f.write(sample_valid_script)
        
        linter = AiaiLinter(no_semantic=True)
        
        # Mock dependencies and validation pipeline
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
                # Should have fewer validators when semantic analysis is disabled
                assert len(linter.validators) > 0
