from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    nomination_number: int,
    *,
    format_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/nomination/{congress}/{nomination_number}",
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
    nomination_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified nomination.

     GET /nomination/:congress/:nominationNumber

    **Example Request**

    https://api.congress.gov/v3/nomination/117/2467?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"nomination\": {
                \"actions\": {
                    \"count\": 1,
                    \"url\": \"https://api.congress.gov/v3/nomination/117/2467/actions?format=json\"
                },
                \"citation\": \"PN2467\",
                \"committees\": {
                    \"count\": 1,
                    \"url\": \"https://api.congress.gov/v3/nomination/117/2467/committees?format=json\"
                },
                \"congress\": 117,
                \"isList\": true,
                \"latestAction\": {
                    \"actionDate\": \"2022-08-03\",
                    \"text\": \"Received in the Senate and referred to the Committee on Armed
    Services.\"
                },
                \"nominees\": [
                    {
                        \"introText\": \"THE FOLLOWING NAMED OFFICERS FOR APPOINTMENT TO THE GRADE
    INDICATED IN THE UNITED STATES AIR FORCE UNDER TITLE 10, U.S.C., SECTION 624:\",
                        \"nomineeCount\": 12,
                        \"ordinal\": 1,
                        \"organization\": \"Air Force\",
                        \"positionTitle\": \"Colonel\",
                        \"url\": \"https://api.congress.gov/v3/nomination/117/2467/1?format=json\"
                    }
                ],
                \"number\": 2467,
                \"partNumber\": \"00\",
                \"receivedDate\": \"2022-08-03\",
                \"updateDate\": \"2022-08-04T04:25:12Z\"
            },
        }

    Args:
        congress (int):
        nomination_number (int):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        nomination_number=nomination_number,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    nomination_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified nomination.

     GET /nomination/:congress/:nominationNumber

    **Example Request**

    https://api.congress.gov/v3/nomination/117/2467?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"nomination\": {
                \"actions\": {
                    \"count\": 1,
                    \"url\": \"https://api.congress.gov/v3/nomination/117/2467/actions?format=json\"
                },
                \"citation\": \"PN2467\",
                \"committees\": {
                    \"count\": 1,
                    \"url\": \"https://api.congress.gov/v3/nomination/117/2467/committees?format=json\"
                },
                \"congress\": 117,
                \"isList\": true,
                \"latestAction\": {
                    \"actionDate\": \"2022-08-03\",
                    \"text\": \"Received in the Senate and referred to the Committee on Armed
    Services.\"
                },
                \"nominees\": [
                    {
                        \"introText\": \"THE FOLLOWING NAMED OFFICERS FOR APPOINTMENT TO THE GRADE
    INDICATED IN THE UNITED STATES AIR FORCE UNDER TITLE 10, U.S.C., SECTION 624:\",
                        \"nomineeCount\": 12,
                        \"ordinal\": 1,
                        \"organization\": \"Air Force\",
                        \"positionTitle\": \"Colonel\",
                        \"url\": \"https://api.congress.gov/v3/nomination/117/2467/1?format=json\"
                    }
                ],
                \"number\": 2467,
                \"partNumber\": \"00\",
                \"receivedDate\": \"2022-08-03\",
                \"updateDate\": \"2022-08-04T04:25:12Z\"
            },
        }

    Args:
        congress (int):
        nomination_number (int):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        nomination_number=nomination_number,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
