import pathlib

import typer
from nebari.hookspecs import hookimpl

from nebari_doctor.agent import INITIAL_USER_PROMPT, run_agent  # noqa: F401

HERE = pathlib.Path(__file__).parent
TEST_DATA_DIR = HERE.parent / "tests" / "test_data"


@hookimpl
def nebari_subcommand(cli):
    @cli.command()
    def doctor(
        demo: bool = typer.Option(
            False,
            "--demo",
            "-d",
            help="Run the Nebari Doctor in demo mode",
        ),
        prompt: str = typer.Option(
            None,
            "--prompt",
            "-p",
            help="Describe your Nebari issue",
        ),
        config_filepath: pathlib.Path = typer.Option(
            None,
            "--config",
            "-c",
            help="nebari configuration yaml file path",
        ),
    ):
        main(demo, prompt, config_filepath)


def main(demo: bool = False, prompt: str = None, config_filepath: pathlib.Path = None):
    if demo:
        prompt = prompt or DEMO_USER_ISSUE
        config_filepath = config_filepath or DEMO_CONFIG_FILEPATH

    run_agent(prompt, config_filepath)


DEMO_USER_ISSUE = 'My user ad tried to shut down the My Panel App (Git) app started by Andy.  The Jupyterhub landing page said "Server stopped successfully", but the Status of the dashboard remained "Running".  What\'s going on?'

DEMO_CONFIG_FILEPATH = TEST_DATA_DIR / "test-nebari-config.yaml"
