from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    *,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
    sort: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params["offset"] = offset

    params["limit"] = limit

    params["fromDateTime"] = from_date_time

    params["toDateTime"] = to_date_time

    params["sort"] = sort

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/summaries/{congress}",
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
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
    sort: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns a list of summaries filtered by congress, sorted by date of last update.

     GET /summaries/:congress

    **Example Request**

    https://api.congress.gov/v3/summaries/117?fromDateTime=2022-04-01T00:00:00Z&toDateTime=2022-04-
    03T00:00:00Z&sort=updateDate+desc&api_key=[INSERT_KEY]

    **Example Response**

        {
             \"summaries\": [
                {
                    \"actionDate\": \"2021-02-04\",
                    \"actionDesc\": \"Introduced in Senate\",
                    \"bill\": {
                        \"congress\": 117,
                        \"number\": \"225\",
                        \"originChamber\": \"Senate\",
                        \"originChamberCode\": \"S\",
                        \"title\": \"Competition and Antitrust Law Enforcement Reform Act of 2021\",
                        \"type\": \"S\",
                        \"updateDateIncludingText\": \"2022-09-29T03:41:41Z\",
                        \"url\": \"https://api.congress.gov/v3/bill/117/s/225?format=json\"
                    },
                    \"currentChamber\": \"Senate\",
                    \"currentChamberCode\": \"S\",
                    \"lastSummaryUpdateDate\": \"2022-03-31T15:20:50Z\",
                    \"text\": \" <p><strong>Competition and Antitrust Law Enforcement Reform Act of 2021
    </strong></p> <p>This bill revises antitrust laws applicable to mergers and anticompetitive conduct.
    </p> <p>Specifically, the bill applies a stricter standard for permissible mergers by prohibiting
    mergers that (1) create an appreciable risk of materially lessening competition, or (2) unfairly
    lower the prices of goods or wages because of a lack of competition among buyers or employers (i.e.,
    a monopsony). Under current law, mergers that substantially lessen competition are prohibited. </p>
    <p>Additionally, for some large mergers or mergers that concentrate markets beyond a certain
    threshold, the bill shifts the burden of proof to the merging parties to prove that the merger does
    not violate the law. </p> <p>The bill also prohibits exclusionary conduct that presents an
    appreciable risk of harming competition. </p> <p>The bill also establishes monetary penalties for
    violations, requires annual reporting for certain mergers and acquisitions, establishes within the
    Federal Trade Commission (FTC) the Office of the Competition Advocate, and sets forth whistleblower
    protections. </p> <p>The Government Accountability Office must report on (1) the success of merger
    remedies required by the Department of Justice or the FTC in recent consent decrees; and (2) the
    impact of mergers and acquisitions on wages, employment, innovation, and new business
    formation.</p>\",
                    \"updateDate\": \"2022-04-01T03:31:17Z\",
                    \"versionCode\": \"00\"
                },
                {
                    \"actionDate\": \"2022-03-24\",
                    \"actionDesc\": \"Introduced in Senate\",
                    \"bill\": {
                        \"congress\": 117,
                        \"number\": \"3914\",
                        \"originChamber\": \"Senate\",
                        \"originChamberCode\": \"S\",
                        \"title\": \"Developing and Empowering our Aspiring Leaders Act of 2022\",
                        \"type\": \"S\",
                        \"updateDateIncludingText\": \"2022-09-07T13:35:29Z\",
                        \"url\": \"https://api.congress.gov/v3/bill/117/s/3914?format=json\"
                    },
                    \"currentChamber\": \"Senate\",
                    \"currentChamberCode\": \"S\",
                    \"lastSummaryUpdateDate\": \"2022-03-31T17:52:12Z\",
                    \"text\": \" <p><strong>Developing and Empowering our Aspiring Leaders Act of 2022
    </strong> </p> <p>This bill directs the Securities and Exchange Commission to revise venture capital
    investment regulations. Venture capital funds are exempt from certain regulations applicable to
    other investment firms, including those related to filings, audits, and restricted communications
    with investors. Under current law, non-qualifying investments&#8212;which include secondary
    transactions and investments in other venture capital funds&#8212;may comprise up to 20% of a
    venture capital fund. </p> <p>The bill allows investments acquired through secondary transactions or
    investments in other venture capital funds to be considered as qualifying investments for venture
    capital funds. However, for a private fund to qualify as a venture capital fund, the fund's
    investments must predominately (1) be acquired directly, or (2) be investments in other venture
    capital funds.</p> <p>\",
                    \"updateDate\": \"2022-04-01T03:31:16Z\",
                    \"versionCode\": \"00\"
                },
            ],
        }

    Args:
        congress (int):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_date_time (Union[Unset, str]):
        to_date_time (Union[Unset, str]):
        sort (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        format_=format_,
        offset=offset,
        limit=limit,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
        sort=sort,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
    sort: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns a list of summaries filtered by congress, sorted by date of last update.

     GET /summaries/:congress

    **Example Request**

    https://api.congress.gov/v3/summaries/117?fromDateTime=2022-04-01T00:00:00Z&toDateTime=2022-04-
    03T00:00:00Z&sort=updateDate+desc&api_key=[INSERT_KEY]

    **Example Response**

        {
             \"summaries\": [
                {
                    \"actionDate\": \"2021-02-04\",
                    \"actionDesc\": \"Introduced in Senate\",
                    \"bill\": {
                        \"congress\": 117,
                        \"number\": \"225\",
                        \"originChamber\": \"Senate\",
                        \"originChamberCode\": \"S\",
                        \"title\": \"Competition and Antitrust Law Enforcement Reform Act of 2021\",
                        \"type\": \"S\",
                        \"updateDateIncludingText\": \"2022-09-29T03:41:41Z\",
                        \"url\": \"https://api.congress.gov/v3/bill/117/s/225?format=json\"
                    },
                    \"currentChamber\": \"Senate\",
                    \"currentChamberCode\": \"S\",
                    \"lastSummaryUpdateDate\": \"2022-03-31T15:20:50Z\",
                    \"text\": \" <p><strong>Competition and Antitrust Law Enforcement Reform Act of 2021
    </strong></p> <p>This bill revises antitrust laws applicable to mergers and anticompetitive conduct.
    </p> <p>Specifically, the bill applies a stricter standard for permissible mergers by prohibiting
    mergers that (1) create an appreciable risk of materially lessening competition, or (2) unfairly
    lower the prices of goods or wages because of a lack of competition among buyers or employers (i.e.,
    a monopsony). Under current law, mergers that substantially lessen competition are prohibited. </p>
    <p>Additionally, for some large mergers or mergers that concentrate markets beyond a certain
    threshold, the bill shifts the burden of proof to the merging parties to prove that the merger does
    not violate the law. </p> <p>The bill also prohibits exclusionary conduct that presents an
    appreciable risk of harming competition. </p> <p>The bill also establishes monetary penalties for
    violations, requires annual reporting for certain mergers and acquisitions, establishes within the
    Federal Trade Commission (FTC) the Office of the Competition Advocate, and sets forth whistleblower
    protections. </p> <p>The Government Accountability Office must report on (1) the success of merger
    remedies required by the Department of Justice or the FTC in recent consent decrees; and (2) the
    impact of mergers and acquisitions on wages, employment, innovation, and new business
    formation.</p>\",
                    \"updateDate\": \"2022-04-01T03:31:17Z\",
                    \"versionCode\": \"00\"
                },
                {
                    \"actionDate\": \"2022-03-24\",
                    \"actionDesc\": \"Introduced in Senate\",
                    \"bill\": {
                        \"congress\": 117,
                        \"number\": \"3914\",
                        \"originChamber\": \"Senate\",
                        \"originChamberCode\": \"S\",
                        \"title\": \"Developing and Empowering our Aspiring Leaders Act of 2022\",
                        \"type\": \"S\",
                        \"updateDateIncludingText\": \"2022-09-07T13:35:29Z\",
                        \"url\": \"https://api.congress.gov/v3/bill/117/s/3914?format=json\"
                    },
                    \"currentChamber\": \"Senate\",
                    \"currentChamberCode\": \"S\",
                    \"lastSummaryUpdateDate\": \"2022-03-31T17:52:12Z\",
                    \"text\": \" <p><strong>Developing and Empowering our Aspiring Leaders Act of 2022
    </strong> </p> <p>This bill directs the Securities and Exchange Commission to revise venture capital
    investment regulations. Venture capital funds are exempt from certain regulations applicable to
    other investment firms, including those related to filings, audits, and restricted communications
    with investors. Under current law, non-qualifying investments&#8212;which include secondary
    transactions and investments in other venture capital funds&#8212;may comprise up to 20% of a
    venture capital fund. </p> <p>The bill allows investments acquired through secondary transactions or
    investments in other venture capital funds to be considered as qualifying investments for venture
    capital funds. However, for a private fund to qualify as a venture capital fund, the fund's
    investments must predominately (1) be acquired directly, or (2) be investments in other venture
    capital funds.</p> <p>\",
                    \"updateDate\": \"2022-04-01T03:31:16Z\",
                    \"versionCode\": \"00\"
                },
            ],
        }

    Args:
        congress (int):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_date_time (Union[Unset, str]):
        to_date_time (Union[Unset, str]):
        sort (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        format_=format_,
        offset=offset,
        limit=limit,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
        sort=sort,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
