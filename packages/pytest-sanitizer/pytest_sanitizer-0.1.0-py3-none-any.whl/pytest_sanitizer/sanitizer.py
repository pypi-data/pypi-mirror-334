"""
Sanitizer for pytest output.

This module contains functions to sanitize pytest output, removing expected values
from assertion errors.
"""
import re
from typing import Dict, List, Optional, Union, Any
from _pytest.reports import TestReport


# Regex patterns for different types of assertions
PATTERNS = {
    "equality": r"assert\s+(.+?)\s+==\s+(.+?)(?:$|(?=\s+\+\s+where))",
    "equality_where": r"assert\s+(.+?)\s+==\s+(.+?)\s+\+\s+where",
    "approx": r"assert\s+(.+?)\s+==\s+pytest\.approx\((.+?)(?:,|\))",
    "in_membership": r"assert\s+(.+?)\s+in\s+(.+?)(?:$|(?=\s+\+\s+where))",
    "not_in_membership": r"assert\s+(.+?)\s+not\s+in\s+(.+?)(?:$|(?=\s+\+\s+where))",
    "is_identity": r"assert\s+(.+?)\s+is\s+(.+?)(?:$|(?=\s+\+\s+where))",
    "is_not_identity": r"assert\s+(.+?)\s+is\s+not\s+(.+?)(?:$|(?=\s+\+\s+where))",
    "greater_than": r"assert\s+(.+?)\s+>\s+(.+?)(?:$|(?=\s+\+\s+where))",
    "less_than": r"assert\s+(.+?)\s+<\s+(.+?)(?:$|(?=\s+\+\s+where))",
    "greater_equal": r"assert\s+(.+?)\s+>=\s+(.+?)(?:$|(?=\s+\+\s+where))",
    "less_equal": r"assert\s+(.+?)\s+<=\s+(.+?)(?:$|(?=\s+\+\s+where))",
    "not_equal": r"assert\s+(.+?)\s+!=\s+(.+?)(?:$|(?=\s+\+\s+where))",
    # Match patterns that might include quoted strings with operators inside
    "string_in": r'assert\s+"([^"]+)"\s+in\s+(.+?)(?:$|(?=\s+\+\s+where))',
    "string_not_in": r'assert\s+"([^"]+)"\s+not\s+in\s+(.+?)(?:$|(?=\s+\+\s+where))',
    "single_quoted_in": r"assert\s+'([^']+)'\s+in\s+(.+?)(?:$|(?=\s+\+\s+where))",
    "single_quoted_not_in": r"assert\s+'([^']+)'\s+not\s+in\s+(.+?)(?:$|(?=\s+\+\s+where))",
    # Method calls with expected results
    "isinstance": r"assert\s+isinstance\((.+?),\s+(.+?)\)(?:$|(?=\s+\+\s+where))",
    
    # Explanation lines (the E lines that explain the assertion)
    "explanation_where": r"E\s+\+\s+where\s+(.+?)\s+=\s+(.+?)(?:$|(?=\s+\+\s+and|\sand\s+))",
    "explanation_and": r"E\s+\+\s+and\s+(.+?)\s+=\s+(.+?)$",
    "explanation_with_float": r"E\s+\+\s+.*?=\s+float\('(.+?)'\)",
    "explanation_assert": r"E\s+assert\s+(.+?)\s+(?:==|!=|in|not in|is|is not|>|<|>=|<=)\s+(.+?)$",
    "explanation_nan": r"E\s+.*?\s+nan\s+(?:==|!=|in|not in|is|is not|>|<|>=|<=)\s+nan",
    
    # assertAlmostEqual failures
    "assert_almost_equal": r"AssertionError:\s+(.+?)\s+!=\s+(.+?)\s+within",
    "assert_almost_diff": r"within\s+\d+\s+places\s+\((.+?)\s+difference\)",
    
    # pytest.approx explanation lines
    "approx_comparison_failed": r"comparison failed",
    "approx_obtained": r"Obtained:\s+(.+?)$",
    "approx_expected": r"Expected:\s+(.+?)\s+±",
    
    # pytest.approx in assert line with explanation
    "approx_with_explanation": r"assert\s+(.+?)\s+==\s+(.+?)\s*\n\s*E\s*\n\s*E\s+comparison failed",
}


def sanitize_assertion_line(line: str) -> str:
    """
    Sanitize a single line of assertion error.
    
    Args:
        line: The assertion line to sanitize.
        
    Returns:
        The sanitized line with expected values replaced.
    """
    # Skip lines that are already sanitized
    if "[SANITIZED]" in line:
        return line

    original_line = line
    
    # Handle special comparison failure explanations
    if "comparison failed" in line or "Obtained:" in line or "Expected:" in line:
        if "Obtained:" in line:
            match = re.search(r"Obtained:\s+(.+?)$", line)
            if match:
                return "Obtained: [value hidden for sanitization]"
        elif "Expected:" in line:
            match = re.search(r"Expected:\s+(.+?)(?:\s+±|$)", line)
            if match:
                return "Expected: [value hidden for sanitization]"
        return line
        
    # Handle assertEquals/assertAlmostEqual reporting
    if "AssertionError:" in line and "!=" in line and "within" in line:
        match = re.search(r"AssertionError:\s+(.+?)\s+!=\s+(.+?)\s+within", line)
        if match:
            value1, value2 = match.groups()
            return f"AssertionError: {value1} != [SANITIZED] within"
            
    # Handle difference explanations
    if "difference" in line and "within" in line:
        return "within N places (difference details hidden)"
    
    # Try each pattern
    for pattern_name, pattern in PATTERNS.items():
        match = re.search(pattern, line)
        if match:
            # Skip purely informational patterns
            if pattern_name in ["approx_comparison_failed"]:
                return line
                
            # For assertions with expected values in the second group
            if len(match.groups()) >= 2:
                # Replace the expected value with [SANITIZED]
                start, end = match.span(2)
                line = line[:start] + "[SANITIZED]" + line[end:]
                return line
            # Handle NaN comparison specially
            elif pattern_name == "explanation_nan":
                return line  # Leave NaN comparison as is
    
    # Special handling for float('nan') or other complex expressions
    if "float('nan')" in line or 'float("nan")' in line:
        line = line.replace("float('nan')", "[SANITIZED_NAN]")
        line = line.replace('float("nan")', "[SANITIZED_NAN]")
    
    return original_line


def sanitize_message(report: TestReport) -> Optional[Dict[str, Any]]:
    """
    Sanitize the assertion error message in a test report.
    
    Args:
        report: The test report containing the assertion error.
        
    Returns:
        A dictionary with sanitized information, or None if no sanitization needed.
    """
    if not hasattr(report, "longrepr") or not report.longrepr:
        return None
    
    # Convert to string if it's not already
    if not isinstance(report.longrepr, str):
        longrepr_str = str(report.longrepr)
    else:
        longrepr_str = report.longrepr
    
    # Split by lines and sanitize each one
    lines = longrepr_str.split("\n")
    sanitized_lines: List[str] = []
    modified = False
    
    for line in lines:
        sanitized_line = sanitize_assertion_line(line)
        if sanitized_line != line:
            modified = True
        sanitized_lines.append(sanitized_line)
    
    if modified:
        return {
            "sanitized_message": "\n".join(sanitized_lines),
            "original_path": getattr(report, "fspath", "unknown"),
            "original_line": getattr(report, "lineno", 0),
            "original_domain": getattr(report, "domain", "unknown"),
        }
    
    return None 