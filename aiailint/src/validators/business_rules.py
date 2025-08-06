"""
Business Rules Validator for AIAI Scripts

Validates AIAI Scripts against business rules for safety and best practices.
Error Codes: E300-E699 (Business rule violations)

Priority 1 Rules:
- BR001: Destructive command validation (E301-E399)
- BR002: Logic check promotion (W401-W499) 
- BR003: Loop detection (E501-E599)
- BR004: Cross-reference validation (E601-E699)
"""

from pathlib import Path
from typing import Dict, Any, List, Set, Tuple
from utils.validation_result import ValidationResult
from analyzers.bash_analyzer import BashAnalyzer, CommandAnalysis


class BusinessRulesValidator:
    """Validates AIAI Scripts against business rules for safety"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.bash_analyzer = BashAnalyzer(verbose=verbose)
    
    def validate(self, data: Dict[str, Any], file_path: Path) -> ValidationResult:
        """
        Validate AIAI Script against business rules
        
        Args:
            data: Parsed AIAI Script data
            file_path: Path to the file being validated
            
        Returns:
            ValidationResult with business rule validation results
        """
        errors = []
        warnings = []
        info = []
        
        if self.verbose:
            print("→ Running business rules validation...")
        
        # BR001: Destructive command validation (Priority 1)
        destructive_issues = self._validate_destructive_commands(data)
        errors.extend(destructive_issues['errors'])
        warnings.extend(destructive_issues['warnings'])
        
        # BR002: Logic check promotion (Priority 1)  
        logic_issues = self._validate_logic_checks(data)
        warnings.extend(logic_issues['warnings'])
        info.extend(logic_issues['info'])
        
        # BR003: Loop detection (Priority 1) - handled by cross_reference validator
        # BR004: Cross-reference validation (Priority 1) - handled by cross_reference validator
        
        # Additional business rules
        consistency_issues = self._validate_consistency(data)
        warnings.extend(consistency_issues['warnings'])
        
        if self.verbose:
            if errors:
                print(f"  ✗ Found {len(errors)} business rule errors")
            elif warnings:
                print(f"  ⚠ Found {len(warnings)} business rule warnings")
            else:
                print("  ✓ Business rules validation passed")
        
        success = len(errors) == 0
        return ValidationResult(success, errors, warnings, info, str(file_path))
    
    def _validate_destructive_commands(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        BR001: Validate destructive command marking and detection
        
        Priority 1: Commands that perform destructive operations MUST be marked with destructive: true
        """
        errors = []
        warnings = []
        
        # Find all commands in the script
        commands = self._extract_all_commands(data)
        
        for cmd_info in commands:
            command_text = cmd_info['shellCommand']
            destructive_flag = cmd_info.get('destructive', False)
            cmd_id = cmd_info.get('id', 'unknown')
            location = cmd_info.get('location', '')
            
            # Analyze command for destructive operations
            analysis = self.bash_analyzer.analyze_command(command_text)
            
            if not analysis.success:
                # If we can't analyze the command, issue a warning
                warnings.append(f"W302: Cannot analyze command for destructive operations: {cmd_id}")
                continue
            
            # Check for destructive operations not marked as destructive
            if analysis.is_destructive and not destructive_flag:
                reason = analysis.destructive_reason or "contains destructive operations"
                fix_suggestion = f"Add 'destructive: true' to command '{cmd_id}'"
                errors.append(f"E301: Destructive command not marked as destructive: {cmd_id} ({reason}) at {location}")
                if self.verbose:
                    print(f"    Command: {command_text}")
                    print(f"    Fix: {fix_suggestion}")
            
            # Check for commands marked destructive but appear safe
            elif destructive_flag and not analysis.is_destructive:
                warnings.append(f"W301: Command marked destructive but appears safe: {cmd_id} at {location}")
                if self.verbose:
                    print(f"    Command: {command_text}")
                    print(f"    Consider removing 'destructive: true' or verify the command is actually destructive")
            
            # Check for security issues in destructive commands
            if analysis.is_destructive and analysis.potential_security_issues:
                for issue in analysis.potential_security_issues:
                    warnings.append(f"W303: Security concern in destructive command {cmd_id}: {issue}")
        
        return {'errors': errors, 'warnings': warnings}
    
    def _validate_logic_checks(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        BR002: Validate logic check promotion to validation elements
        
        Commands containing logic checks SHOULD be promoted to validation elements
        """
        warnings = []
        info = []
        
        # Find all commands in the script
        commands = self._extract_all_commands(data)
        
        for cmd_info in commands:
            command_text = cmd_info['shellCommand']
            cmd_id = cmd_info.get('id', 'unknown')
            location = cmd_info.get('location', '')
            cmd_type = cmd_info.get('type', 'command')
            
            # Skip if this is already a validation element
            if cmd_type == 'validation':
                continue
            
            # Analyze command for logic checks
            analysis = self.bash_analyzer.analyze_command(command_text)
            
            if analysis.success and analysis.has_logic_checks:
                # Suggest promotion to validation element
                patterns = ', '.join(analysis.logic_patterns)
                suggestion = f"Consider converting command '{cmd_id}' to validation element"
                warnings.append(f"W401: Command contains logic check, consider validation element: {cmd_id} ({patterns}) at {location}")
                
                if self.verbose:
                    print(f"    Command: {command_text}")
                    print(f"    Logic patterns: {patterns}")
                    print(f"    Suggestion: {suggestion}")
        
        return {'warnings': warnings, 'info': info}
    
    def _validate_consistency(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate internal consistency of AIAI Script"""
        warnings = []
        
        # Check for consistent ID patterns
        id_issues = self._check_id_consistency(data)
        warnings.extend(id_issues)
        
        # Check for intent quality
        intent_issues = self._check_intent_quality(data)
        warnings.extend(intent_issues)
        
        return {'warnings': warnings}
    
    def _check_id_consistency(self, data: Dict[str, Any]) -> List[str]:
        """Check for consistent ID naming patterns"""
        warnings = []
        
        # Collect all IDs
        all_ids = []
        self._collect_ids(data, all_ids)
        
        if not all_ids:
            return warnings
        
        # Check for consistent naming patterns
        patterns = {
            'kebab-case': 0,
            'snake_case': 0,
            'camelCase': 0,
            'mixed': 0
        }
        
        for id_str in all_ids:
            if '-' in id_str and '_' not in id_str:
                patterns['kebab-case'] += 1
            elif '_' in id_str and '-' not in id_str:
                patterns['snake_case'] += 1
            elif any(c.isupper() for c in id_str) and '-' not in id_str and '_' not in id_str:
                patterns['camelCase'] += 1
            else:
                patterns['mixed'] += 1
        
        # Find dominant pattern
        dominant_pattern = max(patterns.items(), key=lambda x: x[1])
        total_ids = len(all_ids)
        
        if dominant_pattern[1] < total_ids * 0.8:  # Less than 80% consistency
            warnings.append(f"W501: Inconsistent ID naming patterns detected (consider using {dominant_pattern[0]})")
        
        return warnings
    
    def _check_intent_quality(self, data: Dict[str, Any]) -> List[str]:
        """Check quality of intent descriptions"""
        warnings = []
        
        # Check metadata intent
        metadata = data.get('metadata', {})
        if 'intent' in metadata:
            intent = metadata['intent']
            if len(intent.strip()) < 20:
                warnings.append("W502: Main script intent description is very short")
        
        # Check command and script intents
        intents = []
        self._collect_intents(data, intents)
        
        for intent_info in intents:
            intent = intent_info['intent']
            item_id = intent_info['id']
            location = intent_info['location']
            
            if len(intent.strip()) < 10:
                warnings.append(f"W503: Very short intent description for {item_id} at {location}")
            elif intent.strip().lower() == intent_info['id'].lower().replace('-', ' ').replace('_', ' '):
                warnings.append(f"W504: Intent description is just a rewording of ID for {item_id} at {location}")
        
        return warnings
    
    def _extract_all_commands(self, data: Dict[str, Any], path="") -> List[Dict[str, Any]]:
        """Extract all commands from AIAI Script with location information"""
        commands = []
        
        if isinstance(data, dict):
            # Check if this is a command
            if data.get('type') == 'command' and 'shellCommand' in data:
                cmd_info = data.copy()
                cmd_info['location'] = path
                commands.append(cmd_info)
            
            # Recursively search in all dictionary values
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                commands.extend(self._extract_all_commands(value, new_path))
        
        elif isinstance(data, list):
            # Recursively search in all list items
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                commands.extend(self._extract_all_commands(item, new_path))
        
        return commands
    
    def _collect_ids(self, data: Dict[str, Any], id_list: List[str]):
        """Collect all IDs from the AIAI Script"""
        if isinstance(data, dict):
            if 'id' in data and isinstance(data['id'], str):
                id_list.append(data['id'])
            
            for value in data.values():
                if isinstance(value, (dict, list)):
                    self._collect_ids(value, id_list)
        
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    self._collect_ids(item, id_list)
    
    def _collect_intents(self, data: Dict[str, Any], intent_list: List[Dict[str, str]], path=""):
        """Collect all intent descriptions with location information"""
        if isinstance(data, dict):
            if 'intent' in data and 'id' in data:
                intent_list.append({
                    'intent': data['intent'],
                    'id': data['id'],
                    'location': path
                })
            
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                if isinstance(value, (dict, list)):
                    self._collect_intents(value, intent_list, new_path)
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                if isinstance(item, (dict, list)):
                    self._collect_intents(item, intent_list, new_path)


def validate_business_rules(data: Dict[str, Any], file_path: str = "", verbose=False) -> ValidationResult:
    """
    Standalone function to validate business rules
    
    Args:
        data: AIAI Script data to validate
        file_path: Path to file being validated
        verbose: Enable verbose output
        
    Returns:
        ValidationResult with business rule validation results
    """
    validator = BusinessRulesValidator(verbose=verbose)
    return validator.validate(data, Path(file_path))