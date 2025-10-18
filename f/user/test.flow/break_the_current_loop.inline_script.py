from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal
from typing import Any, Literal
from uuid import UUID

import httpx
import logfire
import pydantic as pyd

from f.lib.metadata import schedule
from f.lib.utils import Json, get_secret, get_variable, now




@contextmanager
def auxilius_client(at: str | None = None) -> Iterator[httpx.Client]:
    transport = httpx.HTTPTransport(
        trust_env=False,
        http2=False,
        retries=10,
    )
    username = get_variable("AUXILIUS_USERNAME")
    password = get_secret("AUXILIUS_PASSWORD").get_secret_value()
    # TODO disable cookies
    client_instance = httpx.Client(
        transport=transport,
        timeout=60.0,
        base_url=get_variable("AUXILIUS_BASE_URL"),
        auth=(username, password),
    )
    if at:
        client_instance.headers["AUX_AUTH"] = f"Bearer {at}"
    logfire.instrument_httpx(client_instance, capture_response_body=True)

    try:
        yield client_instance
    finally:
        client_instance.close()


def authenticate(client: httpx.Client) -> str:
    resp = client.get("/tokens")
    resp.raise_for_status()
    at = resp.json()["token"]
    assert isinstance(at, str)
    client.headers["AUX_AUTH"] = f"Bearer {at}"
    return at


class LoginResult(pyd.BaseModel):
    token: str


def get_access_token() -> LoginResult:
    with auxilius_client() as client:
        at = authenticate(client)
        return LoginResult(token=at)


def create_key(
    prefix: str,
    filename: str | None = None,
    day: pyd.AwareDatetime | None = None,
    suffix: str = "",
    metering_code: str | None = None,
) -> str:
    if day is None:
        day = now("Europe/Berlin")
    if filename is None:
        filename = day.isoformat().replace(":", "_")
    if metering_code:
        filename = f"deviceId={metering_code}/{filename}"
    return f"{prefix}/year={day.year:04d}/month={day.month:02d}/day={day.day:02d}/{filename}{suffix}"


class Value(pyd.BaseModel):
    id: UUID


class ValuesListResponse(pyd.BaseModel):
    truncated: bool
    values: list[Value] = []


class ValuesListResult(pyd.BaseModel):
    data: Json
    values: list[UUID]
    truncated: bool


def get_values_list(at: str) -> ValuesListResult:
    with auxilius_client(at) as client:
        resp = client.get("/values")
        resp.raise_for_status()
        data = resp.json()
        values = ValuesListResponse.model_validate(data)
        return ValuesListResult(
            data=data,
            values=[v.id for v in values.values],
            truncated=values.truncated,
        )


class Entry(pyd.BaseModel):
    channelAddress: str
    unit: Literal["kWh"]
    scaler: int = 0
    value: Decimal
    estimated: bool | None = None
    transducerFactor: Decimal | None = None
    info: str | None = None
    # TODO: Dafür gibt es ein type: "G" field.


class LoadProfile(pyd.BaseModel):
    timestamp: pyd.AwareDatetime
    entry: list[Entry]


class ValuesResponse(pyd.BaseModel):
    vsubtype: str
    meteringCode: str
    deviceId: str
    customerProjectId: str
    loadProfileEntries: list[LoadProfile]

    @pyd.field_validator("loadProfileEntries")
    @classmethod
    def ensureAtLeastOneEntry(cls, v: list[LoadProfile]) -> list[LoadProfile]:
        if len(v) == 0:
            raise ValueError
        return v

    def day(self) -> datetime:
        return self.loadProfileEntries[0].timestamp.replace(
            hour=0, minute=0, second=0, microsecond=0
        )


class ValuesResult(pyd.BaseModel):
    data: Json
    meteringCode: str
    day: datetime


def get_readings(at: str, uuid: UUID) -> ValuesResult:
    with auxilius_client(at) as client:
        resp = client.get(f"/values/{uuid}")
        resp.raise_for_status()
        data = resp.json()
        values = ValuesResponse.model_validate(data)
        return ValuesResult(
            data=data,
            meteringCode=values.meteringCode,
            day=values.day(),
        )


