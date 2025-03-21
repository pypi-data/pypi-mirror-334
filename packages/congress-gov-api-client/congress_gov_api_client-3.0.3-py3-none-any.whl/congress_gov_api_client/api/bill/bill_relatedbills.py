from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    bill_type: str,
    bill_number: int,
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
        "url": f"/bill/{congress}/{bill_type}/{bill_number}/relatedbills",
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
    bill_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns the list of related bills to a specified bill.

     GET /bill/:congress/:billType/:billNumber/relatedbills

    **Example Request**

    https://api.congress.gov/v3/bill/117/hr/3076/relatedbills?api_key=[INSERT_KEY]

    **Example Response**

        {
          \"relatedBills\": [
                {
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2021-05-19\",
                        \"text\": \"Read twice and referred to the Committee on Homeland Security and
    Governmental Affairs.\"
                    },
                    \"number\": 1720,
                    \"relationshipDetails\": [
                        {
                            \"identifiedBy\": \"CRS\",
                            \"type\": \"Related bill\"
                        }
                    ],
                    \"title\": \"Postal Service Reform Act of 2021\",
                    \"type\": \"S\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/s/1720?format=json\"
                },
                {
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2022-02-08\",
                        \"actionTime\": \"14:24:47\",
                        \"text\": \"Motion to reconsider laid on the table Agreed to without
    objection.\"
                    },
                    \"number\": 912,
                    \"relationshipDetails\": [
                        {
                            \"identifiedBy\": \"House\",
                            \"type\": \"Procedurally-related\"
                        },
                        {
                            \"identifiedBy\": \"House\",
                            \"type\": \"Related bill\"
                        }
                    ],
                    \"title\": \"Providing for consideration of the bill (H.R. 3076) to provide
    stability to and enhance the services of the United States Postal Service, and for other purposes;
    providing for consideration of the bill (H.R. 6617) making further continuing appropriations for the
    fiscal year ending September 30, 2022, and for other purposes; and for other purposes.\",
                    \"type\": \"HRES\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/hres/912?format=json\"
                },
            ],
        }

    Args:
        congress (int):
        bill_type (str):
        bill_number (int):
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
        bill_type=bill_type,
        bill_number=bill_number,
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
    bill_type: str,
    bill_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns the list of related bills to a specified bill.

     GET /bill/:congress/:billType/:billNumber/relatedbills

    **Example Request**

    https://api.congress.gov/v3/bill/117/hr/3076/relatedbills?api_key=[INSERT_KEY]

    **Example Response**

        {
          \"relatedBills\": [
                {
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2021-05-19\",
                        \"text\": \"Read twice and referred to the Committee on Homeland Security and
    Governmental Affairs.\"
                    },
                    \"number\": 1720,
                    \"relationshipDetails\": [
                        {
                            \"identifiedBy\": \"CRS\",
                            \"type\": \"Related bill\"
                        }
                    ],
                    \"title\": \"Postal Service Reform Act of 2021\",
                    \"type\": \"S\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/s/1720?format=json\"
                },
                {
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2022-02-08\",
                        \"actionTime\": \"14:24:47\",
                        \"text\": \"Motion to reconsider laid on the table Agreed to without
    objection.\"
                    },
                    \"number\": 912,
                    \"relationshipDetails\": [
                        {
                            \"identifiedBy\": \"House\",
                            \"type\": \"Procedurally-related\"
                        },
                        {
                            \"identifiedBy\": \"House\",
                            \"type\": \"Related bill\"
                        }
                    ],
                    \"title\": \"Providing for consideration of the bill (H.R. 3076) to provide
    stability to and enhance the services of the United States Postal Service, and for other purposes;
    providing for consideration of the bill (H.R. 6617) making further continuing appropriations for the
    fiscal year ending September 30, 2022, and for other purposes; and for other purposes.\",
                    \"type\": \"HRES\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/hres/912?format=json\"
                },
            ],
        }

    Args:
        congress (int):
        bill_type (str):
        bill_number (int):
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
        bill_type=bill_type,
        bill_number=bill_number,
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
