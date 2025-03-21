from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    chamber: str,
    jacket_number: int,
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
        "url": f"/committee-print/{congress}/{chamber}/{jacket_number}/text",
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
    chamber: str,
    jacket_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns the list of texts for a specified committee print.

     GET /committee-print/:congress/:chamber/:jacketNumber/text

    **Example Request**

    https://api.congress.gov/v3/committee-print/117/house/48144/text?api_key=[INSERT_KEY]

    **Example Response**

          {
              \"text\": [
                  {
                      \"type\": \"Formatted Text\",
                      \"url\": \"https://www.congress.gov/117/cprt/HPRT48144/CPRT-117HPRT48144.htm\"
                  },
                  {
                      \"type\": \"PDF\",
                      \"url\": \"https://www.congress.gov/117/cprt/HPRT48144/CPRT-117HPRT48144.pdf\"
                  },
                  {
                      \"type\": \"Formatted XML\",
                      \"url\": \"https://www.congress.gov/117/cprt/HPRT48144/CPRT-117HPRT48144.xml\"
                  },
                  {
                      \"type\": \"Generated HTML\",
                      \"url\": \"https://www.congress.gov/117/cprt/HPRT48144/CPRT-117HPRT48144_gen.htm\"
                  }
              ]
          }

    Args:
        congress (int):
        chamber (str):
        jacket_number (int):
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
        chamber=chamber,
        jacket_number=jacket_number,
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
    chamber: str,
    jacket_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns the list of texts for a specified committee print.

     GET /committee-print/:congress/:chamber/:jacketNumber/text

    **Example Request**

    https://api.congress.gov/v3/committee-print/117/house/48144/text?api_key=[INSERT_KEY]

    **Example Response**

          {
              \"text\": [
                  {
                      \"type\": \"Formatted Text\",
                      \"url\": \"https://www.congress.gov/117/cprt/HPRT48144/CPRT-117HPRT48144.htm\"
                  },
                  {
                      \"type\": \"PDF\",
                      \"url\": \"https://www.congress.gov/117/cprt/HPRT48144/CPRT-117HPRT48144.pdf\"
                  },
                  {
                      \"type\": \"Formatted XML\",
                      \"url\": \"https://www.congress.gov/117/cprt/HPRT48144/CPRT-117HPRT48144.xml\"
                  },
                  {
                      \"type\": \"Generated HTML\",
                      \"url\": \"https://www.congress.gov/117/cprt/HPRT48144/CPRT-117HPRT48144_gen.htm\"
                  }
              ]
          }

    Args:
        congress (int):
        chamber (str):
        jacket_number (int):
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
        chamber=chamber,
        jacket_number=jacket_number,
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
