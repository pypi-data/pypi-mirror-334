from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    treaty_number: int,
    treaty_suffix: str,
    *,
    format_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/treaty/{congress}/{treaty_number}/{treaty_suffix}",
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
    treaty_number: int,
    treaty_suffix: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified partitioned treaty.

     GET /treaty/:congress/:treatyNumber/:treatySuffix

    **Example Request**

    https://api.congress.gov/v3/treaty/114/13/A?api_key=[INSERT_KEY]

    **Example Response**

          {
              \"treaty\": {
                    \"actions\": {
                      \"count\": 5,
                      \"url\": \"https://api.congress.gov/v3/treaty/114/13/A/actions?format=json\"
                  },
                    \"congressConsidered\": 115,
                    \"congressReceived\": 114,
                    \"countriesParties\": [
                        {
                            \"name\": \"Micronesia, Federated States of\"
                        }
                    ]
                    \"inForceDate\": null,
                    \"indexTerms\": [
                        {
                           \"name\": \"Maritime\"
                        },
                        {
                           \"name\": \"Micronesia\"
                        },
                        {
                            \"name\": \"Pacific\"
                        }
                    ],
                    \"number\": 13
                    \"oldNumber\": null,
                    \"oldNumberDisplayName\": null,
                    \"parts\": {
                      \"count\": 2,
                      \"urls\": [
                        \"https://api.congress.gov/v3/treaty/114/13/B?format=json\",
                        \"https://api.congress.gov/v3/treaty/114/13?format=json\"
                        ]
                      },
                    \"relatedDocs\": [],
                    \"resolutionText\": \"<!DOCTYPE html><html xmlns=\"http://www.w3.org/1999/xhtml\"
    lang=\"en\"><head><meta name=\"dc:title\" content=\"[115] TreatyRes. 3 for TreatyDoc. 114 - 13A\"
    /><meta name=\"Content-Type\" content=\"application/rtf\" /><title>[115] TreatyRes. 3 for TreatyDoc.
    114 - 13A</title></head><body><p><i>As approved by the Senate: </i></p><p></p><p>Resolved, (two-
    thirds of the Senators present concurring therein),</p><p><b>SECTION 1. SENATE ADVICE AND CONSENT
    SUBJECT TO A DECLARATION.</b></p><p>The Senate advises and consents to the ratification of the
    Treaty between the Government of the United States of America and the Government of the Republic of
    Kiribati on the Delimitation of Maritime Boundaries, signed at Majuro on September 6, 2013 (the
    \"Treaty\") (Treaty Doc 114-13B), subject to the declaration in section 2.</p><p><b>SEC. 2.
    DECLARATION.</b></p><p>The Senate&rsquo;s advice and consent under section 1 is subject to the
    following declaration: The Treaty is self-executing.</p><p></p><p></p></body></html>\",
                    \"suffix\": \"A\",
                    \"titles\": [
                        {
                            \"title\": \"Treaty between the Government of the United States of America
    and the Government of the Federated States of Micronesia on the Delimitation of a Maritime Boundary,
    signed at Koror on August 1, 2014.\",
                            \"titleType\": \"Treaty - Formal Title\"
                        },
                        {
                            \"title\": \"The Treaty with the Federated States of Micronesia on the
    Delimitation of a Maritime Boundary\",
                            \"titleType\": \"Treaty - Short Title\"
                        }
                    ],
                    \"transmittedDate\": \"2016-12-09T00:00:00Z\",
                    \"treatyNum\": 13,
                    \"topic\": \"Maritime Boundaries and Claims\",
                    \"updateDate\": \"2022-07-12T15:48:45Z\"
                  }
          }

    Args:
        congress (int):
        treaty_number (int):
        treaty_suffix (str):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        treaty_number=treaty_number,
        treaty_suffix=treaty_suffix,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    treaty_number: int,
    treaty_suffix: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified partitioned treaty.

     GET /treaty/:congress/:treatyNumber/:treatySuffix

    **Example Request**

    https://api.congress.gov/v3/treaty/114/13/A?api_key=[INSERT_KEY]

    **Example Response**

          {
              \"treaty\": {
                    \"actions\": {
                      \"count\": 5,
                      \"url\": \"https://api.congress.gov/v3/treaty/114/13/A/actions?format=json\"
                  },
                    \"congressConsidered\": 115,
                    \"congressReceived\": 114,
                    \"countriesParties\": [
                        {
                            \"name\": \"Micronesia, Federated States of\"
                        }
                    ]
                    \"inForceDate\": null,
                    \"indexTerms\": [
                        {
                           \"name\": \"Maritime\"
                        },
                        {
                           \"name\": \"Micronesia\"
                        },
                        {
                            \"name\": \"Pacific\"
                        }
                    ],
                    \"number\": 13
                    \"oldNumber\": null,
                    \"oldNumberDisplayName\": null,
                    \"parts\": {
                      \"count\": 2,
                      \"urls\": [
                        \"https://api.congress.gov/v3/treaty/114/13/B?format=json\",
                        \"https://api.congress.gov/v3/treaty/114/13?format=json\"
                        ]
                      },
                    \"relatedDocs\": [],
                    \"resolutionText\": \"<!DOCTYPE html><html xmlns=\"http://www.w3.org/1999/xhtml\"
    lang=\"en\"><head><meta name=\"dc:title\" content=\"[115] TreatyRes. 3 for TreatyDoc. 114 - 13A\"
    /><meta name=\"Content-Type\" content=\"application/rtf\" /><title>[115] TreatyRes. 3 for TreatyDoc.
    114 - 13A</title></head><body><p><i>As approved by the Senate: </i></p><p></p><p>Resolved, (two-
    thirds of the Senators present concurring therein),</p><p><b>SECTION 1. SENATE ADVICE AND CONSENT
    SUBJECT TO A DECLARATION.</b></p><p>The Senate advises and consents to the ratification of the
    Treaty between the Government of the United States of America and the Government of the Republic of
    Kiribati on the Delimitation of Maritime Boundaries, signed at Majuro on September 6, 2013 (the
    \"Treaty\") (Treaty Doc 114-13B), subject to the declaration in section 2.</p><p><b>SEC. 2.
    DECLARATION.</b></p><p>The Senate&rsquo;s advice and consent under section 1 is subject to the
    following declaration: The Treaty is self-executing.</p><p></p><p></p></body></html>\",
                    \"suffix\": \"A\",
                    \"titles\": [
                        {
                            \"title\": \"Treaty between the Government of the United States of America
    and the Government of the Federated States of Micronesia on the Delimitation of a Maritime Boundary,
    signed at Koror on August 1, 2014.\",
                            \"titleType\": \"Treaty - Formal Title\"
                        },
                        {
                            \"title\": \"The Treaty with the Federated States of Micronesia on the
    Delimitation of a Maritime Boundary\",
                            \"titleType\": \"Treaty - Short Title\"
                        }
                    ],
                    \"transmittedDate\": \"2016-12-09T00:00:00Z\",
                    \"treatyNum\": 13,
                    \"topic\": \"Maritime Boundaries and Claims\",
                    \"updateDate\": \"2022-07-12T15:48:45Z\"
                  }
          }

    Args:
        congress (int):
        treaty_number (int):
        treaty_suffix (str):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        treaty_number=treaty_number,
        treaty_suffix=treaty_suffix,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
