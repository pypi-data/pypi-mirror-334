from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    bioguide_id: str,
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
        "url": f"/member/{bioguide_id}/sponsored-legislation",
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
    bioguide_id: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns the list of legislation sponsored by a specified congressional member.

     GET /member/:bioguideId/sponsored-legislation

    **Example Request**

    https://api.congress.gov/v3/member/L000174/sponsored-legislation?api_key=[INSERT_KEY]

    **Example Response**

        {
             \"sponsoredLegislation\": [
                {
                    \"congress\": 117,
                    \"introducedDate\": \"2022-06-16\",
                    \"latestAction\": {
                        \"actionDate\": \"2022-06-16\",
                        \"text\": \"Read twice and referred to the Committee on the Judiciary.\"
                    },
                    \"number\": \"4417\",
                    \"policyArea\": {
                        \"name\": \"Commerce\"
                    },
                    \"title\": \"Patent Trial and Appeal Board Reform Act of 2022\",
                    \"type\": \"S\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/s/4417?format=json\"
                },
                {
                    \"congress\": 117,
                    \"introducedDate\": \"2022-06-09\",
                    \"latestAction\": {
                        \"actionDate\": \"2022-06-09\",
                        \"text\": \"Read twice and referred to the Committee on the Judiciary.\"
                    },
                    \"number\": \"4373\",
                    \"policyArea\": {
                        \"name\": \"Crime and Law Enforcement\"
                    },
                    \"title\": \"NDO Fairness Act\",
                    \"type\": \"S\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/s/4373?format=json\"
                },
            ]
        }

    Args:
        bioguide_id (str):
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
        bioguide_id=bioguide_id,
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    bioguide_id: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns the list of legislation sponsored by a specified congressional member.

     GET /member/:bioguideId/sponsored-legislation

    **Example Request**

    https://api.congress.gov/v3/member/L000174/sponsored-legislation?api_key=[INSERT_KEY]

    **Example Response**

        {
             \"sponsoredLegislation\": [
                {
                    \"congress\": 117,
                    \"introducedDate\": \"2022-06-16\",
                    \"latestAction\": {
                        \"actionDate\": \"2022-06-16\",
                        \"text\": \"Read twice and referred to the Committee on the Judiciary.\"
                    },
                    \"number\": \"4417\",
                    \"policyArea\": {
                        \"name\": \"Commerce\"
                    },
                    \"title\": \"Patent Trial and Appeal Board Reform Act of 2022\",
                    \"type\": \"S\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/s/4417?format=json\"
                },
                {
                    \"congress\": 117,
                    \"introducedDate\": \"2022-06-09\",
                    \"latestAction\": {
                        \"actionDate\": \"2022-06-09\",
                        \"text\": \"Read twice and referred to the Committee on the Judiciary.\"
                    },
                    \"number\": \"4373\",
                    \"policyArea\": {
                        \"name\": \"Crime and Law Enforcement\"
                    },
                    \"title\": \"NDO Fairness Act\",
                    \"type\": \"S\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/s/4373?format=json\"
                },
            ]
        }

    Args:
        bioguide_id (str):
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
        bioguide_id=bioguide_id,
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
