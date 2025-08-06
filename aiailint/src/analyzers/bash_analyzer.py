"""
Bash Command Semantic Analyzer

Analyzes shell commands using bash parsers to understand command structure,
detect destructive operations, and identify logic checks.

Supports multiple bash parsers with fallback strategy:
1. bashlex (primary) - Most mature and complete
2. bashparser (fallback) - Enhanced semantic capabilities
3. libbash (alternative) - Direct bash source integration
"""

import re
from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CommandAnalysis:
    """Result of bash command semantic analysis"""
    command: str
    success: bool = True
    error: Optional[str] = None
    
    # Command structure
    command_name: Optional[str] = None
    arguments: List[str] = field(default_factory=list)
    
    # Analysis results
    is_destructive: bool = False
    destructive_reason: Optional[str] = None
    has_logic_checks: bool = False
    logic_patterns: List[str] = field(default_factory=list)
    
    # Command classification
    command_type: str = "unknown"  # command, assignment, conditional, pipe, etc.
    uses_sudo: bool = False
    has_redirections: bool = False
    redirections: List[str] = field(default_factory=list)
    
    # Variables and references
    variables_read: Set[str] = field(default_factory=set)
    variables_written: Set[str] = field(default_factory=set)
    
    # Security considerations
    potential_security_issues: List[str] = field(default_factory=list)


