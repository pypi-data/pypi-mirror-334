from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    report_number: str,
    *,
    format_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["format"] = format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/crsreport/{report_number}",
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
    report_number: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specificed Congressional Research Service (CRS) report

     GET /crsreport/:reportNumber

    **Example Request**

    https://api.congress.gov/v3/crsreport/R47175?api_key=[INSERT_KEY]

    **Example Response**

          {
              \"CRSReport\": {
                      \"authors\": [
                           {
                               \"author\": \"Megan S. Lynch\"
                           }
                      ],
                      \"contentType\": \"Reports\",
                      \"formats\": [
                          {
                               \"format\": \"PDF\",
                               \"url\":
    \"https://congress.gov/crs_external_products/R/PDF/R47175/R47175.2.pdf\"
                          },
                          {
                               \"format\": \"HTML\",
                               \"url\":
    \"https://congress.gov/crs_external_products/R/HTML/R47175.html\"
                          }
                      ],
                      \"id\": \"R47175\",
                      \"publishDate\": \"2025-02-05T11:34:31Z\",
                      \"relatedMaterials\": [
                          {
                                        \"URL\": \"http://api.congress.gov/v3/law/93/pub/344\",
                                        \"congress\": 93,
                                        \"number\": \"93-344\",
                                        \"title\": null,
                                        \"type\": \"PUB\"
                           },
                           {
                                        \"URL\": \"http://api.congress.gov/v3/bill/117/HRES/1151\",
                                        \"congress\": 117,
                                        \"number\": 1151,
                                        \"title\": \"Providing for budget allocations, and for other
    purposes.\",
                                        \"type\": \"HRES\"
                            },
                            {
                                        \"URL\": \"http://api.congress.gov/v3/bill/117/HRES/1151\",
                                        \"congress\": 117,
                                        \"number\": 1151,
                                        \"title\": \"Providing for budget allocations, and for other
    purposes.\",
                                        \"type\": \"HRES\"
                            }
                       ],
                       \"status\": \"Active\",
                       \"summary\": \"The Congressional Budget Act of 1974 directs Congress to adopt a
    budget resolution each spring, providing an agreement between the House and Senate on a budget plan
    for the upcoming fiscal year (and at least four additional years). The annual budget resolution
    includes certain spending and revenue levels that become enforceable through points of order once
    both chambers have adopted the resolution.Congress does not always adopt a budget resolution,
    however, and this may complicate the development and consideration of budgetary legislation.
    Congress has, therefore, developed an alternative legislative tool, typically referred to as a
    “deeming resolution” because it is deemed to serve in place of an annual budget resolution for the
    purposes of establishing enforceable budgetary levels. On June 8, 2022, the House of Representatives
    adopted H.Res. 1151, a deeming resolution for FY2023. H.Res. 1151 provided a committee spending
    allocation (302(a) allocation) to the House Appropriations Committee ($1.603 trillion). It also
    directed the chair of the House Budget Committee to subsequently file a statement in the
    Congressional Record that includes committee spending allocations for all other committees, as well
    as aggregate spending and revenue levels. (Those levels were filed on June 21, 2022.) H.Res. 1151
    specified that the levels filed in the Congressional Record be consistent with the “most recent
    baseline of the Congressional Budget Office,” meaning that the committee spending allocations (other
    than for the Appropriations Committee) and the aggregate spending and revenue levels have been set
    at the levels currently projected under current law. In addition to providing enforceable budgetary
    levels within the House, H.Res. 1151 grants authority to the chair of the House Budget Committee to
    “adjust” the budgetary levels provided under the deeming resolution in the future under specified
    circumstances. In addition, the resolution states that provisions designated as “emergency” shall be
    effectively exempt from House budgetary rules and specifies that certain accounts may receive
    advance appropriations for FY2024 and FY2025.\",
                      \"title\": \"Setting Budgetary Levels: The House's FY2023 Deeming Resolution\",
                      \"topics\": [
                          {
                              \"topic\": \"Budget & Appropriations Procedure\"
                          }
                      ],
                      \"updateDate\": \"2025-02-07T01:36:56Z\",
                      \"url\": \"congress.gov/crs-report/R47175\",
                      \"version\": 102
               },
           }

    Args:
        report_number (str):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        report_number=report_number,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    report_number: str,
    *,
    client: AuthenticatedClient,
    format_: Union[Unset, str] = UNSET,
) -> Response[Any]:
    r"""Returns detailed information for a specificed Congressional Research Service (CRS) report

     GET /crsreport/:reportNumber

    **Example Request**

    https://api.congress.gov/v3/crsreport/R47175?api_key=[INSERT_KEY]

    **Example Response**

          {
              \"CRSReport\": {
                      \"authors\": [
                           {
                               \"author\": \"Megan S. Lynch\"
                           }
                      ],
                      \"contentType\": \"Reports\",
                      \"formats\": [
                          {
                               \"format\": \"PDF\",
                               \"url\":
    \"https://congress.gov/crs_external_products/R/PDF/R47175/R47175.2.pdf\"
                          },
                          {
                               \"format\": \"HTML\",
                               \"url\":
    \"https://congress.gov/crs_external_products/R/HTML/R47175.html\"
                          }
                      ],
                      \"id\": \"R47175\",
                      \"publishDate\": \"2025-02-05T11:34:31Z\",
                      \"relatedMaterials\": [
                          {
                                        \"URL\": \"http://api.congress.gov/v3/law/93/pub/344\",
                                        \"congress\": 93,
                                        \"number\": \"93-344\",
                                        \"title\": null,
                                        \"type\": \"PUB\"
                           },
                           {
                                        \"URL\": \"http://api.congress.gov/v3/bill/117/HRES/1151\",
                                        \"congress\": 117,
                                        \"number\": 1151,
                                        \"title\": \"Providing for budget allocations, and for other
    purposes.\",
                                        \"type\": \"HRES\"
                            },
                            {
                                        \"URL\": \"http://api.congress.gov/v3/bill/117/HRES/1151\",
                                        \"congress\": 117,
                                        \"number\": 1151,
                                        \"title\": \"Providing for budget allocations, and for other
    purposes.\",
                                        \"type\": \"HRES\"
                            }
                       ],
                       \"status\": \"Active\",
                       \"summary\": \"The Congressional Budget Act of 1974 directs Congress to adopt a
    budget resolution each spring, providing an agreement between the House and Senate on a budget plan
    for the upcoming fiscal year (and at least four additional years). The annual budget resolution
    includes certain spending and revenue levels that become enforceable through points of order once
    both chambers have adopted the resolution.Congress does not always adopt a budget resolution,
    however, and this may complicate the development and consideration of budgetary legislation.
    Congress has, therefore, developed an alternative legislative tool, typically referred to as a
    “deeming resolution” because it is deemed to serve in place of an annual budget resolution for the
    purposes of establishing enforceable budgetary levels. On June 8, 2022, the House of Representatives
    adopted H.Res. 1151, a deeming resolution for FY2023. H.Res. 1151 provided a committee spending
    allocation (302(a) allocation) to the House Appropriations Committee ($1.603 trillion). It also
    directed the chair of the House Budget Committee to subsequently file a statement in the
    Congressional Record that includes committee spending allocations for all other committees, as well
    as aggregate spending and revenue levels. (Those levels were filed on June 21, 2022.) H.Res. 1151
    specified that the levels filed in the Congressional Record be consistent with the “most recent
    baseline of the Congressional Budget Office,” meaning that the committee spending allocations (other
    than for the Appropriations Committee) and the aggregate spending and revenue levels have been set
    at the levels currently projected under current law. In addition to providing enforceable budgetary
    levels within the House, H.Res. 1151 grants authority to the chair of the House Budget Committee to
    “adjust” the budgetary levels provided under the deeming resolution in the future under specified
    circumstances. In addition, the resolution states that provisions designated as “emergency” shall be
    effectively exempt from House budgetary rules and specifies that certain accounts may receive
    advance appropriations for FY2024 and FY2025.\",
                      \"title\": \"Setting Budgetary Levels: The House's FY2023 Deeming Resolution\",
                      \"topics\": [
                          {
                              \"topic\": \"Budget & Appropriations Procedure\"
                          }
                      ],
                      \"updateDate\": \"2025-02-07T01:36:56Z\",
                      \"url\": \"congress.gov/crs-report/R47175\",
                      \"version\": 102
               },
           }

    Args:
        report_number (str):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        report_number=report_number,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
