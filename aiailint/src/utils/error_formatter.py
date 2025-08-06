"""
Error Message Formatter

Provides consistent error message formatting across all validators.
Follows industry standards for linting tool error messages.
"""

from typing import Optional


class ErrorFormatter:
    """Formats error messages consistently across validators"""
    
    @staticmethod
    def format_error(code: str, message: str, line: Optional[int] = None, 
                    path: Optional[str] = None, command: Optional[str] = None, 
                    fix_suggestion: Optional[str] = None) -> str:
        """
        Format a standardized error message
        
        Args:
            code: Error code (e.g., "E301", "W401")
            message: Error message
            line: Optional line number
            path: Optional path/location information
            command: Optional command that caused the error
            fix_suggestion: Optional suggestion for fixing the error
            
        Returns:
            Formatted error message string
        """
        parts = [f"{code}: {message}"]
        
        # Add location information
        if line is not None:
            parts.append(f"[Line {line}]")
        elif path:
            parts.append(f"[{path}]")
        
        formatted = " ".join(parts)
        
        # Add additional context
        if command:
            formatted += f"\n    Command: {command}"
        
        if fix_suggestion:
            formatted += f"\n    Fix: {fix_suggestion}"
        
        return formatted
    
    @staticmethod
    def format_location(path: str, line: Optional[int] = None) -> str:
        """
        Format location information consistently
        
        Args:
            path: File path or element path
            line: Optional line number
            
        Returns:
            Formatted location string
        """
        if line is not None:
            return f"{path}:{line}"
        return path
    
    @staticmethod
    def format_issue_with_context(severity: str, code: str, message: str, 
                                 context: dict = None) -> str:
        """
        Format issue with additional context information
        
        Args:
            severity: Issue severity ("error", "warning", "info")
            code: Error/warning code
            message: Issue message
            context: Optional context dictionary with additional info
            
        Returns:
            Formatted issue string
        """
        # Severity symbols
        symbols = {
            "error": "✗",
            "warning": "⚠", 
            "info": "ℹ"
        }
        
        symbol = symbols.get(severity, "•")
        formatted = f"{symbol} {code}: {message}"
        
        if context:
            # Add location if available
            if 'line' in context:
                formatted += f" [Line {context['line']}]"
            elif 'path' in context:
                formatted += f" [{context['path']}]"
            
            # Add command context
            if 'command' in context:
                formatted += f"\n    Command: {context['command']}"
            
            # Add fix suggestion
            if 'fix' in context:
                formatted += f"\n    Fix: {context['fix']}"
            
            # Add reason
            if 'reason' in context:
                formatted += f"\n    Reason: {context['reason']}"
        
        return formatted
    
    @staticmethod
    def create_summary(errors: int, warnings: int, info: int = 0) -> str:
        """
        Create a summary message for validation results
        
        Args:
            errors: Number of errors
            warnings: Number of warnings  
            info: Number of info messages
            
        Returns:
            Summary string
        """
        if errors == 0 and warnings == 0 and info == 0:
            return "✓ No issues found"
        
        parts = []
        if errors > 0:
            parts.append(f"{errors} error{'s' if errors != 1 else ''}")
        if warnings > 0:
            parts.append(f"{warnings} warning{'s' if warnings != 1 else ''}")
        if info > 0:
            parts.append(f"{info} info")
        
        issue_text = ", ".join(parts)
        status = "✗ Failed" if errors > 0 else "⚠ Passed"
        
        return f"{status} with {issue_text}"
    
    @staticmethod
    def format_business_rule_error(rule_id: str, element_id: str, reason: str, 
                                  location: str = "", fix: str = "") -> str:
        """
        Format business rule violation error
        
        Args:
            rule_id: Business rule identifier (e.g., "BR001")
            element_id: ID of the element that violates the rule
            reason: Reason for the violation
            location: Location of the violation
            fix: Suggested fix
            
        Returns:
            Formatted business rule error
        """
        message = f"Business rule {rule_id} violation in '{element_id}': {reason}"
        
        if location:
            message += f" at {location}"
        
        if fix:
            message += f"\n    Fix: {fix}"
        
        return message
    
    @staticmethod
    def format_destructive_command_error(command_id: str, command: str, 
                                       reason: str, location: str = "") -> str:
        """
        Format destructive command error with safety focus
        
        Args:
            command_id: Command identifier
            command: The actual command
            reason: Why it's considered destructive
            location: Location in the script
            
        Returns:
            Formatted destructive command error
        """
        error_msg = f"Destructive command not marked as destructive: {command_id}"
        
        if reason:
            error_msg += f" ({reason})"
        
        if location:
            error_msg += f" at {location}"
        
        error_msg += f"\n    Command: {command}"
        error_msg += f"\n    Fix: Add 'destructive: true' to this command"
        error_msg += f"\n    Safety: This command can cause irreversible changes"
        
        return error_msg
    
    @staticmethod
    def format_loop_detection_error(loop_type: str, cycle: list) -> str:
        """
        Format loop detection error
        
        Args:
            loop_type: Type of loop ("command", "script")
            cycle: List of IDs in the cycle
            
        Returns:
            Formatted loop detection error
        """
        cycle_str = " → ".join(cycle + [cycle[0]])
        
        if loop_type == "command":
            return f"Infinite loop detected in command references: {cycle_str}"
        elif loop_type == "script":
            return f"Circular reference detected in script paths: {cycle_str}"
        else:
            return f"Loop detected in {loop_type}: {cycle_str}"
    
    @staticmethod
    def format_schema_error(error_path: str, expected: str, actual: str, 
                           value: str = "") -> str:
        """
        Format JSON schema validation error
        
        Args:
            error_path: Path to the problematic element
            expected: Expected value/type
            actual: Actual value/type found
            value: Optional actual value
            
        Returns:
            Formatted schema error
        """
        error_msg = f"Schema validation failed at {error_path}"
        error_msg += f"\n    Expected: {expected}"
        error_msg += f"\n    Found: {actual}"
        
        if value:
            error_msg += f"\n    Value: {value}"
        
        return error_msg