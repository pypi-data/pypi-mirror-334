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
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params["offset"] = offset

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/law/{congress}",
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
) -> Response[Any]:
    r"""Returns a list of laws filtered by the specified congress.

     GET /law/:congress

    **Example Request**

    https://api.congress.gov/v3/law/118?api_key=[INSERT_KEY]

    **Example Response**

        {
           \"bills\": [
              {
                   \"congress\": 118,
                   \"latestAction\": {
                       \"actionDate\": \"2023-03-20\",
                       \"text\": \"Became Public Law No: 118-1.\"
                    },
                    \"laws\": [
                        {
                            \"number\": \"118-1\",
                            \"type\": \"Public Law\"
                        }
                    ]
                    \"number\": \"26\",
                    \"originChamber\": \"House\",
                    \"originChamberCode\": \"H\",
                    \"title\": \"Disapproving the action of the District of Columbia Council in
    approving the Revised Criminal Code Act of 2022.\",
                    \"type\": \"HJRES\",
                    \"updateDate\": \"2024-03-18\",
                    \"updateDateIncludingText\": \"2024-03-18T20:28:27Z\",
                    \"url\": \"http://api.congress.gov/v3/bill/118/hjres/26?format=json\"
              },
              {
                   \"congress\": 118,
                   \"latestAction\": {
                       \"actionDate\": \"2023-07-26\",
                       \"text\": \"Became Public Law No: 118-10.\"
                   },
                   \"laws\": [
                        {
                            \"number\": \"118-1\",
                            \"type\": \"Public Law\"
                        }
                    ]
                   \"number\": \"1096\",
                   \"originChamber\": \"House\",
                   \"originChamberCode\": \"H\",
                   \"title\": \"250th Anniversary of the United States Marine Corps Commemorative Coin
    Act\",
                   \"type\": \"HR\",
                   \"updateDate\": \"2024-03-18\",
                   \"updateDateIncludingText\": \"2024-03-18T21:14:03Z\",
                   \"url\": \"http://api.congress.gov/v3/bill/118/hr/1096?format=json\"
                },
           ],
        }

    Args:
        congress (int):
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
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns a list of laws filtered by the specified congress.

     GET /law/:congress

    **Example Request**

    https://api.congress.gov/v3/law/118?api_key=[INSERT_KEY]

    **Example Response**

        {
           \"bills\": [
              {
                   \"congress\": 118,
                   \"latestAction\": {
                       \"actionDate\": \"2023-03-20\",
                       \"text\": \"Became Public Law No: 118-1.\"
                    },
                    \"laws\": [
                        {
                            \"number\": \"118-1\",
                            \"type\": \"Public Law\"
                        }
                    ]
                    \"number\": \"26\",
                    \"originChamber\": \"House\",
                    \"originChamberCode\": \"H\",
                    \"title\": \"Disapproving the action of the District of Columbia Council in
    approving the Revised Criminal Code Act of 2022.\",
                    \"type\": \"HJRES\",
                    \"updateDate\": \"2024-03-18\",
                    \"updateDateIncludingText\": \"2024-03-18T20:28:27Z\",
                    \"url\": \"http://api.congress.gov/v3/bill/118/hjres/26?format=json\"
              },
              {
                   \"congress\": 118,
                   \"latestAction\": {
                       \"actionDate\": \"2023-07-26\",
                       \"text\": \"Became Public Law No: 118-10.\"
                   },
                   \"laws\": [
                        {
                            \"number\": \"118-1\",
                            \"type\": \"Public Law\"
                        }
                    ]
                   \"number\": \"1096\",
                   \"originChamber\": \"House\",
                   \"originChamberCode\": \"H\",
                   \"title\": \"250th Anniversary of the United States Marine Corps Commemorative Coin
    Act\",
                   \"type\": \"HR\",
                   \"updateDate\": \"2024-03-18\",
                   \"updateDateIncludingText\": \"2024-03-18T21:14:03Z\",
                   \"url\": \"http://api.congress.gov/v3/bill/118/hr/1096?format=json\"
                },
           ],
        }

    Args:
        congress (int):
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
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
