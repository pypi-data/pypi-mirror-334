import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import requests
from airfold_common.error import AirfoldError
from airfold_common.models import FixResult, Issue
from airfold_common.project import LocalFile, ProjectFile, dump_yaml
from airfold_common.utils import compact_format_to_dict, uuid
from multidict import MultiDict
from requests import JSONDecodeError, PreparedRequest, Response
from requests.auth import AuthBase
from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)
from typing_extensions import Self

from airfold_cli._pydantic import BaseModel, Field, SecretStr
from airfold_cli.error import (
    APIError,
    ConflictError,
    ForbiddenError,
    InternalServerError,
    ProjectNotFoundError,
    RequestTooLargeError,
    UnauthorizedError,
)
from airfold_cli.models import (
    Config,
    CronJobInfo,
    JobInfo,
    JobStatus,
    JobType,
    NamedParam,
    OutputDataFormat,
    PipeInfo,
    PipeInfoStatus,
    Plan,
    ProjectProfile,
    RecalcJobInfo,
    SchemaFormat,
    SourceInfo,
    SourceType,
    UserProfile,
)
from airfold_cli.utils import load_config, normalize_name, subst_error_in_file

AIRFOLD_API_URL = "https://api.us.airfold.co"

RETRY_TIMES = 3
WAIT_MIN_SECONDS = 0.5
WAIT_MAX_SECONDS = 5

ERRORS_TABLE = "_errors"
DEFAULT_DATE = datetime(1970, 1, 1)
MAX_MESSAGE_LENGTH = int(256 * 1024)


class SourceStatsBin(BaseModel):
    ts: str
    bytes_on_disk: int = Field(default=0)
    rows: int = 0
    errors: int = 0
    ingested_bytes: int = Field(default=0)
    ingested_rows: int = Field(default=0)
    ai_prompt_tokens: int = Field(default=0)
    ai_prompt_completion_tokens: int = Field(default=0)
    ai_total_tokens: int = Field(default=0)


class SourceStats(BaseModel):
    name: str
    bytes_on_disk: int = Field(default=0)
    rows: int = 0
    errors: int = 0
    ingested_bytes: int = Field(default=0)
    ingested_rows: int = Field(default=0)
    ai_prompt_tokens: int = Field(default=0)
    ai_prompt_completion_tokens: int = Field(default=0)
    ai_total_tokens: int = Field(default=0)
    bins: list[SourceStatsBin] = Field(default_factory=list)


class LintResult(BaseModel):
    errors: list[str]
    files: list[ProjectFile]
    diff: Optional[str]
    pulled_files: list[ProjectFile]


class DiffResult(BaseModel):
    diff: str
    files: list[ProjectFile]
    pulled_files: list[ProjectFile]


def api_retry(func):
    def wrapper(*args, **kwargs):
        return Retrying(
            retry=retry_if_exception_type(ConflictError),
            stop=stop_after_attempt(max_attempt_number=RETRY_TIMES),
            reraise=True,
            wait=wait_random_exponential(multiplier=1, min=WAIT_MIN_SECONDS, max=WAIT_MAX_SECONDS),
        )(func, *args, **kwargs)

    return wrapper


class BearerAuth(AuthBase):
    def __init__(self, token: Union[str]) -> None:
        self.token = token

    def __call__(self, req: PreparedRequest) -> PreparedRequest:
        req.headers["authorization"] = "Bearer " + self.token
        return req


