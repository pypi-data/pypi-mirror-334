"""
Styling utilities for Nebari Doctor CLI interface.
"""

import contextlib
from enum import Enum
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.theme import Theme

# Define a custom theme with consistent colors
NEBARI_DOCTOR_THEME = Theme(
    {
        # Main conversation colors
        "agent": "bold bright_blue",
        "user": "bold bright_cyan",
        "tool_name": "bold green",
        "tool_output": "dim white",
        "error": "bold red",
        "warning": "yellow",
        "success": "green",
        # UI elements
        "header": "bold bright_magenta",
        "border": "bright_blue",
        "prompt": "bold bright_white",
        "info": "italic bright_black",
    }
)

# Create a console with our theme
console = Console(theme=NEBARI_DOCTOR_THEME)


class MessageType(Enum):
    AGENT = "agent"
    USER = "user"
    TOOL = "tool"
    SYSTEM = "system"
    WARNING = "warning"
    ERROR = "error"


def format_code(code: str, language: str = "yaml") -> Syntax:
    """Format code with syntax highlighting"""
    return Syntax(code, language, theme="monokai", line_numbers=True, word_wrap=True)


def truncate_long_text(
    message: str, max_lines: int = 10, console_width: int = 100
) -> str:
    """Truncate long text to a maximum number of console lines

    Args:
        message (str): The message to truncate
        max_lines (int): Maximum number of lines to display
        console_width (int): Approximate width of the console in characters

    Returns:
        str: The truncated message with indication if truncated
    """
    if not message:
        return ""

    # First split by actual newlines
    lines = message.split("\n")

    # Then handle long lines by wrapping them
    wrapped_lines = []
    for line in lines:
        # Approximate wrapping - subtract some chars for padding and borders
        effective_width = console_width - 10
        if len(line) > effective_width:
            # Split long lines into chunks of approximately console_width
            chunks = [
                line[i : i + effective_width]
                for i in range(0, len(line), effective_width)
            ]
            wrapped_lines.extend(chunks)
        else:
            wrapped_lines.append(line)

    # Apply truncation if needed
    if len(wrapped_lines) > max_lines:
        truncated = wrapped_lines[:max_lines]
        truncated_message = "\n".join(truncated)
        truncated_message += f"\n\n[italic]... (output truncated, {len(wrapped_lines) - max_lines} more lines)[/italic]"
        return truncated_message
    else:
        return "\n".join(wrapped_lines)


def get_clean_text(message: str) -> str:
    """Display clean, copyable text version of the last message

    Args:
        message (str): The message to display

    Returns:
        str: The original message (for potential clipboard integration)
    """
    console.print("\n[bold]Copyable content:[/bold]")
    console.print(message)
    console.print()
    return message


def display_message(
    message: str, message_type: MessageType, title: Optional[str] = None
) -> None:
    """Display a formatted message in the appropriate style"""
    if message_type == MessageType.AGENT:
        panel = Panel(
            Markdown(message),
            title=title or "🤖 Nebari Doctor",
            title_align="left",
            border_style="agent",
            padding=(1, 2),
            expand=False,
        )
        console.print(panel)

    elif message_type == MessageType.USER:
        # Truncate user messages if they're very long
        truncated_message = truncate_long_text(
            message, max_lines=10, console_width=console.width
        )
        panel = Panel(
            truncated_message,
            title=title or "👤 User",
            title_align="left",
            border_style="user",
            padding=(1, 2),
            expand=False,
        )
        console.print(panel)

    elif message_type == MessageType.TOOL:
        # Truncate tool output
        truncated_message = truncate_long_text(
            message, max_lines=10, console_width=console.width
        )
        panel = Panel(
            truncated_message,
            title=title or "🔧 Tool Output",
            title_align="left",
            border_style="tool_name",
            style="tool_output",
            padding=(1, 2),
            expand=False,
        )
        console.print(panel)

    elif message_type == MessageType.SYSTEM:
        console.print(f"[info]{message}[/info]")

    elif message_type == MessageType.WARNING:
        panel = Panel(
            message,
            title="⚠️ Warning",
            title_align="left",
            border_style="warning",
            padding=(1, 2),
            expand=False,
        )
        console.print(panel)

    elif message_type == MessageType.ERROR:
        panel = Panel(
            message,
            title="❌ Error",
            title_align="left",
            border_style="error",
            padding=(1, 2),
            expand=False,
        )
        console.print(panel)


def get_user_input(prompt_text: str = "👤 User: ") -> str:
    """Get input from the user with styled prompt"""
    return hidden_input(f"[prompt]{prompt_text}[/prompt]")


def hidden_input(prompt_text):
    """Gets styled input and hides it afterward using ANSI escape codes

    Compatible with rich console styling
    """

    # Print the prompt with styling, but don't add newline
    console.print(prompt_text, end="", highlight=False)

    # Get input (this adds a newline)
    result = input()

    # Move cursor up and clear the line
    print("\033[1A\033[2K", end="", flush=True)

    return result


def display_header(title: str) -> None:
    """Display a header with the Nebari Doctor title"""
    console.print()
    console.rule(f"[header]{title}[/header]")
    console.print()


@contextlib.contextmanager
def loading_spinner(text: str = "Thinking..."):
    """Display a loading spinner while waiting for an operation to complete"""
    with console.status(f"[info]{text}[/info]", spinner="dots"):
        yield


def display_tool_list(tools: List[Dict[str, Any]]) -> None:
    """Display a formatted list of available tools"""
    table = Table(title="Available Tools", expand=True)
    table.add_column("Tool", style="tool_name")
    table.add_column("Description", style="info")

    for tool in tools:
        table.add_row(tool["name"], tool["description"])

    console.print(table)
    console.print()
