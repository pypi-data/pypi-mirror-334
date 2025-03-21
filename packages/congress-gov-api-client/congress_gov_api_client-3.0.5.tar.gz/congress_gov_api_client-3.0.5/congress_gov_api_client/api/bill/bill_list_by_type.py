from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    bill_type: str,
    *,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
    sort: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params["offset"] = offset

    params["limit"] = limit

    params["fromDateTime"] = from_date_time

    params["toDateTime"] = to_date_time

    params["sort"] = sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/bill/{congress}/{bill_type}",
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
    bill_type: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
    sort: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns a list of bills filtered by the specified congress and bill type, sorted by date of latest
    action.

     GET /bill/:congress/:billType

    **Example Request**

    https://api.congress.gov/v3/bill/117/hr?fromDateTime=2022-08-04T04:02:00Z&toDateTime=2022-09-
    30T04:03:00Z&sort=updateDate+asc&api_key=[INSERT_KEY]

    **Example Response**

        {
            \"bills\": [
                {
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2022-04-06\",
                        \"text\": \"Became Public Law No: 117-108.\"
                    },
                    \"number\": \"3076\",
                    \"originChamber\": \"House\",
                    \"originChamberCode\": \"H\",
                    \"title\": \"Postal Service Reform Act of 2022\",
                    \"type\": \"HR\",
                    \"updateDate\": \"2022-09-29\",
                    \"updateDateIncludingText\": \"2022-09-29\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076?format=json\"
                },
                {
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2022-04-06\",
                        \"text\": \"Read twice. Placed on Senate Legislative Calendar under General
    Orders. Calendar No. 343.\"
                    },
                    \"number\": \"3599\",
                    \"originChamber\": \"House\",
                    \"originChamberCode\": \"H\",
                    \"title\": \"Federal Rotational Cyber Workforce Program Act of 2021\",
                    \"type\": \"HR\",
                    \"updateDate\": \"2022-09-29\",
                    \"updateDateIncludingText\": \"2022-09-29T03:41:50Z\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3599?format=json\"
                },
            ],
        }

    Args:
        congress (int):
        bill_type (str):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_date_time (Union[Unset, str]):
        to_date_time (Union[Unset, str]):
        sort (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        bill_type=bill_type,
        format_=format_,
        offset=offset,
        limit=limit,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
        sort=sort,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    bill_type: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
    sort: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns a list of bills filtered by the specified congress and bill type, sorted by date of latest
    action.

     GET /bill/:congress/:billType

    **Example Request**

    https://api.congress.gov/v3/bill/117/hr?fromDateTime=2022-08-04T04:02:00Z&toDateTime=2022-09-
    30T04:03:00Z&sort=updateDate+asc&api_key=[INSERT_KEY]

    **Example Response**

        {
            \"bills\": [
                {
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2022-04-06\",
                        \"text\": \"Became Public Law No: 117-108.\"
                    },
                    \"number\": \"3076\",
                    \"originChamber\": \"House\",
                    \"originChamberCode\": \"H\",
                    \"title\": \"Postal Service Reform Act of 2022\",
                    \"type\": \"HR\",
                    \"updateDate\": \"2022-09-29\",
                    \"updateDateIncludingText\": \"2022-09-29\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076?format=json\"
                },
                {
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2022-04-06\",
                        \"text\": \"Read twice. Placed on Senate Legislative Calendar under General
    Orders. Calendar No. 343.\"
                    },
                    \"number\": \"3599\",
                    \"originChamber\": \"House\",
                    \"originChamberCode\": \"H\",
                    \"title\": \"Federal Rotational Cyber Workforce Program Act of 2021\",
                    \"type\": \"HR\",
                    \"updateDate\": \"2022-09-29\",
                    \"updateDateIncludingText\": \"2022-09-29T03:41:50Z\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3599?format=json\"
                },
            ],
        }

    Args:
        congress (int):
        bill_type (str):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_date_time (Union[Unset, str]):
        to_date_time (Union[Unset, str]):
        sort (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        bill_type=bill_type,
        format_=format_,
        offset=offset,
        limit=limit,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
        sort=sort,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
