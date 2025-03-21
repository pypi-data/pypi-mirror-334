from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
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
        "url": "/congress",
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
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns a list of congresses and congressional sessions.

     GET /congress

    **Example Request**

    https://api.congress.gov/v3/congress?api_ke[INSERT_KEY]

    **Example Response**

        {
             \"congresses\": [
                {
                    \"endYear\": \"2022\",
                    \"name\": \"117th Congress\",
                    \"sessions\": [
                        {
                            \"chamber\": \"House of Representatives\",
                            \"endDate\": \"2022-01-03\",
                            \"number\": 1,
                            \"startDate\": \"2021-01-03\",
                            \"type\": \"R\"
                        },
                        {
                            \"chamber\": \"Senate\",
                            \"endDate\": \"2022-01-03\",
                            \"number\": 1,
                            \"startDate\": \"2021-01-03\",
                            \"type\": \"R\"
                        },
                        {
                            \"chamber\": \"House of Representatives\",
                            \"endDate\": null,
                            \"number\": 2,
                            \"startDate\": \"2022-01-03\",
                            \"type\": \"R\"
                        },
                        {
                            \"chamber\": \"Senate\",
                            \"endDate\": null,
                            \"number\": 2,
                            \"startDate\": \"2022-01-03\",
                            \"type\": \"R\"
                        }
                    ],
                    \"startYear\": \"2021\"
                },
                {
                    \"endYear\": \"2020\",
                    \"name\": \"116th Congress\",
                    \"sessions\": [
                        {
                            \"chamber\": \"House of Representatives\",
                            \"endDate\": \"2020-01-03\",
                            \"number\": 1,
                            \"startDate\": \"2019-01-03\",
                            \"type\": \"R\"
                        },
                        {
                            \"chamber\": \"Senate\",
                            \"endDate\": \"2020-01-03\",
                            \"number\": 1,
                            \"startDate\": \"2019-01-03\",
                            \"type\": \"R\"
                        },
                        {
                            \"chamber\": \"House of Representatives\",
                            \"endDate\": \"2021-01-03\",
                            \"number\": 2,
                            \"startDate\": \"2020-01-03\",
                            \"type\": \"R\"
                        },
                        {
                            \"chamber\": \"Senate\",
                            \"endDate\": \"2021-01-03\",
                            \"number\": 2,
                            \"startDate\": \"2020-01-03\",
                            \"type\": \"R\"
                        }
                    ],
                    \"startYear\": \"2019\"
                },
            ],
        }

    Args:
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
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns a list of congresses and congressional sessions.

     GET /congress

    **Example Request**

    https://api.congress.gov/v3/congress?api_ke[INSERT_KEY]

    **Example Response**

        {
             \"congresses\": [
                {
                    \"endYear\": \"2022\",
                    \"name\": \"117th Congress\",
                    \"sessions\": [
                        {
                            \"chamber\": \"House of Representatives\",
                            \"endDate\": \"2022-01-03\",
                            \"number\": 1,
                            \"startDate\": \"2021-01-03\",
                            \"type\": \"R\"
                        },
                        {
                            \"chamber\": \"Senate\",
                            \"endDate\": \"2022-01-03\",
                            \"number\": 1,
                            \"startDate\": \"2021-01-03\",
                            \"type\": \"R\"
                        },
                        {
                            \"chamber\": \"House of Representatives\",
                            \"endDate\": null,
                            \"number\": 2,
                            \"startDate\": \"2022-01-03\",
                            \"type\": \"R\"
                        },
                        {
                            \"chamber\": \"Senate\",
                            \"endDate\": null,
                            \"number\": 2,
                            \"startDate\": \"2022-01-03\",
                            \"type\": \"R\"
                        }
                    ],
                    \"startYear\": \"2021\"
                },
                {
                    \"endYear\": \"2020\",
                    \"name\": \"116th Congress\",
                    \"sessions\": [
                        {
                            \"chamber\": \"House of Representatives\",
                            \"endDate\": \"2020-01-03\",
                            \"number\": 1,
                            \"startDate\": \"2019-01-03\",
                            \"type\": \"R\"
                        },
                        {
                            \"chamber\": \"Senate\",
                            \"endDate\": \"2020-01-03\",
                            \"number\": 1,
                            \"startDate\": \"2019-01-03\",
                            \"type\": \"R\"
                        },
                        {
                            \"chamber\": \"House of Representatives\",
                            \"endDate\": \"2021-01-03\",
                            \"number\": 2,
                            \"startDate\": \"2020-01-03\",
                            \"type\": \"R\"
                        },
                        {
                            \"chamber\": \"Senate\",
                            \"endDate\": \"2021-01-03\",
                            \"number\": 2,
                            \"startDate\": \"2020-01-03\",
                            \"type\": \"R\"
                        }
                    ],
                    \"startYear\": \"2019\"
                },
            ],
        }

    Args:
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
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
