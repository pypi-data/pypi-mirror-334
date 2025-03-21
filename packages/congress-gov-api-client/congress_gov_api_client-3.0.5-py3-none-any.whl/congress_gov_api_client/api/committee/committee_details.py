from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    chamber: str,
    committee_code: str,
    *,
    format_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/committee/{chamber}/{committee_code}",
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
    chamber: str,
    committee_code: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified congressional committee.

     GET /committee/:chamber/:committeeCode

    **Example Request**

    https://api.congress.gov/v3/committee/house/hspw00?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"committee\": {
                \"bills\": {
                    \"count\": 25384,
                    \"url\": \"https://api.congress.gov/v3/committee/house/hspw00/bills?format=json\"
                },
                \"communications\": {
                    \"count\": 6775,
                    \"url\": \"https://api.congress.gov/v3/committee/house/hspw00/house-
    communication?format=json\"
                },
                \"history\": [
                    {
                        \"libraryOfCongressName\": \"Transportation and Infrastructure\",
                        \"officialName\": \"Committee on Transportation and Infrastructure\",
                        \"startDate\": \"1995-01-04T05:00:00Z\",
                        \"updateDate\": \"2020-02-14T19:13:07Z\"
                    },
                    {
                        \"endDate\": \"1995-01-03T05:00:00Z\",
                        \"libraryOfCongressName\": \"Public Works and Transportation\",
                        \"officialName\": \"Committee on Public Works and Transportation\",
                        \"startDate\": \"1975-01-01T05:00:00Z\",
                        \"updateDate\": \"2020-02-10T16:49:05Z\"
                    },
                    {
                        \"endDate\": \"1974-12-31T05:00:00Z\",
                        \"libraryOfCongressName\": \"Public Works\",
                        \"officialName\": \"Committee on Public Works\",
                        \"startDate\": \"1946-08-02T04:00:00Z\",
                        \"updateDate\": \"2020-02-10T16:49:05Z\"
                    }
                ],
                \"isCurrent\": true,
                \"reports\": {
                    \"count\": 1382,
                    \"url\": \"https://api.congress.gov/v3/committee/house/hspw00/reports?format=json\"
                },
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
                        \"name\": \"Oversight, Investigations and Emergency Management Subcommittee\",
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
                \"type\": \"Standing\",
                \"updateDate\": \"2020-02-04T00:07:37Z\"
            },
        }

    Args:
        chamber (str):
        committee_code (str):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        chamber=chamber,
        committee_code=committee_code,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    chamber: str,
    committee_code: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified congressional committee.

     GET /committee/:chamber/:committeeCode

    **Example Request**

    https://api.congress.gov/v3/committee/house/hspw00?api_key=[INSERT_KEY]

    **Example Response**

        {
            \"committee\": {
                \"bills\": {
                    \"count\": 25384,
                    \"url\": \"https://api.congress.gov/v3/committee/house/hspw00/bills?format=json\"
                },
                \"communications\": {
                    \"count\": 6775,
                    \"url\": \"https://api.congress.gov/v3/committee/house/hspw00/house-
    communication?format=json\"
                },
                \"history\": [
                    {
                        \"libraryOfCongressName\": \"Transportation and Infrastructure\",
                        \"officialName\": \"Committee on Transportation and Infrastructure\",
                        \"startDate\": \"1995-01-04T05:00:00Z\",
                        \"updateDate\": \"2020-02-14T19:13:07Z\"
                    },
                    {
                        \"endDate\": \"1995-01-03T05:00:00Z\",
                        \"libraryOfCongressName\": \"Public Works and Transportation\",
                        \"officialName\": \"Committee on Public Works and Transportation\",
                        \"startDate\": \"1975-01-01T05:00:00Z\",
                        \"updateDate\": \"2020-02-10T16:49:05Z\"
                    },
                    {
                        \"endDate\": \"1974-12-31T05:00:00Z\",
                        \"libraryOfCongressName\": \"Public Works\",
                        \"officialName\": \"Committee on Public Works\",
                        \"startDate\": \"1946-08-02T04:00:00Z\",
                        \"updateDate\": \"2020-02-10T16:49:05Z\"
                    }
                ],
                \"isCurrent\": true,
                \"reports\": {
                    \"count\": 1382,
                    \"url\": \"https://api.congress.gov/v3/committee/house/hspw00/reports?format=json\"
                },
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
                        \"name\": \"Oversight, Investigations and Emergency Management Subcommittee\",
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
                \"type\": \"Standing\",
                \"updateDate\": \"2020-02-04T00:07:37Z\"
            },
        }

    Args:
        chamber (str):
        committee_code (str):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        chamber=chamber,
        committee_code=committee_code,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
