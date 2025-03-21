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
        "url": f"/house-communication/{congress}/{communication_type}",
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
    r"""Returns a list of House communications filtered by the specified congress and communication type.

     GET /house-communication/:congress/:communicationType

    **Example Request**

    https://api.congress.gov/v3/house-communication/117/ec?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"houseCommunications\": [
                {
                    \"chamber\": \"House\",
                    \"communicationType\": {
                        \"code\": \"EC\",
                        \"name\": \"Executive Communication\"
                    },
                    \"congressNumber\": 117,
                    \"number\": \"2057\",
                    \"reportNature\": \"A letter reporting violations of the Antideficiency Act, by the
    United States Coast Guard.\",
                    \"submittingAgency\": \"Department of Homeland Security\",
                    \"submittingOfficial\": \"Secretary\",
                    \"updateDate\": \"2021-09-01\",
                    \"url\": \"https://api.congress.gov/v3/house-communication/117/ec/2057?format=json\"
                },
                {
                    \"chamber\": \"House\",
                    \"communicationNumber\": 3089,
                    \"communicationType\": {
                        \"code\": \"EC\",
                        \"name\": \"Executive Communication\"
                    },
                    \"congressNumber\": 117,
                    \"legalAuthority\": \"Public Law 93\u2013198, section 602(c)(1); (87 Stat. 814)\",
                    \"number\": \"3089\",
                    \"reportNature\": \"D.C. Act 24-267, \\"Jamal Khashoggi Way Designation Way Act of
    2021\\".\",
                    \"submittingAgency\": \"Council of the District of Columbia\",
                    \"submittingOfficial\": \"Chairman\",
                    \"updateDate\": \"2022-01-12\",
                    \"url\": \"https://api.congress.gov/v3/house-communication/117/ec/3089?format=json\"
                },
            ],
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
    r"""Returns a list of House communications filtered by the specified congress and communication type.

     GET /house-communication/:congress/:communicationType

    **Example Request**

    https://api.congress.gov/v3/house-communication/117/ec?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"houseCommunications\": [
                {
                    \"chamber\": \"House\",
                    \"communicationType\": {
                        \"code\": \"EC\",
                        \"name\": \"Executive Communication\"
                    },
                    \"congressNumber\": 117,
                    \"number\": \"2057\",
                    \"reportNature\": \"A letter reporting violations of the Antideficiency Act, by the
    United States Coast Guard.\",
                    \"submittingAgency\": \"Department of Homeland Security\",
                    \"submittingOfficial\": \"Secretary\",
                    \"updateDate\": \"2021-09-01\",
                    \"url\": \"https://api.congress.gov/v3/house-communication/117/ec/2057?format=json\"
                },
                {
                    \"chamber\": \"House\",
                    \"communicationNumber\": 3089,
                    \"communicationType\": {
                        \"code\": \"EC\",
                        \"name\": \"Executive Communication\"
                    },
                    \"congressNumber\": 117,
                    \"legalAuthority\": \"Public Law 93\u2013198, section 602(c)(1); (87 Stat. 814)\",
                    \"number\": \"3089\",
                    \"reportNature\": \"D.C. Act 24-267, \\"Jamal Khashoggi Way Designation Way Act of
    2021\\".\",
                    \"submittingAgency\": \"Council of the District of Columbia\",
                    \"submittingOfficial\": \"Chairman\",
                    \"updateDate\": \"2022-01-12\",
                    \"url\": \"https://api.congress.gov/v3/house-communication/117/ec/3089?format=json\"
                },
            ],
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
