"""
Algorithm efficiency rules for eco-code-analyzer.
"""

import ast
from typing import Dict, Any
from .base import Rule, RuleMetadata, RuleRegistry
from .context import AnalysisContext
from .patterns import PatternDetector


@RuleRegistry.register
class TimeComplexityRule(Rule):
    """Rule to encourage using algorithms with better time complexity."""

    metadata = RuleMetadata(
        name="optimize_time_complexity",
        description="Use algorithms with optimal time complexity to reduce CPU cycles and energy consumption",
        category="algorithm_efficiency",
        impact="high",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Energy Complexity of Algorithms - Journal of ACM"
        ],
        examples={
            "inefficient": """
                # Bubble sort: O(n²) time complexity
                def bubble_sort(arr):
                    n = len(arr)
                    for i in range(n):
                        for j in range(0, n - i - 1):
                            if arr[j] > arr[j + 1]:
                                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            """,
            "efficient": """
                # Using built-in sort: O(n log n) time complexity
                def efficient_sort(arr):
                    return sorted(arr)
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Reward use of efficient sorting
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == 'sorted':
                return 1.2

        # Penalize nested loops that might indicate quadratic algorithms
        if isinstance(node, ast.For):
            nested_loops = 0
            for child in ast.walk(node):
                if child is not node and isinstance(child, ast.For):
                    nested_loops += 1

            if nested_loops > 1:
                # Potentially O(n³) or worse
                return 0.5
            elif nested_loops == 1:
                # Potentially O(n²)
                return 0.7

        return 1.0


@RuleRegistry.register
class SpaceComplexityRule(Rule):
    """Rule to encourage using algorithms with better space complexity."""

    metadata = RuleMetadata(
        name="optimize_space_complexity",
        description="Use algorithms with optimal space complexity to reduce memory usage and energy consumption",
        category="algorithm_efficiency",
        impact="medium",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Memory-Efficient Algorithms - SIAM Journal on Computing"
        ],
        examples={
            "inefficient": """
                # Creating multiple copies of large data
                def process_data(data):
                    copy1 = data.copy()
                    # Process copy1
                    copy2 = data.copy()
                    # Process copy2
                    return copy1, copy2
            """,
            "efficient": """
                # Processing in-place or with minimal copies
                def process_data(data):
                    result1 = process_first(data)
                    result2 = process_second(data)
                    return result1, result2
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Penalize multiple copies of the same data
        if isinstance(node, ast.FunctionDef):
            copy_calls = []
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Call) and isinstance(stmt.func, ast.Attribute):
                    if stmt.func.attr == 'copy':
                        copy_calls.append(stmt)

            if len(copy_calls) > 1:
                # Check if we're copying the same object multiple times
                copied_objects = set()
                for call in copy_calls:
                    if isinstance(call.func.value, ast.Name):
                        copied_objects.add(call.func.value.id)

                if len(copied_objects) < len(copy_calls):
                    # Some objects are copied multiple times
                    return 0.7

        return 1.0


