import pytest
from rich.panel import Panel

from nebari_doctor.styling import (
    MessageType,
    display_header,
    display_message,
    truncate_long_text,
)


@pytest.fixture
def mock_console(monkeypatch):
    """Mock the rich console to capture output"""
    mock_print_calls = []

    class MockConsole:
        def print(self, *args, **kwargs):
            mock_print_calls.append((args, kwargs))

        def rule(self, *args, **kwargs):
            mock_print_calls.append((args, kwargs))

        @property
        def width(self):
            return 100

    mock_console = MockConsole()
    monkeypatch.setattr("nebari_doctor.styling.console", mock_console)
    return mock_print_calls


def test_truncate_long_text_under_limit():
    """Test that text under the line limit is not truncated"""
    text = "Line 1\nLine 2\nLine 3"
    result = truncate_long_text(text, max_lines=5)
    assert result == text
    assert len(result.split("\n")) == 3


def test_truncate_long_text_over_limit():
    """Test that text over the line limit is truncated"""
    text = "\n".join([f"Line {i}" for i in range(1, 15)])
    result = truncate_long_text(text, max_lines=10)
    assert "Line 10" in result
    assert "Line 11" not in result
    assert "output truncated" in result


def test_truncate_long_text_wrapping():
    """Test that long lines are wrapped"""
    # Create a very long line that should be wrapped
    long_line = "x" * 200
    result = truncate_long_text(long_line, max_lines=5, console_width=100)
    # The line should be split into at least 2 lines
    assert len(result.split("\n")) >= 2


def test_display_message_agent(mock_console):
    """Test displaying an agent message"""
    display_message("Test message", MessageType.AGENT)
    assert len(mock_console) == 1
    args, kwargs = mock_console[0]
    assert isinstance(args[0], Panel)
    assert "Nebari Doctor" in args[0].title


def test_display_message_user(mock_console):
    """Test displaying a user message"""
    display_message("Test user input", MessageType.USER)
    assert len(mock_console) == 1
    args, kwargs = mock_console[0]
    assert isinstance(args[0], Panel)
    assert "User" in args[0].title


def test_display_message_tool(mock_console):
    """Test displaying tool output"""
    display_message("Tool output", MessageType.TOOL)
    assert len(mock_console) == 1
    args, kwargs = mock_console[0]
    assert isinstance(args[0], Panel)
    assert "Tool Output" in args[0].title


def test_display_message_system(mock_console):
    """Test displaying a system message"""
    display_message("System message", MessageType.SYSTEM)
    assert len(mock_console) == 1
    assert "System message" in str(mock_console[0])


def test_display_message_warning(mock_console):
    """Test displaying a warning message"""
    display_message("Warning message", MessageType.WARNING)
    assert len(mock_console) == 1
    args, kwargs = mock_console[0]
    assert isinstance(args[0], Panel)
    assert "Warning" in args[0].title


def test_display_message_error(mock_console):
    """Test displaying an error message"""
    display_message("Error message", MessageType.ERROR)
    assert len(mock_console) == 1
    args, kwargs = mock_console[0]
    assert isinstance(args[0], Panel)
    assert "Error" in args[0].title


def test_display_header(mock_console):
    """Test displaying a header"""
    display_header("Test Header")
    # Should have 3 calls: empty line, rule, empty line
    assert len(mock_console) == 3
    assert "Test Header" in str(mock_console[1])
