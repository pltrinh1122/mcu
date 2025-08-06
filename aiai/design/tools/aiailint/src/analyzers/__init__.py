"""
aiailint analyzers package

This package contains analysis modules for the aiailint tool.
"""

from .bash_analyzer import BashAnalyzer
from .destructive_detector import DestructiveCommandDetector
from .loop_detector import LoopDetector

__all__ = [
    'BashAnalyzer',
    'DestructiveCommandDetector',
    'LoopDetector'
] 