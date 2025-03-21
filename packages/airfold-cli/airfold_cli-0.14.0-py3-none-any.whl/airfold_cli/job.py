import time
from typing import Annotated, Optional

from airfold_common.error import AirfoldError
from typer import Argument, Context

from airfold_cli import app
from airfold_cli.api import AirfoldApi
from airfold_cli.cli import AirfoldTyper
from airfold_cli.completion import cancel_job_ids_completion
from airfold_cli.models import JobStatus, PipeInfo
from airfold_cli.options import MaxWaitOption, WaitOption, with_global_options
from airfold_cli.root import catch_airfold_error
from airfold_cli.utils import dump_json

job_app = AirfoldTyper(
    name="job",
    help="Job commands.",
)

app.add_typer(job_app)


def wait_for_job_status(api: AirfoldApi, job_id: str, desired_states: list[JobStatus], timeout: int = 900) -> JobStatus:
    """Wait for job to reach desired states."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_status: Optional[JobStatus] = None
        job_info = api.list_jobs()
        for ji in job_info:
            if ji.name == job_id:
                current_status = ji.status

        if not current_status:
            raise AirfoldError(f"Job {job_id} not found")

        if current_status in desired_states:
            return current_status
        time.sleep(2)  # Sleep for 2 seconds before polling again
    raise TimeoutError(f"Job {job_id} did not reach desired states {desired_states} within {timeout} seconds.")


@job_app.command("ls")
@catch_airfold_error()
@with_global_options
def ls(ctx: Context) -> None:
    """List jobs.
    \f

    Args:
        ctx: Typer context

    """
    job_app.apply_options(ctx)

    api = AirfoldApi.from_config()

    jobs_info: list[PipeInfo] = api.list_jobs() + api.list_cron_jobs()

    if not jobs_info:
        if job_app.is_terminal():
            job_app.console.print("\t[magenta]NO JOBS[/magenta]")
        return

    data: list[dict] = [job_info.dict(humanize=True) for job_info in jobs_info]
    if job_app.is_terminal():
        columns = {
            "Id": "name",
            "Status": "status",
            "Created": "created",
            "Updated": "updated",
            "Stats": "stats",
        }
        job_app.ui.print_table(columns, data=data, title=f"{len(jobs_info)} jobs")
    else:
        for job_info in jobs_info:
            job_app.console.print(dump_json(job_info.dict()))


@job_app.command("cancel")
@catch_airfold_error()
@with_global_options
def cancel(
    ctx: Context,
    job_id: Annotated[str, Argument(help="Job ID.", autocompletion=cancel_job_ids_completion)],
    wait: Annotated[bool, WaitOption] = False,
    max_wait: Annotated[int, MaxWaitOption] = 900,
) -> None:
    """Cancel job.
    \f

    Args:
        ctx: Typer context
        job_id: Job ID
        wait: Wait for job cancellation to complete
        max_wait: Maximum time to wait for job cancellation
    """
    job_app.apply_options(ctx)

    api = AirfoldApi.from_config()

    api.cancel_job(job_id)

    if wait:
        try:
            wait_for_job_status(api, job_id, [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELED], max_wait)
        except TimeoutError:
            job_app.ui.print_error(f"Waiting for job [cyan]'{job_id}'[/cyan] to cancel timed out")
            return

    if job_app.is_terminal():
        job_app.ui.print_success(f"Job [cyan]'{job_id}'[/cyan] canceled")
