from pathlib import Path

NEBARI_DOCS_DIR = Path(__file__).parent.parent.parent / "resources/nebari-docs"


# TODO: Get logs associated with the version of Nebari the user is using rather than relying on the hard coded docs
def get_nebari_docs_layout_tool():
    """Walk the directory structure of the Nebari docs and return a dictionary
    representing the layout of the docs.
    """
    layout = {}

    if not NEBARI_DOCS_DIR.exists():
        return {"error": f"Docs directory not found at {NEBARI_DOCS_DIR}"}

    # Walk through the directory structure
    for item in NEBARI_DOCS_DIR.glob("**/*"):
        if item.is_file() and item.suffix in [".md", ".rst", ".txt"]:
            # Get relative path from the docs directory
            rel_path = item.relative_to(NEBARI_DOCS_DIR)

            # Create nested dictionary structure based on path
            current = layout
            parts = list(rel_path.parts)

            # Process all directories in the path
            for i, part in enumerate(parts[:-1]):
                if part not in current:
                    current[part] = {}
                current = current[part]

            # Add the file at the end
            current[parts[-1]] = str(rel_path)

    return layout


def get_nebari_docs_content_tool(files: list[Path]):
    """Retrieve the content of the specified documentation files.

    Args:
        files: A list of Path objects pointing to documentation files

    Returns:
        A dictionary mapping file paths to their content

    Raises:
        FileNotFoundError: If any of the specified files don't exist
    """
    content = dict()
    for file in files:
        with open(NEBARI_DOCS_DIR / file) as f:
            content[file] = f.read()
    return content
