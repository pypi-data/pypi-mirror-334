from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    law_type: str,
    law_number: int,
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
        "url": f"/law/{congress}/{law_type}/{law_number}",
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
    law_type: str,
    law_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns a law filtered by specified congress, law type (public or private), and law number.

     GET /law/:congress/:lawType/:lawNumber

    **Example Request**

    https://api.congress.gov/v3/law/117/pub/108?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"bill\": {
                \"actions\": {
                    \"count\": 74,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/actions?format=json\"
                },
                \"amendments\": {
                    \"count\": 48,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/amendments?format=json\"
                },
                \"cboCostEstimates\": [
                    {
                        \"description\": \"As ordered reported by the House Committee on Oversight and
    Reform on May 13, 2021\n\",
                        \"pubDate\": \"2021-07-14T17:27:00Z\",
                        \"title\": \"H.R. 3076, Postal Service Reform Act of 2021\",
                        \"url\": \"https://www.cbo.gov/publication/57356\"
                    },
                    {
                        \"description\": \"As Posted on February 3, 2022,\nand as Amended by Amendment
    #1, the Manager's Amendment, as Posted on February 4, 2022\n\",
                        \"pubDate\": \"2022-02-04T18:03:00Z\",
                        \"title\": \"Estimated Budgetary Effects of Rules Committee Print 117-32 for
    H.R. 3076, the Postal Service Reform Act of 2022\",
                        \"url\": \"https://www.cbo.gov/publication/57821\"
                    }
                ],
                \"committeeReports\": [
                    {
                        \"citation\": \"H. Rept. 117-89,Part 1\",
                        \"url\": \"https://api.congress.gov/v3/committee-
    report/117/HRPT/89?format=json\"
                    },
                    {
                        \"citation\": \"H. Rept. 117-89,Part 2\",
                        \"url\": \"https://api.congress.gov/v3/committee-
    report/117/HRPT/89?format=json\"
                    }
                ],
                \"committees\": {
                    \"count\": 3,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/committees?format=json\"
                },
                \"congress\": 117,
                \"constitutionalAuthorityStatementText\": \"<pre>\n[Congressional Record Volume 167,
    Number 81 (Tuesday, May 11, 2021)]\n[House]\nFrom the Congressional Record Online through the
    Government Publishing Office [<a href=\\"https://www.gpo.gov\\">www.gpo.gov</a>]\nBy Mrs. CAROLYN B.
    MALONEY of New York:\nH.R. 3076.\nCongress has the power to enact this legislation pursuant\nto the
    following:\nArticle I, Section I, Clause 18 (Necessary and Proper\nClause)\n[Page H2195]\n</pre>\",
                \"cosponsors\": {
                    \"count\": 102,
                    \"countIncludingWithdrawnCosponsors\": 102,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/cosponsors?format=json\"
                },
                \"introducedDate\": \"2021-05-11\",
                \"latestAction\": {
                    \"actionDate\": \"2022-04-06\",
                    \"text\": \"Became Public Law No: 117-108.\"
                },
                \"laws\": [
                    {
                        \"number\": \"117-108\",
                        \"type\": \"Public Law\"
                    }
                ],
                \"number\": \"3076\",
                \"originChamber\": \"House\",
                \"policyArea\": {
                    \"name\": \"Government Operations and Politics\"
                },
                \"relatedBills\": {
                    \"count\": 4,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/relatedbills?format=json\"
                },
                \"sponsors\": [
                    {
                        \"bioguideId\": \"M000087\",
                        \"district\": 12,
                        \"firstName\": \"CAROLYN\",
                        \"fullName\": \"Rep. Maloney, Carolyn B. [D-NY-12]\",
                        \"isByRequest\": \"N\",
                        \"lastName\": \"MALONEY\",
                        \"middleName\": \"B.\",
                        \"party\": \"D\",
                        \"state\": \"NY\",
                        \"url\": \"https://api.congress.gov/v3/member/M000087?format=json\"
                    }
                ],
                \"subjects\": {
                    \"count\": 17,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/subjects?format=json\"
                },
                \"summaries\": {
                    \"count\": 5,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/summaries?format=json\"
                },
                \"textVersions\": {
                    \"count\": 7,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/text?format=json\"
                },
                \"title\": \"Postal Service Reform Act of 2022\",
                \"titles\": {
                    \"count\": 14,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/titles?format=json\"
                },
                \"type\": \"HR\",
                \"updateDate\": \"2022-09-29T03:27:05Z\",
                \"updateDateIncludingText\": \"2022-09-29T03:27:05Z\"
            },
        }

    Args:
        congress (int):
        law_type (str):
        law_number (int):
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
        law_type=law_type,
        law_number=law_number,
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
    law_type: str,
    law_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Any]:
    r"""Returns a law filtered by specified congress, law type (public or private), and law number.

     GET /law/:congress/:lawType/:lawNumber

    **Example Request**

    https://api.congress.gov/v3/law/117/pub/108?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"bill\": {
                \"actions\": {
                    \"count\": 74,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/actions?format=json\"
                },
                \"amendments\": {
                    \"count\": 48,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/amendments?format=json\"
                },
                \"cboCostEstimates\": [
                    {
                        \"description\": \"As ordered reported by the House Committee on Oversight and
    Reform on May 13, 2021\n\",
                        \"pubDate\": \"2021-07-14T17:27:00Z\",
                        \"title\": \"H.R. 3076, Postal Service Reform Act of 2021\",
                        \"url\": \"https://www.cbo.gov/publication/57356\"
                    },
                    {
                        \"description\": \"As Posted on February 3, 2022,\nand as Amended by Amendment
    #1, the Manager's Amendment, as Posted on February 4, 2022\n\",
                        \"pubDate\": \"2022-02-04T18:03:00Z\",
                        \"title\": \"Estimated Budgetary Effects of Rules Committee Print 117-32 for
    H.R. 3076, the Postal Service Reform Act of 2022\",
                        \"url\": \"https://www.cbo.gov/publication/57821\"
                    }
                ],
                \"committeeReports\": [
                    {
                        \"citation\": \"H. Rept. 117-89,Part 1\",
                        \"url\": \"https://api.congress.gov/v3/committee-
    report/117/HRPT/89?format=json\"
                    },
                    {
                        \"citation\": \"H. Rept. 117-89,Part 2\",
                        \"url\": \"https://api.congress.gov/v3/committee-
    report/117/HRPT/89?format=json\"
                    }
                ],
                \"committees\": {
                    \"count\": 3,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/committees?format=json\"
                },
                \"congress\": 117,
                \"constitutionalAuthorityStatementText\": \"<pre>\n[Congressional Record Volume 167,
    Number 81 (Tuesday, May 11, 2021)]\n[House]\nFrom the Congressional Record Online through the
    Government Publishing Office [<a href=\\"https://www.gpo.gov\\">www.gpo.gov</a>]\nBy Mrs. CAROLYN B.
    MALONEY of New York:\nH.R. 3076.\nCongress has the power to enact this legislation pursuant\nto the
    following:\nArticle I, Section I, Clause 18 (Necessary and Proper\nClause)\n[Page H2195]\n</pre>\",
                \"cosponsors\": {
                    \"count\": 102,
                    \"countIncludingWithdrawnCosponsors\": 102,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/cosponsors?format=json\"
                },
                \"introducedDate\": \"2021-05-11\",
                \"latestAction\": {
                    \"actionDate\": \"2022-04-06\",
                    \"text\": \"Became Public Law No: 117-108.\"
                },
                \"laws\": [
                    {
                        \"number\": \"117-108\",
                        \"type\": \"Public Law\"
                    }
                ],
                \"number\": \"3076\",
                \"originChamber\": \"House\",
                \"policyArea\": {
                    \"name\": \"Government Operations and Politics\"
                },
                \"relatedBills\": {
                    \"count\": 4,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/relatedbills?format=json\"
                },
                \"sponsors\": [
                    {
                        \"bioguideId\": \"M000087\",
                        \"district\": 12,
                        \"firstName\": \"CAROLYN\",
                        \"fullName\": \"Rep. Maloney, Carolyn B. [D-NY-12]\",
                        \"isByRequest\": \"N\",
                        \"lastName\": \"MALONEY\",
                        \"middleName\": \"B.\",
                        \"party\": \"D\",
                        \"state\": \"NY\",
                        \"url\": \"https://api.congress.gov/v3/member/M000087?format=json\"
                    }
                ],
                \"subjects\": {
                    \"count\": 17,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/subjects?format=json\"
                },
                \"summaries\": {
                    \"count\": 5,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/summaries?format=json\"
                },
                \"textVersions\": {
                    \"count\": 7,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/text?format=json\"
                },
                \"title\": \"Postal Service Reform Act of 2022\",
                \"titles\": {
                    \"count\": 14,
                    \"url\": \"https://api.congress.gov/v3/bill/117/hr/3076/titles?format=json\"
                },
                \"type\": \"HR\",
                \"updateDate\": \"2022-09-29T03:27:05Z\",
                \"updateDateIncludingText\": \"2022-09-29T03:27:05Z\"
            },
        }

    Args:
        congress (int):
        law_type (str):
        law_number (int):
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
        law_type=law_type,
        law_number=law_number,
        format_=format_,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
