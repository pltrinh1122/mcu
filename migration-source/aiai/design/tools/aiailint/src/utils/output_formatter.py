"""
Output Formatters for aiailint

Provides text and JSON output formatting following industry standards.
Supports both human-readable and machine-readable output formats.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from abc import ABC, abstractmethod
from utils.validation_result import ValidationResult


class OutputFormatter(ABC):
    """Abstract base class for output formatters"""
    
    @abstractmethod
    def format_result(self, result: ValidationResult, target_path: Path, package_mode: bool = False) -> str:
        """Format validation result for output"""
        pass


class TextFormatter(OutputFormatter):
    """Human-readable text output formatter with colors and formatting"""
    
    def __init__(self, verbose=False, use_colors=True):
        self.verbose = verbose
        self.use_colors = use_colors and self._supports_color()
    
    def _supports_color(self) -> bool:
        """Check if terminal supports colors"""
        import os
        import sys
        
        # Check if output is being redirected
        if not sys.stdout.isatty():
            return False
        
        # Check for color support
        term = os.environ.get('TERM', '')
        if term in ['dumb', '']:
            return False
        
        return True
    
    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are supported"""
        if not self.use_colors:
            return text
        
        colors = {
            'red': '\033[91m',
            'yellow': '\033[93m',
            'green': '\033[92m',
            'blue': '\033[94m',
            'bold': '\033[1m',
            'reset': '\033[0m'
        }
        
        return f"{colors.get(color, '')}{text}{colors.get('reset', '')}"
    
    def format_result(self, result: ValidationResult, target_path: Path, package_mode: bool = False) -> str:
        """Format validation result as human-readable text"""
        output_lines = []
        
        # Header
        target_type = "AIAI Package" if package_mode else "AIAI Script"
        header = f"=== Validating {target_type}: {target_path} ==="
        output_lines.append(self._colorize(header, 'bold'))
        output_lines.append("")
        
        # Summary line
        if result.success and not result.has_issues:
            summary = "✓ Validation passed with no issues"
            output_lines.append(self._colorize(summary, 'green'))
        elif result.success:
            summary = f"✓ Validation passed with {len(result.warnings)} warning(s)"
            output_lines.append(self._colorize(summary, 'yellow'))
        else:
            summary = f"✗ Validation failed with {len(result.errors)} error(s)"
            output_lines.append(self._colorize(summary, 'red'))
        
        output_lines.append("")
        
        # Detailed issues
        if result.errors:
            output_lines.append(self._colorize("ERRORS:", 'red'))
            for error in result.errors:
                output_lines.append(f"  {self._colorize('✗', 'red')} {error}")
            output_lines.append("")
        
        if result.warnings:
            output_lines.append(self._colorize("WARNINGS:", 'yellow'))
            for warning in result.warnings:
                output_lines.append(f"  {self._colorize('⚠', 'yellow')} {warning}")
            output_lines.append("")
        
        if result.info and self.verbose:
            output_lines.append(self._colorize("INFO:", 'blue'))
            for info in result.info:
                output_lines.append(f"  {self._colorize('ℹ', 'blue')} {info}")
            output_lines.append("")
        
        # Summary statistics
        output_lines.append(self._colorize("SUMMARY:", 'bold'))
        output_lines.append(f"  Files Processed: 1")
        output_lines.append(f"  Errors: {len(result.errors)}")
        output_lines.append(f"  Warnings: {len(result.warnings)}")
        output_lines.append(f"  Info: {len(result.info)}")
        output_lines.append("")
        
        # Final status
        if result.success:
            if result.warnings:
                status = "Validation PASSED with warnings."
            else:
                status = "Validation PASSED."
            output_lines.append(self._colorize(status, 'green'))
        else:
            status = "Validation FAILED due to errors."
            output_lines.append(self._colorize(status, 'red'))
        
        return "\n".join(output_lines)


class JsonFormatter(OutputFormatter):
    """Machine-readable JSON output formatter for CI/CD integration"""
    
    def __init__(self):
        pass
    
    def format_result(self, result: ValidationResult, target_path: Path, package_mode: bool = False) -> str:
        """Format validation result as JSON"""
        # Convert validation result to structured data
        output_data = {
            "aiailint_version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "target": {
                "path": str(target_path),
                "type": "package" if package_mode else "file"
            },
            "validation": {
                "status": "passed" if result.success else "failed",
                "errors": len(result.errors),
                "warnings": len(result.warnings),
                "info": len(result.info)
            },
            "issues": self._format_issues(result),
            "summary": {
                "total_files": 1,
                "passed": 1 if result.success else 0,
                "failed": 0 if result.success else 1,
                "errors": len(result.errors),
                "warnings": len(result.warnings),
                "info": len(result.info)
            },
            "exit_code": 0 if result.success else (2 if result.warnings and not result.errors else 1)
        }
        
        return json.dumps(output_data, indent=2, ensure_ascii=False)
    
    def _format_issues(self, result: ValidationResult) -> List[Dict[str, Any]]:
        """Format issues for JSON output"""
        issues = []
        
        # Add errors
        for error in result.errors:
            issue = self._parse_issue_message(error, "error")
            issues.append(issue)
        
        # Add warnings
        for warning in result.warnings:
            issue = self._parse_issue_message(warning, "warning") 
            issues.append(issue)
        
        # Add info
        for info in result.info:
            issue = self._parse_issue_message(info, "info")
            issues.append(issue)
        
        return issues
    
    def _parse_issue_message(self, message: str, severity: str) -> Dict[str, Any]:
        """Parse issue message to extract structured information"""
        import re
        
        # Try to extract error code
        code_match = re.match(r'([EWI]\d+):\s*(.*)', message)
        if code_match:
            code = code_match.group(1)
            remaining_message = code_match.group(2)
        else:
            code = ""
            remaining_message = message
        
        # Try to extract location information
        location_match = re.search(r'\s+at\s+(.+)$', remaining_message)
        location = ""
        if location_match:
            location = location_match.group(1)
            remaining_message = remaining_message[:location_match.start()]
        
        # Try to extract line number
        line_match = re.search(r'\[Line\s+(\d+)\]', remaining_message)
        line = None
        if line_match:
            line = int(line_match.group(1))
            remaining_message = re.sub(r'\s*\[Line\s+\d+\]\s*', ' ', remaining_message)
        
        # Clean up the message
        clean_message = remaining_message.strip()
        
        issue = {
            "severity": severity,
            "message": clean_message,
        }
        
        if code:
            issue["code"] = code
        if line is not None:
            issue["line"] = line
        if location:
            issue["location"] = location
        
        return issue


class ErrorFormatter:
    """Utility class for formatting error messages consistently"""
    
    @staticmethod
    def format_error(code: str, message: str, line: int = None, path: str = None, 
                    command: str = None, fix_suggestion: str = None) -> str:
        """Format a standardized error message"""
        parts = [f"{code}: {message}"]
        
        if line is not None:
            parts.append(f"[Line {line}]")
        elif path:
            parts.append(f"[{path}]")
        
        formatted = " ".join(parts)
        
        if command:
            formatted += f"\n    Command: {command}"
        
        if fix_suggestion:
            formatted += f"\n    Fix: {fix_suggestion}"
        
        return formatted
    
    @staticmethod
    def format_location(path: str, line: int = None) -> str:
        """Format location information consistently"""
        if line is not None:
            return f"{path}:{line}"
        return path