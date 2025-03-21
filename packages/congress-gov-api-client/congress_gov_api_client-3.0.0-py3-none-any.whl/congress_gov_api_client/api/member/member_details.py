from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    bioguide_id: str,
    *,
    format_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/member/{bioguide_id}",
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
    bioguide_id: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified congressional member.

     GET /member/:bioguideId

    **Example Request**

    https://api.congress.gov/v3/member/L000174?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"member\": {
                \"bioguideId\": \"L000174\",
                \"birthYear\": \"1940\",
                \"cosponsoredLegislation\": {
                    \"count\": 7520,
                    \"URL\": \"url\": \"https://api.congress.gov/v3/member/L000174/cosponsored-
    legislation\"
                },
                \"depiction\": {
                    \"attribution\": \"<a href=\\"http://www.senate.gov/artandhistory/history/common/gen
    eric/Photo_Collection_of_the_Senate_Historical_Office.htm\\">Courtesy U.S. Senate Historical
    Office</a>\",
                    \"imageUrl\": \"https://www.congress.gov/img/member/l000174_200.jpg\"
                },
                \"directOrderName\": \"Patrick J. Leahy\",
                \"firstName\": \"Patrick\",
                \"honorificName\": \"Mr.\",
                \"invertedOrderName\": \"Leahy, Patrick J.\",
                \"lastName\": \"Leahy\",
                \"leadership\": [
                    {
                        \"congress\": 113,
                        \"type\": \"President Pro Tempore\"
                    },
                    {
                        \"congress\": 112,
                        \"type\": \"President Pro Tempore\"
                    },
                    {
                        \"congress\": 117,
                        \"type\": \"President Pro Tempore\"
                    }
                ],
                \"partyHistory\": [
                    {
                        \"partyAbbreviation\": \"D\",
                        \"partyName\": \"Democrat\",
                        \"startYear\": 1975
                    }
                ],
                \"sponsoredLegislation\": {
                    \"count\": 1768,
                    \"url\": \"https://api.congress.gov/v3/member/L000174/sponsored-legislation\"
                },
                \"state\": \"Vermont\",
                \"terms\": [
                    {
                        \"chamber\": \"Senate\",
                        \"congress\": 116,
                        \"endYear\": 2021,
                        \"memberType\": \"Senator\",
                        \"startYear\": 2019,
                        \"stateCode\": \"VT\",
                        \"stateName\": \"Vermont\"
                    },
                    {
                        \"chamber\": \"Senate\",
                        \"congress\": 117,
                        \"endYear\": 2023,
                        \"memberType\": \"Senator\",
                        \"startYear\": 2021,
                        \"stateCode\": \"VT\",
                        \"stateName\": \"Vermont\"
                    }
                    ...
                ],
                \"updateDate\": \"2022-11-07T13:42:19Z\"
            },
            \"request\": {
                \"bioguideId\": \"l000174\",
                \"contentType\": \"application/json\",
                \"format\": \"json\"
             }
        }

    Args:
        bioguide_id (str):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        bioguide_id=bioguide_id,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    bioguide_id: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified congressional member.

     GET /member/:bioguideId

    **Example Request**

    https://api.congress.gov/v3/member/L000174?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"member\": {
                \"bioguideId\": \"L000174\",
                \"birthYear\": \"1940\",
                \"cosponsoredLegislation\": {
                    \"count\": 7520,
                    \"URL\": \"url\": \"https://api.congress.gov/v3/member/L000174/cosponsored-
    legislation\"
                },
                \"depiction\": {
                    \"attribution\": \"<a href=\\"http://www.senate.gov/artandhistory/history/common/gen
    eric/Photo_Collection_of_the_Senate_Historical_Office.htm\\">Courtesy U.S. Senate Historical
    Office</a>\",
                    \"imageUrl\": \"https://www.congress.gov/img/member/l000174_200.jpg\"
                },
                \"directOrderName\": \"Patrick J. Leahy\",
                \"firstName\": \"Patrick\",
                \"honorificName\": \"Mr.\",
                \"invertedOrderName\": \"Leahy, Patrick J.\",
                \"lastName\": \"Leahy\",
                \"leadership\": [
                    {
                        \"congress\": 113,
                        \"type\": \"President Pro Tempore\"
                    },
                    {
                        \"congress\": 112,
                        \"type\": \"President Pro Tempore\"
                    },
                    {
                        \"congress\": 117,
                        \"type\": \"President Pro Tempore\"
                    }
                ],
                \"partyHistory\": [
                    {
                        \"partyAbbreviation\": \"D\",
                        \"partyName\": \"Democrat\",
                        \"startYear\": 1975
                    }
                ],
                \"sponsoredLegislation\": {
                    \"count\": 1768,
                    \"url\": \"https://api.congress.gov/v3/member/L000174/sponsored-legislation\"
                },
                \"state\": \"Vermont\",
                \"terms\": [
                    {
                        \"chamber\": \"Senate\",
                        \"congress\": 116,
                        \"endYear\": 2021,
                        \"memberType\": \"Senator\",
                        \"startYear\": 2019,
                        \"stateCode\": \"VT\",
                        \"stateName\": \"Vermont\"
                    },
                    {
                        \"chamber\": \"Senate\",
                        \"congress\": 117,
                        \"endYear\": 2023,
                        \"memberType\": \"Senator\",
                        \"startYear\": 2021,
                        \"stateCode\": \"VT\",
                        \"stateName\": \"Vermont\"
                    }
                    ...
                ],
                \"updateDate\": \"2022-11-07T13:42:19Z\"
            },
            \"request\": {
                \"bioguideId\": \"l000174\",
                \"contentType\": \"application/json\",
                \"format\": \"json\"
             }
        }

    Args:
        bioguide_id (str):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        bioguide_id=bioguide_id,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
