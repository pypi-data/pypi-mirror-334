"""
I/O efficiency rules for eco-code-analyzer.
"""

import ast
from typing import Dict, Any
from .base import Rule, RuleMetadata, RuleRegistry
from .context import AnalysisContext
from .patterns import PatternDetector


@RuleRegistry.register
class FileOperationRule(Rule):
    """Rule to encourage efficient file operations."""

    metadata = RuleMetadata(
        name="efficient_file_operations",
        description="Use efficient file operations to minimize I/O overhead",
        category="io_efficiency",
        impact="high",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Efficient I/O in Python - PyCon 2020"
        ],
        examples={
            "inefficient": """
                # Reading a file line by line with multiple open/close
                for i in range(100):
                    with open('large_file.txt', 'r') as f:
                        line = f.readlines()[i]  # Reads entire file each time
            """,
            "efficient": """
                # Reading a file once
                with open('large_file.txt', 'r') as f:
                    lines = f.readlines()
                for i in range(100):
                    line = lines[i]
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Check for repeated file operations in loops
        if isinstance(node, ast.For):
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.With):
                    for item in stmt.items:
                        if isinstance(item.context_expr, ast.Call) and isinstance(item.context_expr.func, ast.Name):
                            if item.context_expr.func.id == 'open':
                                # File is opened inside a loop
                                return 0.6

        # Check for inefficient file reading
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == 'readlines' and isinstance(node.func.value, ast.Name):
                # Check if we're only accessing a single line
                parent = context.current_scope()
                if parent and isinstance(parent, ast.With):
                    # This is inside a with statement, which is good
                    return 1.0
                else:
                    # readlines() without with statement
                    return 0.8

        return 1.0


@RuleRegistry.register
class NetworkOperationRule(Rule):
    """Rule to encourage efficient network operations."""

    metadata = RuleMetadata(
        name="efficient_network_operations",
        description="Use efficient network operations to minimize energy consumption",
        category="io_efficiency",
        impact="high",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Green Networking - IEEE Communications Magazine"
        ],
        examples={
            "inefficient": """
                # Making multiple API calls in a loop
                results = []
                for id in ids:
                    response = requests.get(f'https://api.example.com/items/{id}')
                    results.append(response.json())
            """,
            "efficient": """
                # Making a single batch API call
                ids_param = ','.join(ids)
                response = requests.get(f'https://api.example.com/items?ids={ids_param}')
                results = response.json()
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Check for network operations in loops
        if isinstance(node, ast.For):
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Call) and isinstance(stmt.func, ast.Attribute):
                    if isinstance(stmt.func.value, ast.Name):
                        if stmt.func.value.id == 'requests' and stmt.func.attr in ['get', 'post', 'put', 'delete']:
                            # Network operation inside a loop
                            return 0.5
                        if stmt.func.attr in ['urlopen', 'fetch', 'connect']:
                            # Potential network operation inside a loop
                            return 0.6

        return 1.0


@RuleRegistry.register
class DatabaseOperationRule(Rule):
    """Rule to encourage efficient database operations."""

    metadata = RuleMetadata(
        name="efficient_database_operations",
        description="Use efficient database operations to minimize energy consumption",
        category="io_efficiency",
        impact="high",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Energy Efficiency in Database Systems - ACM SIGMOD"
        ],
        examples={
            "inefficient": """
                # N+1 query problem
                users = db.query(User).all()
                for user in users:
                    # This makes a separate query for each user
                    orders = db.query(Order).filter(Order.user_id == user.id).all()
            """,
            "efficient": """
                # Single query with join
                user_orders = db.query(User, Order).join(Order, User.id == Order.user_id).all()
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Check for database operations in loops (N+1 query problem)
        if isinstance(node, ast.For):
            db_calls_in_loop = []

            # Look for database query patterns in the loop body
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Call) and isinstance(stmt.func, ast.Attribute):
                    if stmt.func.attr in ['query', 'execute', 'filter', 'find', 'get']:
                        if isinstance(stmt.func.value, ast.Name) or isinstance(stmt.func.value, ast.Attribute):
                            # This looks like a database query
                            db_calls_in_loop.append(stmt)

            if db_calls_in_loop:
                # Check if the query depends on the loop variable
                loop_var = node.target.id if isinstance(node.target, ast.Name) else None
                if loop_var:
                    for call in db_calls_in_loop:
                        if PatternDetector._contains_name(call, loop_var):
                            # This is likely an N+1 query
                            return 0.5

        return 1.0


@RuleRegistry.register
class CachingRule(Rule):
    """Rule to encourage caching of expensive operations."""

    metadata = RuleMetadata(
        name="use_caching",
        description="Cache results of expensive operations to avoid redundant computation and I/O",
        category="io_efficiency",
        impact="medium",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Caching Strategies for Energy-Efficient Computing - IEEE Transactions"
        ],
        examples={
            "inefficient": """
                def get_data(key):
                    # Expensive operation performed every time
                    result = fetch_from_remote_api(key)
                    return result
            """,
            "efficient": """
                cache = {}
                def get_data(key):
                    if key in cache:
                        return cache[key]
                    result = fetch_from_remote_api(key)
                    cache[key] = result
                    return result
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Reward use of caching decorators
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name) and decorator.id in ['cache', 'lru_cache', 'cached_property']:
                    return 1.3
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                    if decorator.func.id in ['cache', 'lru_cache']:
                        return 1.3

            # Check for manual caching patterns
            cache_var = None
            for stmt in node.body:
                if isinstance(stmt, ast.If) and isinstance(stmt.test, ast.Compare):
                    if any(isinstance(op, ast.In) for op in stmt.test.ops):
                        if isinstance(stmt.test.left, ast.Name) and isinstance(stmt.test.comparators[0], ast.Name):
                            # This looks like "if key in cache:"
                            cache_var = stmt.test.comparators[0].id
                            return 1.2

        return 1.0


@RuleRegistry.register
class BulkOperationRule(Rule):
    """Rule to encourage bulk operations instead of individual ones."""

    metadata = RuleMetadata(
        name="use_bulk_operations",
        description="Use bulk operations instead of individual ones to reduce overhead",
        category="io_efficiency",
        impact="medium",
        references=[
            "https://doi.org/10.1145/3136014.3136031",
            "Energy-Efficient Data Processing - ACM SIGMOD"
        ],
        examples={
            "inefficient": """
                # Individual inserts
                for item in items:
                    db.execute("INSERT INTO table VALUES (?)", (item,))
            """,
            "efficient": """
                # Bulk insert
                db.executemany("INSERT INTO table VALUES (?)", [(item,) for item in items])
            """
        }
    )

    def check(self, node: ast.AST, context: AnalysisContext) -> float:
        # Reward use of bulk operations
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in ['executemany', 'bulk_create', 'bulk_update', 'bulk_insert']:
                return 1.3

            # Penalize individual operations in loops
            if isinstance(node.func.attr, str) and node.func.attr.startswith('execute'):
                parent = context.current_scope()
                if parent and isinstance(parent, ast.For):
                    return 0.7

        return 1.0
