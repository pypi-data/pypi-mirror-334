from datetime import datetime, timezone
from enum import Enum
from typing import Any, List, Optional

import humanize

from airfold_cli._pydantic import BaseModel, Field, SecretStr, validator


class Project(BaseModel, frozen=True):
    id: str
    name: str


class Organization(BaseModel):
    id: str
    name: str

    class Config:
        allow_population_by_field_name = True


class Permission(BaseModel):
    Effect: str
    Action: str
    Resource: str


class UserPermissions(BaseModel):
    org_id: str = Field(..., alias="orgId")
    user_perms: list[Permission] = Field(..., alias="userPerms")
    roles: list[str]

    class Config:
        allow_population_by_field_name = True


class UserProfile(BaseModel):
    id: str
    fname: str
    lname: str
    email: str
    avatar: Optional[str] = None
    full_name: str = Field(..., alias="fullName")
    organizations: List[Organization]
    permissions: List[UserPermissions]

    class Config:
        allow_population_by_field_name = True


class ProjectProfile(BaseModel):
    project_id: str = Field(..., alias="projectId")
    org_id: str = Field(..., alias="orgId")
    permissions: List[Permission]

    class Config:
        allow_population_by_field_name = True


class AirfoldAPIKey(SecretStr):
    def display(self, *args, **kwargs):
        val = self.get_secret_value()
        if len(val) < 4:
            return val
        return f"aft_...{self.get_secret_value()[-4:]}"


class Config(BaseModel):
    endpoint: str
    org_id: Optional[str] = None
    proj_id: Optional[str] = None
    key: AirfoldAPIKey = Field(
        default=None,
        title="API Key",
        description="API key to authenticate with the Airfold API.",
    )

    def dict(self, **kwargs) -> Any:
        unmask = kwargs.pop("unmask", False)
        output = super().dict(**kwargs)

        for k, v in output.items():
            if isinstance(v, SecretStr) and unmask:
                output[k] = v.get_secret_value()

        return output

    class Config:
        frozen = True


class OutputDataFormat(str, Enum):
    JSON = "json"
    NDJSON = "ndjson"

    def __str__(self):
        return self.value


Plan = list[dict]


class NamedParam(BaseModel):
    name: str
    value: str


class SchemaFormat(str, Enum):
    YAML = "yaml"
    JSON = "json"

    def __str__(self):
        return self.value


class PipeInfoStatus(str, Enum):
    PUBLISHED = "published"
    DRAFT = "draft"
    MATERIALIZED = "materialized"

    def __str__(self):
        return self.value


class Info(BaseModel):
    name: str
    created: datetime
    updated: datetime

    @validator("created", "updated")
    def convert_to_utc(cls, v: Any):
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    def dict(self, **kwargs) -> Any:
        humanize_args: bool = kwargs.pop("humanize", False)
        output = super().dict(**kwargs)
        for k, v in output.items():
            if isinstance(v, datetime):
                output[k] = humanize.naturaltime(datetime.now(timezone.utc) - v) if humanize_args else v.isoformat()
            if k.find("bytes") != -1:
                output[k] = humanize.naturalsize(v) if humanize_args else v
        return output


class PipeInfo(Info):
    status: PipeInfoStatus


class SourceType(str, Enum):
    TABLE = "table"
    AI_TABLE = "ai_table"

    def __str__(self):
        return self.value


class SourceInfo(Info):
    type: SourceType
    rows: int
    bytes: int
    errors: int


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"

    def __str__(self):
        return self.value


class JobType(str, Enum):
    AI_RECALC = "ai_recalc"
    CRON = "cron"


class JobInfo(Info):
    type: JobType
    status: JobStatus
    error: Optional[str] = None
    stats: Optional[dict] = None


class RecalcJobInfo(JobInfo):
    columns: list[str]

    @validator("type", pre=True, always=True)
    def get_type(cls, v=None):
        return JobType.AI_RECALC


class CronJobInfo(JobInfo):
    cron: str
    timezone: str
    connector_type: str

    @validator("type", pre=True, always=True)
    def get_type(cls, v=None):
        return JobType.CRON
