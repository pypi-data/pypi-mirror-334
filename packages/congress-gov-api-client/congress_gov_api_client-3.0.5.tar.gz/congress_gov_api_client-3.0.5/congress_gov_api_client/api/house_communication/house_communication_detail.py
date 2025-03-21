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
        "url": f"/house-communication/{congress}/{communication_type}/{communication_number}",
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
    r"""Returns detailed information for a specified House communication.

     GET /house-communication/:congress/:communicationType/:communicationNumber

    **Example Request**

    https://api.congress.gov/v3/house-communication/117/ec/3324?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"house-communication\": {
                \"abstract\": \"A letter from the Chairman, Council of the District of Columbia,
    transmitting DC Act 24-299, \\"Closing of a Portion of a Public Alley in Square 5138, S.O. 20-07517,
    Act of 2021\\", pursuant to Public Law 93\u2013198, section 602(c)(1); (87 Stat. 814); to the
    Committee on Oversight and Reform.\",
                \"chamber\": \"House\",
                \"committees\": [
                    {
                        \"name\": \"Oversight and Accountability Committee\",
                        \"referralDate\": \"2022-02-01\"
                        \"systemCode\": \"hsgo00\",
                        \"url\": \"api.congress.gov/v3/committee/house/hsgo00
                    }
                ],
                \"communicationType\": {
                    \"code\": \"EC\",
                    \"name\": \"Executive Communication\"
                },
                \"congressNumber\": 117,
                \"congressionalRecordDate\": \"2022-02-01\"
                \"congressionalRecordDate\": \"2022-02-01\"
                \"isRulemaking\": \"False\",
                \"legalAuthority\": \"Public Law 93\u2013198, section 602(c)(1); (87 Stat. 814)\",
                \"matchingRequirements\": [
                    { {
                        \"number\": \"2120\",
                        \"url\": \"http://api.congress.gov/v3/house-requirement/2120\"
              }
                ],
                \"number\": \"3324\",
                \"reportNature\": \"DC Act 24-299, \\"Closing of a Portion of a Public Alley in Square
    5138, S.O. 20-07517, Act of 2021\\".\",
                \"sessionNumber\": 2,
                \"submittingAgency\": \"Council of the District of Columbia\",
                 \"submittingOfficial\": \"Chairman\",
                 \"updateDate\": \"2022-02-02\"
            },

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
    r"""Returns detailed information for a specified House communication.

     GET /house-communication/:congress/:communicationType/:communicationNumber

    **Example Request**

    https://api.congress.gov/v3/house-communication/117/ec/3324?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"house-communication\": {
                \"abstract\": \"A letter from the Chairman, Council of the District of Columbia,
    transmitting DC Act 24-299, \\"Closing of a Portion of a Public Alley in Square 5138, S.O. 20-07517,
    Act of 2021\\", pursuant to Public Law 93\u2013198, section 602(c)(1); (87 Stat. 814); to the
    Committee on Oversight and Reform.\",
                \"chamber\": \"House\",
                \"committees\": [
                    {
                        \"name\": \"Oversight and Accountability Committee\",
                        \"referralDate\": \"2022-02-01\"
                        \"systemCode\": \"hsgo00\",
                        \"url\": \"api.congress.gov/v3/committee/house/hsgo00
                    }
                ],
                \"communicationType\": {
                    \"code\": \"EC\",
                    \"name\": \"Executive Communication\"
                },
                \"congressNumber\": 117,
                \"congressionalRecordDate\": \"2022-02-01\"
                \"congressionalRecordDate\": \"2022-02-01\"
                \"isRulemaking\": \"False\",
                \"legalAuthority\": \"Public Law 93\u2013198, section 602(c)(1); (87 Stat. 814)\",
                \"matchingRequirements\": [
                    { {
                        \"number\": \"2120\",
                        \"url\": \"http://api.congress.gov/v3/house-requirement/2120\"
              }
                ],
                \"number\": \"3324\",
                \"reportNature\": \"DC Act 24-299, \\"Closing of a Portion of a Public Alley in Square
    5138, S.O. 20-07517, Act of 2021\\".\",
                \"sessionNumber\": 2,
                \"submittingAgency\": \"Council of the District of Columbia\",
                 \"submittingOfficial\": \"Chairman\",
                 \"updateDate\": \"2022-02-02\"
            },

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
