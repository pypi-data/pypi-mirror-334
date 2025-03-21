from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    congress: int,
    chamber: str,
    event_id: str,
    *,
    format_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/committee-meeting/{congress}/{chamber}/{event_id}",
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
    event_id: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified committee meeting.

     GET /committee-meeting/{congress}/{chamber}/{eventId}

    **Example Request**

    https://api.congress.gov/v3/committee-meeting/118/house/115538?api_key=[INSERT_KEY]

    **Example Response**

          {
              \"committeeMeeting\": {
                  \"chamber\": \"House\",
                  \"committees\": [
                      {
                          \"name\": \"House Natural Resources Subcommittee on Indian and Insular
    Affairs\",
                          \"systemCode\": \"hsii24\",
                          \"url\": \"https://api.congress.gov/v3/committee/house/hsii24?format=json\"
                      }
                  ],
                  \"congress\": 118,
                  \"date\": \"2024-12-02T04:44:57Z\",
                  \"eventId\": \"115538\",
                  \"hearingTranscript\": [],
                  \"location\": {
                      \"building\": \"Longworth House Office Building\",
                      \"room\": \"1324\"
                  },
                  \"meetingDocuments\": [
                      {
                          \"description\": null,
                          \"documentType\": \"Support Document\",
                          \"format\": \"PDF\",
                          \"name\": \"Hearing Notice\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/documents/HHRG-118-II24-20230324-SD001.pdf\"
                      },
                      {
                          \"description\": null,
                          \"documentType\": \"Bills and Resolutions\",
                          \"format\": \"PDF\",
                          \"name\": \"H.R. 1532 (Rep. Hageman), To authorize any Indian Tribe to lease,
    sell, convey, warrant, or otherwise transfer real property to which that Indian Tribe holds fee
    title without the consent of the Federal Government, and for other purposes.\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/documents/BILLS-118HR1532ih.pdf\"
                      },
                      {
                          \"description\": null,
                          \"documentType\": \"Bills and Resolutions\",
                          \"format\": \"PDF\",
                          \"name\": \"H.R. 1246 (Rep. Hageman), To authorize leases of up to 99 years
    for land held in trust for federally recognized Indian tribes.\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/documents/BILLS-118HR1246ih.pdf\"
                      },
                      {
                          \"description\": null,
                          \"documentType\": \"Support Document\",
                          \"format\": \"PDF\",
                          \"name\": \"Hearing Memo\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/documents/HHRG-118-II24-20230324-SD002.pdf\"
                      },
                      {
                          \"description\": null,
                          \"documentType\": \"Support Document\",
                          \"format\": \"PDF\",
                          \"name\": \"Chair Westerman's Submission FTR - Pueblo of Santa Clara Statement
    by Governor Chavarria\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/documents/HHRG-118-II24-20230324-SD003.pdf\"
                      }
                  ],
                  \"meetingStatus\": \"Scheduled\",
                  \"relatedItems\": {
                      \"bills\": [
                          {
                              \"congress\": 118,
                              \"number\": \"1532\",
                              \"type\": \"HR\",
                              \"url\": \"https://api.congress.gov/v3/bill/118/hr/1532?format=json\"
                          },
                          {
                              \"congress\": 118,
                              \"number\": \"1246\",
                              \"type\": \"HR\",
                              \"url\": \"https://api.congress.gov/v3/bill/118/hr/1246?format=json\"
                          }
                      ],
                      \"nominations\": [],
                      \"treaties\": []
                  },
                  \"title\": \"Legislative hearing on: \u2022\tH.R. 1246 (Rep. Hageman), To authorize
    leases of up to 99 years for land held in trust for federally recognized Indian tribes;
    and\r\n\u2022\tH.R. 1532 (Rep. Hageman), To authorize any Indian Tribe to lease, sell, convey,
    warrant, or otherwise transfer real property to which that Indian Tribe holds fee title without the
    consent of the Federal Government, and for other purposes.\",
                  \"type\": \"Hearing\",
                  \"updateDate\": \"2024-12-02T04:44:57Z\",
                  \"videos\": [],
                  \"witnessDocuments\": [
                      {
                          \"documentType\": \"Witness Statement\",
                          \"format\": \"PDF\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/witnesses/HHRG-118-II24-Wstate-
    OsceolaM-20230324.pdf\"
                      },
                      {
                          \"documentType\": \"Witness Statement\",
                          \"format\": \"PDF\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/witnesses/HHRG-118-II24-Wstate-
    WilliamsJ-20230324.pdf\"
                      },
                      {
                          \"documentType\": \"Witness Statement\",
                          \"format\": \"PDF\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/witnesses/HHRG-118-II24-Wstate-
    NewlandB-20230324.pdf\"
                      }
                  ],
                  \"witnesses\": [
                      {
                          \"name\": \"The Honorable Bryan Newland\",
                          \"organization\": \"Bureau of Indian Affairs\",
                          \"position\": \"Assistant Secretary\"
                      },
                      {
                          \"name\": \"The Honorable Marcellus Osceola\",
                          \"organization\": \"Seminole Tribe of Florida\",
                          \"position\": \"Chairman\"
                      },
                      {
                          \"name\": \"The Honorable John Williams\",
                          \"organization\": \"United Auburn Rancheria\",
                          \"position\": \"Vice Chairman\"
                      }
                  ]
              },
          }

    Args:
        congress (int):
        chamber (str):
        event_id (str):
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
        event_id=event_id,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    congress: int,
    chamber: str,
    event_id: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specified committee meeting.

     GET /committee-meeting/{congress}/{chamber}/{eventId}

    **Example Request**

    https://api.congress.gov/v3/committee-meeting/118/house/115538?api_key=[INSERT_KEY]

    **Example Response**

          {
              \"committeeMeeting\": {
                  \"chamber\": \"House\",
                  \"committees\": [
                      {
                          \"name\": \"House Natural Resources Subcommittee on Indian and Insular
    Affairs\",
                          \"systemCode\": \"hsii24\",
                          \"url\": \"https://api.congress.gov/v3/committee/house/hsii24?format=json\"
                      }
                  ],
                  \"congress\": 118,
                  \"date\": \"2024-12-02T04:44:57Z\",
                  \"eventId\": \"115538\",
                  \"hearingTranscript\": [],
                  \"location\": {
                      \"building\": \"Longworth House Office Building\",
                      \"room\": \"1324\"
                  },
                  \"meetingDocuments\": [
                      {
                          \"description\": null,
                          \"documentType\": \"Support Document\",
                          \"format\": \"PDF\",
                          \"name\": \"Hearing Notice\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/documents/HHRG-118-II24-20230324-SD001.pdf\"
                      },
                      {
                          \"description\": null,
                          \"documentType\": \"Bills and Resolutions\",
                          \"format\": \"PDF\",
                          \"name\": \"H.R. 1532 (Rep. Hageman), To authorize any Indian Tribe to lease,
    sell, convey, warrant, or otherwise transfer real property to which that Indian Tribe holds fee
    title without the consent of the Federal Government, and for other purposes.\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/documents/BILLS-118HR1532ih.pdf\"
                      },
                      {
                          \"description\": null,
                          \"documentType\": \"Bills and Resolutions\",
                          \"format\": \"PDF\",
                          \"name\": \"H.R. 1246 (Rep. Hageman), To authorize leases of up to 99 years
    for land held in trust for federally recognized Indian tribes.\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/documents/BILLS-118HR1246ih.pdf\"
                      },
                      {
                          \"description\": null,
                          \"documentType\": \"Support Document\",
                          \"format\": \"PDF\",
                          \"name\": \"Hearing Memo\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/documents/HHRG-118-II24-20230324-SD002.pdf\"
                      },
                      {
                          \"description\": null,
                          \"documentType\": \"Support Document\",
                          \"format\": \"PDF\",
                          \"name\": \"Chair Westerman's Submission FTR - Pueblo of Santa Clara Statement
    by Governor Chavarria\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/documents/HHRG-118-II24-20230324-SD003.pdf\"
                      }
                  ],
                  \"meetingStatus\": \"Scheduled\",
                  \"relatedItems\": {
                      \"bills\": [
                          {
                              \"congress\": 118,
                              \"number\": \"1532\",
                              \"type\": \"HR\",
                              \"url\": \"https://api.congress.gov/v3/bill/118/hr/1532?format=json\"
                          },
                          {
                              \"congress\": 118,
                              \"number\": \"1246\",
                              \"type\": \"HR\",
                              \"url\": \"https://api.congress.gov/v3/bill/118/hr/1246?format=json\"
                          }
                      ],
                      \"nominations\": [],
                      \"treaties\": []
                  },
                  \"title\": \"Legislative hearing on: \u2022\tH.R. 1246 (Rep. Hageman), To authorize
    leases of up to 99 years for land held in trust for federally recognized Indian tribes;
    and\r\n\u2022\tH.R. 1532 (Rep. Hageman), To authorize any Indian Tribe to lease, sell, convey,
    warrant, or otherwise transfer real property to which that Indian Tribe holds fee title without the
    consent of the Federal Government, and for other purposes.\",
                  \"type\": \"Hearing\",
                  \"updateDate\": \"2024-12-02T04:44:57Z\",
                  \"videos\": [],
                  \"witnessDocuments\": [
                      {
                          \"documentType\": \"Witness Statement\",
                          \"format\": \"PDF\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/witnesses/HHRG-118-II24-Wstate-
    OsceolaM-20230324.pdf\"
                      },
                      {
                          \"documentType\": \"Witness Statement\",
                          \"format\": \"PDF\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/witnesses/HHRG-118-II24-Wstate-
    WilliamsJ-20230324.pdf\"
                      },
                      {
                          \"documentType\": \"Witness Statement\",
                          \"format\": \"PDF\",
                          \"url\":
    \"https://www.congress.gov/118/meeting/house/115538/witnesses/HHRG-118-II24-Wstate-
    NewlandB-20230324.pdf\"
                      }
                  ],
                  \"witnesses\": [
                      {
                          \"name\": \"The Honorable Bryan Newland\",
                          \"organization\": \"Bureau of Indian Affairs\",
                          \"position\": \"Assistant Secretary\"
                      },
                      {
                          \"name\": \"The Honorable Marcellus Osceola\",
                          \"organization\": \"Seminole Tribe of Florida\",
                          \"position\": \"Chairman\"
                      },
                      {
                          \"name\": \"The Honorable John Williams\",
                          \"organization\": \"United Auburn Rancheria\",
                          \"position\": \"Vice Chairman\"
                      }
                  ]
              },
          }

    Args:
        congress (int):
        chamber (str):
        event_id (str):
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
        event_id=event_id,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
