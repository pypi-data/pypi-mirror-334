from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    amendment_type: str,
    *,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params["offset"] = offset

    params["limit"] = limit

    params["fromDateTime"] = from_date_time

    params["toDateTime"] = to_date_time

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/amendment/{congress}/{amendment_type}",
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
    amendment_type: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns a list of amendments filtered by the specified congress and amendment type, sorted by date
    of latest action.

     GET /amendment/:congress/:amendmentType

    **Example Request**

    https://api.congress.gov/v3/amendment/117/samdt?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"amendments\": [
                {
                   \"congress\": 117,
                   \"latestAction\": {
                        \"actionDate\": \"2021-08-08\",
                        \"text\": \"Amendment SA 2137 agreed to in Senate by Yea-Nay Vote. 69 - 28.
    Record Vote Number: 312.\"
                    },
                    \"number\": \"2137\",
                    \"purpose\": \"In the nature of a substitute.\",
                    \"type\": \"SAMDT\",
                    \"url\": \"http://api.congress.gov/v3/amendment/117/samdt/2137?format=json\"
                },
                {
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2021-08-08\",
                        \"text\": \"Amendment SA 2131 agreed to in Senate by Voice Vote. \"
                    },
                    \"number\": \"2131\",
                    \"purpose\": \"To strike a definition.\",
                    \"type\": \"SAMDT\",
                    \"updateDate\": \"2022-02-25T17:34:49Z\",
                    \"url\": \"https://api.congress.gov/v3/amendment/117/samdt/2131?format=json\"
                }
            ],
         }

    Args:
        congress (int):
        amendment_type (str):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_date_time (Union[Unset, str]):
        to_date_time (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        amendment_type=amendment_type,
        format_=format_,
        offset=offset,
        limit=limit,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    amendment_type: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns a list of amendments filtered by the specified congress and amendment type, sorted by date
    of latest action.

     GET /amendment/:congress/:amendmentType

    **Example Request**

    https://api.congress.gov/v3/amendment/117/samdt?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"amendments\": [
                {
                   \"congress\": 117,
                   \"latestAction\": {
                        \"actionDate\": \"2021-08-08\",
                        \"text\": \"Amendment SA 2137 agreed to in Senate by Yea-Nay Vote. 69 - 28.
    Record Vote Number: 312.\"
                    },
                    \"number\": \"2137\",
                    \"purpose\": \"In the nature of a substitute.\",
                    \"type\": \"SAMDT\",
                    \"url\": \"http://api.congress.gov/v3/amendment/117/samdt/2137?format=json\"
                },
                {
                    \"congress\": 117,
                    \"latestAction\": {
                        \"actionDate\": \"2021-08-08\",
                        \"text\": \"Amendment SA 2131 agreed to in Senate by Voice Vote. \"
                    },
                    \"number\": \"2131\",
                    \"purpose\": \"To strike a definition.\",
                    \"type\": \"SAMDT\",
                    \"updateDate\": \"2022-02-25T17:34:49Z\",
                    \"url\": \"https://api.congress.gov/v3/amendment/117/samdt/2131?format=json\"
                }
            ],
         }

    Args:
        congress (int):
        amendment_type (str):
        format_ (Union[Unset, str]):
        offset (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_date_time (Union[Unset, str]):
        to_date_time (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        congress=congress,
        amendment_type=amendment_type,
        format_=format_,
        offset=offset,
        limit=limit,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
