from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    treaty_number: int,
    *,
    format_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/treaty/{congress}/{treaty_number}",
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
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified treaty.

     GET /treaty/:congress/:treatyNumber

    **Example Request**

    https://api.congress.gov/v3/treaty/117/3?api_key=[INSERT_KEY]

    **Example Response**

          {

              \"request\": {
              \"congress\": \"116\",
              \"contentType\": \"application/json\",
              \"format\": \"json\"
          },
              \"treaty\": {
                 \"actions\": {
                    \"count\": 18,
                    \"url\": \"http://api.congress.gov/v3/treaty/116/1/actions?format=json\"
                  },
                   \"congressConsidered\": 116,
                   \"congressReceived\": 116,
                   \"countriesParties\": [
                       {
                          \"name\": \"North Macedonia, The Republic of\"
                       }
                    ],
                    \"inForceDate\": null,
                    \"indexTerms\": [
                        {
                          \"name\": \"116-1\"
                        },
                        {
                          \"name\": \"Accession\"
                        },
                        {
                          \"name\": \"North Atlantic Treaty of 1949\"
                        },
                        {
                          \"name\": \"North Macedonia\"
                        },
                        {
                          \"name\": \"North Macedonia, The Republic of\"
                        },
                        {
                          \"name\": \"TD116-1\"
                        },
                        {
                          \"name\": \"The Republic of North Macedonia\"
                        },
                        {
                          \"name\": \"Ex. Rept. 116-5\"
                        }
                    ],
                    \"number\": 1,
                    \"oldNumber\": null,
                    \"oldNumberDisplayName\": null,
                    \"parts\": {},
                    \"relatedDocs\":
                      {
                          \"citation\": \"Ex. Rept. 116-5\",
                          \"url\": \"http://api.congress.gov/v3/committee-report/116/ERPT/5\"
                      }
                  ],
                  \"resolutionText\": \"<!DOCTYPE html><html xmlns=\\"http://www.w3.org/1999/xhtml\\"
    lang=\\"en\\"><head><meta name=\\"meta:creation-date\\" content=\\"2022/08/03 18:28:08\\" /><meta
    name=\\"dc:title\\" content=\\"[117] TreatyRes. 6 for TreatyDoc. 117 - 3\\" /><meta
    name=\\"Creation-Date\\" content=\\"2022/08/03 18:28:08\\" /><meta name=\\"dcterms:created\\"
    content=\\"2022/08/03 18:28:08\\" /><meta name=\\"Content-Type\\" content=\\"application/rtf\\"
    /><title>[117] TreatyRes. 6 for TreatyDoc. 117 - 3</title></head><body><p>As approved by the Senate:
    </p><p><i>Resolved (two-thirds of the Senators present concurring
    therein),</i></p><p></p><p><b>SECTION 1. SENATE ADVICE AND CONSENT SUBJECT TO DECLARATIONS AND
    CONDITIONS.</b></p>...\",
                  \"suffix\": \"\",
                  \"titles\": [
                      {
                          \"title\": \"Protocol to the North Atlantic Treaty of 1949 on the Accession of
    the Republic of North Macedonia\",
                          \"titleType\": \"Treaty - Short Title\"
                      },
                      {
                          \"title\": \"Protocol to the North Atlantic Treaty of 1949 on the Accession of
    the Republic of North Macedonia\",
                          \"titleType\": \"Treaty - Formal Title\"
                      }
                  ],
                  \"topic\": \"International Law and Organization\",
                  \"transmittedDate\": \"2022-07-11T00:00:00Z\",
                  \"updateDate\": \"2022-08-04T02:46:11Z\",
                }
            ]
        }

    Args:
        congress (int):
        treaty_number (int):
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
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    treaty_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified treaty.

     GET /treaty/:congress/:treatyNumber

    **Example Request**

    https://api.congress.gov/v3/treaty/117/3?api_key=[INSERT_KEY]

    **Example Response**

          {

              \"request\": {
              \"congress\": \"116\",
              \"contentType\": \"application/json\",
              \"format\": \"json\"
          },
              \"treaty\": {
                 \"actions\": {
                    \"count\": 18,
                    \"url\": \"http://api.congress.gov/v3/treaty/116/1/actions?format=json\"
                  },
                   \"congressConsidered\": 116,
                   \"congressReceived\": 116,
                   \"countriesParties\": [
                       {
                          \"name\": \"North Macedonia, The Republic of\"
                       }
                    ],
                    \"inForceDate\": null,
                    \"indexTerms\": [
                        {
                          \"name\": \"116-1\"
                        },
                        {
                          \"name\": \"Accession\"
                        },
                        {
                          \"name\": \"North Atlantic Treaty of 1949\"
                        },
                        {
                          \"name\": \"North Macedonia\"
                        },
                        {
                          \"name\": \"North Macedonia, The Republic of\"
                        },
                        {
                          \"name\": \"TD116-1\"
                        },
                        {
                          \"name\": \"The Republic of North Macedonia\"
                        },
                        {
                          \"name\": \"Ex. Rept. 116-5\"
                        }
                    ],
                    \"number\": 1,
                    \"oldNumber\": null,
                    \"oldNumberDisplayName\": null,
                    \"parts\": {},
                    \"relatedDocs\":
                      {
                          \"citation\": \"Ex. Rept. 116-5\",
                          \"url\": \"http://api.congress.gov/v3/committee-report/116/ERPT/5\"
                      }
                  ],
                  \"resolutionText\": \"<!DOCTYPE html><html xmlns=\\"http://www.w3.org/1999/xhtml\\"
    lang=\\"en\\"><head><meta name=\\"meta:creation-date\\" content=\\"2022/08/03 18:28:08\\" /><meta
    name=\\"dc:title\\" content=\\"[117] TreatyRes. 6 for TreatyDoc. 117 - 3\\" /><meta
    name=\\"Creation-Date\\" content=\\"2022/08/03 18:28:08\\" /><meta name=\\"dcterms:created\\"
    content=\\"2022/08/03 18:28:08\\" /><meta name=\\"Content-Type\\" content=\\"application/rtf\\"
    /><title>[117] TreatyRes. 6 for TreatyDoc. 117 - 3</title></head><body><p>As approved by the Senate:
    </p><p><i>Resolved (two-thirds of the Senators present concurring
    therein),</i></p><p></p><p><b>SECTION 1. SENATE ADVICE AND CONSENT SUBJECT TO DECLARATIONS AND
    CONDITIONS.</b></p>...\",
                  \"suffix\": \"\",
                  \"titles\": [
                      {
                          \"title\": \"Protocol to the North Atlantic Treaty of 1949 on the Accession of
    the Republic of North Macedonia\",
                          \"titleType\": \"Treaty - Short Title\"
                      },
                      {
                          \"title\": \"Protocol to the North Atlantic Treaty of 1949 on the Accession of
    the Republic of North Macedonia\",
                          \"titleType\": \"Treaty - Formal Title\"
                      }
                  ],
                  \"topic\": \"International Law and Organization\",
                  \"transmittedDate\": \"2022-07-11T00:00:00Z\",
                  \"updateDate\": \"2022-08-04T02:46:11Z\",
                }
            ]
        }

    Args:
        congress (int):
        treaty_number (int):
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
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
