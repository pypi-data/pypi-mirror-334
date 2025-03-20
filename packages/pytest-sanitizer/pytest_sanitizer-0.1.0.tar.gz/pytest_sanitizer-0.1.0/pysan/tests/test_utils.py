"""
Tests to demonstrate the PySan sanitizer plugin.
"""

def test_equals_assertion():
    """Test an equality assertion."""
    result = "hello"
    expected = "world"
    assert result == expected, "Message should not be visible"

def test_not_equals_assertion():
    """Test a not-equal assertion."""
    result = 42
    expected = 43
    assert result != expected, "This message should be hidden"

def test_in_assertion():
    """Test an 'in' assertion."""
    result = "a"
    expected_list = ["b", "c", "d"]
    assert result in expected_list, "Should not see the list contents"

def test_not_in_assertion():
    """Test a 'not in' assertion."""
    result = "x"
    expected_list = ["x", "y", "z"]
    assert result not in expected_list, "Should not see the list contents"

def test_with_comment():
    """Test with a comment that might leak the answer."""
    value = 5
    # The expected value should be 10
    assert value == 10, "Comment should be filtered out" 