from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    report_type: str,
    report_number: int,
    *,
    format_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/committee-report/{congress}/{report_type}/{report_number}",
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
    report_type: str,
    report_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified committee report.

     GET /committee-report/:congress/:reportType/:reportNumber

    **Example Request**

    https://api.congress.gov/v3/committee-report/116/HRPT/617?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"committeeReports\": [
                {
                    \"associatedBill\": [
                        {
                            \"congress\": 116,
                            \"number\": \"6395\",
                            \"type\": \"HR\",
                            \"url\": \"https://api.congress.gov/v3/bill/116/hr/6395?format=json\"
                        }
                    ],
                    \"chamber\": \"House\",
                    \"citation\": \"H. Rept. 116-617\",
                    \"congress\": 116,
                    \"isConferenceReport\": true,
                    \"issueDate\": \"2020-12-03T05:00:00Z\",
                    \"number\": 617,
                    \"part\": 1,
                    \"reportType\": \"H.Rept.\",
                    \"sessionNumber\": 2,
                    \"text\": {
                      \"count\": 2,
                      \"url\": https://api.congress.gov/v3/committee-
    report/116/hrpt/617/text?format=json\"
                    },
                    \"title\": \"WILLIAM M. (MAC) THORNBERRY NATIONAL DEFENSE AUTHORIZATION ACT FOR
    FISCAL YEAR 2021\",
                    \"type\": \"HRPT\",
                    \"updateDate\": \"2022-05-20T16:27:57Z\"
                }
            ],
        }

    Args:
        congress (int):
        report_type (str):
        report_number (int):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        report_type=report_type,
        report_number=report_number,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    report_type: str,
    report_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified committee report.

     GET /committee-report/:congress/:reportType/:reportNumber

    **Example Request**

    https://api.congress.gov/v3/committee-report/116/HRPT/617?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"committeeReports\": [
                {
                    \"associatedBill\": [
                        {
                            \"congress\": 116,
                            \"number\": \"6395\",
                            \"type\": \"HR\",
                            \"url\": \"https://api.congress.gov/v3/bill/116/hr/6395?format=json\"
                        }
                    ],
                    \"chamber\": \"House\",
                    \"citation\": \"H. Rept. 116-617\",
                    \"congress\": 116,
                    \"isConferenceReport\": true,
                    \"issueDate\": \"2020-12-03T05:00:00Z\",
                    \"number\": 617,
                    \"part\": 1,
                    \"reportType\": \"H.Rept.\",
                    \"sessionNumber\": 2,
                    \"text\": {
                      \"count\": 2,
                      \"url\": https://api.congress.gov/v3/committee-
    report/116/hrpt/617/text?format=json\"
                    },
                    \"title\": \"WILLIAM M. (MAC) THORNBERRY NATIONAL DEFENSE AUTHORIZATION ACT FOR
    FISCAL YEAR 2021\",
                    \"type\": \"HRPT\",
                    \"updateDate\": \"2022-05-20T16:27:57Z\"
                }
            ],
        }

    Args:
        congress (int):
        report_type (str):
        report_number (int):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        report_type=report_type,
        report_number=report_number,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
