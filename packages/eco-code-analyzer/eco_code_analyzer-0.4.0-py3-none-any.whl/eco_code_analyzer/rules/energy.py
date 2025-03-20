"""
Energy efficiency rules for eco-code-analyzer.
"""

import ast
from typing import Dict, Any
from .base import Rule, RuleMetadata, RuleRegistry
from .context import AnalysisContext
from .patterns import PatternDetector


@RuleRegistry.register
class ListComprehensionRule(Rule):
    """Rule to encourage using list comprehensions instead of loops that build lists."""

    metadata = RuleMetadata(
        name="use_list_comprehension",
        description="Use list comprehensions instead of loops that build lists",
        category="energy_efficiency",
        impact="medium",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Green Algorithms: Quantifying the Carbon Footprint of Computation - Lannelongue et al."
        ],
        examples={
            "inefficient": """
                result = []
                for item in items:
                    result.append(item * 2)
            """,
            "efficient": """
                result = [item * 2 for item in items]
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        if not isinstance(node, ast.For):
            return 1.0

        # Use pattern detector to check if this is a loop that could be a list comprehension
        if PatternDetector.is_list_append_in_loop(node, context):
            # Check loop complexity - simple transformations are easier to convert
            if PatternDetector.is_simple_transformation(node, context):
                return 0.6  # Significant penalty for simple cases
            else:
                return 0.8  # Lighter penalty for complex cases

        return 1.0


@RuleRegistry.register
class GeneratorExpressionRule(Rule):
    """Rule to encourage using generator expressions for iteration without storing all results."""

    metadata = RuleMetadata(
        name="use_generator_expression",
        description="Use generator expressions instead of list comprehensions when you only need to iterate once",
        category="energy_efficiency",
        impact="medium",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Energy Efficiency across Programming Languages - Pereira et al."
        ],
        examples={
            "inefficient": """
                # Creating a list just to iterate once
                for x in [f(y) for y in items]:
                    print(x)
            """,
            "efficient": """
                # Using a generator expression
                for x in (f(y) for y in items):
                    print(x)
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Reward generator expressions
        if isinstance(node, ast.GeneratorExp):
            return 1.3

        # Penalize list comprehensions used in for loops
        if isinstance(node, ast.For) and isinstance(node.iter, ast.ListComp):
            # Check if the list comprehension result is only used for iteration
            return 0.7

        return 1.0


@RuleRegistry.register
class LazyEvaluationRule(Rule):
    """Rule to encourage using lazy evaluation techniques."""

    metadata = RuleMetadata(
        name="use_lazy_evaluation",
        description="Use lazy evaluation techniques like 'any()' and 'all()' instead of loops for boolean checks",
        category="energy_efficiency",
        impact="medium",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Software Development Methodology in a Green IT Environment - Kern et al."
        ],
        examples={
            "inefficient": """
                found = False
                for item in items:
                    if condition(item):
                        found = True
                        break
            """,
            "efficient": """
                found = any(condition(item) for item in items)
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Reward use of any() and all()
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ('any', 'all') and len(node.args) == 1:
                if isinstance(node.args[0], ast.GeneratorExp):
                    return 1.3
                return 1.2

        # Penalize loops that could use any() or all()
        if isinstance(node, ast.For):
            # Look for patterns like:
            # for x in items: if condition: return True/break
            if len(node.body) == 1 and isinstance(node.body[0], ast.If):
                if_node = node.body[0]
                if len(if_node.body) == 1:
                    stmt = if_node.body[0]
                    if (isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Constant) and
                            isinstance(stmt.value.value, bool)):
                        return 0.7
                    if isinstance(stmt, ast.Break):
                        # Look for a boolean assignment before or after the loop
                        return 0.7

        return 1.0


@RuleRegistry.register
class NestedLoopRule(Rule):
    """Rule to discourage deeply nested loops due to their high computational complexity."""

    metadata = RuleMetadata(
        name="avoid_nested_loops",
        description="Avoid deeply nested loops which have high computational complexity and energy consumption",
        category="energy_efficiency",
        impact="high",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Energy Efficiency across Programming Languages - Pereira et al."
        ],
        examples={
            "inefficient": """
                for i in range(n):
                    for j in range(n):
                        for k in range(n):
                            # O(n³) complexity
            """,
            "efficient": """
                # Use more efficient algorithms or data structures
                # Or vectorized operations if possible
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        if not isinstance(node, ast.For):
            return 1.0

        # Check for nested loops
        if PatternDetector.is_nested_loop(node, context):
            # Get the loop depth
            depth = context.get_loop_depth(node)
            if depth >= 3:
                return 0.5  # Severe penalty for deeply nested loops
            elif depth == 2:
                return 0.7  # Moderate penalty for double-nested loops
            else:
                return 0.9  # Light penalty for simple nested loops

        return 1.0


@RuleRegistry.register
class RedundantComputationRule(Rule):
    """Rule to discourage redundant computations inside loops."""

    metadata = RuleMetadata(
        name="avoid_redundant_computation",
        description="Avoid redundant computations inside loops that could be moved outside",
        category="energy_efficiency",
        impact="medium",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Energy-Efficient Software Development - Johann et al."
        ],
        examples={
            "inefficient": """
                for i in range(n):
                    x = expensive_function()  # Same result each time
                    result.append(i + x)
            """,
            "efficient": """
                x = expensive_function()  # Computed once
                for i in range(n):
                    result.append(i + x)
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        if not isinstance(node, ast.For):
            return 1.0

        # Check for redundant computations
        if PatternDetector.has_redundant_computation(node, context):
            return 0.7  # Penalty for redundant computations

        return 1.0