class AirfoldApi:
    def __init__(self, api_key: str = "", endpoint: str = ""):
        self.auth: AuthBase = BearerAuth(api_key)
        self.endpoint: str = os.environ.get("AIRFOLD_API_URL", endpoint or AIRFOLD_API_URL)
        self._identity: Union[UserProfile, ProjectProfile] | None = None

    @classmethod
    def from_config(cls, _config: Config | None = None) -> Self:
        config: Config = _config or load_config()
        return cls.from_data(api_key=config.key, endpoint=config.endpoint)

    @classmethod
    def from_data(cls, api_key: SecretStr | str, endpoint: str) -> Self:
        if isinstance(api_key, SecretStr):
            return cls(api_key=api_key.get_secret_value(), endpoint=endpoint)
        return cls(api_key=api_key, endpoint=endpoint)

    def _get_identity(self) -> Response:
        return requests.get(self.endpoint + "/v1/auth/identity", auth=self.auth)

    @api_retry
    def get_identity(self) -> Union[ProjectProfile, UserProfile]:
        res = self._get_identity()
        if res.ok:
            json_data = res.json()
            if json_data.get("user"):
                return UserProfile(**json_data.get("user"))
            else:
                return ProjectProfile(**json_data)

        raise self._resp_to_err(res)

    @property
    def identity(self) -> Union[ProjectProfile, UserProfile]:
        if not self._identity:
            self._identity = self.get_identity()
        return self._identity  # type: ignore

    def get_project_profile(self) -> ProjectProfile:
        if isinstance(self.identity, UserProfile):
            raise APIError("User-scoped API key used, please use workspace-scoped key")
        return self.identity

    def get_org_id(self) -> str:
        if isinstance(self.identity, UserProfile):
            return self.identity.organizations[0].id
        return self.identity.org_id

    @api_retry
    def list_projects(self, org_id: Optional[str] = None) -> Response:
        return requests.get(self.endpoint + f"/v1/{org_id or self.get_org_id()}/projects", auth=self.auth)

    @staticmethod
    def parse_error_response(res: Response) -> str:
        try:
            data: Dict = res.json()
            if data.get("error"):
                return data["error"]
            return res.reason
        except JSONDecodeError:
            pass
        if len(res.text) > 0 and res.status_code == 500:
            return res.text
        return res.reason

    def _resp_to_err(self, res: Response, files: list[LocalFile] | None = None) -> APIError:
        desc = self.parse_error_response(res)
        if files:
            desc = subst_error_in_file(desc, files)
        if res.status_code == 401:
            return UnauthorizedError(desc)
        elif res.status_code == 403:
            return ForbiddenError(desc)
        elif res.status_code == 404:
            return ProjectNotFoundError(desc)
        elif res.status_code == 409:
            return ConflictError(desc)
        elif res.status_code >= 500:
            return InternalServerError(desc)
        elif res.status_code == 413:
            return RequestTooLargeError(desc)
        return APIError(desc)

    def _push(
        self,
        data: str,
        dry_run: bool,
        force: bool,
        rename: Optional[NamedParam],
    ) -> Response:
        url = self.endpoint + f"/v1/push"
        params: dict[str, Any] = {"dry_run": dry_run, "force": force}
        if rename:
            params["rename"] = f"{rename.name}={rename.value}"
        headers = {"Content-Type": "application/yaml"}
        response = requests.post(url, data=data, params=params, headers=headers, auth=self.auth)

        return response

    @api_retry
    def push(
        self,
        data: str,
        dry_run: bool = False,
        force: bool = False,
        rename: Optional[NamedParam] = None,
        files: list[LocalFile] | None = None,
    ) -> Plan:
        res = self._push(data, dry_run, force, rename)
        if res.ok:
            return list(res.json())
        raise self._resp_to_err(res, files)

    def _pull(self, names: list[str]) -> Response:
        params: MultiDict = MultiDict()
        for name in names:
            params.add("name", name)
        return requests.get(self.endpoint + f"/v1/pull", auth=self.auth, params=params.items())

    @api_retry
    def pull(
        self,
        names: Optional[list[str]] = None,
    ) -> List[ProjectFile]:
        res = self._pull(names or [])
        if res.ok:
            return [ProjectFile(name=data["name"], data=data, pulled=True) for data in res.json()]  # type: ignore
        raise self._resp_to_err(res)

    def _graph(
        self,
    ) -> Response:
        return requests.get(self.endpoint + f"/v1/graph", auth=self.auth)

    @api_retry
    def graph(
        self,
    ) -> Dict:
        res = self._graph()
        if res.ok:
            return res.json()
        raise self._resp_to_err(res)

    def _pipe_delete(self, name: str, dry_run: bool, force: bool) -> Response:
        params = {"dry_run": dry_run, "force": force}
        return requests.delete(
            self.endpoint + f"/v1/pipes/{name}",
            params=params,
            auth=self.auth,
        )

    @api_retry
    def pipe_delete(self, name: str, dry_run: bool = False, force: bool = False) -> Plan:
        res = self._pipe_delete(name, dry_run, force)
        if res.ok:
            return list(res.json())
        raise self._resp_to_err(res)

    def _source_delete(self, name: str, dry_run: bool, force: bool) -> Response:
        params = {"dry_run": dry_run, "force": force}
        return requests.delete(
            self.endpoint + f"/v1/sources/{name}",
            params=params,
            auth=self.auth,
        )

    @api_retry
    def source_delete(self, name: str, dry_run: bool = False, force: bool = False) -> Plan:
        res = self._source_delete(name, dry_run, force)
        if res.ok:
            return list(res.json())
        raise self._resp_to_err(res)

    @staticmethod
    def _parse_data(res: Response, format: OutputDataFormat) -> List[Dict]:
        if format == OutputDataFormat.JSON:
            return [res.json()]

        ndjson_lines = res.text.split("\n")
        parsed_json = []
        for line in ndjson_lines:
            if line:
                json_object = json.loads(line)
                parsed_json.append(json_object)

        return parsed_json

    @staticmethod
    def _make_pipe_name_format(name: str, output_format: OutputDataFormat) -> str:
        return f"{name}.{output_format}"

    def _pipe_get_data(
        self, name: str, output_format: OutputDataFormat, params: Optional[dict[str, str]] = None
    ) -> Response:
        return requests.get(
            self.endpoint + f"/v1/pipes/{self._make_pipe_name_format(name, output_format)}",
            auth=self.auth,
            params=params,
        )

    @api_retry
    def pipe_get_data(
        self,
        name: str,
        output_format: OutputDataFormat = OutputDataFormat.NDJSON,
        params: Optional[dict[str, str]] = None,
    ) -> List[Dict]:
        res = self._pipe_get_data(name, output_format=output_format, params=params)
        if res.ok:
            return self._parse_data(res, output_format)
        raise self._resp_to_err(res)

    def _pipe_run(
        self,
        name: str,
        pipe_schema: Optional[Union[dict[str, Any], list[dict[str, Any]]]],
        output_format: OutputDataFormat,
        params: Optional[dict[str, str]],
    ) -> Response:
        headers = {"Content-Type": "application/yaml"}
        return requests.post(
            self.endpoint + f"/v1/run/{self._make_pipe_name_format(name, output_format)}",
            headers=headers,
            data=dump_yaml(pipe_schema) if pipe_schema else None,
            auth=self.auth,
            params=params,
        )

    @api_retry
    def pipe_run(
        self,
        name: str,
        pipe_schema: Optional[Union[dict[str, Any], list[dict[str, Any]]]] = None,
        output_format: OutputDataFormat = OutputDataFormat.NDJSON,
        params: Optional[dict[str, str]] = None,
    ) -> List[Dict]:
        res = self._pipe_run(name, pipe_schema, output_format, params)
        if res.ok:
            return self._parse_data(res, output_format)
        raise self._resp_to_err(res)

    @api_retry
    def sql_run(self, query: str, output_format: OutputDataFormat = OutputDataFormat.NDJSON) -> List[Dict]:
        res = self._pipe_run(
            name=f"pipe_{uuid()}",
            pipe_schema={
                "nodes": [{"runner": {"sql": query}}],
            },
            output_format=output_format,
            params=None,
        )
        if res.ok:
            return self._parse_data(res, output_format)
        raise self._resp_to_err(res)

    def list_pipe_names(self) -> List[str]:
        json_graph = self.graph()
        pipes: list[dict] = json_graph.get("pipes", [])
        return [p["data"]["name"] for p in pipes]

    def list_pipes(self) -> List[PipeInfo]:
        json_graph = self.graph()

        pipes: list[dict] = json_graph.get("pipes", [])
        if not pipes:
            return []

        pipes_info: list[PipeInfo] = []
        for pipe in pipes:
            data: dict[str, Any] = pipe["data"]

            status: PipeInfoStatus = PipeInfoStatus.DRAFT
            if data.get("publish"):
                status = PipeInfoStatus.PUBLISHED
            elif data.get("to"):
                status = PipeInfoStatus.MATERIALIZED

            metadata: dict = data.get("metadata") or {}

            pipes_info.append(
                PipeInfo(
                    name=data["name"],
                    status=status,
                    created=metadata.get("created_at", DEFAULT_DATE),
                    updated=metadata.get("updated_at", DEFAULT_DATE),
                )
            )

        return pipes_info

    def list_source_names(self) -> List[str]:
        json_graph = self.graph()
        sources: list[dict] = list(filter(lambda s: s["type"] != "external", json_graph.get("sources", [])))
        return [s["data"]["name"] for s in sources]

    def list_sources(self) -> List[SourceInfo]:
        json_graph = self.graph()

        sources: list[dict] = list(filter(lambda s: s["type"] != "external", json_graph.get("sources", [])))
        if not sources:
            return []

        metrics: dict[str, Any] = self.get_metrics(names=[s["data"]["name"] for s in sources])

        sources_info: list[SourceInfo] = []
        for source in sources:
            data: dict[str, Any] = source["data"]
            name = data["name"]
            sm: Optional[dict] = metrics.get(name)
            if not sm:
                raise APIError(f"Failed to get metrics for source {name}")

            metadata: dict = data.get("metadata") or {}
            sources_info.append(
                SourceInfo(
                    name=name,
                    type=SourceType.AI_TABLE if data.get("kind") == "AITable" else SourceType.TABLE,
                    created=metadata.get("created_at", DEFAULT_DATE),
                    updated=metadata.get("updated_at", DEFAULT_DATE),
                    rows=sm.get("rows", 0),
                    bytes=sm.get("bytes_on_disk", 0),
                    errors=sm.get("errors", 0),
                )
            )

        return sources_info

    def _rename(self, url_path: str, new_name: str, dry_run: bool, force: bool) -> Response:
        params: dict[str, bool | str] = {"new_name": new_name, "dry_run": dry_run, "force": force}
        return requests.post(
            self.endpoint + url_path,
            params=params,
            auth=self.auth,
        )

    @api_retry
    def rename_source(self, name: str, new_name: str, dry_run: bool = False, force: bool = False) -> Plan:
        res = self._rename(f"/v1/sources/{name}", new_name, dry_run, force)
        if res.ok:
            return list(res.json())
        raise self._resp_to_err(res)

    @api_retry
    def rename_pipe(self, name: str, new_name: str, dry_run: bool = False, force: bool = False) -> Plan:
        res = self._rename(f"/v1/pipes/{name}", new_name, dry_run, force)
        if res.ok:
            return list(res.json())
        raise self._resp_to_err(res)

    def _send_events(
        self,
        src_name: str,
        data: str,
    ) -> Response:
        url = self.endpoint + f"/v1/events/{src_name}"
        response = requests.post(url, data=data, auth=self.auth)

        return response

    def send_events(self, src_name: str, events: list[str]) -> str:
        ndjson = "\n".join(events)
        res = self._send_events(src_name, ndjson)
        if res.ok:
            return "ok"
        raise self._resp_to_err(res)

    def get_max_events_length(self) -> int:
        return MAX_MESSAGE_LENGTH

    def _doctor_run(self, checks: Optional[list[str]] = None, fix: bool = False) -> Response:
        params: dict[str, Any] = {"fix": fix}
        if checks:
            params["checks"] = ",".join(checks)
        return requests.post(self.endpoint + f"/v1/doctor", params=params, auth=self.auth)

    def _doctor_list_checks(self) -> Response:
        return requests.get(self.endpoint + f"/v1/doctor", auth=self.auth)

    @api_retry
    def doctor_run(self, checks: Optional[list[str]] = None, fix: bool = False) -> tuple[list[Issue], list[FixResult]]:
        res = self._doctor_run(checks, fix)
        if res.ok:
            json_data = res.json()
            fix_results: list[FixResult] = []
            issues: list[Issue] = []

            if fix:
                fix_results = [FixResult(**fix_result) for fix_result in json_data]
                issues = [fix_result.issue for fix_result in fix_results]
            else:
                issues = [Issue(**issue) for issue in json_data]
            return issues, fix_results
        raise self._resp_to_err(res)

    @api_retry
    def doctor_list_checks(self) -> list[str]:
        res = self._doctor_list_checks()
        if res.ok:
            return res.json()
        raise self._resp_to_err(res)

    @staticmethod
    def _schema_format_to_mime_type(schema_format: SchemaFormat) -> str:
        if schema_format == SchemaFormat.YAML:
            return "application/yaml"
        elif schema_format == SchemaFormat.JSON:
            return "application/json"

    def _infer_schema(self, data: str, schema_format: SchemaFormat) -> Response:
        url = self.endpoint + f"/v1/schemas"
        headers = {
            "Content-Type": "application/x-ndjson",
            "Accept": self._schema_format_to_mime_type(schema_format),
        }
        response = requests.post(
            url,
            data=data,
            headers=headers,
            auth=self.auth,
        )

        return response

    @api_retry
    def infer_schema(self, events: list[str]) -> dict[str, Any]:
        ndjson = "\n".join(events)
        res = self._infer_schema(ndjson, SchemaFormat.JSON)
        if res.ok:
            return res.json()
        raise self._resp_to_err(res)

    def _get_metrics(
        self,
        names: Optional[list[str]],
        from_dt: Optional[datetime],
        to_dt: Optional[datetime],
        interval_s: Optional[int],
    ) -> Response:
        params: dict[str, Any] = {}
        if names:
            params["name"] = names
        if from_dt:
            params["from_dt"] = from_dt.isoformat()
        if to_dt:
            params["to_dt"] = to_dt.isoformat()
        if interval_s:
            params["interval_s"] = interval_s

        return requests.get(self.endpoint + f"/v1/metrics", params=params, auth=self.auth)

    @api_retry
    def get_metrics(
        self,
        names: Optional[list[str]] = None,
        from_dt: Optional[datetime] = None,
        to_dt: Optional[datetime] = None,
        interval_s: Optional[int] = None,
    ) -> dict[str, Any]:
        res = self._get_metrics(names, from_dt, to_dt, interval_s)
        if res.ok:
            metrics_of_sources = res.json()
            if not metrics_of_sources:
                return {}

            json_compact: bool = isinstance(metrics_of_sources, list)
            if json_compact:
                schema = SourceStats.schema()
                decoded_metrics: list = [compact_format_to_dict(item, schema) for item in metrics_of_sources]
                return {sm["name"]: sm for sm in decoded_metrics}

            return metrics_of_sources

        raise self._resp_to_err(res)

    def _source_delete_data(self, name: str, where_condition: Optional[str]) -> Response:
        params: dict[str, Any] = {}
        if where_condition:
            params["where"] = where_condition
        return requests.delete(
            self.endpoint + f"/v1/sources/{name}/data",
            params=params,
            auth=self.auth,
        )

    @api_retry
    def source_truncate(self, name: str) -> None:
        res = self._source_delete_data(name, None)
        if not res.ok:
            raise self._resp_to_err(res)

    @api_retry
    def source_delete_data(self, name: str, where: str) -> None:
        res = self._source_delete_data(name, where)
        if not res.ok:
            raise self._resp_to_err(res)

    def _fetch_source_schema(self, db: str, table: str, schema_format: SchemaFormat) -> Response:
        url = self.endpoint + f"/v1/schemas/import/{db}/{table}"
        headers = {
            "Accept": self._schema_format_to_mime_type(schema_format),
        }
        response = requests.get(
            url,
            headers=headers,
            auth=self.auth,
        )

        return response

    @api_retry
    def fetch_source_schema(self, db: str, table: str) -> dict[str, Any]:
        res = self._fetch_source_schema(db, table, SchemaFormat.JSON)
        if res.ok:
            return res.json()
        raise self._resp_to_err(res)

    def _get_importable_tables(self) -> Response:
        return requests.get(self.endpoint + f"/v1/schemas/import", auth=self.auth)

    @api_retry
    def get_importable_tables(self) -> dict[str, list[str]]:
        res = self._get_importable_tables()
        if res.ok:
            return res.json()
        raise self._resp_to_err(res)

    def _pipe_materialize(self, name: str) -> Response:
        return requests.get(
            self.endpoint + f"/v1/pipes/{name}/materialize",
            auth=self.auth,
        )

    @api_retry
    def pipe_materialize(self, name: str) -> list[ProjectFile]:
        res = self._pipe_materialize(name)
        if res.ok:
            return [ProjectFile(name=data["name"], data=data, pulled=False) for data in res.json()]
        raise self._resp_to_err(res)

    def _template_subscribe(self, name: str = "", unsubscribe: bool = False) -> Response:
        if unsubscribe:
            body = {"subscription": "stop"}
        else:
            body = {"subscription": "start", "name": name}
        return requests.put(
            self.endpoint + f"/v1/templates",
            auth=self.auth,
            json=body,
        )

    @api_retry
    def template_subscribe(self, name: str = "", unsubscribe: bool = False) -> None:
        res = self._template_subscribe(name, unsubscribe)
        if res.ok:
            return None
        raise self._resp_to_err(res)

    def _list_jobs(self, cron: bool) -> Response:
        path = "/v1/transforms/jobs" if not cron else "/v1/cron/jobs"
        return requests.get(self.endpoint + path, auth=self.auth)

    @staticmethod
    def _create_job_info(job: dict, cron: bool) -> JobInfo:
        params: dict = {
            "name": job["id"],
            "status": job["status"],
            "created": job["created_at"],
            "updated": job["updated_at"],
            "error": job.get("error"),
            "stats": job.get("stats", {}),
        }
        if cron:
            params["cron"] = job["cron"]
            params["timezone"] = job["timezone"]
            params["connector_type"] = job["func"]
            params["type"] = JobType.CRON
            return CronJobInfo(**params)
        params["columns"] = job["columns"]
        params["type"] = JobType.AI_RECALC
        return RecalcJobInfo(**params)

    @api_retry
    def list_jobs(self, running: bool = False) -> list[JobInfo]:
        res = self._list_jobs(cron=False)
        if res.ok:
            data: list[dict] = res.json()
            jobs_info: list[JobInfo] = []
            for job in data:
                jobs_info.append(self._create_job_info(job, False))
            return (
                [ji for ji in jobs_info if ji.stats in [JobStatus.RUNNING, JobStatus.PENDING]] if running else jobs_info
            )
        raise self._resp_to_err(res)

    @api_retry
    def list_cron_jobs(self, running: bool = False) -> list[JobInfo]:
        res = self._list_jobs(cron=True)
        if res.ok:
            data: list[dict] = res.json()
            jobs_info: list[JobInfo] = []
            for job in data:
                jobs_info.append(self._create_job_info(job, True))
            return (
                [ji for ji in jobs_info if ji.stats in [JobStatus.RUNNING, JobStatus.PENDING]] if running else jobs_info
            )
        raise self._resp_to_err(res)

    def _job_cancel(self, job_id: str) -> Response:
        headers = {"Content-Type": "application/json"}
        data = json.dumps({"status": JobStatus.CANCELED})
        return requests.post(
            self.endpoint + f"/v1/transforms/jobs/{job_id}", data=data, headers=headers, auth=self.auth
        )

    @api_retry
    def cancel_job(self, job_id: str) -> None:
        res = self._job_cancel(job_id)
        if not res.ok:
            raise self._resp_to_err(res)

    def _source_recalculate_columns(self, name: str, columns: list[str]) -> Response:
        return requests.post(
            self.endpoint + f"/v1/transforms/{name}",
            auth=self.auth,
            json={"columns": columns},
        )

    @api_retry
    def source_recalculate_columns(
        self, name: str, columns: Optional[list[str]] = None
    ) -> tuple[list[str], Optional[str]]:
        res = self._source_recalculate_columns(name, columns or [])
        if not res.ok:
            raise self._resp_to_err(res)

        response_data: dict = res.json()
        return response_data.get("columns", []), response_data.get("job_id")

    def _lint(
        self,
        data: str,
        push_dry_run: bool,
        diff: bool,
    ) -> Response:
        url = self.endpoint + f"/v1/lint"
        params: dict[str, Any] = {"dry_run": push_dry_run, "diff": diff}
        headers = {"Content-Type": "application/yaml"}
        response = requests.post(url, data=data, params=params, headers=headers, auth=self.auth)

        return response

    @api_retry
    def lint(
        self,
        files: List[ProjectFile],
        push_dry_run: bool = True,
        diff: bool = False,
    ) -> LintResult:
        res = self._lint(self._dump_project_files(files), push_dry_run, diff)
        if res.ok:
            lint_resp = res.json()
            return LintResult(
                errors=lint_resp.get("errors", []),
                files=[ProjectFile(name=f["name"], data=f) for f in lint_resp["files"]],
                diff=lint_resp.get("diff"),
                pulled_files=[ProjectFile(name=f["name"], data=f) for f in lint_resp.get("pulled_files", [])],
            )
        raise self._resp_to_err(res)

    @staticmethod
    def _dump_project_files(files: List[ProjectFile]) -> str:
        return dump_yaml([normalize_name(f.data, f.name) for f in files])

    @api_retry
    def diff(self, files: List[ProjectFile]) -> DiffResult:
        res = self._lint(self._dump_project_files(files), False, True)
        if res.ok:
            lint_resp = res.json()
            if not lint_resp.get("diff"):
                raise AirfoldError("Diff is empty")
            if lint_resp.get("errors"):
                raise AirfoldError("\n".join(lint_resp["errors"]))
            diff_result = DiffResult(
                files=[ProjectFile(name=f["name"], data=f) for f in lint_resp["files"]],
                diff=lint_resp["diff"],
                pulled_files=[ProjectFile(name=f["name"], data=f) for f in lint_resp["pulled_files"]],
            )
            return diff_result
        raise self._resp_to_err(res)
