from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    volume_number: str,
    issue_number: str,
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
        "url": f"/daily-congressional-record/{volume_number}/{issue_number}",
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
    volume_number: str,
    issue_number: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns a list of daily Congressional Records filtered by the specified volume number and specified
    issue number.

     GET /daily-congressional-record/:volumeNumber/:issueNumber

    **Example Request**

    https://api.congress.gov/v3/daily-congressional-record/168/153?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"issue\": [
                {
                    \"congress\": \"117\",
                    \"fullIssue\": \"2021-01-03T05:00:00Z\",
                        \"articles\": {
                            \"count\": 256,
                            \"url\": \"http://api.congress.gov/v3/daily-congressional-
    record/168/153/articles?format=json\",
                        },
                        \"entireIssue\": [
                            {
                                \"part\": \"1\",
                                \"type\": \"Formatted Text\",
                                \"url\":
    \"https://congress.gov/117/crec/2022/09/22/168/153/CREC-2022-09-22-pt1-PgD1015.htm\"
                            },
                            {
                               \"part\": \"1\",
                               \"type\": \"PDF\",
                               \"url\":
    \"https://congress.gov/117/crec/2022/09/22/168/153/CREC-2022-09-22.pdf\"
                            }
                          ],
                          \"sections\": [
                              {
                                \"endPage\": \"D1020\",
                                \"name\": \"Daily Digest\",
                                \"startPage\": \"D1015\",
                                \"text\": [
                                    {
                                        \"type\": \"PDF\",
                                        \"url\":
    \"https://congress.gov/117/crec/2022/09/22/168/153/CREC-2022-09-22-dailydigest.pdf\"
                                    },
                                    {
                                        \"type\": \"Formatted Text\",
                                        \"url\":
    \"https://congress.gov/117/crec/2022/09/22d22se2-1.htm\"
                                    }
                                ]
                              },
                              {
                                \"endPage\": \"E976\",
                                \"name\": \"Extension of Remarks Section\",
                                \"startPage\": \"E965\",
                                \"text\": [
                                    {
                                        \"part\": \"1\",
                                        \"type\": \"PDF\",
                                        \"url\":
    \"https://congress.gov/117/crec/2022/09/22/168/153/CREC-2022-09-22-extensions.pdf\"
                                    }
                                ]
                              }
                              {
                                 \"endPage\": \"E976\",
                                 \"name\": \"House Section\",
                                 \"startPage\": \"H8069\",
                                 \"text\": [
                                    {
                                        \"part\": \"1\",
                                        \"type\": \"PDF\",
                                        \"url\":
    https://congress.gov/117/crec/2022/09/22/168/153/CREC-2022-09-22-house.pdf
                                    }
                                 ]
                              }
                              {
                                 \"endPage\": \"E976\",
                                 \"name\": \"Senate Section\",
                                 \"startPage\": \"S4941\",
                                 \"text\": [
                                    {
                                        \"part\": \"1\",
                                        \"type\": \"PDF\",
                                        \"url\":
    https://congress.gov/117/crec/2022/09/22/168/153/CREC-2022-09-22-senate.pdf
                                    }
                                 ]
                              }
                          ]
                        }
                      ]
                    },
                    \"issueDate\": \"2022-09-22T04:00:00Z\",
                    \"issueNumber\": \"153\",
                    \"sessionNumber\": 2,
                    \"updateDate\": \"2022-09-23T12:00:14Z\",
                    \"url\": \"http://api.congress.gov/v3/daily-congressional-
    record/168/153?format=json\",
                    \"volumeNumber\": 168
             },
                \"request\": {
                \"contentType\": \"application/json\",
                \"format\": \"json\",
                \"issueNumber\": \"153\",
                \"volumeNumber\": \"168\"
              }
        }

    Args:
        volume_number (str):
        issue_number (str):
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
        volume_number=volume_number,
        issue_number=issue_number,
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    volume_number: str,
    issue_number: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns a list of daily Congressional Records filtered by the specified volume number and specified
    issue number.

     GET /daily-congressional-record/:volumeNumber/:issueNumber

    **Example Request**

    https://api.congress.gov/v3/daily-congressional-record/168/153?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"issue\": [
                {
                    \"congress\": \"117\",
                    \"fullIssue\": \"2021-01-03T05:00:00Z\",
                        \"articles\": {
                            \"count\": 256,
                            \"url\": \"http://api.congress.gov/v3/daily-congressional-
    record/168/153/articles?format=json\",
                        },
                        \"entireIssue\": [
                            {
                                \"part\": \"1\",
                                \"type\": \"Formatted Text\",
                                \"url\":
    \"https://congress.gov/117/crec/2022/09/22/168/153/CREC-2022-09-22-pt1-PgD1015.htm\"
                            },
                            {
                               \"part\": \"1\",
                               \"type\": \"PDF\",
                               \"url\":
    \"https://congress.gov/117/crec/2022/09/22/168/153/CREC-2022-09-22.pdf\"
                            }
                          ],
                          \"sections\": [
                              {
                                \"endPage\": \"D1020\",
                                \"name\": \"Daily Digest\",
                                \"startPage\": \"D1015\",
                                \"text\": [
                                    {
                                        \"type\": \"PDF\",
                                        \"url\":
    \"https://congress.gov/117/crec/2022/09/22/168/153/CREC-2022-09-22-dailydigest.pdf\"
                                    },
                                    {
                                        \"type\": \"Formatted Text\",
                                        \"url\":
    \"https://congress.gov/117/crec/2022/09/22d22se2-1.htm\"
                                    }
                                ]
                              },
                              {
                                \"endPage\": \"E976\",
                                \"name\": \"Extension of Remarks Section\",
                                \"startPage\": \"E965\",
                                \"text\": [
                                    {
                                        \"part\": \"1\",
                                        \"type\": \"PDF\",
                                        \"url\":
    \"https://congress.gov/117/crec/2022/09/22/168/153/CREC-2022-09-22-extensions.pdf\"
                                    }
                                ]
                              }
                              {
                                 \"endPage\": \"E976\",
                                 \"name\": \"House Section\",
                                 \"startPage\": \"H8069\",
                                 \"text\": [
                                    {
                                        \"part\": \"1\",
                                        \"type\": \"PDF\",
                                        \"url\":
    https://congress.gov/117/crec/2022/09/22/168/153/CREC-2022-09-22-house.pdf
                                    }
                                 ]
                              }
                              {
                                 \"endPage\": \"E976\",
                                 \"name\": \"Senate Section\",
                                 \"startPage\": \"S4941\",
                                 \"text\": [
                                    {
                                        \"part\": \"1\",
                                        \"type\": \"PDF\",
                                        \"url\":
    https://congress.gov/117/crec/2022/09/22/168/153/CREC-2022-09-22-senate.pdf
                                    }
                                 ]
                              }
                          ]
                        }
                      ]
                    },
                    \"issueDate\": \"2022-09-22T04:00:00Z\",
                    \"issueNumber\": \"153\",
                    \"sessionNumber\": 2,
                    \"updateDate\": \"2022-09-23T12:00:14Z\",
                    \"url\": \"http://api.congress.gov/v3/daily-congressional-
    record/168/153?format=json\",
                    \"volumeNumber\": 168
             },
                \"request\": {
                \"contentType\": \"application/json\",
                \"format\": \"json\",
                \"issueNumber\": \"153\",
                \"volumeNumber\": \"168\"
              }
        }

    Args:
        volume_number (str):
        issue_number (str):
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
        volume_number=volume_number,
        issue_number=issue_number,
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
