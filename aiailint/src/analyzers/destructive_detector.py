"""
Destructive Command Detector

Specialized detector for identifying destructive shell commands.
Used by business rules validator for safety checks.
"""

from typing import List, Dict, Any, Tuple


class DestructiveCommandDetector:
    """Detects destructive commands and operations"""
    
    def __init__(self):
        self.destructive_patterns = self._load_destructive_patterns()
    
    def _load_destructive_patterns(self) -> Dict[str, str]:
        """Load patterns for destructive command detection"""
        return {
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
            'umount': 'Filesystem unmounting'
        }
    
    def is_destructive_command(self, command: str) -> Tuple[bool, str]:
        """
        Check if a command is destructive
        
        Args:
            command: Shell command to analyze
            
        Returns:
            Tuple of (is_destructive, reason)
        """
        # This functionality is implemented in bash_analyzer.py
        # This is a stub for future expansion
        return False, ""