class BashAnalyzer:
    """Semantic analyzer for bash commands with multiple parser support"""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.parser = None
        self.parser_name = ""
        self._initialize_parser()
    
    def _initialize_parser(self):
        """Initialize bash parser with fallback strategy"""
        # Try bashlex first (most mature)
        try:
            import bashlex
            self.parser = bashlex
            self.parser_name = "bashlex"
            if self.verbose:
                print("✓ Using bashlex for shell command analysis")
            return
        except ImportError:
            pass
        
        # Try bashparser as fallback
        try:
            import bashparser
            self.parser = bashparser
            self.parser_name = "bashparser"
            if self.verbose:
                print("✓ Using bashparser for shell command analysis")
            return
        except ImportError:
            pass
        
        # Try libbash as alternative
        try:
            import libbash
            self.parser = libbash
            self.parser_name = "libbash"
            if self.verbose:
                print("✓ Using libbash for shell command analysis")
            return
        except ImportError:
            pass
        
        # No parser available
        self.parser = None
        self.parser_name = "none"
        if self.verbose:
            print("⚠ No bash parser available - semantic analysis will be limited")
    
    def analyze_command(self, shell_command: str) -> CommandAnalysis:
        """
        Analyze a shell command for semantic properties
        
        Args:
            shell_command: Shell command string to analyze
            
        Returns:
            CommandAnalysis with detailed analysis results
        """
        if not shell_command or not shell_command.strip():
            return CommandAnalysis(
                command=shell_command,
                success=False,
                error="Empty command"
            )
        
        command = shell_command.strip()
        analysis = CommandAnalysis(command=command)
        
        try:
            if self.parser and self.parser_name == "bashlex":
                self._analyze_with_bashlex(command, analysis)
            elif self.parser and self.parser_name == "bashparser":
                self._analyze_with_bashparser(command, analysis)
            elif self.parser and self.parser_name == "libbash":
                self._analyze_with_libbash(command, analysis)
            else:
                # Fallback to regex-based analysis
                self._analyze_with_regex(command, analysis)
            
            # Perform common analysis regardless of parser
            self._analyze_destructive_patterns(command, analysis)
            self._analyze_logic_checks(command, analysis)
            self._analyze_security_issues(command, analysis)
            
        except Exception as e:
            analysis.success = False
            analysis.error = f"Analysis failed: {e}"
            
            # Still try regex-based analysis for basic detection
            try:
                self._analyze_with_regex(command, analysis)
                self._analyze_destructive_patterns(command, analysis)
                self._analyze_logic_checks(command, analysis)
                analysis.success = True  # Partial success with regex
            except Exception:
                pass  # Keep the original error
        
        return analysis
    
    def _analyze_with_bashlex(self, command: str, analysis: CommandAnalysis):
        """Analyze command using bashlex parser"""
        try:
            # Parse command into AST
            ast = self.parser.parse(command)
            
            for node in ast:
                self._analyze_bashlex_node(node, analysis)
                
        except Exception as e:
            # If bashlex fails, fall back to regex analysis
            if self.verbose:
                print(f"  Bashlex parsing failed: {e}, falling back to regex")
            self._analyze_with_regex(command, analysis)
    
    def _analyze_bashlex_node(self, node, analysis: CommandAnalysis):
        """Recursively analyze bashlex AST node"""
        if not hasattr(node, 'kind'):
            return
        
        if node.kind == 'command':
            # Extract command name and arguments
            parts = getattr(node, 'parts', [])
            if parts:
                first_part = parts[0]
                if hasattr(first_part, 'word'):
                    analysis.command_name = first_part.word
                    analysis.command_type = "command"
                
                # Extract arguments
                for part in parts[1:]:
                    if hasattr(part, 'word'):
                        analysis.arguments.append(part.word)
        
        elif node.kind == 'pipeline':
            analysis.command_type = "pipeline"
            # Analyze each part of the pipeline
            parts = getattr(node, 'parts', [])
            for part in parts:
                self._analyze_bashlex_node(part, analysis)
        
        elif node.kind == 'list':
            # Handle command lists (&&, ||, ;)
            analysis.command_type = "list"
            parts = getattr(node, 'parts', [])
            for part in parts:
                self._analyze_bashlex_node(part, analysis)
        
        elif node.kind == 'word':
            # Check for variable references
            word = getattr(node, 'word', '')
            self._extract_variables_from_word(word, analysis)
        
        elif node.kind == 'assignment':
            analysis.command_type = "assignment"
            # Extract variable assignment
            word = getattr(node, 'word', '')
            if '=' in word:
                var_name = word.split('=')[0]
                analysis.variables_written.add(var_name)
        
        # Recursively analyze child nodes
        if hasattr(node, 'list') and node.list:
            for child in node.list:
                self._analyze_bashlex_node(child, analysis)
        
        if hasattr(node, 'parts') and node.parts:
            for child in node.parts:
                self._analyze_bashlex_node(child, analysis)
    
    def _analyze_with_bashparser(self, command: str, analysis: CommandAnalysis):
        """Analyze command using bashparser"""
        # Implementation for bashparser would go here
        # For now, fall back to regex analysis
        self._analyze_with_regex(command, analysis)
    
    def _analyze_with_libbash(self, command: str, analysis: CommandAnalysis):
        """Analyze command using libbash"""
        # Implementation for libbash would go here
        # For now, fall back to regex analysis
        self._analyze_with_regex(command, analysis)
    
    def _analyze_with_regex(self, command: str, analysis: CommandAnalysis):
        """Fallback regex-based analysis when no parser available"""
        # Extract basic command structure
        parts = command.split()
        if parts:
            analysis.command_name = parts[0]
            analysis.arguments = parts[1:]
        
        # Detect command type
        if '|' in command:
            analysis.command_type = "pipeline"
        elif '&&' in command or '||' in command:
            analysis.command_type = "list"
        elif '=' in command and not command.startswith('['):
            analysis.command_type = "assignment"
        else:
            analysis.command_type = "command"
        
        # Check for sudo usage
        analysis.uses_sudo = command.strip().startswith('sudo ')
        
        # Check for redirections
        redirection_patterns = [r'>', r'>>', r'<', r'<<', r'2>', r'2>>', r'&>']
        for pattern in redirection_patterns:
            if pattern in command:
                analysis.has_redirections = True
                analysis.redirections.append(pattern)
        
        # Extract variables
        self._extract_variables_regex(command, analysis)
    
    def _extract_variables_from_word(self, word: str, analysis: CommandAnalysis):
        """Extract variable references from a word"""
        # Variable patterns: $VAR, ${VAR}, "$VAR", etc.
        var_patterns = [
            r'\$([A-Za-z_][A-Za-z0-9_]*)',  # $VAR
            r'\$\{([A-Za-z_][A-Za-z0-9_]*)[^}]*\}',  # ${VAR} with potential modifiers
        ]
        
        for pattern in var_patterns:
            matches = re.findall(pattern, word)
            for match in matches:
                analysis.variables_read.add(match)
    
    def _extract_variables_regex(self, command: str, analysis: CommandAnalysis):
        """Extract variables using regex patterns"""
        # Read variables
        read_patterns = [
            r'\$([A-Za-z_][A-Za-z0-9_]*)',  # $VAR
            r'\$\{([A-Za-z_][A-Za-z0-9_]*)[^}]*\}',  # ${VAR}
        ]
        
        for pattern in read_patterns:
            matches = re.findall(pattern, command)
            for match in matches:
                analysis.variables_read.add(match)
        
        # Written variables (assignments)
        assign_pattern = r'([A-Za-z_][A-Za-z0-9_]*)\s*='
        matches = re.findall(assign_pattern, command)
        for match in matches:
            analysis.variables_written.add(match)
    
    def _analyze_destructive_patterns(self, command: str, analysis: CommandAnalysis):
        """Analyze command for destructive patterns"""
        # Destructive command patterns
        destructive_commands = {
            'rm': 'File removal',
            'rmdir': 'Directory removal', 
            'unlink': 'File unlinking',
            'shred': 'Secure file deletion',
            'dd': 'Direct disk operations',
            'fdisk': 'Disk partitioning',
            'parted': 'Disk partitioning',
            'mkfs': 'Filesystem creation',
            'format': 'Disk formatting',
            'mount': 'Filesystem mounting',
            'umount': 'Filesystem unmounting',
            'kill': 'Process termination',
            'killall': 'Process termination',
            'pkill': 'Process termination'
        }
        
        # Check command name
        if analysis.command_name in destructive_commands:
            analysis.is_destructive = True
            analysis.destructive_reason = destructive_commands[analysis.command_name]
        
        # Check for destructive patterns in arguments
        destructive_patterns = [
            (r'rm\s+.*-[rf]', 'rm with recursive or force flags'),
            (r'dd\s+.*of=', 'dd writing to output device'),
            (r'>\s*/dev/', 'Redirecting to device files'),
            (r'systemctl\s+(stop|disable|mask)', 'Service control commands'),
            (r'chmod\s+000', 'Removing all permissions'),
            (r'chown\s+.*:', 'Changing file ownership'),
        ]
        
        for pattern, reason in destructive_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                analysis.is_destructive = True
                analysis.destructive_reason = reason
                break
    
    def _analyze_logic_checks(self, command: str, analysis: CommandAnalysis):
        """Analyze command for logic check patterns"""
        logic_patterns = [
            (r'\[\s+.*\s+\]', 'Test command with brackets'),
            (r'\[\[\s+.*\s+\]\]', 'Extended test command'),
            (r'test\s+', 'Test command'),
            (r'&&|\|\|', 'Conditional operators'),
            (r'if\s+.*;.*then', 'If-then construct'),
            (r'case\s+.*in', 'Case statement'),
            (r'-[a-z]\s+\$?\w+', 'File/directory tests'),
            (r'\$\?\s*[!=]=', 'Exit code checks'),
            (r'\[\s*-[nz]\s+\$', 'Variable existence checks'),
            (r'\$\{.*:-.*\}', 'Parameter expansion with defaults'),
        ]
        
        for pattern, description in logic_patterns:
            if re.search(pattern, command):
                analysis.has_logic_checks = True
                analysis.logic_patterns.append(description)
    
    def _analyze_security_issues(self, command: str, analysis: CommandAnalysis):
        """Analyze command for potential security issues"""
        security_patterns = [
            (r'eval\s+', 'Use of eval command'),
            (r'exec\s+', 'Use of exec command'),
            (r'\$\([^)]*\)', 'Command substitution'),
            (r'`[^`]*`', 'Backtick command substitution'),
            (r'curl\s+.*\|\s*sh', 'Piping remote content to shell'),
            (r'wget\s+.*\|\s*sh', 'Piping remote content to shell'),
            (r'echo\s+.*\|\s*sh', 'Piping echo output to shell'),
            (r'su\s+', 'User switching'),
            (r'sudo\s+su', 'Sudo with su'),
        ]
        
        for pattern, issue in security_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                analysis.potential_security_issues.append(issue)


def analyze_shell_command(command: str, verbose=False) -> CommandAnalysis:
    """
    Standalone function to analyze a shell command
    
    Args:
        command: Shell command to analyze
        verbose: Enable verbose output
        
    Returns:
        CommandAnalysis with analysis results
    """
    analyzer = BashAnalyzer(verbose=verbose)
    return analyzer.analyze_command(command)