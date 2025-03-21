from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
    current_member: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params["offset"] = offset

    params["limit"] = limit

    params["fromDateTime"] = from_date_time

    params["toDateTime"] = to_date_time

    params["currentMember"] = current_member

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/member",
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
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
    current_member: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns a list of congressional members.

     GET /member

    **Example Request**

    https://api.congress.gov/v3/member?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"members\": [
            {
                \"bioguideId\": \"L000174\",
                \"depiction\": {
                    \"attribution\": \"<a href=\\"http://www.senate.gov/artandhistory/history/common/gen
    eric/Photo_Collection_of_the_Senate_Historical_Office.htm\\">Courtesy U.S. Senate Historical
    Office</a>\",
                    \"imageUrl\": \"https://www.congress.gov/img/member/l000174_200.jpg\"
                },
                \"district\": null,
                \"name\": \"Leahy, Patrick J.\",
                \"partyName\": \"Democratic\",
                \"state\": \"Vermont\",
                \"terms\": {
                    \"item\": [
                        {
                            \"chamber\": Senate,
                            \"endYear\": null,
                            \"startYear\": 1975
                        }
                    ]
                },
                \"updateDate\": \"2022-11-07T13:42:19Z\",
                \"url\": \"https://api.congress.gov/v3/member/L000174?format=json\"
            },
            {
                \"bioguideId\": \"K000377\",
                \"depiction\": {
                    \"attribution\": \"<a href=\\"http://www.senate.gov/artandhistory/history/common/gen
    eric/Photo_Collection_of_the_Senate_Historical_Office.htm\\">Courtesy U.S. Senate Historical
    Office</a>\",
                    \"imageUrl\": \"https://www.congress.gov/img/member/k000377_200.jpg\"
                },
                \"district\": null,
                \"name\": \"Kelly, Mark\",
                \"partyName\": \"Democratic\",
                \"state\": \"Arizona\",
                \"terms\": {
                    \"item\": [
                        {
                            \"chamber\": Senate,
                            \"end\": null,
                            \"start\": 2020
                        }
                    ]
                },
                \"updateDate\": \"2023-04-01T12:42:17Z\",
                \"url\": \"https://api.congress.gov/v3/member/K000377?format=json\"
            },
          ]
        }

    Args:
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_date_time (Union[Unset, str]):
        to_date_time (Union[Unset, str]):
        current_member (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        format_=format_,
        offset=offset,
        limit=limit,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
        current_member=current_member,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
    current_member: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns a list of congressional members.

     GET /member

    **Example Request**

    https://api.congress.gov/v3/member?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"members\": [
            {
                \"bioguideId\": \"L000174\",
                \"depiction\": {
                    \"attribution\": \"<a href=\\"http://www.senate.gov/artandhistory/history/common/gen
    eric/Photo_Collection_of_the_Senate_Historical_Office.htm\\">Courtesy U.S. Senate Historical
    Office</a>\",
                    \"imageUrl\": \"https://www.congress.gov/img/member/l000174_200.jpg\"
                },
                \"district\": null,
                \"name\": \"Leahy, Patrick J.\",
                \"partyName\": \"Democratic\",
                \"state\": \"Vermont\",
                \"terms\": {
                    \"item\": [
                        {
                            \"chamber\": Senate,
                            \"endYear\": null,
                            \"startYear\": 1975
                        }
                    ]
                },
                \"updateDate\": \"2022-11-07T13:42:19Z\",
                \"url\": \"https://api.congress.gov/v3/member/L000174?format=json\"
            },
            {
                \"bioguideId\": \"K000377\",
                \"depiction\": {
                    \"attribution\": \"<a href=\\"http://www.senate.gov/artandhistory/history/common/gen
    eric/Photo_Collection_of_the_Senate_Historical_Office.htm\\">Courtesy U.S. Senate Historical
    Office</a>\",
                    \"imageUrl\": \"https://www.congress.gov/img/member/k000377_200.jpg\"
                },
                \"district\": null,
                \"name\": \"Kelly, Mark\",
                \"partyName\": \"Democratic\",
                \"state\": \"Arizona\",
                \"terms\": {
                    \"item\": [
                        {
                            \"chamber\": Senate,
                            \"end\": null,
                            \"start\": 2020
                        }
                    ]
                },
                \"updateDate\": \"2023-04-01T12:42:17Z\",
                \"url\": \"https://api.congress.gov/v3/member/K000377?format=json\"
            },
          ]
        }

    Args:
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_date_time (Union[Unset, str]):
        to_date_time (Union[Unset, str]):
        current_member (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        format_=format_,
        offset=offset,
        limit=limit,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
        current_member=current_member,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
