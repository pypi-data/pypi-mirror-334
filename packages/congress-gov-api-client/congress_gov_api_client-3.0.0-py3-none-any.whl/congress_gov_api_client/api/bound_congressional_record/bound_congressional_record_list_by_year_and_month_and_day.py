from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    year: str,
    month: str,
    day: str,
    *,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params["offset"] = offset

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/bound-congressional-record/{year}/{month}/{day}",
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
    year: str,
    month: str,
    day: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns a list of bound Congressional Records filtered by the specified year, specified month and
    specified day.

     GET /bound-congressional-record/:year/:month/:day

    **Example Request**

    https://api.congress.gov/v3/bound-congressional-record/1948/05/19?api_key=[INSERT_KEY]

    **Example Response**

        {
           \"boundCongressionalRecord\": [
               {
                  \"congress\": 80,
                  \"date\": \"1948-05-19\",
                  \"sections\": [
                      {
                      \"endPage\": 6155,
                      \"name\": \"House of Representatives\",
                      \"startPage\": 6099
                }
                ],
                  \"sessionNumber\": 2,
                  \"updateDate\": \"2023-04-27\",
                  \"volumeNumber\": 94
                },
                {
                  \"congress\": 80,
                  \"date\": \"1948-05-19\",
                  \"sections\": [
                      {
                      \"endPage\": 6098,
                      \"name\": \"Senate\",
                      \"startPage\": 6051
                }
                ],
                  \"sessionNumber\": 2,
                  \"updateDate\": \"2023-04-27\",
                  \"volumeNumber\": 94
                },
                {
                  \"congress\": 80,
                  \"date\": \"1948-05-19\",
                  \"sections\": [
                      {
                      \"endPage\": 6155,
                      \"name\": \"Entire Issue\",
                      \"startPage\": 6051
                }
                ],
                  \"sessionNumber\": 2,
                  \"updateDate\": \"2023-04-27\",
                  \"volumeNumber\": 94
                },
                {
                  \"congress\": 80,
                  \"dailyDigest\": {
                            \"endPage\": 365,
                            \"startPage\": 362,
                            \"text\": [
                                {
                                    \"type\": \"PDF\",
                                    \"url\": \"http://congress.gov/crecb/1948/GPO-
    CRECB-1948-pt14-Pages362-365.pdf\"
                                }
                            ]
                    },
                    \"date\": \"1948-05-19\",
                    \"sections\": [
                        {
                            \"endPage\": 365,
                            \"name\": \"Daily Digest\",
                            \"startPage\": 362
                        }
                    ],
                    \"sessionNumber\": 2,
                    \"updateDate\": \"2022-11-04\",
                    \"volumeNumber\": 94
                    }
                    ],
                    \"pagination\": {
                        \"count\": 4
                    },
                    {
                    \"request\": {
                    \"contentType\": \"application/json\",
                    \"day\": \"19\",
                    \"format\": \"json\",
                    \"month\": \"05\",
                    \"year\": \"1948\"
                   },

    Args:
        year (str):
        month (str):
        day (str):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        year=year,
        month=month,
        day=day,
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    year: str,
    month: str,
    day: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns a list of bound Congressional Records filtered by the specified year, specified month and
    specified day.

     GET /bound-congressional-record/:year/:month/:day

    **Example Request**

    https://api.congress.gov/v3/bound-congressional-record/1948/05/19?api_key=[INSERT_KEY]

    **Example Response**

        {
           \"boundCongressionalRecord\": [
               {
                  \"congress\": 80,
                  \"date\": \"1948-05-19\",
                  \"sections\": [
                      {
                      \"endPage\": 6155,
                      \"name\": \"House of Representatives\",
                      \"startPage\": 6099
                }
                ],
                  \"sessionNumber\": 2,
                  \"updateDate\": \"2023-04-27\",
                  \"volumeNumber\": 94
                },
                {
                  \"congress\": 80,
                  \"date\": \"1948-05-19\",
                  \"sections\": [
                      {
                      \"endPage\": 6098,
                      \"name\": \"Senate\",
                      \"startPage\": 6051
                }
                ],
                  \"sessionNumber\": 2,
                  \"updateDate\": \"2023-04-27\",
                  \"volumeNumber\": 94
                },
                {
                  \"congress\": 80,
                  \"date\": \"1948-05-19\",
                  \"sections\": [
                      {
                      \"endPage\": 6155,
                      \"name\": \"Entire Issue\",
                      \"startPage\": 6051
                }
                ],
                  \"sessionNumber\": 2,
                  \"updateDate\": \"2023-04-27\",
                  \"volumeNumber\": 94
                },
                {
                  \"congress\": 80,
                  \"dailyDigest\": {
                            \"endPage\": 365,
                            \"startPage\": 362,
                            \"text\": [
                                {
                                    \"type\": \"PDF\",
                                    \"url\": \"http://congress.gov/crecb/1948/GPO-
    CRECB-1948-pt14-Pages362-365.pdf\"
                                }
                            ]
                    },
                    \"date\": \"1948-05-19\",
                    \"sections\": [
                        {
                            \"endPage\": 365,
                            \"name\": \"Daily Digest\",
                            \"startPage\": 362
                        }
                    ],
                    \"sessionNumber\": 2,
                    \"updateDate\": \"2022-11-04\",
                    \"volumeNumber\": 94
                    }
                    ],
                    \"pagination\": {
                        \"count\": 4
                    },
                    {
                    \"request\": {
                    \"contentType\": \"application/json\",
                    \"day\": \"19\",
                    \"format\": \"json\",
                    \"month\": \"05\",
                    \"year\": \"1948\"
                   },

    Args:
        year (str):
        month (str):
        day (str):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        year=year,
        month=month,
        day=day,
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
