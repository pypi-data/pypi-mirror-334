from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    *,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params["offset"] = offset

    params["limit"] = limit

    params["fromDateTime"] = from_date_time

    params["toDateTime"] = to_date_time

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/nomination/{congress}",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == 200:
        return None
    if response.status_code == 400:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    congress: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns a list of nominations filtered by the specified congress and sorted by date received from
    the President.

     GET /nomination/:congress

    **Example Request**

    https://api.congress.gov/v3/nomination/117?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"nominations\": [
                {
                    \"citation\": \"PN2804\",
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2022-12-07\",
                        \"text\": \"Received in the Senate and referred to the Committee on Armed
    Services.\"
                    },
                    \"nominationType\": {
                        \"isMilitary\": true
                    },
                    \"number\": 2804,
                    \"organization\": \"Army\",
                    \"partNumber\": \"00\",
                    \"receivedDate\": \"2022-12-07\",
                    \"updateDate\": \"2022-12-08T05:25:17Z\",
                    \"url\": \"https://api.congress.gov/v3/nomination/117/2804?format=json\"
                },
                {
                    \"citation\": \"PN2803\",
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2022-12-07\",
                        \"text\": \"Received in the Senate and referred to the Committee on Armed
    Services.\"
                    },
                    \"nominationType\": {
                        \"isMilitary\": true
                    },
                    \"number\": 2803,
                    \"organization\": \"Army\",
                    \"partNumber\": \"00\",
                    \"receivedDate\": \"2022-12-07\",
                    \"updateDate\": \"2022-12-08T05:25:17Z\",
                    \"url\": \"https://api.congress.gov/v3/nomination/117/2803?format=json\"
                },
            ],
        }

    Args:
        congress (int):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_date_time (Union[Unset, str]):
        to_date_time (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        format_=format_,
        offset=offset,
        limit=limit,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns a list of nominations filtered by the specified congress and sorted by date received from
    the President.

     GET /nomination/:congress

    **Example Request**

    https://api.congress.gov/v3/nomination/117?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"nominations\": [
                {
                    \"citation\": \"PN2804\",
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2022-12-07\",
                        \"text\": \"Received in the Senate and referred to the Committee on Armed
    Services.\"
                    },
                    \"nominationType\": {
                        \"isMilitary\": true
                    },
                    \"number\": 2804,
                    \"organization\": \"Army\",
                    \"partNumber\": \"00\",
                    \"receivedDate\": \"2022-12-07\",
                    \"updateDate\": \"2022-12-08T05:25:17Z\",
                    \"url\": \"https://api.congress.gov/v3/nomination/117/2804?format=json\"
                },
                {
                    \"citation\": \"PN2803\",
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2022-12-07\",
                        \"text\": \"Received in the Senate and referred to the Committee on Armed
    Services.\"
                    },
                    \"nominationType\": {
                        \"isMilitary\": true
                    },
                    \"number\": 2803,
                    \"organization\": \"Army\",
                    \"partNumber\": \"00\",
                    \"receivedDate\": \"2022-12-07\",
                    \"updateDate\": \"2022-12-08T05:25:17Z\",
                    \"url\": \"https://api.congress.gov/v3/nomination/117/2803?format=json\"
                },
            ],
        }

    Args:
        congress (int):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_date_time (Union[Unset, str]):
        to_date_time (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        format_=format_,
        offset=offset,
        limit=limit,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
