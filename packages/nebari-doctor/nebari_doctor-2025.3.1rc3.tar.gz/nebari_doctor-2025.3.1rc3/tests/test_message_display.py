from unittest.mock import patch

import pytest
from rich.panel import Panel

from nebari_doctor.styling import MessageType, display_message


@pytest.fixture
def mock_console():
    """Create a mock console for testing"""
    with patch("nebari_doctor.styling.console") as mock:
        mock.width = 100
        yield mock


def test_agent_message_display(mock_console):
    """Test that agent messages are displayed correctly"""
    display_message("Test agent message", MessageType.AGENT)

    # Check that console.print was called with a Panel
    mock_console.print.assert_called_once()
    args, kwargs = mock_console.print.call_args

    # Check that the panel contains the message and has the right title
    panel = args[0]
    assert isinstance(panel, Panel)
    assert "Test agent message" in panel.renderable.markup
    assert "Nebari Doctor" in panel.title


def test_user_message_display(mock_console):
    """Test that user messages are displayed correctly"""
    display_message("Test user message", MessageType.USER)

    # Check that console.print was called with a Panel
    mock_console.print.assert_called_once()
    args, kwargs = mock_console.print.call_args

    # Check that the panel contains the message and has the right title
    panel = args[0]
    assert isinstance(panel, Panel)
    assert "Test user message" in panel.renderable
    assert "User" in panel.title


def test_tool_message_display(mock_console):
    """Test that tool output messages are displayed correctly"""
    display_message("Test tool output", MessageType.TOOL)

    # Check that console.print was called with a Panel
    mock_console.print.assert_called_once()
    args, kwargs = mock_console.print.call_args

    # Check that the panel contains the message and has the right title
    panel = args[0]
    assert isinstance(panel, Panel)
    assert "Test tool output" in panel.renderable
    assert "Tool Output" in panel.title


def test_system_message_display(mock_console):
    """Test that system messages are displayed correctly"""
    display_message("Test system message", MessageType.SYSTEM)

    # Check that console.print was called with the message
    mock_console.print.assert_called_once()
    args, kwargs = mock_console.print.call_args

    # System messages are printed directly, not in a panel
    assert "Test system message" in args[0]


def test_warning_message_display(mock_console):
    """Test that warning messages are displayed correctly"""
    display_message("Test warning message", MessageType.WARNING)

    # Check that console.print was called with a Panel
    mock_console.print.assert_called_once()
    args, kwargs = mock_console.print.call_args

    # Check that the panel contains the message and has the right title
    panel = args[0]
    assert isinstance(panel, Panel)
    assert "Test warning message" in panel.renderable
    assert "Warning" in panel.title


def test_error_message_display(mock_console):
    """Test that error messages are displayed correctly"""
    display_message("Test error message", MessageType.ERROR)

    # Check that console.print was called with a Panel
    mock_console.print.assert_called_once()
    args, kwargs = mock_console.print.call_args

    # Check that the panel contains the message and has the right title
    panel = args[0]
    assert isinstance(panel, Panel)
    assert "Test error message" in panel.renderable
    assert "Error" in panel.title


def test_custom_title_display(mock_console):
    """Test that custom titles are used when provided"""
    display_message("Test message", MessageType.AGENT, title="Custom Title")

    # Check that console.print was called with a Panel
    mock_console.print.assert_called_once()
    args, kwargs = mock_console.print.call_args

    # Check that the panel has the custom title
    panel = args[0]
    assert isinstance(panel, Panel)
    assert "Custom Title" in panel.title


def test_long_message_truncation(mock_console):
    """Test that long messages are truncated"""
    # Create a message with many lines
    long_message = "\n".join([f"Line {i}" for i in range(20)])

    display_message(long_message, MessageType.TOOL)

    # Check that console.print was called with a Panel
    mock_console.print.assert_called_once()
    args, kwargs = mock_console.print.call_args

    # Check that the panel contains truncation message
    panel = args[0]
    assert isinstance(panel, Panel)
    assert "output truncated" in panel.renderable
