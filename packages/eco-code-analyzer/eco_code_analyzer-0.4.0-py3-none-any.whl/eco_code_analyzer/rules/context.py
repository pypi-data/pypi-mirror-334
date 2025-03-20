"""
Context for code analysis, maintaining state between rule checks.
"""

import ast
from typing import Dict, Set, List, Optional, Any


class AnalysisContext:
    """Context for code analysis, maintaining state between rule checks."""

    def __init__(self):
        self.scope_stack: List[ast.AST] = []  # Track current scope (function, class, module)
        self.variable_types: Dict[str, str] = {}  # Track variable types when possible
        self.imported_modules: Set[str] = set()  # Track imported modules
        self.function_calls: Dict[str, int] = {}  # Track function calls and their frequency
        self.loop_depths: Dict[int, int] = {}  # Track loop nesting depths
        self.node_energy: Dict[int, float] = {}  # Cache energy estimates for nodes
        self.file_path: Optional[str] = None  # Current file being analyzed
        self.code_lines: List[str] = []  # Lines of code being analyzed

    def enter_scope(self, node: ast.AST):
        """Enter a new scope (function, class, etc.)."""
        self.scope_stack.append(node)

    def exit_scope(self):
        """Exit the current scope."""
        if self.scope_stack:
            self.scope_stack.pop()

    def current_scope(self) -> Optional[ast.AST]:
        """Get the current scope node."""
        return self.scope_stack[-1] if self.scope_stack else None

    def record_variable_type(self, name: str, type_hint: str):
        """Record a variable's type."""
        self.variable_types[name] = type_hint

    def get_variable_type(self, name: str) -> Optional[str]:
        """Get a variable's type if known."""
        return self.variable_types.get(name)

    def record_import(self, module_name: str):
        """Record an imported module."""
        self.imported_modules.add(module_name)

    def has_import(self, module_name: str) -> bool:
        """Check if a module has been imported."""
        return module_name in self.imported_modules

    def record_function_call(self, func_name: str):
        """Record a function call."""
        self.function_calls[func_name] = self.function_calls.get(func_name, 0) + 1

    def get_call_count(self, func_name: str) -> int:
        """Get the number of times a function has been called."""
        return self.function_calls.get(func_name, 0)

    def enter_loop(self, node: ast.AST):
        """Enter a loop, tracking nesting depth."""
        node_id = id(node)
        parent_depth = 0
        if self.scope_stack:
            parent_id = id(self.scope_stack[-1])
            parent_depth = self.loop_depths.get(parent_id, 0)
        self.loop_depths[node_id] = parent_depth + 1

    def get_loop_depth(self, node: ast.AST) -> int:
        """Get the nesting depth of a loop."""
        return self.loop_depths.get(id(node), 0)

    def cache_node_energy(self, node: ast.AST, energy: float):
        """Cache the energy estimate for a node."""
        self.node_energy[id(node)] = energy

    def get_cached_energy(self, node: ast.AST) -> Optional[float]:
        """Get the cached energy estimate for a node if available."""
        return self.node_energy.get(id(node))

    def set_file_path(self, file_path: str):
        """Set the current file being analyzed."""
        self.file_path = file_path

    def set_code_lines(self, code: str):
        """Set the lines of code being analyzed."""
        self.code_lines = code.splitlines()

    def get_node_source(self, node: ast.AST) -> str:
        """Get the source code for a node."""
        if not hasattr(node, 'lineno') or not hasattr(node, 'end_lineno'):
            return ""

        start_line = getattr(node, 'lineno', 0) - 1  # 0-indexed
        end_line = getattr(node, 'end_lineno', start_line + 1)

        if not self.code_lines or start_line >= len(self.code_lines):
            return ""

        return "\n".join(self.code_lines[start_line:end_line])

    def reset(self):
        """Reset the context for a new analysis."""
        self.__init__()
