"""
Semantic Validator for AIAI Scripts

Validates shell commands for semantic correctness using bash parsers.
Error Codes: E200-E299 (Semantic validation errors)
"""

from pathlib import Path
from typing import Dict, Any, List
from utils.validation_result import ValidationResult
from analyzers.bash_analyzer import BashAnalyzer


class SemanticValidator:
    """Validates shell commands for semantic correctness"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.bash_analyzer = BashAnalyzer(verbose=verbose)
    
    def validate(self, data: Dict[str, Any], file_path: Path) -> ValidationResult:
        """
        Validate AIAI Script for semantic correctness
        
        Args:
            data: Parsed AIAI Script data
            file_path: Path to the file being validated
            
        Returns:
            ValidationResult with semantic validation results
        """
        errors = []
        warnings = []
        info = []
        
        if self.verbose:
            print("→ Running semantic validation...")
        
        # Extract all shell commands
        commands = self._extract_shell_commands(data)
        
        for cmd_info in commands:
            command_text = cmd_info['command']
            cmd_id = cmd_info.get('id', 'unknown')
            location = cmd_info.get('location', '')
            cmd_type = cmd_info.get('type', 'command')
            
            # Analyze command semantically
            analysis = self.bash_analyzer.analyze_command(command_text)
            
            if not analysis.success:
                if analysis.error:
                    errors.append(f"E200: Cannot parse shell command in {cmd_id}: {analysis.error} at {location}")
                else:
                    errors.append(f"E201: Shell command parsing failed for {cmd_id} at {location}")
                continue
            
            # Check for problematic command patterns
            command_issues = self._check_command_issues(analysis, cmd_id, location)
            errors.extend(command_issues['errors'])
            warnings.extend(command_issues['warnings'])
            
            # Check for security concerns
            security_issues = self._check_security_issues(analysis, cmd_id, location)
            warnings.extend(security_issues)
            
            # Provide informational analysis
            info_items = self._generate_command_info(analysis, cmd_id, cmd_type)
            info.extend(info_items)
        
        if self.verbose:
            if errors:
                print(f"  ✗ Found {len(errors)} semantic errors")
            elif warnings:
                print(f"  ⚠ Found {len(warnings)} semantic warnings")
            else:
                print("  ✓ Semantic validation passed")
        
        success = len(errors) == 0
        return ValidationResult(success, errors, warnings, info, str(file_path))
    
    def _extract_shell_commands(self, data: Dict[str, Any], path="") -> List[Dict[str, Any]]:
        """Extract all shell commands from AIAI Script"""
        commands = []
        
        if isinstance(data, dict):
            # Extract shellCommand from commands
            if data.get('type') == 'command' and 'shellCommand' in data:
                commands.append({
                    'command': data['shellCommand'],
                    'id': data.get('id', 'unknown'),
                    'location': path,
                    'type': 'command'
                })
            
            # Extract command from validations
            elif data.get('type') == 'validation' and 'command' in data:
                commands.append({
                    'command': data['command'],
                    'id': data.get('id', 'unknown'),
                    'location': path,
                    'type': 'validation'
                })
            
            # Recursively search nested structures
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                commands.extend(self._extract_shell_commands(value, new_path))
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                commands.extend(self._extract_shell_commands(item, new_path))
        
        return commands
    
    def _check_command_issues(self, analysis, cmd_id: str, location: str) -> Dict[str, List[str]]:
        """Check for problematic command patterns"""
        errors = []
        warnings = []
        
        # Check for empty or whitespace-only commands
        if not analysis.command.strip():
            errors.append(f"E202: Empty shell command in {cmd_id} at {location}")
            return {'errors': errors, 'warnings': warnings}
        
        # Check for very long commands (potential embedded scripts)
        if len(analysis.command) > 500:
            warnings.append(f"W200: Very long shell command in {cmd_id} ({len(analysis.command)} chars) at {location}")
        
        # Check for commands with no clear purpose
        if not analysis.command_name:
            warnings.append(f"W201: Cannot determine command name for {cmd_id} at {location}")
        
        # Check for potentially problematic command combinations
        if analysis.command_type == "pipeline" and len(analysis.arguments) > 10:
            warnings.append(f"W202: Complex pipeline with many arguments in {cmd_id} at {location}")
        
        # Check for sudo usage without marking as destructive
        if analysis.uses_sudo:
            warnings.append(f"W203: Command uses sudo but may not be marked as destructive: {cmd_id} at {location}")
        
        return {'errors': errors, 'warnings': warnings}
    
    def _check_security_issues(self, analysis, cmd_id: str, location: str) -> List[str]:
        """Check for security-related issues in commands"""
        warnings = []
        
        for issue in analysis.potential_security_issues:
            warnings.append(f"W210: Security concern in {cmd_id}: {issue} at {location}")
        
        # Additional security checks
        command_lower = analysis.command.lower()
        
        # Check for hardcoded credentials patterns
        credential_patterns = ['password=', 'token=', 'secret=', 'key=', 'passwd=']
        for pattern in credential_patterns:
            if pattern in command_lower:
                warnings.append(f"W211: Potential hardcoded credential in {cmd_id} at {location}")
        
        # Check for network operations without validation
        network_commands = ['curl', 'wget', 'ssh', 'scp', 'rsync']
        if analysis.command_name in network_commands:
            warnings.append(f"W212: Network operation in {cmd_id} - ensure proper validation at {location}")
        
        return warnings
    
    def _generate_command_info(self, analysis, cmd_id: str, cmd_type: str) -> List[str]:
        """Generate informational messages about command analysis"""
        info = []
        
        # Only provide info in verbose mode
        if not self.verbose:
            return info
        
        # Command classification info
        if analysis.command_type != "unknown":
            info.append(f"I200: Command {cmd_id} classified as: {analysis.command_type}")
        
        # Variable usage info
        if analysis.variables_read:
            vars_read = ', '.join(sorted(analysis.variables_read))
            info.append(f"I201: Command {cmd_id} reads variables: {vars_read}")
        
        if analysis.variables_written:
            vars_written = ', '.join(sorted(analysis.variables_written))
            info.append(f"I202: Command {cmd_id} writes variables: {vars_written}")
        
        # Redirection info
        if analysis.has_redirections:
            redirections = ', '.join(analysis.redirections)
            info.append(f"I203: Command {cmd_id} uses redirections: {redirections}")
        
        return info


def validate_semantics(data: Dict[str, Any], file_path: str = "", verbose=False) -> ValidationResult:
    """
    Standalone function to validate semantic correctness
    
    Args:
        data: AIAI Script data to validate
        file_path: Path to file being validated
        verbose: Enable verbose output
        
    Returns:
        ValidationResult with semantic validation results
    """
    validator = SemanticValidator(verbose=verbose)
    return validator.validate(data, Path(file_path))