def delete_reatings(at: str, uuid: UUID) -> None:
    with auxilius_client(at) as client:
        resp = client.delete(f"/values/{uuid}")
        resp.raise_for_status()


class ForStatusResult(pyd.BaseModel):
    errors: int
    success: int
    break_while: bool


from f.lib.utils import script
@script()
def main(data: list[Any], truncated: bool) -> ForStatusResult:
    errors = 0
    for v in data:
        if isinstance(v, dict) and "error" in v:
            errors += 1

    success = len(data) - errors
    return ForStatusResult(
        errors=errors,
        success=success,
        break_while=not (success > 0 and truncated),
    )


class AuxiliusFlowError(Exception): ...


def check_flow_status(data: list[ForStatusResult]) -> None:
    errors = sum(v.errors for v in data)
    if errors > 0:
        msg = f"We got {errors} values with errors."
        raise AuxiliusFlowError(msg)


@schedule(
    schedule="0 0 9 * * *",
    enabled=True,
    args={"bucket": "$var:f/vars/AUXILIUS_BUCKET_NAME"},
)
def flow() -> Any:
    from f.lib import flows

    return flows.Flow(
        "Ingest auxilius metering data",
        on_behalf_of_email=True,
        steps=[
            loop_value_lists := flows.While(
                summary="Loop values lists",
                skip_failures=False,
                steps=[
                    login := flows.Action(
                        get_access_token,
                        summary="Get Auxilius access-token",
                        retry=flows.ExpRetry(attempts=2, seconds=5),
                    ),
                    values := flows.Action(
                        get_values_list,
                        summary="Get values list",
                        kwargs={"at": login.result.token},
                        retry=flows.ExpRetry(attempts=2, seconds=5),
                    ),
                    values_key := flows.Action(
                        create_key,
                        summary="Generate s3 key",
                        kwargs={
                            "prefix": "meterdata/provider=auxilius/type=values",
                            "suffix": ".json.gz",
                        },
                    ),
                    flows.Action(
                        "f.scripts.store_s3",
                        summary="Store values list",
                        kwargs={
                            "data": values.result.data,
                            "bucket": flows.INPUT.bucket,
                            "key": values_key.result,
                        },
                    ),
                    for_values := flows.For(
                        summary="Loop readings from values list.",
                        skip_failures=True,
                        parallel=True,
                        parallelism=10,
                        over=values.result.values,
                        steps=[
                            value := flows.Action(
                                get_readings,
                                summary="Get value",
                                kwargs={
                                    "at": login.result.token,
                                    "uuid": flows.INPUT.iter.value,
                                },
                            ),
                            value_key := flows.Action(
                                create_key,
                                summary="Generate s3 key",
                                kwargs={
                                    "prefix": "meterdata/provider=auxilius/type=value",
                                    "suffix": ".json.gz",
                                    "metering_code": value.result.meteringCode,
                                    "filename": flows.INPUT.iter.value,
                                    "day": value.result.day,
                                },
                            ),
                            flows.Action(
                                "f.scripts.store_s3",
                                summary="Store value",
                                kwargs={
                                    "data": value.result.data,
                                    "bucket": flows.INPUT.bucket,
                                    "key": value_key.result,
                                },
                            ),
                            flows.Action(
                                delete_reatings,
                                summary="Delete value from auxilius",
                                kwargs={
                                    "at": login.result.token,
                                    "uuid": flows.INPUT.iter.value,
                                },
                                retry=flows.ExpRetry(attempts=2, seconds=5),
                            ),
                        ],
                    ),
                    flows.BreakIf(
                        check_for_status,
                        kwargs={
                            "data": for_values.result,
                            "truncated": values.result.truncated,
                        },
                        result=flows.RESULT.break_while,
                    ),
                ],
            ),
            flows.Action(
                check_flow_status,
                summary="Check status of while loop",
                kwargs={"data": loop_value_lists.result},
            ),
        ],
    )
