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
        "url": f"/bill/{congress}/{bill_type}/{bill_number}/amendments",
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
    r"""Returns the list of amendments to a specified bill.

     GET /bill/:congress/:billType/:billNumber/amendments

    **Example Request**

    https://api.congress.gov/v3/bill/117/hr/3076/amendments?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"amendments\": [
                {
                    \"congress\": 117,
                    \"description\": \"An amendment numbered 1 printed in House Report 117-243 to
    clarifiy the roles and responsibilities of the Office of Personnel Management, the Social Security
    Administration, and the Centers for Medicare & Medicaid Services regarding the information postal
    employees will need to enroll in Medicare Part B; specify that performance standards must be
    submitted to the Postal Regulatory Commission for each product; and make other technical and
    conforming changes to the bill.\",
                    \"latestAction\": {
                        \"actionDate\": \"2022-02-08\",
                        \"actionTime\": \"15:39:53\",
                        \"text\": \"On agreeing to the Maloney, Carolyn B. amendment (A002) Agreed to by
    voice vote. \"
                    },
                    \"number\": \"173\",
                    \"type\": \"HAMDT\",
                    \"updateDate\": \"2022-02-18T16:38:41Z\",
                    \"url\": \"https://api.congress.gov/v3/amendment/117/hamdt/173?format=json\"
                },
                {
                    \"congress\": 117,
                    \"description\": \"Pursuant to the provisions of H. Res. 912, the amendment in the
    nature of a substitute consisting of the text of Rules Committee Print 117-32 is considered as
    adopted.\",
                    \"latestAction\": {
                        \"actionDate\": \"2022-02-08\",
                        \"text\": \"On agreeing to the Rules amendment (A001) Agreed to without
    objection. \"
                    },
                    \"number\": \"172\",
                    \"type\": \"HAMDT\",
                    \"updateDate\": \"2022-02-18T16:38:41Z\",
                    \"url\": \"https://api.congress.gov/v3/amendment/117/hamdt/172?format=json\"
                }
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
    r"""Returns the list of amendments to a specified bill.

     GET /bill/:congress/:billType/:billNumber/amendments

    **Example Request**

    https://api.congress.gov/v3/bill/117/hr/3076/amendments?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"amendments\": [
                {
                    \"congress\": 117,
                    \"description\": \"An amendment numbered 1 printed in House Report 117-243 to
    clarifiy the roles and responsibilities of the Office of Personnel Management, the Social Security
    Administration, and the Centers for Medicare & Medicaid Services regarding the information postal
    employees will need to enroll in Medicare Part B; specify that performance standards must be
    submitted to the Postal Regulatory Commission for each product; and make other technical and
    conforming changes to the bill.\",
                    \"latestAction\": {
                        \"actionDate\": \"2022-02-08\",
                        \"actionTime\": \"15:39:53\",
                        \"text\": \"On agreeing to the Maloney, Carolyn B. amendment (A002) Agreed to by
    voice vote. \"
                    },
                    \"number\": \"173\",
                    \"type\": \"HAMDT\",
                    \"updateDate\": \"2022-02-18T16:38:41Z\",
                    \"url\": \"https://api.congress.gov/v3/amendment/117/hamdt/173?format=json\"
                },
                {
                    \"congress\": 117,
                    \"description\": \"Pursuant to the provisions of H. Res. 912, the amendment in the
    nature of a substitute consisting of the text of Rules Committee Print 117-32 is considered as
    adopted.\",
                    \"latestAction\": {
                        \"actionDate\": \"2022-02-08\",
                        \"text\": \"On agreeing to the Rules amendment (A001) Agreed to without
    objection. \"
                    },
                    \"number\": \"172\",
                    \"type\": \"HAMDT\",
                    \"updateDate\": \"2022-02-18T16:38:41Z\",
                    \"url\": \"https://api.congress.gov/v3/amendment/117/hamdt/172?format=json\"
                }
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
