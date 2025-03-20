"""
Pattern detection utilities for identifying common code patterns.
"""

import ast
from typing import Optional, List, Set, Dict, Any
from .context import AnalysisContext


class PatternDetector:
    """Detect common code patterns in AST nodes."""

    @staticmethod
    def is_list_append_in_loop(node: ast.For, context: AnalysisContext) -> bool:
        """
        Detect if a for loop is just appending to a list and could be a list comprehension.
        Example:
            result = []
            for item in items:
                result.append(item)
        """
        if not isinstance(node, ast.For) or not node.body:
            return False

        # Check if body is a single append statement
        if len(node.body) != 1:
            return False

        stmt = node.body[0]
        if not isinstance(stmt, ast.Expr):
            return False

        call = stmt.value
        if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Attribute):
            return False

        if call.func.attr != 'append':
            return False

        # More sophisticated: check if the target is actually used in the append
        # This distinguishes between transformations and simple copies
        target_name = node.target.id if isinstance(node.target, ast.Name) else None
        if target_name:
            arg = call.args[0] if call.args else None
            uses_target = PatternDetector._contains_name(arg, target_name)
            return True  # Even if it doesn't use the target, it could still be a list comprehension

        return True

    @staticmethod
    def is_simple_transformation(node: ast.For, context: AnalysisContext) -> bool:
        """
        Detect if a for loop is doing a simple transformation that could be a list comprehension.
        Example:
            result = []
            for item in items:
                result.append(item * 2)  # Simple transformation
        vs.
            result = []
            for item in items:
                x = complex_function(item)
                if x > 10:
                    result.append(x)  # Complex transformation
        """
        if not PatternDetector.is_list_append_in_loop(node, context):
            return False

        # Check if the append argument is a simple expression
        stmt = node.body[0]
        call = stmt.value
        if not call.args:
            return False

        arg = call.args[0]

        # Simple expressions are: Name, Constant, BinOp with simple operands,
        # UnaryOp with simple operand, or Attribute access
        return PatternDetector._is_simple_expression(arg)

    @staticmethod
    def is_string_concatenation_in_loop(node: ast.For, context: AnalysisContext) -> bool:
        """
        Detect if a for loop is concatenating strings inefficiently.
        Example:
            result = ""
            for item in items:
                result += str(item)  # Inefficient
        """
        if not isinstance(node, ast.For) or not node.body:
            return False

        # Check if body contains string concatenation
        for stmt in node.body:
            if isinstance(stmt, ast.AugAssign) and isinstance(stmt.op, ast.Add):
                if isinstance(stmt.target, ast.Name):
                    # Check if we're adding to a string
                    var_name = stmt.target.id
                    var_type = context.get_variable_type(var_name)
                    if var_type == 'str' or PatternDetector._is_string_operation(stmt.value):
                        return True
        return False

    @staticmethod
    def is_dict_key_lookup_in_loop(node: ast.For, context: AnalysisContext) -> bool:
        """
        Detect if a for loop is doing repeated dictionary key lookups.
        Example:
            for item in items:
                if item in my_dict:  # Lookup 1
                    x = my_dict[item]  # Lookup 2 (could use my_dict.get(item) instead)
        """
        if not isinstance(node, ast.For) or not node.body:
            return False

        # Look for patterns like: if key in dict: ... dict[key]
        dict_lookups = set()
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Subscript) and isinstance(stmt.value, ast.Name):
                dict_name = stmt.value.id
                dict_lookups.add(dict_name)

        # Look for membership tests on the same dictionaries
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Compare) and any(isinstance(op, ast.In) for op in stmt.ops):
                if isinstance(stmt.comparators[0], ast.Name):
                    dict_name = stmt.comparators[0].id
                    if dict_name in dict_lookups:
                        return True

        return False

    @staticmethod
    def is_nested_loop(node: ast.For, context: AnalysisContext) -> bool:
        """
        Detect if a loop contains another loop (nested loops).
        Example:
            for i in range(n):
                for j in range(m):
                    # O(n*m) complexity
        """
        if not isinstance(node, ast.For):
            return False

        for stmt in ast.walk(node):
            if stmt is not node and isinstance(stmt, (ast.For, ast.While)):
                return True

        return False

    @staticmethod
    def has_redundant_computation(node: ast.For, context: AnalysisContext) -> bool:
        """
        Detect if a loop has redundant computations that could be moved outside.
        Example:
            for i in range(n):
                x = expensive_function()  # Could be moved outside the loop
                result.append(i + x)
        """
        if not isinstance(node, ast.For) or not node.body:
            return False

        # This is a simplified check - a more sophisticated version would
        # analyze dependencies between variables
        loop_var = node.target.id if isinstance(node.target, ast.Name) else None
        if not loop_var:
            return False

        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                # Check if the assignment doesn't depend on the loop variable
                if not PatternDetector._contains_name(stmt.value, loop_var):
                    return True

        return False

    @staticmethod
    def _contains_name(node: ast.AST, name: str) -> bool:
        """Check if an AST node contains a specific name."""
        if node is None:
            return False

        if isinstance(node, ast.Name):
            return node.id == name

        # Recursively check all child nodes
        for child in ast.iter_child_nodes(node):
            if PatternDetector._contains_name(child, name):
                return True

        return False

    @staticmethod
    def _is_simple_expression(node: ast.AST) -> bool:
        """Check if an AST node is a simple expression."""
        if node is None:
            return False

        if isinstance(node, (ast.Name, ast.Constant)):
            return True

        if isinstance(node, ast.BinOp):
            return (PatternDetector._is_simple_expression(node.left) and
                    PatternDetector._is_simple_expression(node.right))

        if isinstance(node, ast.UnaryOp):
            return PatternDetector._is_simple_expression(node.operand)

        if isinstance(node, ast.Attribute):
            return PatternDetector._is_simple_expression(node.value)

        return False

    @staticmethod
    def _is_string_operation(node: ast.AST) -> bool:
        """Check if an AST node is a string operation."""
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return True

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'str':
            return True

        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return (PatternDetector._is_string_operation(node.left) or
                    PatternDetector._is_string_operation(node.right))

        return False
