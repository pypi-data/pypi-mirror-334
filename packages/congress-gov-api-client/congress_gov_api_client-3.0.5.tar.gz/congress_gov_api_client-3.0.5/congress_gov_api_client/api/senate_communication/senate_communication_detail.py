from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    communication_type: str,
    communication_number: int,
    *,
    format_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/senate-communication/{congress}/{communication_type}/{communication_number}",
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
    communication_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified Senate communication.

     GET /senate-communication/:congress/:communicationType/:communicationNumber

    **Example Request**

    https://api.congress.gov/v3/senate-communication/117/ec/2561?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"senateCommunication\": {
                \"abstract\": \"A communication from the Board Chairman and Chief Executive Officer,
    Farm Credit Administration, transmitting, pursuant to law, the Administration's annual report for
    calendar year 2021; to the Committee on Agriculture, Nutrition, and Forestry.\",
                \"chamber\": \"Senate\",
                \"committees\": [
                    {
                        \"name\": \"Agriculture, Nutrition, and Forestry Committee\",
                        \"referralDate\": \"2021-11-03\",
                        \"systemCode\": \"ssaf00\",
                        \"url\": \"https://api.congress.gov/v3/committee/senate/ssaf00\"
                    }
                ],
                \"communicationType\": {
                    \"code\": \"EC\",
                    \"name\": \"Executive Communication\"
                },
                \"congress\": 117,
                \"congressionalRecordDate\": \"2021-11-03\",
                \"number\": 2561,
                \"sessionNumber\": 1,
                \"updateDate\": \"2021-11-04T07:15:16Z\"
            }
        }

    Args:
        congress (int):
        communication_type (str):
        communication_number (int):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        communication_type=communication_type,
        communication_number=communication_number,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    communication_type: str,
    communication_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified Senate communication.

     GET /senate-communication/:congress/:communicationType/:communicationNumber

    **Example Request**

    https://api.congress.gov/v3/senate-communication/117/ec/2561?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"senateCommunication\": {
                \"abstract\": \"A communication from the Board Chairman and Chief Executive Officer,
    Farm Credit Administration, transmitting, pursuant to law, the Administration's annual report for
    calendar year 2021; to the Committee on Agriculture, Nutrition, and Forestry.\",
                \"chamber\": \"Senate\",
                \"committees\": [
                    {
                        \"name\": \"Agriculture, Nutrition, and Forestry Committee\",
                        \"referralDate\": \"2021-11-03\",
                        \"systemCode\": \"ssaf00\",
                        \"url\": \"https://api.congress.gov/v3/committee/senate/ssaf00\"
                    }
                ],
                \"communicationType\": {
                    \"code\": \"EC\",
                    \"name\": \"Executive Communication\"
                },
                \"congress\": 117,
                \"congressionalRecordDate\": \"2021-11-03\",
                \"number\": 2561,
                \"sessionNumber\": 1,
                \"updateDate\": \"2021-11-04T07:15:16Z\"
            }
        }

    Args:
        congress (int):
        communication_type (str):
        communication_number (int):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        communication_type=communication_type,
        communication_number=communication_number,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
