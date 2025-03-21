from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    amendment_type: str,
    amendment_number: int,
    *,
    format_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/amendment/{congress}/{amendment_type}/{amendment_number}",
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
    amendment_type: str,
    amendment_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified amendment.

     GET /amendment/:congress/:amendmentType/:amendmentNumber

    **Example Request**

    https://api.congress.gov/v3/amendment/117/samdt/2137?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"amendment\": {
                \"actions\": {
                    \"count\": 19,
                    \"url\":
    \"https://api.congress.gov/v3/amendment/117/samdt/2137/actions?format=json\"
                },
                \"amendedBill\": {
                    \"congress\": 117,
                    \"number\": \"3684\",
                    \"originChamber\": \"House\",
                    \"originChamberCode\": \"H\",
                    \"title\": \"Infrastructure Investment and Jobs Act\",
                    \"type\": \"HR\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3684?format=json\"
                },
                \"amendmentsToAmendment\": {
                     \"count\": 507,
                     \"url\":
    \"https://api.congress.gov/v3/amendment/117/samdt/2137/amendments?format=json\"
                },
                \"chamber\": \"Senate\",
                \"congress\": 117,
                \"cosponsors\": {
                    \"count\": 9,
                    \"countIncludingWithdrawnCosponsors\": 9,
                    \"url\":
    \"https://api.congress.gov/v3/amendment/117/samdt/2137/cosponsors?format=json\"
                },
                \"latestAction\": {
                    \"actionDate\": \"2021-08-08\",
                    \"text\": \"Amendment SA 2137 agreed to in Senate by Yea-Nay Vote. 69 - 28. Record
    Vote Number: 312.\"
                },
                \"number\": \"2137\",
                \"proposedDate\": \"2021-08-01T04:00:00Z\",
                \"purpose\": \"In the nature of a substitute.\",
                \"sponsors\": [
                    {
                        \"bioguideId\": \"S001191\",
                        \"firstName\": \"Kyrsten\",
                        \"fullName\": \"Sen. Sinema, Kyrsten [D-AZ]\",
                        \"lastName\": \"Sinema\",
                        \"url\": \"https://api.congress.gov/v3/member/S001191?format=json\"
                    }
                ],
                \"submittedDate\": \"2021-08-01T04:00:00Z\",
                \"type\": \"SAMDT\"
                \"updateDate\": \"2022-02-08T17:27:59Z\",
            }
        }

    Args:
        congress (int):
        amendment_type (str):
        amendment_number (int):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        amendment_type=amendment_type,
        amendment_number=amendment_number,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    amendment_type: str,
    amendment_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified amendment.

     GET /amendment/:congress/:amendmentType/:amendmentNumber

    **Example Request**

    https://api.congress.gov/v3/amendment/117/samdt/2137?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"amendment\": {
                \"actions\": {
                    \"count\": 19,
                    \"url\":
    \"https://api.congress.gov/v3/amendment/117/samdt/2137/actions?format=json\"
                },
                \"amendedBill\": {
                    \"congress\": 117,
                    \"number\": \"3684\",
                    \"originChamber\": \"House\",
                    \"originChamberCode\": \"H\",
                    \"title\": \"Infrastructure Investment and Jobs Act\",
                    \"type\": \"HR\",
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3684?format=json\"
                },
                \"amendmentsToAmendment\": {
                     \"count\": 507,
                     \"url\":
    \"https://api.congress.gov/v3/amendment/117/samdt/2137/amendments?format=json\"
                },
                \"chamber\": \"Senate\",
                \"congress\": 117,
                \"cosponsors\": {
                    \"count\": 9,
                    \"countIncludingWithdrawnCosponsors\": 9,
                    \"url\":
    \"https://api.congress.gov/v3/amendment/117/samdt/2137/cosponsors?format=json\"
                },
                \"latestAction\": {
                    \"actionDate\": \"2021-08-08\",
                    \"text\": \"Amendment SA 2137 agreed to in Senate by Yea-Nay Vote. 69 - 28. Record
    Vote Number: 312.\"
                },
                \"number\": \"2137\",
                \"proposedDate\": \"2021-08-01T04:00:00Z\",
                \"purpose\": \"In the nature of a substitute.\",
                \"sponsors\": [
                    {
                        \"bioguideId\": \"S001191\",
                        \"firstName\": \"Kyrsten\",
                        \"fullName\": \"Sen. Sinema, Kyrsten [D-AZ]\",
                        \"lastName\": \"Sinema\",
                        \"url\": \"https://api.congress.gov/v3/member/S001191?format=json\"
                    }
                ],
                \"submittedDate\": \"2021-08-01T04:00:00Z\",
                \"type\": \"SAMDT\"
                \"updateDate\": \"2022-02-08T17:27:59Z\",
            }
        }

    Args:
        congress (int):
        amendment_type (str):
        amendment_number (int):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        amendment_type=amendment_type,
        amendment_number=amendment_number,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
