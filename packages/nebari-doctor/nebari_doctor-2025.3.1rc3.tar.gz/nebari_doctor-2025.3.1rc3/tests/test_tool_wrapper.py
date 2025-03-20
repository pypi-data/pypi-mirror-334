from unittest.mock import patch

import pytest

from nebari_doctor.agent import tool_output_wrapper
from nebari_doctor.styling import MessageType


@patch("nebari_doctor.agent.display_message")
def test_tool_wrapper_with_result(mock_display_message):
    """Test tool_output_wrapper with a function that returns a result"""

    # Define a test function
    def test_tool(arg1, arg2=None):
        """Test tool docstring"""
        return f"Result: {arg1}, {arg2}"

    # Apply the wrapper
    wrapped_tool = tool_output_wrapper(test_tool)

    # Check that the wrapper preserves the function metadata
    assert wrapped_tool.__name__ == "test_tool"
    assert wrapped_tool.__doc__ == "Test tool docstring"

    # Call the wrapped function
    result = wrapped_tool("value1", arg2="value2")

    # Check that display_message was called correctly
    assert mock_display_message.call_count == 2

    # First call should announce the tool is running
    first_call_args = mock_display_message.call_args_list[0][0]
    assert first_call_args[0] == "Running tool: test_tool"
    assert first_call_args[1] == MessageType.SYSTEM

    # Second call should display the result
    second_call_args = mock_display_message.call_args_list[1][0]
    assert second_call_args[0] == "Result: value1, value2"
    assert second_call_args[1] == MessageType.TOOL

    # Check that the function returns the correct result
    assert result == "Result: value1, value2"


@patch("nebari_doctor.agent.display_message")
def test_tool_wrapper_no_result(mock_display_message):
    """Test tool_output_wrapper with a function that returns None"""

    # Define a test function that returns None
    def test_tool_no_result():
        """Test tool with no result"""
        return None

    # Apply the wrapper
    wrapped_tool = tool_output_wrapper(test_tool_no_result)

    # Call the wrapped function
    result = wrapped_tool()

    # Check that display_message was called only once (to announce the tool)
    assert mock_display_message.call_count == 1

    # The call should announce the tool is running
    call_args = mock_display_message.call_args[0]
    assert call_args[0] == "Running tool: test_tool_no_result"
    assert call_args[1] == MessageType.SYSTEM

    # Check that the function returns None
    assert result is None


@patch("nebari_doctor.agent.display_message")
def test_tool_wrapper_exception(mock_display_message):
    """Test tool_output_wrapper with a function that raises an exception"""

    # Define a test function that raises an exception
    def test_tool_exception():
        """Test tool that raises an exception"""
        raise ValueError("Test exception")

    # Apply the wrapper
    wrapped_tool = tool_output_wrapper(test_tool_exception)

    # Call the wrapped function and expect an exception
    with pytest.raises(ValueError, match="Test exception"):
        wrapped_tool()

    # Check that display_message was called only once (to announce the tool)
    assert mock_display_message.call_count == 1

    # The call should announce the tool is running
    call_args = mock_display_message.call_args[0]
    assert call_args[0] == "Running tool: test_tool_exception"
    assert call_args[1] == MessageType.SYSTEM
