from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    chamber: str,
    committee_code: str,
    *,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params["offset"] = offset

    params["limit"] = limit

    params["fromDateTime"] = from_date_time

    params["toDateTime"] = to_date_time

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/committee/{chamber}/{committee_code}/bills",
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
    chamber: str,
    committee_code: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns the list of legislation associated with the specified congressional committee.

     GET /committee/:chamber/:committeeCode/bills

    **Example Request**

    https://api.congress.gov/v3/committee/house/hspw00/bills?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"committee-bills\": {
                \"bills\": [
                    {
                        \"actionDate\": \"2012-04-19T13:01:00Z\",
                        \"congress\": 112,
                        \"number\": \"117\",
                        \"relationshipType\": \"Referred to\",
                        \"type\": \"HCONRES\",
                        \"updateDate\": \"2019-02-17T21:10:13Z\",
                        \"url\": \"https://api.congress.gov/v3/bill/112/hconres/117?format=json\"
                    },
                    {
                        \"actionDate\": \"2012-02-08T14:51:00Z\",
                        \"congress\": 112,
                        \"number\": \"543\",
                        \"relationshipType\": \"Referred to\",
                        \"type\": \"HRES\",
                        \"updateDate\": \"2019-02-17T21:05:25Z\",
                        \"url\": \"https://api.congress.gov/v3/bill/112/hres/543?format=json\"
                    },
                ],
            },
        }

    Args:
        chamber (str):
        committee_code (str):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_date_time (Union[Unset, str]):
        to_date_time (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        chamber=chamber,
        committee_code=committee_code,
        format_=format_,
        offset=offset,
        limit=limit,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    chamber: str,
    committee_code: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns the list of legislation associated with the specified congressional committee.

     GET /committee/:chamber/:committeeCode/bills

    **Example Request**

    https://api.congress.gov/v3/committee/house/hspw00/bills?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"committee-bills\": {
                \"bills\": [
                    {
                        \"actionDate\": \"2012-04-19T13:01:00Z\",
                        \"congress\": 112,
                        \"number\": \"117\",
                        \"relationshipType\": \"Referred to\",
                        \"type\": \"HCONRES\",
                        \"updateDate\": \"2019-02-17T21:10:13Z\",
                        \"url\": \"https://api.congress.gov/v3/bill/112/hconres/117?format=json\"
                    },
                    {
                        \"actionDate\": \"2012-02-08T14:51:00Z\",
                        \"congress\": 112,
                        \"number\": \"543\",
                        \"relationshipType\": \"Referred to\",
                        \"type\": \"HRES\",
                        \"updateDate\": \"2019-02-17T21:05:25Z\",
                        \"url\": \"https://api.congress.gov/v3/bill/112/hres/543?format=json\"
                    },
                ],
            },
        }

    Args:
        chamber (str):
        committee_code (str):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_date_time (Union[Unset, str]):
        to_date_time (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        chamber=chamber,
        committee_code=committee_code,
        format_=format_,
        offset=offset,
        limit=limit,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
