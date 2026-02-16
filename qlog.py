# https://datatracker.ietf.org/doc/draft-ietf-quic-qlog-main-schema/13/

from datetime import datetime
from enum import Enum
from typing_extensions import Annotated

from pydantic import BaseModel, BeforeValidator, ValidationError

class LogFile(BaseModel):
    file_schema: str
    serialization_format: str
    title: str | None = None
    description: str | None = None

class TimeFormat(str, Enum):
    relative_to_epoch = "relative_to_epoch"
    relative_to_previous_event = "relative_to_previous_event"

class ClockTypeEnum(str, Enum):
    system = "system"
    monotonic = "monotonic"

def parse_datetime(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%YYYY-%mm-%ddT%HH%MM%SS.%sssZ")
    except ValueError:
        raise ValueError("Invalid datetime format.")

RFC3339DateTime = Annotated[datetime, BeforeValidator(parse_datetime)]

class ReferenceTime(BaseModel):
    clock_type: ClockTypeEnum = "system"
    epoch: RFC3339DateTime | "unknown" = "1970-01-01T00:00:00.000Z"
    wall_clock_time: RFC3339DateTime | None

class CommonFields(BaseModel):
    tuple: str | None = "" # TODO: TupleID in spec
    time_format: TimeFormat | None = "relative_to_epoch"
    reference_time: ReferenceTime | None = None
    group_id: str | None = None # TODO: GroupID in spec
    # TODO: "* text => any" from I-D spec?

class VantagePointType(str, Enum):
    client = "client"
    server = "server"
    network = "network"
    unknown = "unknown"

class VantagePoint(BaseModel):
    name: str | None = None
    type: VantagePointType
    flow: VantagePointType | None = None

class Trace(BaseModel):
    title: str | None = None
    description: str | None = None
    common_files: CommonFields | None = None
    vantage_point: VantagePoint | None = None
    event_schemas: list
    events: list

class TraceError(BaseModel):
    error_description: str
    uri: str | None = None
    vantage_point: VantagePoint | None = None

class QlogFile(LogFile):
    traces: list | None = []

# TODO: events, QlogFileSeq
