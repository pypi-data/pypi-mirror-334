from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    communication_type: str,
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
        "url": f"/senate-communication/{congress}/{communication_type}",
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
    communication_type: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns a list of Senate communications filtered by the specified congress and communication type.

     GET /senate-communication/:congress/:communicationType

    **Example Request**

    https://api.congress.gov/v3/senate-communication/117/ec

    **Example Response**

          {
              \"senateCommunications\": [
                  {
                      \"chamber\": \"Senate\",
                      \"communicationType\": {
                          \"code\": \"EC\",
                          \"name\": \"Executive Communication\"
                      },
                      \"congress\": 117,
                      \"number\": 1615,
                      \"updateDate\": \"2021-08-16 20:24:19+00:00\",
                      \"url\": \"https://api.congress.gov/v3/senate-
    communication/117/ec/1615?format=json\"
                  },
                  {
                      \"chamber\": \"Senate\",
                      \"communicationType\": {
                          \"code\": \"EC\",
                          \"name\": \"Executive Communication\"
                      },
                      \"congress\": 117,
                      \"number\": 2040,
                      \"updateDate\": \"2021-09-23T07:15:14:00Z\",
                      \"url\": \"https://api.congress.gov/v3/senate-
    communication/117/ec/2040?format=json\"
                  },
              ]
          }

    Args:
        congress (int):
        communication_type (str):
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
        communication_type=communication_type,
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
    communication_type: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns a list of Senate communications filtered by the specified congress and communication type.

     GET /senate-communication/:congress/:communicationType

    **Example Request**

    https://api.congress.gov/v3/senate-communication/117/ec

    **Example Response**

          {
              \"senateCommunications\": [
                  {
                      \"chamber\": \"Senate\",
                      \"communicationType\": {
                          \"code\": \"EC\",
                          \"name\": \"Executive Communication\"
                      },
                      \"congress\": 117,
                      \"number\": 1615,
                      \"updateDate\": \"2021-08-16 20:24:19+00:00\",
                      \"url\": \"https://api.congress.gov/v3/senate-
    communication/117/ec/1615?format=json\"
                  },
                  {
                      \"chamber\": \"Senate\",
                      \"communicationType\": {
                          \"code\": \"EC\",
                          \"name\": \"Executive Communication\"
                      },
                      \"congress\": 117,
                      \"number\": 2040,
                      \"updateDate\": \"2021-09-23T07:15:14:00Z\",
                      \"url\": \"https://api.congress.gov/v3/senate-
    communication/117/ec/2040?format=json\"
                  },
              ]
          }

    Args:
        congress (int):
        communication_type (str):
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
        communication_type=communication_type,
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
