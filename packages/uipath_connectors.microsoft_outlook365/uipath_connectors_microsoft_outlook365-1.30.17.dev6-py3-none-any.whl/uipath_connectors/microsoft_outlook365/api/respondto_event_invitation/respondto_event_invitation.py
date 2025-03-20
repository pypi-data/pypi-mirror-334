from http import HTTPStatus
from typing import Any, Optional, Union

import httpx
from pydantic import Field

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.default_error import DefaultError
from ...models.respondto_event_invitation_request import RespondtoEventInvitationRequest
from ...models.respondto_event_invitation_response import (
    RespondtoEventInvitationResponse,
)


def _get_kwargs(
    *,
    body: RespondtoEventInvitationRequest,
    response: str = Field(alias="response", default="accept"),
    apply_on_series: Optional[bool] = Field(alias="applyOnSeries", default=False),
    calendar_id: Optional[str] = Field(alias="calendarID", default=None),
    id: str = Field(alias="id"),
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["response"] = response

    params["applyOnSeries"] = apply_on_series

    params["calendarID"] = calendar_id

    params["id"] = id

    params = {k: v for k, v in params.items() if v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/RespondtoEventInvitation",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DefaultError, RespondtoEventInvitationResponse]]:
    if response.status_code == 200:
        response_200 = RespondtoEventInvitationResponse.from_dict(response.json())

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
) -> Response[Union[DefaultError, RespondtoEventInvitationResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RespondtoEventInvitationRequest,
    response: str = Field(alias="response", default="accept"),
    apply_on_series: Optional[bool] = Field(alias="applyOnSeries", default=False),
    calendar_id: Optional[str] = Field(alias="calendarID", default=None),
    calendar_id_lookup: Any,
    id: str = Field(alias="id"),
) -> Response[Union[DefaultError, RespondtoEventInvitationResponse]]:
    """Respond to Event Invitation

     Respond to Event Invitation

    Args:
        response (str):  Default: 'accept'.
        apply_on_series (Optional[bool]):  Default: False.
        calendar_id (Optional[str]):
        id (str):
        body (RespondtoEventInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, RespondtoEventInvitationResponse]]
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

    kwargs = _get_kwargs(
        body=body,
        response=response,
        apply_on_series=apply_on_series,
        calendar_id=calendar_id,
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RespondtoEventInvitationRequest,
    response: str = Field(alias="response", default="accept"),
    apply_on_series: Optional[bool] = Field(alias="applyOnSeries", default=False),
    calendar_id: Optional[str] = Field(alias="calendarID", default=None),
    calendar_id_lookup: Any,
    id: str = Field(alias="id"),
) -> Optional[Union[DefaultError, RespondtoEventInvitationResponse]]:
    """Respond to Event Invitation

     Respond to Event Invitation

    Args:
        response (str):  Default: 'accept'.
        apply_on_series (Optional[bool]):  Default: False.
        calendar_id (Optional[str]):
        id (str):
        body (RespondtoEventInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, RespondtoEventInvitationResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
        response=response,
        apply_on_series=apply_on_series,
        calendar_id=calendar_id,
        calendar_id_lookup=calendar_id_lookup,
        id=id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RespondtoEventInvitationRequest,
    response: str = Field(alias="response", default="accept"),
    apply_on_series: Optional[bool] = Field(alias="applyOnSeries", default=False),
    calendar_id: Optional[str] = Field(alias="calendarID", default=None),
    calendar_id_lookup: Any,
    id: str = Field(alias="id"),
) -> Response[Union[DefaultError, RespondtoEventInvitationResponse]]:
    """Respond to Event Invitation

     Respond to Event Invitation

    Args:
        response (str):  Default: 'accept'.
        apply_on_series (Optional[bool]):  Default: False.
        calendar_id (Optional[str]):
        id (str):
        body (RespondtoEventInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DefaultError, RespondtoEventInvitationResponse]]
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

    kwargs = _get_kwargs(
        body=body,
        response=response,
        apply_on_series=apply_on_series,
        calendar_id=calendar_id,
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: RespondtoEventInvitationRequest,
    response: str = Field(alias="response", default="accept"),
    apply_on_series: Optional[bool] = Field(alias="applyOnSeries", default=False),
    calendar_id: Optional[str] = Field(alias="calendarID", default=None),
    calendar_id_lookup: Any,
    id: str = Field(alias="id"),
) -> Optional[Union[DefaultError, RespondtoEventInvitationResponse]]:
    """Respond to Event Invitation

     Respond to Event Invitation

    Args:
        response (str):  Default: 'accept'.
        apply_on_series (Optional[bool]):  Default: False.
        calendar_id (Optional[str]):
        id (str):
        body (RespondtoEventInvitationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DefaultError, RespondtoEventInvitationResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            response=response,
            apply_on_series=apply_on_series,
            calendar_id=calendar_id,
            calendar_id_lookup=calendar_id_lookup,
            id=id,
        )
    ).parsed
