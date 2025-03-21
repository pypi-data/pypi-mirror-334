from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    state_code: str,
    district: int,
    *,
    format_: Union[Unset, str] = UNSET,
    current_member: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params["currentMember"] = current_member

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/member/congress/{congress}/{state_code}/{district}",
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
    state_code: str,
    district: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    current_member: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns a list of members filtered by congress, state and district.

     GET /member/congress/:congress/:stateCode/:district

    **Example Request**

    https://api.congress.gov/v3/member/congress/118/MI/10?currentMember=True&api_key=[INSERT_KEY]

    **Example Request for a previous Congress**

    https://api.congress.gov/v3/member/congress/97/TX/10?currentMember=False&api_key=[INSERT_KEY]

    **Example Response**

        {
         \"members\": [
         {
             \"bioguideId\": \"J000307\",
             \"depiction\": {
                 \"attribution\": \"Image courtesy of the Member\",
                 \"imageUrl\": \"https://www.congress.gov/img/member/j000307_200.jpg\"
         },
             \"district\": 10,
             \"name\": \"James, John\",
             \"partyName\": \"Republican\",
             \"state\": \"Michigan\",
             \"terms\": {
                 \"item\": [
                     {
                         \"chamber\": \"House of Representatives\",
                         \"startYear\": 2023
                     }
                 ]
             },
             \"updateDate\": \"2024-03-22T18:36:13Z\",
             \"url\": \"http://api.congress.gov/v3/member/J000307?format=json\"
           },
         ]
        }

    Args:
        congress (int):
        state_code (str):
        district (int):
        format_ (Union[Unset, str]):
        current_member (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        state_code=state_code,
        district=district,
        format_=format_,
        current_member=current_member,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    state_code: str,
    district: int,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    current_member: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns a list of members filtered by congress, state and district.

     GET /member/congress/:congress/:stateCode/:district

    **Example Request**

    https://api.congress.gov/v3/member/congress/118/MI/10?currentMember=True&api_key=[INSERT_KEY]

    **Example Request for a previous Congress**

    https://api.congress.gov/v3/member/congress/97/TX/10?currentMember=False&api_key=[INSERT_KEY]

    **Example Response**

        {
         \"members\": [
         {
             \"bioguideId\": \"J000307\",
             \"depiction\": {
                 \"attribution\": \"Image courtesy of the Member\",
                 \"imageUrl\": \"https://www.congress.gov/img/member/j000307_200.jpg\"
         },
             \"district\": 10,
             \"name\": \"James, John\",
             \"partyName\": \"Republican\",
             \"state\": \"Michigan\",
             \"terms\": {
                 \"item\": [
                     {
                         \"chamber\": \"House of Representatives\",
                         \"startYear\": 2023
                     }
                 ]
             },
             \"updateDate\": \"2024-03-22T18:36:13Z\",
             \"url\": \"http://api.congress.gov/v3/member/J000307?format=json\"
           },
         ]
        }

    Args:
        congress (int):
        state_code (str):
        district (int):
        format_ (Union[Unset, str]):
        current_member (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        state_code=state_code,
        district=district,
        format_=format_,
        current_member=current_member,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
