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
        "url": f"/bill/{congress}/{bill_type}/{bill_number}/summaries",
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
    r"""Returns the list of summaries for a specified bill.

     GET /bill/:congress/:billType/:billNumber/summaries

    **Example Request**

    https://api.congress.gov/v3/bill/117/hr/3076/summaries?api_key=[INSERT_KEY]

    **Example Response**

        {
          \"summaries\": [
                {
                    \"actionDate\": \"2022-03-08\",
                    \"actionDesc\": \"Passed Senate\",
                    \"text\": \" <p><strong>Postal Service Reform Act of
    202</strong><strong>2</strong></p> <p>This bill addresses the finances and operations of the U.S.
    Postal Service (USPS).</p> <p>The bill requires the Office of Personnel Management (OPM) to
    establish the Postal Service Health Benefits Program within the Federal Employees Health Benefits
    Program under which OPM may contract with carriers to offer health benefits plans for USPS employees
    and retirees.</p> <p>The bill provides for coordinated enrollment of retirees under this program and
    Medicare.</p> <p>The bill repeals the requirement that the USPS annually prepay future retirement
    health benefits.</p> <p>Additionally, the USPS may establish a program to enter into agreements with
    an agency of any state government, local government, or tribal government, and with other government
    agencies, to provide certain nonpostal products and services that reasonably contribute to the costs
    of the USPS and meet other specified criteria.</p> <p>The USPS must develop and maintain a publicly
    available dashboard to track service performance and must report regularly on its operations and
    financial condition.</p> <p>The Postal Regulatory Commission must annually submit to the USPS a
    budget of its expenses. It must also conduct a study to identify the causes and effects of postal
    inefficiencies relating to flats (e.g., large envelopes).</p> <p>The USPS Office of Inspector
    General shall perform oversight of the Postal Regulatory Commission. </p>\",
                    \"updateDate\": \"2022-03-14T18:17:02Z\",
                    \"versionCode\": \"55\"
                },
                {
                    \"actionDate\": \"2022-04-06\",
                    \"actionDesc\": \"Public Law\",
                    \"text\": \" <p><strong>Postal Service Reform Act of
    202</strong><strong>2</strong></p> <p>This bill addresses the finances and operations of the U.S.
    Postal Service (USPS).</p> <p>The bill requires the Office of Personnel Management (OPM) to
    establish the Postal Service Health Benefits Program within the Federal Employees Health Benefits
    Program under which OPM may contract with carriers to offer health benefits plans for USPS employees
    and retirees.</p> <p>The bill provides for coordinated enrollment of retirees under this program and
    Medicare.</p> <p>The bill repeals the requirement that the USPS annually prepay future retirement
    health benefits.</p> <p>Additionally, the USPS may establish a program to enter into agreements with
    an agency of any state government, local government, or tribal government, and with other government
    agencies, to provide certain nonpostal products and services that reasonably contribute to the costs
    of the USPS and meet other specified criteria.</p> <p>The USPS must develop and maintain a publicly
    available dashboard to track service performance and must report regularly on its operations and
    financial condition.</p> <p>The Postal Regulatory Commission must annually submit to the USPS a
    budget of its expenses. It must also conduct a study to identify the causes and effects of postal
    inefficiencies relating to flats (e.g., large envelopes).</p> <p>The USPS Office of Inspector
    General shall perform oversight of the Postal Regulatory Commission. </p>\",
                    \"updateDate\": \"2022-04-11T14:35:39Z\",
                    \"versionCode\": \"49\"
                }
            ]
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
    r"""Returns the list of summaries for a specified bill.

     GET /bill/:congress/:billType/:billNumber/summaries

    **Example Request**

    https://api.congress.gov/v3/bill/117/hr/3076/summaries?api_key=[INSERT_KEY]

    **Example Response**

        {
          \"summaries\": [
                {
                    \"actionDate\": \"2022-03-08\",
                    \"actionDesc\": \"Passed Senate\",
                    \"text\": \" <p><strong>Postal Service Reform Act of
    202</strong><strong>2</strong></p> <p>This bill addresses the finances and operations of the U.S.
    Postal Service (USPS).</p> <p>The bill requires the Office of Personnel Management (OPM) to
    establish the Postal Service Health Benefits Program within the Federal Employees Health Benefits
    Program under which OPM may contract with carriers to offer health benefits plans for USPS employees
    and retirees.</p> <p>The bill provides for coordinated enrollment of retirees under this program and
    Medicare.</p> <p>The bill repeals the requirement that the USPS annually prepay future retirement
    health benefits.</p> <p>Additionally, the USPS may establish a program to enter into agreements with
    an agency of any state government, local government, or tribal government, and with other government
    agencies, to provide certain nonpostal products and services that reasonably contribute to the costs
    of the USPS and meet other specified criteria.</p> <p>The USPS must develop and maintain a publicly
    available dashboard to track service performance and must report regularly on its operations and
    financial condition.</p> <p>The Postal Regulatory Commission must annually submit to the USPS a
    budget of its expenses. It must also conduct a study to identify the causes and effects of postal
    inefficiencies relating to flats (e.g., large envelopes).</p> <p>The USPS Office of Inspector
    General shall perform oversight of the Postal Regulatory Commission. </p>\",
                    \"updateDate\": \"2022-03-14T18:17:02Z\",
                    \"versionCode\": \"55\"
                },
                {
                    \"actionDate\": \"2022-04-06\",
                    \"actionDesc\": \"Public Law\",
                    \"text\": \" <p><strong>Postal Service Reform Act of
    202</strong><strong>2</strong></p> <p>This bill addresses the finances and operations of the U.S.
    Postal Service (USPS).</p> <p>The bill requires the Office of Personnel Management (OPM) to
    establish the Postal Service Health Benefits Program within the Federal Employees Health Benefits
    Program under which OPM may contract with carriers to offer health benefits plans for USPS employees
    and retirees.</p> <p>The bill provides for coordinated enrollment of retirees under this program and
    Medicare.</p> <p>The bill repeals the requirement that the USPS annually prepay future retirement
    health benefits.</p> <p>Additionally, the USPS may establish a program to enter into agreements with
    an agency of any state government, local government, or tribal government, and with other government
    agencies, to provide certain nonpostal products and services that reasonably contribute to the costs
    of the USPS and meet other specified criteria.</p> <p>The USPS must develop and maintain a publicly
    available dashboard to track service performance and must report regularly on its operations and
    financial condition.</p> <p>The Postal Regulatory Commission must annually submit to the USPS a
    budget of its expenses. It must also conduct a study to identify the causes and effects of postal
    inefficiencies relating to flats (e.g., large envelopes).</p> <p>The USPS Office of Inspector
    General shall perform oversight of the Postal Regulatory Commission. </p>\",
                    \"updateDate\": \"2022-04-11T14:35:39Z\",
                    \"versionCode\": \"49\"
                }
            ]
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
