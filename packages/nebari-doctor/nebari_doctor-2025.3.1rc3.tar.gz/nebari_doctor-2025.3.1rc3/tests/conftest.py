import pathlib
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_console():
    """Mock the rich console"""
    with patch("nebari_doctor.styling.console") as mock:
        mock.width = 100
        yield mock


@pytest.fixture
def mock_display_message():
    """Mock the display_message function"""
    with patch("nebari_doctor.styling.display_message") as mock:
        yield mock


@pytest.fixture
def mock_get_user_input():
    """Mock the get_user_input function"""
    with patch("nebari_doctor.styling.get_user_input") as mock:
        mock.return_value = "Test user input"
        yield mock


@pytest.fixture
def mock_agent():
    """Mock the Agent class"""
    with patch("nebari_doctor.agent.Agent") as mock_agent_class:
        agent_instance = MagicMock()
        mock_agent_class.return_value = agent_instance

        # Set up the run_sync method
        run_result = MagicMock()
        run_result.data.message = "Test agent response"
        agent_instance.run_sync.return_value = run_result

        yield agent_instance


@pytest.fixture
def test_config_path():
    """Create a test config path"""
    return pathlib.Path("tests/test_data/test-nebari-config.yaml")
