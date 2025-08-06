#!/usr/bin/env python3
"""
Unit tests for BashAnalyzer

Tests bash command analysis functionality including destructive command detection,
logic check identification, and command type classification.
"""

import unittest
import sys
from pathlib import Path

# Add src to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from analyzers.bash_analyzer import BashAnalyzer


class TestBashAnalyzer(unittest.TestCase):
    """Test cases for BashAnalyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = BashAnalyzer()
    
    def test_destructive_command_detection(self):
        """Test detection of destructive commands"""
        destructive_commands = [
            'rm -rf /tmp/test',
            'mkfs.ext4 /dev/sdb1',
            'dd if=/dev/zero of=/dev/sdb',
            'fdisk /dev/sdb',
            'parted /dev/sdb mklabel gpt',
            'mkfs.btrfs /dev/sdb1',
            'mount /dev/sdb1 /mnt',
            'umount /mnt',
            'chmod 777 /etc/passwd',
            'chown root:root /etc/shadow'
        ]
        
        for command in destructive_commands:
            with self.subTest(command=command):
                analysis = self.analyzer.analyze_command(command)
                self.assertTrue(analysis.is_destructive, f"Command '{command}' should be destructive")
    
    def test_readonly_command_not_destructive(self):
        """Test that read-only commands are not flagged as destructive"""
        readonly_commands = [
            'ls -la',
            'cat /etc/passwd',
            'echo "Hello World"',
            'grep "pattern" file.txt',
            'find /tmp -name "*.txt"',
            'ps aux',
            'df -h',
            'free -h',
            'uname -a',
            'whoami'
        ]
        
        for command in readonly_commands:
            with self.subTest(command=command):
                analysis = self.analyzer.analyze_command(command)
                self.assertFalse(analysis.is_destructive,
                               f"Command '{command}' should not be destructive")
    
    def test_logic_check_detection(self):
        """Test detection of logic checks that could be promoted to validation"""
        logic_checks = [
            '[ -n "$SUDO_USER" ] && echo "sudo_active" || echo "no_sudo"',
            'test -f /etc/passwd && echo "exists" || echo "missing"',
            '[ -d /tmp ] && echo "directory exists" || echo "no directory"',
            '[[ $UID -eq 0 ]] && echo "root" || echo "user"',
            'command -v git >/dev/null 2>&1 && echo "git available" || echo "git missing"'
        ]
        
        for command in logic_checks:
            with self.subTest(command=command):
                analysis = self.analyzer.analyze_command(command)
                self.assertTrue(analysis.is_logic_check, f"Command '{command}' should be a logic check")
    
    def test_simple_command_not_logic_check(self):
        """Test that simple commands are not flagged as logic checks"""
        simple_commands = [
            'echo "Hello World"',
            'ls -la',
            'mkdir -p /tmp/test',
            'rm -rf /tmp/test',
            'cat /etc/passwd',
            'grep "pattern" file.txt'
        ]
        
        for command in simple_commands:
            with self.subTest(command=command):
                analysis = self.analyzer.analyze_command(command)
                self.assertFalse(analysis.is_logic_check,
                               f"Command '{command}' should not be a logic check")
    
    def test_command_type_classification(self):
        """Test classification of command types"""
        test_cases = [
            ('echo "Hello World"', 'simple'),
            ('ls -la | grep "pattern"', 'pipeline'),
            ('mkdir -p /tmp/test && echo "done"', 'list'),
            ('[ -f /etc/passwd ] && echo "exists"', 'conditional'),
            ('for i in 1 2 3; do echo $i; done', 'loop')
        ]
        
        for command, expected_type in test_cases:
            with self.subTest(command=command):
                analysis = self.analyzer.analyze_command(command)
                self.assertEqual(analysis.command_type, expected_type,
                               f"Command '{command}' should be classified as '{expected_type}'")
    
    def test_conditional_detection(self):
        """Test detection of conditional commands"""
        conditional_commands = [
            '[ -n "$SUDO_USER" ] && echo "sudo_active" || echo "no_sudo"',
            'test -f /etc/passwd && echo "exists" || echo "missing"',
            'if [ -d /tmp ]; then echo "exists"; else echo "missing"; fi',
            '[[ $UID -eq 0 ]] && echo "root" || echo "user"'
        ]
        
        for command in conditional_commands:
            with self.subTest(command=command):
                analysis = self.analyzer.analyze_command(command)
                self.assertEqual(analysis.command_type, 'conditional',
                               f"Command '{command}' should be classified as conditional")
    
    def test_sudo_usage_detection(self):
        """Test detection of sudo usage in commands"""
        sudo_commands = [
            'sudo rm -rf /tmp/test',
            'sudo mkfs.ext4 /dev/sdb1',
            'sudo chmod 777 /etc/passwd',
            'sudo mount /dev/sdb1 /mnt'
        ]
        
        for command in sudo_commands:
            with self.subTest(command=command):
                analysis = self.analyzer.analyze_command(command)
                self.assertTrue(analysis.uses_sudo, f"Command '{command}' should use sudo")
    
    def test_non_sudo_commands(self):
        """Test that non-sudo commands are not flagged as using sudo"""
        non_sudo_commands = [
            'echo "Hello World"',
            'ls -la',
            'cat /etc/passwd',
            'mkdir -p /tmp/test',
            'rm -rf /tmp/test'
        ]
        
        for command in non_sudo_commands:
            with self.subTest(command=command):
                analysis = self.analyzer.analyze_command(command)
                self.assertFalse(analysis.uses_sudo,
                               f"Command '{command}' should not use sudo")
    
    def test_variable_extraction(self):
        """Test extraction of variables from commands"""
        test_cases = [
            ('echo $HOME', ['HOME']),
            ('ls $PWD', ['PWD']),
            ('cat $FILE', ['FILE']),
            ('echo "$USER:$PATH"', ['USER', 'PATH']),
            ('mkdir -p $TEMP_DIR', ['TEMP_DIR'])
        ]
        
        for command, expected_vars in test_cases:
            with self.subTest(command=command):
                analysis = self.analyzer.analyze_command(command)
                for var in expected_vars:
                    self.assertIn(var, analysis.variables,
                                f"Variable '{var}' should be extracted from '{command}'")
    
    def test_redirection_detection(self):
        """Test detection of redirections in commands"""
        redirection_commands = [
            'echo "Hello" > output.txt',
            'cat input.txt >> output.txt',
            'ls -la 2> error.log',
            'grep "pattern" file.txt > results.txt 2>&1'
        ]
        
        for command in redirection_commands:
            with self.subTest(command=command):
                analysis = self.analyzer.analyze_command(command)
                self.assertTrue(analysis.has_redirections,
                              f"Command '{command}' should have redirections")
    
    def test_false_positive_destructive(self):
        """Test that commands with redirections to /dev/null are not destructive"""
        safe_commands = [
            'lsblk >/dev/null',
            'echo "test" >/dev/null',
            'grep "pattern" file.txt >/dev/null 2>&1',
            'find /tmp -name "*.txt" >/dev/null'
        ]
        
        for command in safe_commands:
            with self.subTest(command=command):
                analysis = self.analyzer.analyze_command(command)
                self.assertFalse(analysis.is_destructive,
                               f"Command '{command}' should not be destructive despite redirection")
    
    def test_security_issue_detection(self):
        """Test detection of potential security issues"""
        security_commands = [
            'chmod 777 /etc/passwd',
            'chown root:root /etc/shadow',
            'rm -rf /',
            'dd if=/dev/zero of=/dev/sda',
            'mkfs.ext4 /dev/sda'
        ]
        
        for command in security_commands:
            with self.subTest(command=command):
                analysis = self.analyzer.analyze_command(command)
                self.assertTrue(analysis.has_security_issues,
                              f"Command '{command}' should have security issues")
    
    def test_safe_command_no_security_issues(self):
        """Test that safe commands don't have security issues"""
        safe_commands = [
            'echo "Hello World"',
            'ls -la',
            'cat /etc/passwd',
            'mkdir -p /tmp/test',
            'grep "pattern" file.txt'
        ]
        
        for command in safe_commands:
            with self.subTest(command=command):
                analysis = self.analyzer.analyze_command(command)
                self.assertFalse(analysis.has_security_issues,
                               f"Command '{command}' should not have security issues")


if __name__ == '__main__':
    unittest.main() 