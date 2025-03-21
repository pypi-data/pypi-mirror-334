import os
from pathlib import Path
from typing import Annotated, List, Optional

from airfold_common.error import AirfoldError
from airfold_common.plan import print_plan
from airfold_common.project import (
    dump_project_files,
    dump_yaml,
    find_project_files,
    get_local_files,
    load_files,
)
from airfold_common.utils import STREAM_MARKER, is_path_stream
from rich.syntax import Syntax
from typer import Argument, Context

from airfold_cli import app
from airfold_cli.api import AirfoldApi
from airfold_cli.cli import AirfoldTyper
from airfold_cli.completion import (
    all_pipe_names_completion,
    endpoint_names_completion,
    materializable_pipe_names_completion,
)
from airfold_cli.log import log
from airfold_cli.models import NamedParam, OutputDataFormat, PipeInfo
from airfold_cli.options import (
    DryRunOption,
    ForceOption,
    OutputDataFormatOption,
    PathArgument,
    PipeNodeNameOption,
    PipeParamOption,
    TargetDir,
    with_global_options,
)
from airfold_cli.root import catch_airfold_error
from airfold_cli.tui.syntax import get_syntax_theme
from airfold_cli.utils import dump_json, normalize_name, normalize_path_args

pipe_app = AirfoldTyper(
    name="pipe",
    help="Pipe commands.",
)

app.add_typer(pipe_app)


@pipe_app.command("drop")
@catch_airfold_error()
@with_global_options
def drop(
    ctx: Context,
    name: Annotated[str, Argument(help="Pipe name", autocompletion=all_pipe_names_completion)],
    dry_run: Annotated[bool, DryRunOption] = False,
    force: Annotated[bool, ForceOption] = False,
) -> None:
    """Delete pipe.
    \f

    Args:
        ctx: Typer context
        name: pipe name
        dry_run: show plan without executing it
        force: force delete/overwrite even if data will be lost

    """
    pipe_app.apply_options(ctx)

    api = AirfoldApi.from_config()
    commands = api.pipe_delete(name=name, dry_run=dry_run, force=force)
    if pipe_app.is_terminal():
        print_plan(commands, console=pipe_app.console)
    else:
        pipe_app.console.print(dump_json(commands))


@pipe_app.command("ls")
@catch_airfold_error()
@with_global_options
def ls(ctx: Context) -> None:
    """List pipes.
    \f

    Args:
        ctx: Typer context

    """
    pipe_app.apply_options(ctx)

    api = AirfoldApi.from_config()

    pipes_info: list[PipeInfo] = api.list_pipes()

    if not pipes_info:
        if pipe_app.is_terminal():
            pipe_app.console.print("\t[magenta]NO PIPES[/magenta]")
        return

    data: list[dict] = [pipe_info.dict(humanize=True) for pipe_info in pipes_info]
    if pipe_app.is_terminal():
        columns = {
            "Name": "name",
            "Status": "status",
            "Created": "created",
            "Updated": "updated",
        }
        pipe_app.ui.print_table(columns, data=data, title=f"{len(pipes_info)} pipes")
    else:
        for pipe_info in pipes_info:
            pipe_app.console.print(dump_json(pipe_info.dict()))


@pipe_app.command("query")
@catch_airfold_error()
@with_global_options
def query(
    ctx: Context,
    name: Annotated[str, Argument(help="Pipe name", autocompletion=endpoint_names_completion)],
    format: Annotated[OutputDataFormat, OutputDataFormatOption] = OutputDataFormat.NDJSON,
    params: Annotated[Optional[list[NamedParam]], PipeParamOption] = None,
) -> None:
    """Query pipe data.
    \f

    Args:
        ctx: Typer context
        name: pipe name
        format: output data format
        params: pipe parameter(key=value)

    """
    pipe_app.apply_options(ctx)

    api = AirfoldApi.from_config()

    jsons = api.pipe_get_data(
        name=name, output_format=format, params={p.name: p.value for p in params} if params else None
    )

    for json_data in jsons:
        app.console.print(Syntax(dump_json(json_data), "json", theme=get_syntax_theme()))


