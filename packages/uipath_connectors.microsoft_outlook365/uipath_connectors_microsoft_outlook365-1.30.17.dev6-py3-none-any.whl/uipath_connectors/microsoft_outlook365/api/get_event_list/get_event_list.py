from http import HTTPStatus
from typing import Any, Optional, Union

import httpx
from pydantic import Field

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.get_event_list import GetEventList
import datetime


def _get_kwargs(
    *,
    from_: datetime.datetime = Field(alias="from"),
    until: datetime.datetime = Field(alias="until"),
    calendar_id: Optional[str] = Field(alias="calendarID", default=None),
    fields: Optional[str] = Field(alias="fields", default=None),
    filter_: Optional[str] = Field(alias="filter", default=None),
    next_page: Optional[str] = Field(alias="nextPage", default=None),
    output_timezone: Optional[str] = Field(alias="outputTimezone", default=None),
    page_size: Optional[int] = Field(alias="pageSize", default=None),
    size: Optional[str] = Field(alias="size", default="50"),
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_until = until.isoformat()
    params["until"] = json_until

    params["calendarID"] = calendar_id

    params["fields"] = fields

    params["filter"] = filter_

    params["nextPage"] = next_page

    params["outputTimezone"] = output_timezone

    params["pageSize"] = page_size

    params["size"] = size

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/GetEventList",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, list["GetEventList"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_get_event_list_list_item_data in _response_200:
            componentsschemas_get_event_list_list_item = GetEventList.from_dict(
                componentsschemas_get_event_list_list_item_data
            )

            response_200.append(componentsschemas_get_event_list_list_item)

        return response_200
    if response.status_code == 400:
        response_400 = DefaultError.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = DefaultError.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = DefaultError.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = DefaultError.from_dict(response.json())

        return response_404
    if response.status_code == 405:
        response_405 = DefaultError.from_dict(response.json())

        return response_405
    if response.status_code == 406:
        response_406 = DefaultError.from_dict(response.json())

        return response_406
    if response.status_code == 409:
        response_409 = DefaultError.from_dict(response.json())

        return response_409
    if response.status_code == 415:
        response_415 = DefaultError.from_dict(response.json())

        return response_415
    if response.status_code == 500:
        response_500 = DefaultError.from_dict(response.json())

        return response_500
    if response.status_code == 402:
        response_402 = DefaultError.from_dict(response.json())

        return response_402
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DefaultError, list["GetEventList"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    from_: datetime.datetime = Field(alias="from"),
    until: datetime.datetime = Field(alias="until"),
    calendar_id: Optional[str] = Field(alias="calendarID", default=None),
    calendar_id_lookup: Any,
    fields: Optional[str] = Field(alias="fields", default=None),
    filter_: Optional[str] = Field(alias="filter", default=None),
    next_page: Optional[str] = Field(alias="nextPage", default=None),
    output_timezone: Optional[str] = Field(alias="outputTimezone", default=None),
    output_timezone_lookup: Any,
    page_size: Optional[int] = Field(alias="pageSize", default=None),
    size: Optional[str] = Field(alias="size", default="50"),
) -> Response[Union[DefaultError, list["GetEventList"]]]:
    """Get Event List

    Args:
        from_ (datetime.datetime):
        until (datetime.datetime):
        calendar_id (Optional[str]):
        fields (Optional[str]):
        filter_ (Optional[str]):
        next_page (Optional[str]):
        output_timezone (Optional[str]):
        page_size (Optional[int]):
        size (Optional[str]):  Default: '50'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['GetEventList']]]
    """

    if not calendar_id and calendar_id_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/CalendarList"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if calendar_id_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for calendar_id_lookup in CalendarList")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for calendar_id_lookup in CalendarList. Using the first match."
            )

        calendar_id = found_items[0]["ID"]
    if not output_timezone and output_timezone_lookup:
        lookup_response_raw = client.get_httpx_client().request(
            method="get", url="/timezones"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if output_timezone_lookup in item["displayName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for output_timezone_lookup in timezones"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for output_timezone_lookup in timezones. Using the first match."
            )

        output_timezone = found_items[0]["alias"]

    kwargs = _get_kwargs(
        from_=from_,
        until=until,
        calendar_id=calendar_id,
        fields=fields,
        filter_=filter_,
        next_page=next_page,
        output_timezone=output_timezone,
        page_size=page_size,
        size=size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    from_: datetime.datetime = Field(alias="from"),
    until: datetime.datetime = Field(alias="until"),
    calendar_id: Optional[str] = Field(alias="calendarID", default=None),
    calendar_id_lookup: Any,
    fields: Optional[str] = Field(alias="fields", default=None),
    filter_: Optional[str] = Field(alias="filter", default=None),
    next_page: Optional[str] = Field(alias="nextPage", default=None),
    output_timezone: Optional[str] = Field(alias="outputTimezone", default=None),
    output_timezone_lookup: Any,
    page_size: Optional[int] = Field(alias="pageSize", default=None),
    size: Optional[str] = Field(alias="size", default="50"),
) -> Optional[Union[DefaultError, list["GetEventList"]]]:
    """Get Event List

    Args:
        from_ (datetime.datetime):
        until (datetime.datetime):
        calendar_id (Optional[str]):
        fields (Optional[str]):
        filter_ (Optional[str]):
        next_page (Optional[str]):
        output_timezone (Optional[str]):
        page_size (Optional[int]):
        size (Optional[str]):  Default: '50'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['GetEventList']]
    """

    return sync_detailed(
        client=client,
        from_=from_,
        until=until,
        calendar_id=calendar_id,
        calendar_id_lookup=calendar_id_lookup,
        fields=fields,
        filter_=filter_,
        next_page=next_page,
        output_timezone=output_timezone,
        output_timezone_lookup=output_timezone_lookup,
        page_size=page_size,
        size=size,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    from_: datetime.datetime = Field(alias="from"),
    until: datetime.datetime = Field(alias="until"),
    calendar_id: Optional[str] = Field(alias="calendarID", default=None),
    calendar_id_lookup: Any,
    fields: Optional[str] = Field(alias="fields", default=None),
    filter_: Optional[str] = Field(alias="filter", default=None),
    next_page: Optional[str] = Field(alias="nextPage", default=None),
    output_timezone: Optional[str] = Field(alias="outputTimezone", default=None),
    output_timezone_lookup: Any,
    page_size: Optional[int] = Field(alias="pageSize", default=None),
    size: Optional[str] = Field(alias="size", default="50"),
) -> Response[Union[DefaultError, list["GetEventList"]]]:
    """Get Event List

    Args:
        from_ (datetime.datetime):
        until (datetime.datetime):
        calendar_id (Optional[str]):
        fields (Optional[str]):
        filter_ (Optional[str]):
        next_page (Optional[str]):
        output_timezone (Optional[str]):
        page_size (Optional[int]):
        size (Optional[str]):  Default: '50'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, list['GetEventList']]]
    """

    if not calendar_id and calendar_id_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/CalendarList"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if calendar_id_lookup in item["FullName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError("No matches found for calendar_id_lookup in CalendarList")
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for calendar_id_lookup in CalendarList. Using the first match."
            )

        calendar_id = found_items[0]["ID"]
    if not output_timezone and output_timezone_lookup:
        lookup_response_raw = await client.get_async_httpx_client().request(
            method="get", url="/timezones"
        )
        lookup_response = lookup_response_raw.json()

        found_items = []
        for item in lookup_response:
            if output_timezone_lookup in item["displayName"]:
                found_items.append(item)

        if not found_items:
            raise ValueError(
                "No matches found for output_timezone_lookup in timezones"
            )
        if len(found_items) > 1:
            print(
                "Warning: Multiple matches found for output_timezone_lookup in timezones. Using the first match."
            )

        output_timezone = found_items[0]["alias"]

    kwargs = _get_kwargs(
        from_=from_,
        until=until,
        calendar_id=calendar_id,
        fields=fields,
        filter_=filter_,
        next_page=next_page,
        output_timezone=output_timezone,
        page_size=page_size,
        size=size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    from_: datetime.datetime = Field(alias="from"),
    until: datetime.datetime = Field(alias="until"),
    calendar_id: Optional[str] = Field(alias="calendarID", default=None),
    calendar_id_lookup: Any,
    fields: Optional[str] = Field(alias="fields", default=None),
    filter_: Optional[str] = Field(alias="filter", default=None),
    next_page: Optional[str] = Field(alias="nextPage", default=None),
    output_timezone: Optional[str] = Field(alias="outputTimezone", default=None),
    output_timezone_lookup: Any,
    page_size: Optional[int] = Field(alias="pageSize", default=None),
    size: Optional[str] = Field(alias="size", default="50"),
) -> Optional[Union[DefaultError, list["GetEventList"]]]:
    """Get Event List

    Args:
        from_ (datetime.datetime):
        until (datetime.datetime):
        calendar_id (Optional[str]):
        fields (Optional[str]):
        filter_ (Optional[str]):
        next_page (Optional[str]):
        output_timezone (Optional[str]):
        page_size (Optional[int]):
        size (Optional[str]):  Default: '50'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, list['GetEventList']]
    """

    return (
        await asyncio_detailed(
            client=client,
            from_=from_,
            until=until,
            calendar_id=calendar_id,
            calendar_id_lookup=calendar_id_lookup,
            fields=fields,
            filter_=filter_,
            next_page=next_page,
            output_timezone=output_timezone,
            output_timezone_lookup=output_timezone_lookup,
            page_size=page_size,
            size=size,
        )
    ).parsed
