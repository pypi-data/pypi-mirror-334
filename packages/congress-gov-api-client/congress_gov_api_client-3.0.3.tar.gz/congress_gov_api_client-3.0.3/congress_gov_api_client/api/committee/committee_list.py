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
        "url": "/committee",
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
) -> Response[Any]:
    r"""Returns a list of congressional committees.

     GET /committee

    **Example Request**

    https://api.congress.gov/v3/committee?api_key=[INSERT_KEY]

    **Example Response**

        {
             \"committees\": [
                {
                    \"chamber\": \"House\",
                    \"committeeTypeCode\": \"Standing\",
                    \"updateDate\": \"2020-02-04T00:07:37Z\"
                    \"name\": \"Transportation and Infrastructure Committee\",
                    \"parent\": null,
                    \"subcommittees\": [
                        {
                            \"name\": \"Investigations and Oversight Subcommittee\",
                            \"systemCode\": \"hspw01\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw01?format=json\"
                        },
                        {
                            \"name\": \"Public Buildings and Grounds Subcommittee\",
                            \"systemCode\": \"hspw04\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw04?format=json\"
                        },
                        {
                            \"name\": \"Economic Development Subcommittee\",
                            \"systemCode\": \"hspw06\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw06?format=json\"
                        },
                        {
                            \"name\": \"Economic Development, Public Buildings, Hazardous Materials and
    Pipeline Transportation Subcommittee\",
                            \"systemCode\": \"hspw08\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw08?format=json\"
                        },
                        {
                            \"name\": \"Railroads Subcommittee\",
                            \"systemCode\": \"hspw09\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw09?format=json\"
                        },
                        {
                            \"name\": \"Ground Transportation Subcommittee\",
                            \"systemCode\": \"hspw10\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw10?format=json\"
                        },
                        {
                            \"name\": \"Aviation Subcommittee\",
                            \"systemCode\": \"hspw05\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw05?format=json\"
                        },
                        {
                            \"name\": \"Economic Development, Public Buildings, and Emergency Management
    Subcommittee\",
                            \"systemCode\": \"hspw13\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw13?format=json\"
                        },
                        {
                            \"name\": \"Highways and Transit Subcommittee\",
                            \"systemCode\": \"hspw12\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw12?format=json\"
                        },
                        {
                            \"name\": \"Railroads, Pipelines, and Hazardous Materials Subcommittee\",
                            \"systemCode\": \"hspw14\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw14?format=json\"
                        },
                        {
                            \"name\": \"Water Resources and Environment Subcommittee\",
                            \"systemCode\": \"hspw02\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw02?format=json\"
                        },
                        {
                            \"name\": \"Public-Private Partnerships Subcommittee\",
                            \"systemCode\": \"hspw33\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw33?format=json\"
                        },
                        {
                            \"name\": \"Surface Transportation Subcommittee\",
                            \"systemCode\": \"hspw03\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw03?format=json\"
                        },
                        {
                            \"name\": \"Oversight, Investigations and Emergency Management
    Subcommittee\",
                            \"systemCode\": \"hspw11\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw11?format=json\"
                        },
                        {
                            \"name\": \"Coast Guard and Maritime Transportation Subcommittee\",
                            \"systemCode\": \"hspw07\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw07?format=json\"
                        }
                    ],
                    \"systemCode\": \"hspw00\",
                    \"url\": \"https://api.congress.gov/v3/committee/house/hspw00?format=json\"
                },
             ]
        }

    Args:
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
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_date_time: Union[Unset, str] = UNSET,
    to_date_time: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns a list of congressional committees.

     GET /committee

    **Example Request**

    https://api.congress.gov/v3/committee?api_key=[INSERT_KEY]

    **Example Response**

        {
             \"committees\": [
                {
                    \"chamber\": \"House\",
                    \"committeeTypeCode\": \"Standing\",
                    \"updateDate\": \"2020-02-04T00:07:37Z\"
                    \"name\": \"Transportation and Infrastructure Committee\",
                    \"parent\": null,
                    \"subcommittees\": [
                        {
                            \"name\": \"Investigations and Oversight Subcommittee\",
                            \"systemCode\": \"hspw01\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw01?format=json\"
                        },
                        {
                            \"name\": \"Public Buildings and Grounds Subcommittee\",
                            \"systemCode\": \"hspw04\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw04?format=json\"
                        },
                        {
                            \"name\": \"Economic Development Subcommittee\",
                            \"systemCode\": \"hspw06\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw06?format=json\"
                        },
                        {
                            \"name\": \"Economic Development, Public Buildings, Hazardous Materials and
    Pipeline Transportation Subcommittee\",
                            \"systemCode\": \"hspw08\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw08?format=json\"
                        },
                        {
                            \"name\": \"Railroads Subcommittee\",
                            \"systemCode\": \"hspw09\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw09?format=json\"
                        },
                        {
                            \"name\": \"Ground Transportation Subcommittee\",
                            \"systemCode\": \"hspw10\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw10?format=json\"
                        },
                        {
                            \"name\": \"Aviation Subcommittee\",
                            \"systemCode\": \"hspw05\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw05?format=json\"
                        },
                        {
                            \"name\": \"Economic Development, Public Buildings, and Emergency Management
    Subcommittee\",
                            \"systemCode\": \"hspw13\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw13?format=json\"
                        },
                        {
                            \"name\": \"Highways and Transit Subcommittee\",
                            \"systemCode\": \"hspw12\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw12?format=json\"
                        },
                        {
                            \"name\": \"Railroads, Pipelines, and Hazardous Materials Subcommittee\",
                            \"systemCode\": \"hspw14\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw14?format=json\"
                        },
                        {
                            \"name\": \"Water Resources and Environment Subcommittee\",
                            \"systemCode\": \"hspw02\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw02?format=json\"
                        },
                        {
                            \"name\": \"Public-Private Partnerships Subcommittee\",
                            \"systemCode\": \"hspw33\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw33?format=json\"
                        },
                        {
                            \"name\": \"Surface Transportation Subcommittee\",
                            \"systemCode\": \"hspw03\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw03?format=json\"
                        },
                        {
                            \"name\": \"Oversight, Investigations and Emergency Management
    Subcommittee\",
                            \"systemCode\": \"hspw11\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw11?format=json\"
                        },
                        {
                            \"name\": \"Coast Guard and Maritime Transportation Subcommittee\",
                            \"systemCode\": \"hspw07\",
                            \"url\": \"https://api.congress.gov/v3/committee/house/hspw07?format=json\"
                        }
                    ],
                    \"systemCode\": \"hspw00\",
                    \"url\": \"https://api.congress.gov/v3/committee/house/hspw00?format=json\"
                },
             ]
        }

    Args:
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
        format_=format_,
        offset=offset,
        limit=limit,
        from_date_time=from_date_time,
        to_date_time=to_date_time,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
