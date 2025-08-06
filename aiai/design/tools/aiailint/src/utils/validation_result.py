"""
Validation Result Data Structures

Common data structures used across all validation modules.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ValidationIssue:
    """Individual validation issue with detailed information"""
    code: str
    severity: str  # "error", "warning", "info"
    message: str
    line: Optional[int] = None
    path: Optional[str] = None
    command: Optional[str] = None
    fix_suggestion: Optional[str] = None
    
    def __str__(self) -> str:
        """String representation for display"""
        location = ""
        if self.line:
            location = f" [Line {self.line}]"
        elif self.path:
            location = f" [{self.path}]"
        
        severity_symbol = {
            "error": "✗",
            "warning": "⚠",
            "info": "ℹ"
        }.get(self.severity, "•")
        
        return f"{severity_symbol} {self.code}{location}: {self.message}"


@dataclass  
class ValidationResult:
    """Result of validation operation with structured issue tracking"""
    success: bool
    errors: List[str]
    warnings: List[str] 
    info: List[str]
    file_path: Optional[str] = None
    issues: Optional[List[ValidationIssue]] = None
    
    def __post_init__(self):
        """Initialize issues list if not provided"""
        if self.issues is None:
            self.issues = []
    
    @property
    def has_issues(self) -> bool:
        """Check if there are any validation issues"""
        return len(self.errors) > 0 or len(self.warnings) > 0 or len(self.info) > 0
    
    @property
    def total_issues(self) -> int:
        """Total count of all issues"""
        return len(self.errors) + len(self.warnings) + len(self.info)
    
    def add_error(self, message: str, code: str = "", line: Optional[int] = None, 
                  path: Optional[str] = None, command: Optional[str] = None,
                  fix_suggestion: Optional[str] = None):
        """Add an error to the result"""
        self.errors.append(message)
        if code:
            issue = ValidationIssue(
                code=code,
                severity="error", 
                message=message,
                line=line,
                path=path,
                command=command,
                fix_suggestion=fix_suggestion
            )
            self.issues.append(issue)
        
        # Update success status
        self.success = False
    
    def add_warning(self, message: str, code: str = "", line: Optional[int] = None,
                    path: Optional[str] = None, command: Optional[str] = None,
                    fix_suggestion: Optional[str] = None):
        """Add a warning to the result"""
        self.warnings.append(message)
        if code:
            issue = ValidationIssue(
                code=code,
                severity="warning",
                message=message, 
                line=line,
                path=path,
                command=command,
                fix_suggestion=fix_suggestion
            )
            self.issues.append(issue)
    
    def add_info(self, message: str, code: str = "", line: Optional[int] = None,
                 path: Optional[str] = None, command: Optional[str] = None):
        """Add an info message to the result"""
        self.info.append(message)
        if code:
            issue = ValidationIssue(
                code=code,
                severity="info",
                message=message,
                line=line, 
                path=path,
                command=command
            )
            self.issues.append(issue)
    
    def merge(self, other: 'ValidationResult') -> 'ValidationResult':
        """Merge another validation result into this one"""
        merged_errors = self.errors + other.errors
        merged_warnings = self.warnings + other.warnings
        merged_info = self.info + other.info
        merged_issues = (self.issues or []) + (other.issues or [])
        
        # Success is true only if both results are successful
        merged_success = self.success and other.success
        
        return ValidationResult(
            success=merged_success,
            errors=merged_errors,
            warnings=merged_warnings,
            info=merged_info,
            file_path=self.file_path or other.file_path,
            issues=merged_issues
        )
    
    def apply_strict_mode(self) -> 'ValidationResult':
        """Apply strict mode - treat warnings as errors"""
        if not self.warnings:
            return self
        
        # Convert warnings to errors
        new_errors = self.errors + self.warnings
        
        # Update issues severity
        new_issues = []
        for issue in (self.issues or []):
            if issue.severity == "warning":
                new_issue = ValidationIssue(
                    code=issue.code,
                    severity="error",
                    message=issue.message,
                    line=issue.line,
                    path=issue.path,
                    command=issue.command,
                    fix_suggestion=issue.fix_suggestion
                )
                new_issues.append(new_issue)
            else:
                new_issues.append(issue)
        
        return ValidationResult(
            success=False,  # Has errors now
            errors=new_errors,
            warnings=[],    # No warnings in strict mode
            info=self.info,
            file_path=self.file_path,
            issues=new_issues
        )
    
    def get_summary(self) -> str:
        """Get a summary string of the validation result"""
        if self.success and not self.has_issues:
            return "✓ Validation passed"
        
        parts = []
        if self.errors:
            parts.append(f"{len(self.errors)} error{'s' if len(self.errors) != 1 else ''}")
        if self.warnings:
            parts.append(f"{len(self.warnings)} warning{'s' if len(self.warnings) != 1 else ''}")
        if self.info:
            parts.append(f"{len(self.info)} info")
        
        status = "✓ Passed" if self.success else "✗ Failed"
        issues_text = ", ".join(parts) if parts else "no issues"
        
        return f"{status} with {issues_text}"