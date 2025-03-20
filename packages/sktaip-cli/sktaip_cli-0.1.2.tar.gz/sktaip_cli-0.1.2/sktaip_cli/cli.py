import os
import sys
import click
import json
from click import secho


@click.group()
def cli():
    """Command-line interface for AIP server management."""
    pass


@cli.command()
@click.option("--host", default="127.0.0.1", help="Host address")
@click.option("--port", default=28080, type=int, help="Port number")
@click.option(
    "--langgraph_json", default="./langgraph.json", help="Path to langgraph.json"
)
def dev(host, port, langgraph_json):
    """Run the development server."""
    try:
        from sktaip_api.server import run_server
    except ImportError as e:
        py_version_msg = ""
        if sys.version_info < (3, 10):
            py_version_msg = (
                "\n\nNote: The in-mem server requires Python 3.10 or higher to be installed."
                f" You are currently using Python {sys.version_info.major}.{sys.version_info.minor}."
                ' Please upgrade your Python version before installing "langgraph-cli[inmem]".'
            )
        try:
            from importlib import util

            if not util.find_spec("sktaip_api"):
                raise click.UsageError(
                    "Required package 'sktaip_api' is not installed.\n"
                    "Please install it with:\n\n"
                    '    pip install -U "sktaip_api"'
                    f"{py_version_msg}"
                )
        except ImportError:
            raise click.UsageError(
                "Could not verify package installation. Please ensure Python is up to date and\n"
                "Please install it with:\n\n"
                '    pip install -U "sktaip_api"'
                f"{py_version_msg}"
            )
        raise click.UsageError(
            "Could not import run_server. This likely means your installation is incomplete.\n"
            "Please install it with:\n\n"
            '    pip install -U "sktaip_api"'
            f"{py_version_msg}"
        )

    working_dir = os.getcwd()
    working_dir = os.path.abspath(working_dir)

    config_path = os.path.join(working_dir, langgraph_json)
    with open(config_path, "r") as f:
        config = json.load(f)

    # include_path를 Python 경로에 추가
    include_paths = config.get("include_path", [])
    for path in include_paths:
        # 상대 경로를 절대 경로로 변환
        abs_path = os.path.abspath(os.path.join(working_dir, path))
        if abs_path not in sys.path:
            sys.path.append(abs_path)
    # If the graph_path contains a directory path and the graph name
    # Handle both "./template/react_agent/graph.py:graph" and "graph.py:graph" formats
    graph_name = config.get("graph_name")
    graph_path = config.get("graph_path")
    abs_graph_path = os.path.abspath(os.path.join(working_dir, graph_path))
    env_path = config.get("env_file")
    abs_env_file = os.path.abspath(os.path.join(working_dir, env_path))

    secho(
        f"Starting server at {host}:{port} with graph {graph_name} from {abs_graph_path}",
        fg="green",
    )
    run_server(
        host=host,
        port=port,
        graph_name=graph_name,
        graph_path=abs_graph_path,
        reload=True,
        env_file=abs_env_file,
    )


if __name__ == "__main__":
    cli()
