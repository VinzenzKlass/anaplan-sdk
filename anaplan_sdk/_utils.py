from itertools import chain
from typing import Any, Literal, Type, TypeVar

from pydantic.alias_generators import to_camel

from anaplan_sdk._services import logger
from anaplan_sdk.exceptions import AnaplanException, InvalidIdentifierException
from anaplan_sdk.models import (
    AnaplanModel,
    InsertionResult,
    ModelCalendar,
    MonthsQuartersYearsCalendar,
    WeeksGeneralCalendar,
    WeeksGroupingCalendar,
    WeeksPeriodsCalendar,
)
from anaplan_sdk.models.cloud_works import (
    AmazonS3ConnectionInput,
    AzureBlobConnectionInput,
    ConnectionBody,
    GoogleBigQueryConnectionInput,
    IntegrationInput,
    IntegrationProcessInput,
    ScheduleInput,
)

T = TypeVar("T", bound=AnaplanModel)


def models_url(only_in_workspace: bool | str, workspace_id: str | None) -> str:
    if isinstance(only_in_workspace, bool) and only_in_workspace:
        if not workspace_id:
            raise ValueError(
                "Cannot list models in the current workspace, since no workspace Id was "
                "provided when instantiating the client. Either provide a workspace Id when "
                "instantiating the client, or pass a specific workspace Id to this method."
            )
        return f"https://api.anaplan.com/2/0/workspaces/{workspace_id}/models"
    if isinstance(only_in_workspace, str):
        return f"https://api.anaplan.com/2/0/workspaces/{only_in_workspace}/models"
    return "https://api.anaplan.com/2/0/models"


def sort_params(sort_by: str | None, descending: bool) -> dict[str, str | bool]:
    """
    Construct search parameters for sorting. This also converts snake_case to camelCase.
    :param sort_by: The field to sort by, optionally in snake_case.
    :param descending: Whether to sort in descending order.
    :return: A dictionary of search parameters in Anaplan's expected format.
    """
    if not sort_by:
        return {}
    return {"sort": f"{'-' if descending else '+'}{to_camel(sort_by)}"}


def construct_payload(model: Type[T], body: T | dict[str, Any]) -> dict[str, Any]:
    """
    Construct a payload for the given model and body.
    :param model: The model class to use for validation.
    :param body: The body to validate and optionally convert to a dictionary.
    :return: A dictionary representation of the validated body.
    """
    if isinstance(body, dict):
        body = model.model_validate(body)
    return body.model_dump(exclude_none=True, by_alias=True)


def connection_body_payload(body: ConnectionBody | dict[str, Any]) -> dict[str, Any]:
    """
    Construct a payload for the given integration body.
    :param body: The body to validate and optionally convert to a dictionary.
    :return: A dictionary representation of the validated body.
    """
    if isinstance(body, dict):
        if "sasToken" in body:
            body = AzureBlobConnectionInput.model_validate(body)
        elif "secretAccessKey" in body:
            body = AmazonS3ConnectionInput.model_validate(body)
        else:
            body = GoogleBigQueryConnectionInput.model_validate(body)
    return body.model_dump(exclude_none=True, by_alias=True)


def integration_payload(
    body: IntegrationInput | IntegrationProcessInput | dict[str, Any],
) -> dict[str, Any]:
    """
    Construct a payload for the given integration body.
    :param body: The body to validate and optionally convert to a dictionary.
    :return: A dictionary representation of the validated body.
    """
    if isinstance(body, dict):
        body = (
            IntegrationInput.model_validate(body)
            if "jobs" in body
            else IntegrationProcessInput.model_validate(body)
        )
    return body.model_dump(exclude_none=True, by_alias=True)


def schedule_payload(
    integration_id: str, schedule: ScheduleInput | dict[str, Any]
) -> dict[str, Any]:
    """
    Construct a payload for the given integration ID and schedule.
    :param integration_id: The ID of the integration.
    :param schedule: The schedule to validate and optionally convert to a dictionary.
    :return: A dictionary representation of the validated schedule.
    """
    if isinstance(schedule, dict):
        schedule = ScheduleInput.model_validate(schedule)
    return {
        "integrationId": integration_id,
        "schedule": schedule.model_dump(exclude_none=True, by_alias=True),
    }


def action_url(action_id: int) -> Literal["imports", "exports", "actions", "processes"]:
    """
    Determine the type of action based on its identifier.
    :param action_id: The identifier of the action.
    :return: The type of action.
    """
    if 12000000000 <= action_id < 113000000000:
        return "imports"
    if 116000000000 <= action_id < 117000000000:
        return "exports"
    if 117000000000 <= action_id < 118000000000:
        return "actions"
    if 118000000000 <= action_id < 119000000000:
        return "processes"
    raise InvalidIdentifierException(f"Action '{action_id}' is not a valid identifier.")


def parse_calendar_response(data: dict) -> ModelCalendar:
    """
    Parse calendar response and return appropriate calendar model.
    :param data: The calendar data from the API response.
    :return: The calendar settings of the model based on calendar type.
    """
    calendar_data = data["modelCalendar"]
    cal_type = calendar_data["calendarType"]
    if cal_type == "Calendar Months/Quarters/Years":
        return MonthsQuartersYearsCalendar.model_validate(calendar_data)
    if cal_type == "Weeks: 4-4-5, 4-5-4 or 5-4-4":
        return WeeksGroupingCalendar.model_validate(calendar_data)
    if cal_type == "Weeks: General":
        return WeeksGeneralCalendar.model_validate(calendar_data)
    if cal_type == "Weeks: 13 4-week Periods":
        return WeeksPeriodsCalendar.model_validate(calendar_data)
    raise AnaplanException(
        "Unknown calendar type encountered. Please report this issue: "
        "https://github.com/VinzenzKlass/anaplan-sdk/issues/new"
    )


def parse_insertion_response(data: list[dict]) -> InsertionResult:
    failures, added, ignored, total = [], 0, 0, 0
    for res in data:
        failures.append(res.get("failures", []))
        added += res.get("added", 0)
        total += res.get("total", 0)
        ignored += res.get("ignored", 0)
    return InsertionResult(
        added=added, ignored=ignored, total=total, failures=list(chain.from_iterable(failures))
    )


def validate_dimension_id(dimension_id: int) -> int:
    if not (
        dimension_id == 101999999999
        or 101_000_000_000 <= dimension_id < 102_000_000_000
        or 109_000_000_000 <= dimension_id < 110_000_000_000
        or 114_000_000_000 <= dimension_id < 115_000_000_000
    ):
        raise InvalidIdentifierException(
            "Invalid dimension_id. Must be a List (101xxxxxxxxx), List Subset (109xxxxxxxxx), "
            "Line Item Subset (114xxxxxxxxx), or Users (101999999999)."
        )
    msg = (
        "Using `get_dimension_items` for {} is discouraged. "
        "Prefer `{}` for better performance and more details on the members."
    )
    if dimension_id == 101999999999:
        logger.warning(msg.format("Users", "get_users"))
    if 101000000000 <= dimension_id < 102000000000:
        logger.warning(msg.format("Lists", "get_list_items"))
    return dimension_id
