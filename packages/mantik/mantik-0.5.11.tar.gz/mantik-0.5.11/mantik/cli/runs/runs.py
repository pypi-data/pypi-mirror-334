import uuid

import click

import mantik.cli._options as _options
import mantik.cli.main as main
import mantik.runs.artifacts as artifacts


@main.cli.group("runs")
def cli() -> None:
    """Interaction with Mantik runs."""


@cli.command("download-artifacts")
@_options.PROJECT_ID
@_options.get_run_id(required=True)
@_options.get_target_dir_option(
    help_option="Path to directory where the artifacts will be downloaded.",
)
@click.option(
    "--unzip/--no-unzip",
    default=True,
    help="Unzip the artifacts in the target dir.",
    show_default=True,
)
def download_artifacts(
    project_id: uuid.UUID,
    run_id: uuid.UUID,
    target_dir: str,
    unzip: bool,
) -> None:
    """Download the artifacts from a run."""
    artifacts.download_artifacts(
        project_id=project_id, run_id=run_id, target_dir=target_dir, unzip=unzip
    )