# @pipe_app.command("rename")
@catch_airfold_error()
@with_global_options
def rename(
    ctx: Context,
    name: Annotated[str, Argument(help="Pipe name", autocompletion=all_pipe_names_completion)],
    new_name: Annotated[str, Argument(help="New pipe name")],
    dry_run: Annotated[bool, DryRunOption] = False,
    force: Annotated[bool, ForceOption] = False,
) -> None:
    """Rename pipe.
    \f

    Args:
        ctx: Typer context
        name: pipe name
        new_name: new pipe name
        dry_run: show plan without executing it
        force: force delete/overwrite even if data will be lost
    """
    pipe_app.apply_options(ctx)

    api = AirfoldApi.from_config()
    commands = api.rename_pipe(name=name, new_name=new_name, dry_run=dry_run, force=force)
    print_plan(commands, console=pipe_app.console)


@pipe_app.command("materialize")
@catch_airfold_error()
@with_global_options
def materialize(
    ctx: Context,
    name: Annotated[str, Argument(help="Pipe name", autocompletion=materializable_pipe_names_completion)],
    path: Annotated[Optional[str], TargetDir] = None,
) -> None:
    """Materialize draft pipe.
    \f

    Args:
        ctx: Typer context
        name: pipe name
        path: target directory to create files in, ('-' will dump to stdout)
    """
    pipe_app.apply_options(ctx)

    api = AirfoldApi.from_config()
    files = get_local_files(api.pipe_materialize(name=name))

    if not path:
        path = STREAM_MARKER

    if not is_path_stream(path):
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            raise AirfoldError(f"Target path is not a directory: {path}")

    if not is_path_stream(path):
        dump_project_files(files, path)
    else:
        app.console.print(Syntax(dump_yaml([file.data for file in files]), "yaml", theme=get_syntax_theme()))


@pipe_app.command("run")
@catch_airfold_error()
@with_global_options
def run(
    ctx: Context,
    name: Annotated[str, Argument(help="Pipe name")],
    path: Annotated[Optional[List[str]], PathArgument] = None,
    format: Annotated[OutputDataFormat, OutputDataFormatOption] = OutputDataFormat.NDJSON,
    params: Annotated[Optional[list[NamedParam]], PipeParamOption] = None,
    node: Annotated[Optional[str], PipeNodeNameOption] = None,
) -> None:
    """Run pipe and get data.
    \f

    Args:
        ctx: Typer context
        name: pipe name
        path: path to local object file(s), ('-' will read objects from stdin)
        format: output data format
        params: pipe parameter(key=value)
        node: pipe node name

    """
    pipe_app.apply_options(ctx)
    api = AirfoldApi.from_config()

    args = normalize_path_args(path)
    files: list[Path] = find_project_files(args)

    pipe_schema: Optional[list[dict]] = None
    if files:
        loaded_files = load_files(files)
        pipe_schema = [normalize_name(file.data, file.name) for file in loaded_files]

    if node:
        if not pipe_schema:
            pulled_files = api.pull(names=[name])
            pipe_schema = [normalize_name(file.data, file.name) for file in pulled_files]
        else:
            pipe_schema = [pipe for pipe in pipe_schema if pipe["name"] == name]

        if not pipe_schema:
            raise AirfoldError(f"Pipe not found: {name}")
        if len(pipe_schema) > 1:
            raise AirfoldError(f"Multiple pipes with name {name} found")
        nodes = pipe_schema[0].get("nodes", [])
        node_idx = next((i for i, n in enumerate(nodes) if list(n.keys())[0] == node), None)
        if node_idx is not None:
            nodes = nodes[: node_idx + 1]
        else:
            raise AirfoldError(f"Node {node} not found in pipe {name}")
        pipe_schema[0]["nodes"] = nodes
        pipe_schema[0]["name"] = "generatedFile"  # same name as UI uses
    jsons = api.pipe_run(
        name=name,
        pipe_schema=pipe_schema,
        output_format=format,
        params={p.name: p.value for p in params} if params else None,
    )

    for json_data in jsons:
        app.console.print(Syntax(dump_json(json_data), "json", theme=get_syntax_theme()))
