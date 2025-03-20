from unittest.mock import MagicMock, patch

import pytest

from nebari_doctor.agent import (
    ChatResponse,
    message_user,
    run_agent,
    tool_output_wrapper,
)
from nebari_doctor.styling import MessageType


@pytest.fixture
def mock_display_message():
    """Mock the display_message function"""
    with patch("nebari_doctor.agent.display_message") as mock:
        yield mock


@pytest.fixture
def mock_get_user_input():
    """Mock the get_user_input function"""
    with patch("nebari_doctor.agent.get_user_input") as mock:
        mock.return_value = "Test user input"
        yield mock


@pytest.fixture
def mock_agent():
    """Mock the Agent class"""
    with patch("nebari_doctor.agent.Agent") as mock:
        agent_instance = MagicMock()
        mock.return_value = agent_instance

        # Mock the run_sync method
        result = MagicMock()
        result.data = ChatResponse(message="Test agent response")
        result.new_messages.return_value = []
        agent_instance.run_sync.return_value = result

        yield agent_instance


def test_tool_output_wrapper(mock_display_message):
    """Test that the tool output wrapper correctly displays tool information"""

    # Create a test function
    def test_tool():
        return "Tool result"

    # Apply the wrapper
    wrapped_tool = tool_output_wrapper(test_tool)

    # Call the wrapped function
    result = wrapped_tool()

    # Check that display_message was called correctly
    assert mock_display_message.call_count == 2
    # First call should be for running the tool
    assert mock_display_message.call_args_list[0][0][0] == "Running tool: test_tool"
    assert mock_display_message.call_args_list[0][0][1] == MessageType.SYSTEM

    # Second call should be for the tool output
    assert mock_display_message.call_args_list[1][0][0] == "Tool result"
    assert mock_display_message.call_args_list[1][0][1] == MessageType.TOOL

    # Check that the function returns the correct result
    assert result == "Tool result"


def test_message_user(mock_display_message, mock_get_user_input):
    """Test that message_user correctly displays a message and gets user input"""
    result = message_user("Test message")

    # Check that display_message was called correctly
    mock_display_message.assert_called_once_with("Test message", MessageType.AGENT)

    # Check that get_user_input was called
    mock_get_user_input.assert_called_once()

    # Check that the function returns the user input
    assert result == "Test user input"


@patch("nebari_doctor.agent.display_header")
@patch("nebari_doctor.agent.display_tool_info")
def test_run_agent_with_input(
    mock_display_tool_info,
    mock_display_header,
    mock_display_message,
    mock_get_user_input,
    mock_agent,
):
    """Test running the agent with initial user input"""
    # Mock KeyboardInterrupt to exit the infinite loop
    mock_agent.run_sync.side_effect = KeyboardInterrupt

    # Run the agent with initial input
    try:
        run_agent(user_input="Initial input")
    except KeyboardInterrupt:
        pass

    # Check that display_header was called
    mock_display_header.assert_called_once()

    # Check that the agent was run with the initial input
    mock_agent.run_sync.assert_called_once()
    # Get the first call arguments
    args, kwargs = mock_agent.run_sync.call_args
    assert args[0] == "Initial input"


@patch("nebari_doctor.agent.display_header")
@patch("nebari_doctor.agent.display_tool_info")
def test_run_agent_without_input(
    mock_display_tool_info,
    mock_display_header,
    mock_display_message,
    mock_get_user_input,
    mock_agent,
):
    """Test running the agent without initial user input"""
    # Mock KeyboardInterrupt to exit the infinite loop
    mock_agent.run_sync.side_effect = KeyboardInterrupt

    # Run the agent without initial input
    try:
        run_agent()
    except KeyboardInterrupt:
        pass

    # Check that get_user_input was called to get the initial input
    mock_get_user_input.assert_called_once()

    # Check that the agent was run with the user input
    mock_agent.run_sync.assert_called_once()


@patch("nebari_doctor.agent.display_header")
@patch("nebari_doctor.agent.display_tool_info")
def test_run_agent_with_exception(
    mock_display_tool_info,
    mock_display_header,
    mock_display_message,
    mock_get_user_input,
    mock_agent,
):
    """Test handling exceptions in the agent"""
    # Set up the agent to raise an exception on first call, then KeyboardInterrupt on second call
    mock_agent.run_sync.side_effect = [Exception("Test exception"), KeyboardInterrupt]

    # Run the agent
    try:
        run_agent(user_input="Initial input")
    except KeyboardInterrupt:
        pass

    # Check that an error message was displayed
    mock_display_message.assert_any_call(
        "Error while processing: Test exception", MessageType.ERROR
    )
