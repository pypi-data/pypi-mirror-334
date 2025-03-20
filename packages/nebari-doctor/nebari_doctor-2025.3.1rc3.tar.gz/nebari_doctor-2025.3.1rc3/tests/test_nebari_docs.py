import tempfile
from pathlib import Path

import pytest

from nebari_doctor.tools.get_nebari_docs import (
    get_nebari_docs_content_tool,
    get_nebari_docs_layout_tool,
)


@pytest.fixture
def mock_docs_dir(monkeypatch):
    """Create a temporary directory with mock documentation files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create directory structure
        (temp_path / "getting-started").mkdir()
        (temp_path / "reference").mkdir()
        (temp_path / "reference" / "architecture").mkdir()

        # Create some mock files
        with open(temp_path / "index.md", "w") as f:
            f.write("# Nebari Documentation\n\nWelcome to Nebari docs.")

        with open(temp_path / "getting-started" / "installation.md", "w") as f:
            f.write("# Installation Guide\n\nHow to install Nebari.")

        with open(temp_path / "reference" / "architecture" / "overview.md", "w") as f:
            f.write("# Architecture Overview\n\nNebari architecture details.")

        with open(temp_path / "reference" / "config.rst", "w") as f:
            f.write("Configuration\n=============\n\nConfiguration options.")

        # Create a non-doc file that should be ignored
        with open(temp_path / "reference" / "image.png", "w") as f:
            f.write("fake image content")

        # Patch the NEBARI_DOCS_DIR to point to our temp directory
        monkeypatch.setattr(
            "nebari_doctor.tools.get_nebari_docs.NEBARI_DOCS_DIR", temp_path
        )

        yield temp_path


def test_get_nebari_docs_layout_tool(mock_docs_dir):
    """Test that the layout tool correctly maps the directory structure."""
    layout = get_nebari_docs_layout_tool()

    # Check top level files
    assert "index.md" in layout
    assert isinstance(layout["index.md"], str)
    assert layout["index.md"].endswith("index.md")

    # Check nested directories
    assert "getting-started" in layout
    assert "installation.md" in layout["getting-started"]

    # Check deeply nested files
    assert "reference" in layout
    assert "architecture" in layout["reference"]
    assert "overview.md" in layout["reference"]["architecture"]
    assert "config.rst" in layout["reference"]

    # Check that non-doc files are excluded
    assert "image.png" not in layout["reference"]


def test_get_nebari_docs_layout_tool_empty_dir(monkeypatch, tmp_path):
    """Test behavior when docs directory is empty."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    monkeypatch.setattr(
        "nebari_doctor.tools.get_nebari_docs.NEBARI_DOCS_DIR", empty_dir
    )

    layout = get_nebari_docs_layout_tool()
    assert layout == {}


def test_get_nebari_docs_layout_tool_missing_dir(monkeypatch, tmp_path):
    """Test behavior when docs directory doesn't exist."""
    missing_dir = tmp_path / "does-not-exist"
    monkeypatch.setattr(
        "nebari_doctor.tools.get_nebari_docs.NEBARI_DOCS_DIR", missing_dir
    )

    layout = get_nebari_docs_layout_tool()
    assert "error" in layout
    assert str(missing_dir) in layout["error"]


def test_get_nebari_docs_content_tool(mock_docs_dir):
    """Test that the content tool correctly retrieves file contents."""
    # Create a list of files to retrieve
    files = [
        mock_docs_dir / "index.md",
        mock_docs_dir / "getting-started" / "installation.md",
    ]

    content = get_nebari_docs_content_tool(files)

    # Check that we got content for both files
    assert len(content) == 2
    assert mock_docs_dir / "index.md" in content
    assert mock_docs_dir / "getting-started" / "installation.md" in content

    # Check the actual content
    assert "Welcome to Nebari docs" in content[mock_docs_dir / "index.md"]
    assert (
        "How to install Nebari"
        in content[mock_docs_dir / "getting-started" / "installation.md"]
    )


def test_get_nebari_docs_content_tool_missing_file(mock_docs_dir, tmp_path):
    """Test behavior when a file doesn't exist."""
    missing_file = tmp_path / "missing.md"

    # This should raise a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        get_nebari_docs_content_tool([missing_file])
