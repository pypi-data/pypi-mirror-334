import pathlib

import rich
from _nebari.config import (  # TODO: Don't import from non public module
    read_configuration,
)


def make_get_nebari_config_tool(config_filepath: pathlib.Path) -> str:
    def get_nebari_config_tool():
        """
        Returns the Nebari configuration for inspection"""
        return get_nebari_config(config_filepath)

    return get_nebari_config_tool


def get_nebari_config(config_filepath: pathlib.Path):
    from nebari.plugins import nebari_plugin_manager

    NebariConfigSchema = nebari_plugin_manager.config_schema

    rich.print("[grey70]Reading nebari config...[/grey70]")
    nebari_config = read_configuration(config_filepath, NebariConfigSchema)
    return nebari_config.model_dump_json(indent=2)
