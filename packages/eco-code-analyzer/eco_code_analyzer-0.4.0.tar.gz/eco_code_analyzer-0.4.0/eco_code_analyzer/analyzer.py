import ast
import os
import json
from typing import Dict, List, Tuple, Any
from .rules import Rule, RuleRegistry, AnalysisContext
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_code(code: str, file_path: str = None, config: Dict[str, Any] = None) -> Dict[str, float]:
    """
    Analyze the given Python code for ecological impact.

    Args:
        code: The Python code to analyze
        file_path: Optional path to the file being analyzed
        config: Optional configuration dictionary

    Returns:
        Dictionary with category scores
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        logger.error(f"Syntax error in code: {e}")
        return {
            'energy_efficiency': 0.0,
            'resource_usage': 0.0,
            'io_efficiency': 0.0,
            'algorithm_efficiency': 0.0,
            'custom_rules': 0.0,
        }

    # Create analysis context
    context = AnalysisContext()
    context.set_code_lines(code)
    if file_path:
        context.set_file_path(file_path)

    # Create rule instances
    rule_instances = RuleRegistry.create_rule_instances(config or {})

    # Analyze code with each category of rules
    result = {
        'energy_efficiency': analyze_category(tree, context, rule_instances.get('energy_efficiency', {})),
        'resource_usage': analyze_category(tree, context, rule_instances.get('memory_usage', {})),
        'io_efficiency': analyze_category(tree, context, rule_instances.get('io_efficiency', {})),
        'algorithm_efficiency': analyze_category(tree, context, rule_instances.get('algorithm_efficiency', {})),
        'custom_rules': analyze_custom_rules(tree, context, rule_instances),
    }

    return result

def analyze_project(project_path: str, config: Dict[str, Any] = None) -> Dict[str, Dict[str, float]]:
    """
    Analyze all Python files in the given project directory.

    Args:
        project_path: Path to the project directory
        config: Optional configuration dictionary

    Returns:
        Dictionary with file paths as keys and analysis results as values
    """
    project_results = {}
    total_lines = 0
    total_score = 0

    logger.info(f"Analyzing project at {project_path}")

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code = f.read()

                    logger.info(f"Analyzing file: {file_path}")
                    file_results = analyze_code(code, file_path, config)
                    project_results[file_path] = file_results

                    lines = len(code.splitlines())
                    total_lines += lines
                    total_score += get_eco_score(file_results) * lines
                except Exception as e:
                    logger.error(f"Error analyzing {file_path}: {e}")

    if total_lines > 0:
        project_results['overall_score'] = total_score / total_lines
    else:
        project_results['overall_score'] = 0

    return project_results

def get_eco_score(analysis_result: Dict[str, float]) -> float:
    """
    Calculate an overall eco-score based on the analysis result.

    Args:
        analysis_result: Dictionary with category scores

    Returns:
        Overall eco-score between 0 and 1
    """
    weights = {
        'energy_efficiency': 0.25,
        'resource_usage': 0.25,
        'io_efficiency': 0.2,
        'algorithm_efficiency': 0.2,
        'custom_rules': 0.1,
    }

    # Ensure all categories exist in the result
    for key in weights:
        if key not in analysis_result:
            analysis_result[key] = 1.0

    score = sum(analysis_result[key] * weights[key] for key in weights)
    return round(score, 2)

def get_project_eco_score(project_results: Dict[str, Dict[str, float]]) -> float:
    """
    Calculate an overall eco-score for the entire project.
    """
    return project_results['overall_score']

def analyze_category(tree: ast.AST, context: AnalysisContext, rules: Dict[str, Rule]) -> float:
    """
    Analyze code with a specific category of rules.

    Args:
        tree: AST of the code
        context: Analysis context
        rules: Dictionary of rules to apply

    Returns:
        Category score between 0 and 1
    """
    if not rules:
        return 1.0

    score = 1.0
    for node in ast.walk(tree):
        for rule in rules.values():
            try:
                score *= rule.check(node, context)
            except Exception as e:
                logger.error(f"Error applying rule {rule.metadata.name}: {e}")

    return round(score, 2)

def analyze_custom_rules(tree: ast.AST, context: AnalysisContext, rule_instances: Dict[str, Dict[str, Rule]]) -> float:
    """
    Apply custom rules that don't fit into standard categories.

    Args:
        tree: AST of the code
        context: Analysis context
        rule_instances: Dictionary of rule instances by category

    Returns:
        Custom rules score between 0 and 1
    """
    custom_rules = rule_instances.get('custom_rules', {})
    if not custom_rules:
        return 1.0

    score = 1.0
    for node in ast.walk(tree):
        for rule in custom_rules.values():
            try:
                score *= rule.check(node, context)
            except Exception as e:
                logger.error(f"Error applying custom rule {rule.metadata.name}: {e}")

    return round(score, 2)

def get_improvement_suggestions(analysis_result: Dict[str, float], config: Dict[str, Any] = None) -> List[Dict[str, str]]:
    """
    Generate improvement suggestions based on the analysis result.

    Args:
        analysis_result: Dictionary with category scores
        config: Optional configuration dictionary

    Returns:
        List of suggestion dictionaries
    """
    suggestions = []
    threshold = 0.7  # Default threshold for suggestions

    if config and 'thresholds' in config:
        threshold = config['thresholds'].get('category_score', 0.7)

    # Create rule instances to get their suggestions
    rule_instances = RuleRegistry.create_rule_instances(config or {})

    # Get suggestions for each category
    categories = {
        'energy_efficiency': 'Energy Efficiency',
        'resource_usage': 'Resource Usage',
        'io_efficiency': 'I/O Efficiency',
        'algorithm_efficiency': 'Algorithm Efficiency',
        'custom_rules': 'Custom Rules'
    }

    for category_key, category_name in categories.items():
        if category_key in analysis_result and analysis_result[category_key] < threshold:
            # Get rules for this category
            category_rules = {}
            for cat, rules in rule_instances.items():
                if cat.lower().replace('_', '') == category_key.lower().replace('_', ''):
                    category_rules = rules
                    break

            # Add suggestions from each rule
            for rule in category_rules.values():
                suggestions.append(rule.get_suggestion())

    return suggestions

def get_detailed_analysis(analysis_result: Dict[str, float]) -> str:
    """
    Generate a detailed analysis report as a string.

    Args:
        analysis_result: Dictionary with category scores

    Returns:
        Formatted string with detailed analysis
    """
    details = []

    # Energy Efficiency
    details.append(f"Energy Efficiency: {analysis_result.get('energy_efficiency', 0):.2f}")
    details.append("- Evaluates the use of efficient loop constructs, list comprehensions, and generator expressions.")
    details.append("- Checks for lazy evaluation techniques and redundant computations.")
    details.append("- Analyzes loop nesting and complexity.")
    impact = 'High' if analysis_result.get('energy_efficiency', 0) >= 0.8 else 'Medium' if analysis_result.get('energy_efficiency', 0) >= 0.6 else 'Low'
    details.append(f"Environmental Impact: {impact}")

    # Resource Usage
    details.append(f"\nResource Usage: {analysis_result.get('resource_usage', 0):.2f}")
    details.append("- Analyzes memory usage and resource management practices.")
    details.append("- Evaluates the use of context managers and efficient data structures.")
    details.append("- Checks for potential memory leaks and global variable usage.")
    impact = 'High' if analysis_result.get('resource_usage', 0) >= 0.8 else 'Medium' if analysis_result.get('resource_usage', 0) >= 0.6 else 'Low'
    details.append(f"Environmental Impact: {impact}")

    # I/O Efficiency
    details.append(f"\nI/O Efficiency: {analysis_result.get('io_efficiency', 0):.2f}")
    details.append("- Examines file, network, and database operations.")
    details.append("- Checks for efficient use of caching and bulk operations.")
    details.append("- Identifies potential N+1 query problems and repeated I/O operations.")
    impact = 'High' if analysis_result.get('io_efficiency', 0) >= 0.8 else 'Medium' if analysis_result.get('io_efficiency', 0) >= 0.6 else 'Low'
    details.append(f"Environmental Impact: {impact}")

    # Algorithm Efficiency
    details.append(f"\nAlgorithm Efficiency: {analysis_result.get('algorithm_efficiency', 0):.2f}")
    details.append("- Analyzes time and space complexity of algorithms.")
    details.append("- Evaluates data structure selection for operations.")
    details.append("- Checks for optimized recursive algorithms and appropriate algorithm selection.")
    impact = 'High' if analysis_result.get('algorithm_efficiency', 0) >= 0.8 else 'Medium' if analysis_result.get('algorithm_efficiency', 0) >= 0.6 else 'Low'
    details.append(f"Environmental Impact: {impact}")

    # Custom Rules
    details.append(f"\nCustom Rules: {analysis_result.get('custom_rules', 0):.2f}")
    details.append("- Applies user-defined custom rules for project-specific optimizations.")
    impact = 'High' if analysis_result.get('custom_rules', 0) >= 0.8 else 'Medium' if analysis_result.get('custom_rules', 0) >= 0.6 else 'Low'
    details.append(f"Environmental Impact: {impact}")

    return "\n".join(details)

def generate_report(project_results: Dict[str, Dict[str, float]], output_file: str):
    """
    Generate a detailed report of the project analysis.
    """
    report = {
        'project_score': get_project_eco_score(project_results),
        'file_scores': {file: get_eco_score(result) for file, result in project_results.items() if file != 'overall_score'},
        'detailed_results': project_results,
        'improvement_suggestions': get_improvement_suggestions(project_results['overall_score']),
        'estimated_energy_savings': estimate_energy_savings(project_results),
    }

    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

def load_config(config_file: str) -> Dict:
    """
    Load configuration from a JSON file.
    """
    with open(config_file, 'r') as f:
        return json.load(f)

def analyze_with_git_history(repo_path: str, num_commits: int = 5) -> List[Tuple[str, float]]:
    """
    Analyze the eco-score of the project over the last n commits.
    """
    try:
        from git import Repo
    except ImportError:
        print("GitPython is not installed. Please install it to use this feature.")
        return []

    repo = Repo(repo_path)
    commits = list(repo.iter_commits('master', max_count=num_commits))

    scores = []
    for commit in commits:
        repo.git.checkout(commit.hexsha)
        project_results = analyze_project(repo_path)
        score = get_project_eco_score(project_results)
        scores.append((commit.hexsha[:7], score))

    repo.git.checkout('master')
    return scores

def estimate_energy_savings(project_results: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """
    Estimate potential energy savings based on the project's eco-score.
    """
    overall_score = project_results['overall_score']
    potential_improvement = 1 - overall_score

    # These are rough estimates and should be refined with more accurate data
    estimated_savings = {
        'energy_kwh_per_year': potential_improvement * 100,  # Assuming 100 kWh/year for a typical project
        'co2_kg_per_year': potential_improvement * 50,  # Assuming 50 kg CO2/year for a typical project
        'trees_equivalent': potential_improvement * 2,  # Assuming 2 trees can offset the CO2 of a typical project
    }

    return estimated_savings

def visualize_eco_score_trend(scores: List[Tuple[str, float]], output_file: str):
    """
    Generate a visualization of the eco-score trend over time.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed. Please install it to use this feature.")
        return

    commits, eco_scores = zip(*scores)
    plt.figure(figsize=(10, 6))
    plt.plot(commits, eco_scores, marker='o')
    plt.title('Eco-Score Trend Over Time')
    plt.xlabel('Commits')
    plt.ylabel('Eco-Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def calculate_project_carbon_footprint(project_results: Dict[str, Dict[str, float]]) -> float:
    """
    Calculate an estimated carbon footprint for the project based on its eco-score.
    """
    overall_score = project_results['overall_score']
    # This is a simplified model and should be refined with more accurate data
    base_footprint = 100  # kg CO2 per year for a typical project
    return base_footprint * (1 - overall_score)
