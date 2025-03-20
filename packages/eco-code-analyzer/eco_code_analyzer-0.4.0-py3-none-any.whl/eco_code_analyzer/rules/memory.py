"""
Memory usage rules for eco-code-analyzer.
"""

import ast
from typing import Dict, Any
from .base import Rule, RuleMetadata, RuleRegistry
from .context import AnalysisContext
from .patterns import PatternDetector


@RuleRegistry.register
class ContextManagerRule(Rule):
    """Rule to encourage using context managers for proper resource management."""

    metadata = RuleMetadata(
        name="use_context_managers",
        description="Use context managers (with statements) for resource management",
        category="memory_usage",
        impact="high",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Resource Management in Python - PyCon 2019"
        ],
        examples={
            "inefficient": """
                f = open('file.txt', 'r')
                data = f.read()
                f.close()  # Might not be called if an exception occurs
            """,
            "efficient": """
                with open('file.txt', 'r') as f:
                    data = f.read()
                # File is automatically closed, even if an exception occurs
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Reward use of with statements
        if isinstance(node, ast.With):
            # Extra reward for multiple context managers in a single with statement
            if len(node.items) > 1:
                return 1.3
            return 1.2

        # Penalize open() without with
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'open':
            # Check if this open() call is not inside a with statement
            current_scope = context.current_scope()
            if current_scope and not isinstance(current_scope, ast.With):
                return 0.6

        return 1.0


@RuleRegistry.register
class GlobalVariableRule(Rule):
    """Rule to discourage excessive use of global variables."""

    metadata = RuleMetadata(
        name="minimize_global_variables",
        description="Minimize the use of global variables to reduce memory usage and improve code maintainability",
        category="memory_usage",
        impact="medium",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Memory Management in Python - PyCon 2020"
        ],
        examples={
            "inefficient": """
                global_data = {}  # Global variable

                def process_data(key, value):
                    global_data[key] = value  # Modifying global state
            """,
            "efficient": """
                def process_data(data, key, value):
                    data[key] = value  # Explicit parameter passing
                    return data
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Penalize global statements
        if isinstance(node, ast.Global):
            return 0.7

        # Penalize nonlocal statements (slightly less)
        if isinstance(node, ast.Nonlocal):
            return 0.8

        return 1.0


@RuleRegistry.register
class MemoryEfficientDataStructureRule(Rule):
    """Rule to encourage using memory-efficient data structures."""

    metadata = RuleMetadata(
        name="use_memory_efficient_data_structures",
        description="Use memory-efficient data structures like sets for membership testing and generators for large sequences",
        category="memory_usage",
        impact="medium",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Memory Efficient Python - Raymond Hettinger"
        ],
        examples={
            "inefficient": """
                # Using a list for membership testing
                items = [1, 2, 3, 4, 5]
                if x in items:  # O(n) operation
                    print("Found")
            """,
            "efficient": """
                # Using a set for membership testing
                items = {1, 2, 3, 4, 5}
                if x in items:  # O(1) operation
                    print("Found")
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Reward use of sets and set comprehensions
        if isinstance(node, (ast.Set, ast.SetComp)):
            return 1.2

        # Penalize inefficient membership testing
        if isinstance(node, ast.Compare) and any(isinstance(op, ast.In) for op in node.ops):
            # Check if we're testing membership in a list
            comparator = node.comparators[0]
            if isinstance(comparator, ast.Name):
                var_name = comparator.id
                var_type = context.get_variable_type(var_name)
                if var_type == 'list':
                    return 0.8

        return 1.0


@RuleRegistry.register
class MemoryLeakRule(Rule):
    """Rule to detect potential memory leaks."""

    metadata = RuleMetadata(
        name="avoid_memory_leaks",
        description="Avoid patterns that can lead to memory leaks, such as circular references and unclosed resources",
        category="memory_usage",
        impact="high",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Tracking Down Memory Leaks in Python - PyCon 2018"
        ],
        examples={
            "inefficient": """
                class Node:
                    def __init__(self, parent=None):
                        self.parent = parent
                        self.children = []

                    def add_child(self, child):
                        self.children.append(child)
                        child.parent = self  # Creates a circular reference
            """,
            "efficient": """
                class Node:
                    def __init__(self, parent=None):
                        self.parent = parent
                        self.children = []

                    def add_child(self, child):
                        self.children.append(child)
                        child.parent = weakref.ref(self)  # Use weak reference
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Check for circular references in class definitions
        if isinstance(node, ast.ClassDef):
            # This is a simplified check - a more sophisticated version would
            # analyze the class structure more deeply
            for method in [n for n in node.body if isinstance(n, ast.FunctionDef)]:
                if method.name == '__init__':
                    # Look for assignments that might create circular references
                    for stmt in ast.walk(method):
                        if isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0], ast.Attribute):
                            if stmt.targets[0].attr == 'parent' and isinstance(stmt.value, ast.Name):
                                # Potential circular reference
                                return 0.8

        # Check for unclosed resources
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ['open', 'socket', 'connect']:
                    # Check if this call is not inside a with statement and not assigned to a variable
                    current_scope = context.current_scope()
                    if current_scope and not isinstance(current_scope, ast.With):
                        # This is a simplified check - a more sophisticated version would
                        # track the returned object and check if close() is called
                        return 0.7

        return 1.0


@RuleRegistry.register
class LargeObjectLifetimeRule(Rule):
    """Rule to encourage limiting the lifetime of large objects."""

    metadata = RuleMetadata(
        name="limit_large_object_lifetime",
        description="Limit the lifetime of large objects by using them in the smallest possible scope",
        category="memory_usage",
        impact="medium",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Python Memory Management Best Practices - PyCon 2021"
        ],
        examples={
            "inefficient": """
                # Large object created at module level
                large_data = load_large_dataset()

                def process_small_part(index):
                    return large_data[index]  # Only uses a small part
            """,
            "efficient": """
                def process_small_part(index):
                    # Load only what's needed
                    data_item = load_specific_data(index)
                    return data_item
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # This is a complex rule that would require more sophisticated analysis
        # For now, we'll implement a simplified version

        # Penalize large data structures defined at module level
        if isinstance(node, ast.Assign) and len(context.scope_stack) == 0:
            # Check if this is potentially a large data structure
            value = node.value
            if isinstance(value, (ast.List, ast.Dict, ast.Set)) and len(getattr(value, 'elts', [])) > 10:
                return 0.8
            if isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
                if value.func.id in ['list', 'dict', 'set', 'array', 'DataFrame', 'load', 'read']:
                    return 0.8

        return 1.0
