import re
import tempfile
from pathlib import Path
from typing import Annotated, List, Optional

from airfold_common.project import dump_project_files, find_project_files, load_files
from typer import Context

from airfold_cli import app
from airfold_cli.api import AirfoldApi
from airfold_cli.options import PathArgument, with_global_options
from airfold_cli.root import catch_airfold_error
from airfold_cli.tui.diff import render_diff
from airfold_cli.utils import get_local_files, normalize_path_args


@app.command("diff")
@catch_airfold_error()
@with_global_options
def diff(
    ctx: Context,
    path: Annotated[Optional[List[str]], PathArgument] = None,
):
    """Diff between local and remote objects.
    \f

    Args:
        ctx: Typer context
        path: path to local object file(s), ('-' will read objects from stdin)
    """
    app.apply_options(ctx)
    api = AirfoldApi.from_config()

    args = normalize_path_args(path)
    paths: list[Path] = find_project_files(args)
    files = load_files(paths)

    diff_result = api.diff(files)
    with tempfile.TemporaryDirectory() as local_files_tmp_dir:
        dump_project_files(get_local_files(diff_result.files), local_files_tmp_dir)
        with tempfile.TemporaryDirectory() as pulled_local_files_tmp_dir:
            dump_project_files(get_local_files(diff_result.pulled_files), pulled_local_files_tmp_dir)
            render_diff(Path(local_files_tmp_dir), re.sub(r"\/tmp\/[^\/]+", "", diff_result.diff), console=app.console)
            # TODO: print diff as json if it's not a tty
