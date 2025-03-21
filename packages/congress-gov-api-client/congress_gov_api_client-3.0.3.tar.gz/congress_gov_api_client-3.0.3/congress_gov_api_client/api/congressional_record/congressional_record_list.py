from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    format_: Union[Unset, str] = UNSET,
    y: Union[Unset, int] = UNSET,
    m: Union[Unset, int] = UNSET,
    d: Union[Unset, int] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params["y"] = y

    params["m"] = m

    params["d"] = d

    params["offset"] = offset

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/congressional-record",
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
    y: Union[Unset, int] = UNSET,
    m: Union[Unset, int] = UNSET,
    d: Union[Unset, int] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns a list of congressional record issues sorted by most recent.

     GET /congressional-record/?y=:year&m=:month&d=:day

    **Example Request**

    https://api.congress.gov/v3/congressional-record/?y=2022&m=6&d=28&api_key=[INSERT_KEY]

    **Example Response**

        {
            \"Results\": {
                \"IndexStart\": 1,
                \"Issues\": [
                    {
                        \"Congress\": \"117\",
                        \"Id\": 26958,
                        \"Issue\": \"109\",
                        \"Links\": {
                            \"Digest\": {
                                \"Label\": \"Daily Digest\",
                                \"Ordinal\": 1,
                                \"PDF\": [
                                    {
                                        \"Part\": \"1\",
                                        \"Url\":
    \"https://www.congress.gov/117/crec/2022/06/28/168/109/CREC-2022-06-28-dailydigest.pdf\"
                                    }
                                ]
                            },
                            \"FullRecord\": {
                                \"Label\": \"Entire Issue\",
                                \"Ordinal\": 5,
                                \"PDF\": [
                                    {
                                        \"Part\": \"1\",
                                        \"Url\":
    \"https://www.congress.gov/117/crec/2022/06/28/168/109/CREC-2022-06-28.pdf\"
                                    }
                                ]
                            },
                            \"House\": {
                                \"Label\": \"House Section\",
                                \"Ordinal\": 3,
                                \"PDF\": [
                                    {
                                        \"Part\": \"1\",
                                        \"Url\":
    \"https://www.congress.gov/117/crec/2022/06/28/168/109/CREC-2022-06-28-house.pdf\"
                                    }
                                ]
                            },
                            \"Remarks\": {
                                \"Label\": \"Extensions of Remarks Section\",
                                \"Ordinal\": 4,
                                \"PDF\": [
                                    {
                                        \"Part\": \"1\",
                                        \"Url\":
    \"https://www.congress.gov/117/crec/2022/06/28/168/109/CREC-2022-06-28-extensions.pdf\"
                                    }
                                ]
                            },
                            \"Senate\": {
                                \"Label\": \"Senate Section\",
                                \"Ordinal\": 2,
                                \"PDF\": [
                                    {
                                        \"Part\": \"1\",
                                        \"Url\":
    \"https://www.congress.gov/117/crec/2022/06/28/168/109/CREC-2022-06-28-senate.pdf\"
                                    }
                                ]
                            }
                        },
                        \"PublishDate\": \"2022-06-28\",
                        \"Session\": \"2\",
                        \"Volume\": \"168\"
                    },
                ],
           }
        }

    Args:
        format_ (Union[Unset, str]):
        y (Union[Unset, int]):
        m (Union[Unset, int]):
        d (Union[Unset, int]):
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
        y=y,
        m=m,
        d=d,
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
    y: Union[Unset, int] = UNSET,
    m: Union[Unset, int] = UNSET,
    d: Union[Unset, int] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns a list of congressional record issues sorted by most recent.

     GET /congressional-record/?y=:year&m=:month&d=:day

    **Example Request**

    https://api.congress.gov/v3/congressional-record/?y=2022&m=6&d=28&api_key=[INSERT_KEY]

    **Example Response**

        {
            \"Results\": {
                \"IndexStart\": 1,
                \"Issues\": [
                    {
                        \"Congress\": \"117\",
                        \"Id\": 26958,
                        \"Issue\": \"109\",
                        \"Links\": {
                            \"Digest\": {
                                \"Label\": \"Daily Digest\",
                                \"Ordinal\": 1,
                                \"PDF\": [
                                    {
                                        \"Part\": \"1\",
                                        \"Url\":
    \"https://www.congress.gov/117/crec/2022/06/28/168/109/CREC-2022-06-28-dailydigest.pdf\"
                                    }
                                ]
                            },
                            \"FullRecord\": {
                                \"Label\": \"Entire Issue\",
                                \"Ordinal\": 5,
                                \"PDF\": [
                                    {
                                        \"Part\": \"1\",
                                        \"Url\":
    \"https://www.congress.gov/117/crec/2022/06/28/168/109/CREC-2022-06-28.pdf\"
                                    }
                                ]
                            },
                            \"House\": {
                                \"Label\": \"House Section\",
                                \"Ordinal\": 3,
                                \"PDF\": [
                                    {
                                        \"Part\": \"1\",
                                        \"Url\":
    \"https://www.congress.gov/117/crec/2022/06/28/168/109/CREC-2022-06-28-house.pdf\"
                                    }
                                ]
                            },
                            \"Remarks\": {
                                \"Label\": \"Extensions of Remarks Section\",
                                \"Ordinal\": 4,
                                \"PDF\": [
                                    {
                                        \"Part\": \"1\",
                                        \"Url\":
    \"https://www.congress.gov/117/crec/2022/06/28/168/109/CREC-2022-06-28-extensions.pdf\"
                                    }
                                ]
                            },
                            \"Senate\": {
                                \"Label\": \"Senate Section\",
                                \"Ordinal\": 2,
                                \"PDF\": [
                                    {
                                        \"Part\": \"1\",
                                        \"Url\":
    \"https://www.congress.gov/117/crec/2022/06/28/168/109/CREC-2022-06-28-senate.pdf\"
                                    }
                                ]
                            }
                        },
                        \"PublishDate\": \"2022-06-28\",
                        \"Session\": \"2\",
                        \"Volume\": \"168\"
                    },
                ],
           }
        }

    Args:
        format_ (Union[Unset, str]):
        y (Union[Unset, int]):
        m (Union[Unset, int]):
        d (Union[Unset, int]):
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
        y=y,
        m=m,
        d=d,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
