from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    chamber: str,
    jacket_number: int,
    *,
    format_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/hearing/{congress}/{chamber}/{jacket_number}",
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
    chamber: str,
    jacket_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified hearing.

     GET /hearing/:congress/:chamber/:jacketNumber

    **Example Request**

    https://api.congress.gov/v3/hearing/116/house/41365?api_key=[INSERT_KEY]

    **Example Response**

          {
              \"hearing\": {
                  \"associatedMeeting\": {
                      \"eventId\": \"110484\"
                      \"url\": \"http://api.congress.gov/v3/committee-
    meeting/116/house/110484?format=xml\"
                  },
                  \"chamber\": \"House\",
                  \"citation\": \"H.Hrg.116\",
                  \"committees\": [
                      {
                          \"name\": \"House Agriculture Committee\",
                          \"systemCode\": \"hsag00\",
                          \"url\": \"https://api.congress.gov/v3/committee/house/hsag00?format=json\"
                      }
                  ],
                  \"congress\": 116,
                  \"dates\": [
                      {
                          \"date\": \"2020-02-11\"
                      }
                  ],
                  \"formats\": [
                      {
                          \"type\": \"Formatted Text\",
                          \"url\":
    \"https://www.congress.gov/116/chrg/CHRG-116hhrg41365/CHRG-116hhrg41365.htm\"
                      },
                      {
                          \"type\": \"PDF\",
                          \"url\":
    \"https://www.congress.gov/116/chrg/CHRG-116hhrg41365/CHRG-116hhrg41365.pdf\"
                      }
                  ],
                  \"jacketNumber\": 41365,
                  \"libraryOfCongressIdentifier\": \"LC65344\",
                  \"title\": \"ECONOMIC OPPORTUNITIES FROM LOCAL AGRICULTURAL MARKETS\",
                  \"updateDate\": \"2022-06-30 03:50:43+00:00\"
              },
          }

    Args:
        congress (int):
        chamber (str):
        jacket_number (int):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        chamber=chamber,
        jacket_number=jacket_number,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    chamber: str,
    jacket_number: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified hearing.

     GET /hearing/:congress/:chamber/:jacketNumber

    **Example Request**

    https://api.congress.gov/v3/hearing/116/house/41365?api_key=[INSERT_KEY]

    **Example Response**

          {
              \"hearing\": {
                  \"associatedMeeting\": {
                      \"eventId\": \"110484\"
                      \"url\": \"http://api.congress.gov/v3/committee-
    meeting/116/house/110484?format=xml\"
                  },
                  \"chamber\": \"House\",
                  \"citation\": \"H.Hrg.116\",
                  \"committees\": [
                      {
                          \"name\": \"House Agriculture Committee\",
                          \"systemCode\": \"hsag00\",
                          \"url\": \"https://api.congress.gov/v3/committee/house/hsag00?format=json\"
                      }
                  ],
                  \"congress\": 116,
                  \"dates\": [
                      {
                          \"date\": \"2020-02-11\"
                      }
                  ],
                  \"formats\": [
                      {
                          \"type\": \"Formatted Text\",
                          \"url\":
    \"https://www.congress.gov/116/chrg/CHRG-116hhrg41365/CHRG-116hhrg41365.htm\"
                      },
                      {
                          \"type\": \"PDF\",
                          \"url\":
    \"https://www.congress.gov/116/chrg/CHRG-116hhrg41365/CHRG-116hhrg41365.pdf\"
                      }
                  ],
                  \"jacketNumber\": 41365,
                  \"libraryOfCongressIdentifier\": \"LC65344\",
                  \"title\": \"ECONOMIC OPPORTUNITIES FROM LOCAL AGRICULTURAL MARKETS\",
                  \"updateDate\": \"2022-06-30 03:50:43+00:00\"
              },
          }

    Args:
        congress (int):
        chamber (str):
        jacket_number (int):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        chamber=chamber,
        jacket_number=jacket_number,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
