from itertools import chain
from typing import Generator

from airfold_common.project import ProjectFile
from cachetools import TTLCache, cached

from airfold_cli.api import AirfoldApi
from airfold_cli.models import JobInfo, JobStatus, PipeInfo, PipeInfoStatus


@cached(cache=TTLCache(maxsize=10000, ttl=5))
def get_source_names() -> list[str]:
    api = AirfoldApi.from_config()
    return api.list_source_names()


@cached(cache=TTLCache(maxsize=10000, ttl=5))
def get_objects() -> list[ProjectFile]:
    api = AirfoldApi.from_config()
    return api.pull()


@cached(cache=TTLCache(maxsize=10000, ttl=5))
def get_importable_tables() -> dict[str, list[str]]:
    api = AirfoldApi.from_config()
    return api.get_importable_tables()


def source_name_completion(cur: str) -> Generator[str, None, None]:
    """Pipe name completion."""
    try:
        source_names: list[str] = get_source_names()
        yield from filter(lambda name: name.startswith(cur), source_names) if cur else source_names
    except Exception as e:
        pass


def ai_source_name_completion(cur: str) -> Generator[str, None, None]:
    """Pipe name completion."""
    try:
        objects: list[ProjectFile] = get_objects()
        ai_source_names: list[str] = [source.name for source in objects if source.data.get("type") == "AITable"]
        yield from filter(lambda name: name.startswith(cur), ai_source_names) if cur else ai_source_names
    except Exception as e:
        pass


def importable_table_name_completion(cur: str) -> Generator[str, None, None]:
    """Importable table name completion."""
    try:
        importable_tables: dict[str, list[str]] = get_importable_tables()
        table_names: set[str] = set(chain(*importable_tables.values()))
        yield from filter(lambda name: name.startswith(cur), table_names) if cur else table_names
    except Exception as e:
        pass


def importable_database_name_completion(cur: str) -> Generator[str, None, None]:
    """Importable database name completion."""
    try:
        importable_tables: dict[str, list[str]] = get_importable_tables()
        db_names: list[str] = list(importable_tables.keys())
        yield from filter(lambda name: name.startswith(cur), db_names) if cur else db_names
    except Exception as e:
        pass


@cached(cache=TTLCache(maxsize=10000, ttl=5))
def get_pipes() -> list[PipeInfo]:
    api = AirfoldApi.from_config()
    return api.list_pipes()


def all_pipe_names_completion(cur: str) -> Generator[str, None, None]:
    """All pipe name completion."""
    try:
        pipe_names: list[str] = [pipe.name for pipe in get_pipes()]
        yield from filter(lambda name: name.startswith(cur), pipe_names) if cur else pipe_names
    except Exception as e:
        pass


def endpoint_names_completion(cur: str) -> Generator[str, None, None]:
    """Endpoint name completion."""
    try:
        pipe_names: list[str] = [pipe.name for pipe in get_pipes() if pipe.status == PipeInfoStatus.PUBLISHED]
        yield from filter(lambda name: name.startswith(cur), pipe_names) if cur else pipe_names
    except Exception as e:
        pass


def materializable_pipe_names_completion(cur: str) -> Generator[str, None, None]:
    """Materializable pipe name completion."""
    try:
        pipe_names: list[str] = [pipe.name for pipe in get_pipes() if pipe.status == PipeInfoStatus.DRAFT]
        yield from filter(lambda name: name.startswith(cur), pipe_names) if cur else pipe_names
    except Exception as e:
        pass


def job_ids_completion(cur: str) -> Generator[str, None, None]:
    """Job ID completion."""
    try:
        api = AirfoldApi.from_config()
        jobs: list[JobInfo] = api.list_jobs()
        job_names: list[str] = [job.name for job in jobs if job.status]
        yield from filter(lambda name: name.startswith(cur), job_names) if cur else job_names
    except Exception as e:
        pass


def cancel_job_ids_completion(cur: str) -> Generator[str, None, None]:
    """Job ID completion for cancel command."""
    try:
        api = AirfoldApi.from_config()
        jobs: list[JobInfo] = api.list_jobs()
        job_names: list[str] = [job.name for job in jobs if job.status in [JobStatus.RUNNING, JobStatus.PENDING]]
        yield from filter(lambda name: name.startswith(cur), job_names) if cur else job_names
    except Exception as e:
        pass
