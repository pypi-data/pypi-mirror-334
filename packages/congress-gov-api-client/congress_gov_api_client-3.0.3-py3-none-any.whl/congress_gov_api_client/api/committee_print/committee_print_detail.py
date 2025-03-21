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
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/committee-print/{congress}/{chamber}/{jacket_number}",
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
) -> Response[Any]:
    r"""Returns detailed information for a specified committee print.

     GET /committee-print/:congress/:chamber/:jacketNumber

    **Example Request**

    https://api.congress.gov/v3/committee-print/117/house/48144?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"committeePrint\": [
                {
                    \"associatedBills\": [
                        {
                            \"congress\": 117,
                            \"number\": \"5768\",
                            \"type\": \"HR\",
                            \"url\": \"https://api.congress.gov/v3/bill/117/hr/5768?format=json\"
                        }
                    ],
                    \"chamber\": \"House\",
                    \"citation\": \"117-62\",
                    \"committees\": [
                        {
                            \"name\": \"Rules Committee\",
                            \"systemCode\": \"hsru00\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hsru00?format=json\"
                        }
                    ],
                    \"congress\": 117,
                    \"jacketNumber\": 48144,
                    \"number\": \"62\",
                    \"text\": {
                        \"count\": 4,
                        \"url\": \"https://api.congress.gov/v3/committee-
    print/117/house/48144/text?format=json\"
                    },
                    \"title\": \"RULES COMMITTEE PRINT 117-62 TEXT OF H.R. 5768, VIOLENT INCIDENT CLEAR-
    ANCE AND TECHNOLOGICAL INVESTIGATIVE METHODS ACT OF 2022\",
                    \"updateDate\": \"2022-08-01 21:19:33+00:00\"
                }
            ],
        }

    Args:
        congress (int):
        chamber (str):
        jacket_number (int):
        format_ (Union[Unset, str]):

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
) -> Response[Any]:
    r"""Returns detailed information for a specified committee print.

     GET /committee-print/:congress/:chamber/:jacketNumber

    **Example Request**

    https://api.congress.gov/v3/committee-print/117/house/48144?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"committeePrint\": [
                {
                    \"associatedBills\": [
                        {
                            \"congress\": 117,
                            \"number\": \"5768\",
                            \"type\": \"HR\",
                            \"url\": \"https://api.congress.gov/v3/bill/117/hr/5768?format=json\"
                        }
                    ],
                    \"chamber\": \"House\",
                    \"citation\": \"117-62\",
                    \"committees\": [
                        {
                            \"name\": \"Rules Committee\",
                            \"systemCode\": \"hsru00\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hsru00?format=json\"
                        }
                    ],
                    \"congress\": 117,
                    \"jacketNumber\": 48144,
                    \"number\": \"62\",
                    \"text\": {
                        \"count\": 4,
                        \"url\": \"https://api.congress.gov/v3/committee-
    print/117/house/48144/text?format=json\"
                    },
                    \"title\": \"RULES COMMITTEE PRINT 117-62 TEXT OF H.R. 5768, VIOLENT INCIDENT CLEAR-
    ANCE AND TECHNOLOGICAL INVESTIGATIVE METHODS ACT OF 2022\",
                    \"updateDate\": \"2022-08-01 21:19:33+00:00\"
                }
            ],
        }

    Args:
        congress (int):
        chamber (str):
        jacket_number (int):
        format_ (Union[Unset, str]):

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
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