@RuleRegistry.register
class AlgorithmSelectionRule(Rule):
    """Rule to encourage selecting appropriate algorithms for the task."""

    metadata = RuleMetadata(
        name="select_appropriate_algorithms",
        description="Select algorithms appropriate for the task and data size to optimize energy efficiency",
        category="algorithm_efficiency",
        impact="high",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Energy-Aware Algorithm Selection - IEEE Transactions"
        ],
        examples={
            "inefficient": """
                # Using a complex algorithm for a simple task
                def find_max(numbers):
                    numbers.sort()  # O(n log n)
                    return numbers[-1]
            """,
            "efficient": """
                # Using a simpler algorithm for the same task
                def find_max(numbers):
                    return max(numbers)  # O(n)
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Reward use of appropriate built-in functions
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ['max', 'min', 'sum', 'any', 'all']:
                return 1.2

        # Penalize potentially inefficient algorithm selections
        if isinstance(node, ast.FunctionDef):
            # Check for common inefficient patterns

            # Pattern: Sorting just to get min/max
            sorts = []
            min_max_access = []

            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Call) and isinstance(stmt.func, (ast.Name, ast.Attribute)):
                    func_name = stmt.func.id if isinstance(stmt.func, ast.Name) else stmt.func.attr
                    if func_name in ['sort', 'sorted']:
                        sorts.append(stmt)

                if isinstance(stmt, ast.Subscript) and isinstance(stmt.slice, ast.UnaryOp):
                    if isinstance(stmt.slice.op, ast.USub) and isinstance(stmt.slice.operand, ast.Constant):
                        if stmt.slice.operand.value == 1:
                            # This is accessing the first or last element (e.g., arr[-1])
                            min_max_access.append(stmt)

            if sorts and min_max_access:
                # This might be sorting just to get min/max
                return 0.7

        return 1.0


@RuleRegistry.register
class DataStructureSelectionRule(Rule):
    """Rule to encourage selecting appropriate data structures for the task."""

    metadata = RuleMetadata(
        name="select_appropriate_data_structures",
        description="Select data structures appropriate for the operations being performed to optimize energy efficiency",
        category="algorithm_efficiency",
        impact="medium",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Energy-Efficient Data Structures - ACM Computing Surveys"
        ],
        examples={
            "inefficient": """
                # Using a list for frequent lookups by key
                data = [(key1, value1), (key2, value2), ...]

                def get_value(key):
                    for k, v in data:  # O(n) lookup
                        if k == key:
                            return v
                    return None
            """,
            "efficient": """
                # Using a dictionary for frequent lookups by key
                data = {key1: value1, key2: value2, ...}

                def get_value(key):
                    return data.get(key)  # O(1) lookup
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Penalize inefficient data structure usage

        # Check for linear searches in lists where dictionaries would be better
        if isinstance(node, ast.For) and isinstance(node.iter, ast.Name):
            iter_var = node.iter.id
            var_type = context.get_variable_type(iter_var)

            # Look for equality comparisons in the loop body
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Compare) and any(isinstance(op, ast.Eq) for op in stmt.ops):
                    # This might be a linear search
                    if var_type == 'list':
                        return 0.7

        # Reward use of appropriate data structures
        if isinstance(node, ast.Dict):
            return 1.1

        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ['defaultdict', 'Counter', 'deque', 'OrderedDict']:
                # These are specialized data structures that are often more efficient
                return 1.2

        return 1.0


@RuleRegistry.register
class RecursionOptimizationRule(Rule):
    """Rule to encourage optimizing recursive algorithms."""

    metadata = RuleMetadata(
        name="optimize_recursion",
        description="Optimize recursive algorithms to avoid redundant calculations and stack overflow",
        category="algorithm_efficiency",
        impact="high",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Energy-Efficient Recursive Algorithms - SIAM Journal"
        ],
        examples={
            "inefficient": """
                # Naive recursive Fibonacci with redundant calculations
                def fibonacci(n):
                    if n <= 1:
                        return n
                    return fibonacci(n-1) + fibonacci(n-2)  # Exponential time complexity
            """,
            "efficient": """
                # Memoized Fibonacci to avoid redundant calculations
                memo = {}
                def fibonacci(n):
                    if n in memo:
                        return memo[n]
                    if n <= 1:
                        return n
                    memo[n] = fibonacci(n-1) + fibonacci(n-2)
                    return memo[n]
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Check for recursive functions
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            calls_self = False

            # Look for self-calls in the function body
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Call) and isinstance(stmt.func, ast.Name):
                    if stmt.func.id == func_name:
                        calls_self = True
                        break

            if calls_self:
                # This is a recursive function

                # Check for memoization patterns
                has_memo = False
                for stmt in node.body:
                    if isinstance(stmt, ast.If) and isinstance(stmt.test, ast.Compare):
                        if any(isinstance(op, ast.In) for op in stmt.test.ops):
                            # This looks like "if n in memo:"
                            has_memo = True
                            break

                if has_memo:
                    # Memoized recursion is good
                    return 1.2
                else:
                    # Naive recursion might be inefficient
                    return 0.7

        return 1.0
