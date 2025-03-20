import pathlib
import textwrap
import traceback
from functools import wraps

from loguru import logger
from pydantic import BaseModel, Field
from pydantic_ai import Agent

from nebari_doctor.prompts import LLM_SYSTEM_PROMPT, display_tool_info
from nebari_doctor.styling import (
    MessageType,
    display_header,
    display_message,
    get_user_input,
)
from nebari_doctor.tools.get_nebari_config import make_get_nebari_config_tool
from nebari_doctor.tools.get_nebari_docs import (
    get_nebari_docs_content_tool,
    get_nebari_docs_layout_tool,
)
from nebari_doctor.tools.get_pod_logs import (
    get_nebari_pod_logs_tool,
    make_get_nebari_pod_names_tool,
)
from nebari_doctor.utils.clipboard import copy_to_clipboard


def tool_output_wrapper(func):
    """Wrapper to display tool outputs in a consistent format"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        tool_name = func.__name__
        display_message(f"Running tool: {tool_name}", MessageType.SYSTEM)
        result = func(*args, **kwargs)
        if result:
            display_message(
                str(result), MessageType.TOOL, title=f"🔧 {tool_name} Output"
            )
        return result

    return wrapper


MODEL_CONTEXT_LIMIT = {
    # Not in pydantic-ai somewhere
    "openai:gpt-4o": 128_000,
    "google-gla:gemini-2.0-flash-exp": 1_000_000,
}


def message_user(message: str) -> str:
    """
    Send a message to the user.  This tool is used to update the user on the status of trying to fix their problem or to ask the user for additional information, or any other message that the agent wants to send to the user.

    Args:
        message (str): message to display to user

    Returns:
        str: user's response to the message
    """
    display_message(message, MessageType.AGENT)
    user_input = get_user_input()
    return user_input


INITIAL_USER_PROMPT = textwrap.dedent(
    """
    I am an AI Agent designed to help users resolve any Nebari issues and answer questions about Nebari. Tell me the issue you're seeing and I'll do my best to help you resolve your issue.

    I have the following tools at my disposal.
    """
)


class ChatResponse(BaseModel):
    message: str = Field(description="The message to display to the user.")


def run_agent(user_input: str = None, nebari_config_path: pathlib.Path = None) -> None:
    """Runs the Nebari Doctor agent to help users resolve Nebari issues.

    Args:
        user_input (str, optional): Initial user input describing the issue.
            If not given, user will be prompted for input. Defaults to None.
        nebari_config_path (pathlib.Path, optional): Path to nebari config file.
            Needed for some agent tools. Defaults to None.

    Returns:
        None: This function doesn't return a value but runs the interactive agent.
            The agent continues running until manually interrupted.

    Raises:
        KeyboardInterrupt: When the user exits with Ctrl+C
        Exception: For any errors that occur during agent execution
    """
    try:
        display_header("🔍 Welcome to Nebari Doctor")

        tools = [
            tool_output_wrapper(get_nebari_docs_layout_tool),
            tool_output_wrapper(get_nebari_docs_content_tool),
        ]
        for tool in [
            make_get_nebari_config_tool(nebari_config_path),
            make_get_nebari_pod_names_tool(nebari_config_path),
            get_nebari_pod_logs_tool,
        ]:
            if nebari_config_path:
                tools.append(tool_output_wrapper(tool))
        if not nebari_config_path:
            display_message(
                "Nebari config file path not provided. It is strongly recommended to pass in the nebari config file path. The agent's ability to help is severely limited without it.",
                MessageType.WARNING,
            )

        # Show introduction
        display_message(INITIAL_USER_PROMPT, MessageType.SYSTEM)
        show_tools = True

        if show_tools:
            display_tool_info(tools)

        agent = Agent(
            # 'google-gla:gemini-2.0-flash',
            "openai:gpt-4o",  # TODO: Make model configurable
            system_prompt=LLM_SYSTEM_PROMPT,
            result_type=ChatResponse,
            tools=tools,
        )

        latest_result = ChatResponse(message=INITIAL_USER_PROMPT)

        # Display initial user issue
        user_input = user_input
        if not user_input:
            user_input = get_user_input()
        display_message(user_input, MessageType.USER)

        # Main conversation loop
        message_history = []
        latest_result = None
        while True:
            # Handle special commands
            if user_input.strip().startswith("/"):
                command = user_input.strip()

                if command == "/copy":
                    if latest_result:
                        copy_to_clipboard(latest_result.message)
                        display_message(
                            "✅ Copied the last agent message to system clipboard",
                            MessageType.SYSTEM,
                        )
                    else:
                        display_message("No message to copy", MessageType.SYSTEM)
                elif command == "/help":
                    display_message(
                        "Available commands:\n"
                        "/copy - Display the last agent message in copyable format\n"
                        "/help - Show this help message\n"
                        "/clear - Clear the message history\n"
                        "/exit - Exit the application",
                        MessageType.SYSTEM,
                    )
                elif command == "/clear":
                    message_history = []
                    display_message("Message history cleared", MessageType.SYSTEM)
                elif command == "/exit":
                    display_message("Exiting...", MessageType.SYSTEM)
                    return
                else:
                    display_message(
                        f"Unknown command: {command}. Type /help for available commands.",
                        MessageType.SYSTEM,
                    )

                # Get new input after handling command
                user_input = get_user_input()
                display_message(user_input, MessageType.USER)
                continue

            # TODO: Stream the LLM message to a panel

            # Show thinking message
            display_message("Thinking about your question...", MessageType.SYSTEM)

            # Run the agent
            try:
                result = agent.run_sync(user_input, message_history=message_history)
                message_history.extend(result.new_messages())
            except Exception as e:
                logger.error(f"Error while processing: {e}")
                traceback.print_exc()
                display_message(f"Error while processing: {str(e)}", MessageType.ERROR)
                user_input = get_user_input(
                    "Would you like to try again with a different question?"
                )
                continue

            latest_result = result.data
            user_input = message_user(latest_result.message)
            display_message(user_input, MessageType.USER)

    except KeyboardInterrupt:
        display_message("Exiting...", MessageType.SYSTEM)
    except Exception as e:
        display_message(
            f"An error occurred. Now Exiting...\n{str(e)}", MessageType.ERROR
        )
