from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: str,
    *,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    current_member: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params["offset"] = offset

    params["limit"] = limit

    params["currentMember"] = current_member

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/member/congress/{congress}",
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
    congress: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    current_member: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns the list of members specified by Congress

     GET /member/congress/:congress

    **Example Request**

    https://api.congress.gov/v3/member/congress/118?api_key=[INSERT_KEY]

    **Example Request for a previous Congress**

    https://api.congress.gov/v3/member/congress/117?currentMember=False&api_key=[INSERT_KEY]

    **Example Response**

        {
            \"members\": [
            {
                \"bioguideId\": \"B001320\",
                \"depiction\": {
                    \"attribution\": \"Image courtesy of the Senator's office\",
                    \"imageUrl\": \"https://www.congress.gov/img/member/b001320_200.jpg\"
            },
                \"name\": \"Butler, Laphonza R.\",
                \"partyName\": \"Democratic\",
                \"state\": \"California\",
                \"terms\": {
                    \"item\": [
                        {
                            \"chamber\": \"Senate\",
                            \"startYear\": 2023
                        }
                    ]
                },
                \"updateDate\": \"2024-04-09T15:54:25Z\",
                \"url\": \"http://api.congress.gov/v3/member/B001320?format=json\"
            },
            {
                 \"bioguideId\": \"A000376\",
                 \"depiction\": {
                     \"attribution\": \"Image courtesy of the Member\",
                     \"imageUrl\": \"https://www.congress.gov/img/member/a000376_200.jpg\"
            },
                  \"district\": 32,
                  \"name\": \"Allred, Colin Z.\",
                  \"partyName\": \"Democratic\",
                  \"state\": \"Texas\",
                  \"terms\": {
                      \"item\": [
                          {
                              \"chamber\": \"House of Representatives\",
                              \"startYear\": 2019
                          }
                      ]
                  },
                 \"updateDate\": \"2024-04-09T13:26:21Z\",
                 \"url\": \"http://api.congress.gov/v3/member/A000376?format=json\"
            },
          ]
        }

    Args:
        congress (str):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        current_member (Union[Unset, str]):

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
        current_member=current_member,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    current_member: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns the list of members specified by Congress

     GET /member/congress/:congress

    **Example Request**

    https://api.congress.gov/v3/member/congress/118?api_key=[INSERT_KEY]

    **Example Request for a previous Congress**

    https://api.congress.gov/v3/member/congress/117?currentMember=False&api_key=[INSERT_KEY]

    **Example Response**

        {
            \"members\": [
            {
                \"bioguideId\": \"B001320\",
                \"depiction\": {
                    \"attribution\": \"Image courtesy of the Senator's office\",
                    \"imageUrl\": \"https://www.congress.gov/img/member/b001320_200.jpg\"
            },
                \"name\": \"Butler, Laphonza R.\",
                \"partyName\": \"Democratic\",
                \"state\": \"California\",
                \"terms\": {
                    \"item\": [
                        {
                            \"chamber\": \"Senate\",
                            \"startYear\": 2023
                        }
                    ]
                },
                \"updateDate\": \"2024-04-09T15:54:25Z\",
                \"url\": \"http://api.congress.gov/v3/member/B001320?format=json\"
            },
            {
                 \"bioguideId\": \"A000376\",
                 \"depiction\": {
                     \"attribution\": \"Image courtesy of the Member\",
                     \"imageUrl\": \"https://www.congress.gov/img/member/a000376_200.jpg\"
            },
                  \"district\": 32,
                  \"name\": \"Allred, Colin Z.\",
                  \"partyName\": \"Democratic\",
                  \"state\": \"Texas\",
                  \"terms\": {
                      \"item\": [
                          {
                              \"chamber\": \"House of Representatives\",
                              \"startYear\": 2019
                          }
                      ]
                  },
                 \"updateDate\": \"2024-04-09T13:26:21Z\",
                 \"url\": \"http://api.congress.gov/v3/member/A000376?format=json\"
            },
          ]
        }

    Args:
        congress (str):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        current_member (Union[Unset, str]):

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
        current_member=current_member,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
