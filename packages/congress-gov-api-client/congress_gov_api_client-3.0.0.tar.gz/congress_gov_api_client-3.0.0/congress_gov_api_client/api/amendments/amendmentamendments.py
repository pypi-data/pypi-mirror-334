from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    amendment_type: str,
    amendment_number: int,
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
        "url": f"/amendment/{congress}/{amendment_type}/{amendment_number}/amendments",
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
    amendment_type: str,
    amendment_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns the list of amendments to a specified amendment.

     GET /amendment/:congress/:amendmentType/:amendmentNumber/amendments

    **Example Request**

    https://api.congress.gov/v3/amendment/117/samdt/2137/amendments?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"amendments\": [
                {
                    \"congress\": 117,
                    \"latestAction\": {
                        \"date\": \"2021-08-04\",
                        \"text\": \"Amendment SA 2548 agreed to in Senate by Voice Vote.\"
                    },
                    \"number\": \"2548\",
                    \"purpose\": \"To require the Secretary of Agriculture to establish a Joint Chiefs
    Landscape Restoration Partnership program.\",
                    \"type\": \"SAMDT\",
                    \"url\": \"https://api.congress.gov/v3/amendment/117/samdt/2548?format=json\"
                },
                {
                    \"congress\": 117,
                    \"number\": \"2547\",
                    \"type\": \"SAMDT\",
                    \"updateDate\": \"2022-02-25T17:34:50Z\",
                    \"url\": \"https://api.congress.gov/v3/amendment/117/samdt/2547?format=json\"
                },
            ],
        }

    Args:
        congress (int):
        amendment_type (str):
        amendment_number (int):
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
        congress=congress,
        amendment_type=amendment_type,
        amendment_number=amendment_number,
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    amendment_type: str,
    amendment_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns the list of amendments to a specified amendment.

     GET /amendment/:congress/:amendmentType/:amendmentNumber/amendments

    **Example Request**

    https://api.congress.gov/v3/amendment/117/samdt/2137/amendments?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"amendments\": [
                {
                    \"congress\": 117,
                    \"latestAction\": {
                        \"date\": \"2021-08-04\",
                        \"text\": \"Amendment SA 2548 agreed to in Senate by Voice Vote.\"
                    },
                    \"number\": \"2548\",
                    \"purpose\": \"To require the Secretary of Agriculture to establish a Joint Chiefs
    Landscape Restoration Partnership program.\",
                    \"type\": \"SAMDT\",
                    \"url\": \"https://api.congress.gov/v3/amendment/117/samdt/2548?format=json\"
                },
                {
                    \"congress\": 117,
                    \"number\": \"2547\",
                    \"type\": \"SAMDT\",
                    \"updateDate\": \"2022-02-25T17:34:50Z\",
                    \"url\": \"https://api.congress.gov/v3/amendment/117/samdt/2547?format=json\"
                },
            ],
        }

    Args:
        congress (int):
        amendment_type (str):
        amendment_number (int):
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
        congress=congress,
        amendment_type=amendment_type,
        amendment_number=amendment_number,
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
