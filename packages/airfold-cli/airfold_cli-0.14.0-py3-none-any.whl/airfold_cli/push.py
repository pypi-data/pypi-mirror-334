from pathlib import Path
from typing import Annotated, List, Optional

from airfold_common.plan import print_plan
from airfold_common.project import LocalFile, dump_yaml, find_project_files, load_files
from typer import Context

from airfold_cli import app
from airfold_cli.api import AirfoldApi
from airfold_cli.error import AirfoldError
from airfold_cli.log import log
from airfold_cli.models import Config, NamedParam
from airfold_cli.options import (
    DryRunOption,
    ForceOption,
    PathArgument,
    PushRenameOption,
    with_global_options,
)
from airfold_cli.root import catch_airfold_error
from airfold_cli.tui.progress import with_spinner
from airfold_cli.utils import dump_json, normalize_name, normalize_path_args


@app.command("push")
@catch_airfold_error()
@with_global_options
def push(
    ctx: Context,
    path: Annotated[Optional[List[str]], PathArgument] = None,
    dry_run: Annotated[bool, DryRunOption] = False,
    force: Annotated[bool, ForceOption] = False,
    rename: Annotated[Optional[NamedParam], PushRenameOption] = None,
) -> None:
    """Push object(s) into runtime database.
    \f

    Args:
        ctx: Typer context
        path: path to local object file(s), ('-' will read objects from stdin)
        dry_run: show execution plan without executing it
        force: force delete/overwrite even if data will be lost
        rename: use `rename` strategy. Specify a single renamed object and its new name.
    """
    app.apply_options(ctx)

    args = normalize_path_args(path)
    files: list[Path] = find_project_files(args)
    if not files:
        raise AirfoldError(f"Cannot find any project files in: {', '.join(args)}")
    log.info(f"Pushing files: {', '.join([str(f) for f in files])}")
    push_all(load_files(files), dry_run=dry_run, force=force, rename=rename)


def push_all(
    files: list[LocalFile],
    dry_run: bool = False,
    force: bool = False,
    rename: NamedParam | None = None,
) -> None:
    api = AirfoldApi.from_config()

    def _push():
        return api.push(
            data=dump_yaml([normalize_name(file.data, file.name) for file in files]),
            dry_run=dry_run,
            force=force,
            rename=rename,
            files=files,
        )

    if app.is_terminal():
        with with_spinner("Pushing objects...", app.console) as progress:
            push_task = progress.add_task("Push", total=1)
            commands = _push()
            progress.update(push_task, completed=1)
            print_plan(commands, console=app.console)
    else:
        commands = _push()
        app.console.print(dump_json(commands))
