"""
Enhanced rules module for eco-code-analyzer.
This package contains the rule system for analyzing code for ecological impact.
"""

from .base import Rule, RuleMetadata, RuleRegistry
from .context import AnalysisContext
from .patterns import PatternDetector

# Import all rule categories to register them
from . import energy
from . import memory
from . import io
from . import algorithm

# Export the rule registry for use by the analyzer
__all__ = ['Rule', 'RuleMetadata', 'RuleRegistry', 'AnalysisContext', 'PatternDetector']
