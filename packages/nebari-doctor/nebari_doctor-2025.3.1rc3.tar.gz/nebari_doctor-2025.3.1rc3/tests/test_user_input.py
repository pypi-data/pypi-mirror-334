from unittest.mock import patch

from nebari_doctor.styling import get_user_input


@patch("nebari_doctor.styling.hidden_input")
def test_get_user_input_default_prompt(mock_input):
    """Test get_user_input with default prompt"""
    mock_input.return_value = "Test input"

    result = get_user_input()

    # Check that hidden_input was called with the default prompt
    mock_input.assert_called_once()
    args = mock_input.call_args[0][0]
    assert "User" in args

    # Check that the function returns the input
    assert result == "Test input"


@patch("nebari_doctor.styling.hidden_input")
def test_get_user_input_custom_prompt(mock_input):
    """Test get_user_input with custom prompt"""
    mock_input.return_value = "Test input"

    result = get_user_input("Custom prompt")

    # Check that hidden_input was called with the custom prompt
    mock_input.assert_called_once()
    args = mock_input.call_args[0][0]
    assert "Custom prompt" in args

    # Check that the function returns the input
    assert result == "Test input"
