from nebari_doctor.styling import truncate_long_text


def test_truncate_short_text():
    """Test that short text is not truncated"""
    text = "This is a short text"
    result = truncate_long_text(text, max_lines=10)
    assert result == text


def test_truncate_multiline_text():
    """Test truncation of multiline text"""
    lines = [f"Line {i}" for i in range(20)]
    text = "\n".join(lines)
    result = truncate_long_text(text, max_lines=10)

    # Should contain first 10 lines
    for i in range(10):
        assert f"Line {i}" in result

    # Should not contain lines after 10
    for i in range(10, 20):
        assert f"Line {i}" not in result

    # Should contain truncation message
    assert "output truncated" in result
    assert "10 more lines" in result


def test_truncate_long_line():
    """Test truncation of a single long line"""
    # Create a line that's much longer than the console width
    long_line = "x" * 500
    result = truncate_long_text(long_line, max_lines=10, console_width=80)

    # The line should be split into multiple lines
    lines = result.split("\n")
    assert len(lines) > 1

    # Each line should be approximately console_width in length
    for line in lines:
        if "output truncated" not in line:  # Skip the truncation message
            assert len(line) <= 80


def test_truncate_mixed_content():
    """Test truncation of mixed content (short and long lines)"""
    # Create a mix of short and long lines
    lines = []
    for i in range(5):
        lines.append(f"Short line {i}")
    for i in range(5):
        lines.append("x" * 200)  # Long lines

    text = "\n".join(lines)
    result = truncate_long_text(text, max_lines=10, console_width=80)

    # Count the number of lines in the result
    result_lines = result.split("\n")
    # Should be more than 10 due to wrapping of long lines
    assert len(result_lines) > 10

    # Should contain truncation message
    assert "output truncated" in result


def test_truncate_edge_cases():
    """Test edge cases for truncation"""
    # Empty string
    assert truncate_long_text("", max_lines=10) == ""

    # Single line exactly at max_lines
    text = "\n".join([f"Line {i}" for i in range(10)])
    assert truncate_long_text(text, max_lines=10) == text

    # Single line exactly at max_lines + 1
    text = "\n".join([f"Line {i}" for i in range(11)])
    result = truncate_long_text(text, max_lines=10)
    assert "Line 10" not in result
    assert "output truncated" in result
