"""
Sanitization logic for pytest output.

This module contains functions to sanitize assertion errors in pytest output,
particularly to prevent LLMs from seeing expected values.
"""
import re
from typing import Optional, Union, Any

# Regex patterns for different types of assertions
EQUALS_PATTERN = re.compile(r'assert .+?\s*==\s*.+')
NOT_EQUALS_PATTERN = re.compile(r'assert .+?\s*!=\s*.+')
IN_PATTERN = re.compile(r'assert .+?\s+in\s+.+')
NOT_IN_PATTERN = re.compile(r'assert .+?\s+not in\s+.+')
COMMENT_PATTERN = re.compile(r'#.*')  # Match Python comments

def sanitize_assertion_line(line: str) -> str:
    """
    Sanitize a single line containing an assertion error.
    
    Args:
        line: A line of text that may contain an assertion error
        
    Returns:
        The sanitized line with expected values removed
    """
    # Remove comments that might leak expected values
    line = COMMENT_PATTERN.sub('', line)
    
    # Handle equals assertions (==)
    if EQUALS_PATTERN.search(line):
        # Find the position of ==
        eq_pos = line.find('==')
        if eq_pos != -1:
            # Keep everything up to and including ==, then add [SANITIZED]
            return line[:eq_pos+2] + ' [SANITIZED]'
    
    # Handle not equals assertions (!=)
    if NOT_EQUALS_PATTERN.search(line):
        neq_pos = line.find('!=')
        if neq_pos != -1:
            return line[:neq_pos+2] + ' [SANITIZED]'
    
    # Handle 'in' assertions
    if IN_PATTERN.search(line):
        in_pos = line.find(' in ')
        if in_pos != -1:
            return line[:in_pos+4] + ' [SANITIZED]'
    
    # Handle 'not in' assertions
    if NOT_IN_PATTERN.search(line):
        not_in_pos = line.find(' not in ')
        if not_in_pos != -1:
            return line[:not_in_pos+8] + ' [SANITIZED]'
    
    return line

def sanitize_message(rep: Any) -> Optional[str]:
    """
    Sanitize the failure message in a test report.
    
    Args:
        rep: A pytest test report object
        
    Returns:
        The sanitized error message or None if no sanitization was needed
    """
    # Check if there's a failure message to sanitize
    if not hasattr(rep, 'longrepr') or not rep.longrepr:
        return None
    
    longrepr = str(rep.longrepr)
    lines = longrepr.split('\n')
    sanitized_lines = []
    modified = False
    
    for line in lines:
        sanitized_line = sanitize_assertion_line(line)
        if sanitized_line != line:
            modified = True
        sanitized_lines.append(sanitized_line)
    
    if modified:
        return '\n'.join(sanitized_lines)
    
    return None 