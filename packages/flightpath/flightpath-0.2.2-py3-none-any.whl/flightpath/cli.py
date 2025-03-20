#!/usr/bin/env python3

import logging
import importlib.metadata

import click

from flightpath.tracer import AirflowClient, CriticalPathTracer
from flightpath.config import get_auth_config

# Get version from package metadata
try:
    __version__ = importlib.metadata.version("flightpath")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


# Updated CLI commands
@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Flightpath: A tool for calculating critical paths in orchestrated workflows

    This CLI helps calculate and analyze the critical paths in your orchestrated
    workflows (DAGs). Identify bottlenecks and optimization opportunities in your
    workflows.
    """
    # Configure flightpath logger only
    flightpath_logger = logging.getLogger("flightpath")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    flightpath_logger.addHandler(handler)
    flightpath_logger.setLevel(logging.DEBUG if verbose else logging.INFO)


@cli.command()
def version():
    """Display the version of flightpath."""
    click.echo(__version__)


@cli.command()
@click.option("-u", "--username", type=str, help="Airflow username")
@click.option("-p", "--password", type=str, help="Airflow password")
@click.option("--baseurl", help="Base URL of the Airflow instance")
@click.option(
    "--end-task-id",
    required=True,
    help="ID of the task from which to trace the critical path",
)
@click.option(
    "--end-dag-id",
    help="ID of the dag from which to trace the critical path",
)
@click.option(
    "--dag-run-id", required=True, help="DAG run ID in which to trace the critical path"
)
@click.option(
    "-e",
    "--external",
    is_flag=True,
    help="Recursively trace critical path through external DAGs that are upstream dependencies of the DAG specified by --end-dag-id.",
)
@click.option(
    "--url",
    is_flag=True,
    help="Print the full URL for each task instance instead of using hyperlinks. Helpful if your terminal does not support OSC8 hyperlinks.",
)
@click.option(
    "-f",
    "--format",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Output format. 'table' for human-readable tabular output, 'json' for machine-readable JSON.",
)
@click.pass_context
def trace(
    ctx: click.Context,
    username: str,
    password: str,
    baseurl: str,
    end_task_id: str,
    end_dag_id: str,
    dag_run_id: str,
    external: bool,
    url: bool,
    format: str,
) -> None:
    """Trace and analyze the critical path of an Airflow DAG run.

    Terminology:\n
    - Running Time: The time a task takes to run (end_time minus start_time)\n
    - Ready Time: The time from when task's upstream dependencies are satisfied to when the task starts to run\n
    - Total Time: Ready Time + Running Time\n
    - Critical Path: Given an end task, the critical path is the longest task in the DAG ending at said task. Here, path length is defined as the sum of the Total Time for each task on the path.\n

    Examples:\n
        # Analyze a local Airflow instance\n
        $ flightpath trace -u admin -p admin --baseurl http://localhost:8080 --end-task-id end --end-dag-id my_dag --dag-run-id scheduled__2024-01-01T00:00:00+00:00
    """
    # Get config values
    config = get_auth_config()

    # Command line args take precedence over config file
    username = username or config["username"]
    password = password or config["password"]
    baseurl = baseurl or config["baseurl"]

    # Validate required auth parameters
    if not all([username, password, baseurl]):
        missing = []
        if not username:
            missing.append("username")
        if not password:
            missing.append("password")
        if not baseurl:
            missing.append("baseurl")
        raise click.UsageError(
            f"Missing required authentication parameters: {', '.join(missing)}. "
            "Please provide them via command line arguments or in ~/.config/flightpath/config.json"
        )

    client = AirflowClient(user=username, password=password, base_url=baseurl)
    tracer = CriticalPathTracer(client)

    root_ti = tracer.trace(
        end_dag_id=end_dag_id,
        end_task_id=end_task_id,
        dag_run_id=dag_run_id,
        external=external,
    )

    CriticalPathTracer.print_critical_path(
        root_ti=root_ti, print_url=url, output_format=format
    )


if __name__ == "__main__":
    cli()

    # Start toy airflow instance
    # cd ~/src/flightpath/tests/airflow_example; astro dev start; cd -

    # Run flightpath
    # uv run flightpath --verbose trace -u admin -p admin --baseurl http://localhost:8080 --end-task-id end --end-dag-id diamond1 --dag-run-id scheduled__2025-03-15T17:20:00+00:00
