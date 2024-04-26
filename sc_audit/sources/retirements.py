"""
Fetch Stellarcarbon retirements from the Verra Registry.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt

import httpx
from parsel import Selector

from sc_audit.constants import VERRA_ASSET_SEARCH_URL, VERRA_ASSET_SEARCH_TIMEOUT
from sc_audit.sources.common import verra_default_headers


def get_retirements_list(from_date: dt.date | None = None):
    with httpx.Client(headers=verra_default_headers) as client:
        query_filter = "startswith(retirementDetails,'stellarcarbon')"
        if from_date:
            iso_date = dt.datetime(from_date.year, from_date.month, from_date.day).isoformat()
            query_filter = f"({query_filter} and retireOrCancelDate ge {iso_date}.000Z)"

        headers = {
            "accept": "application/json",
            "referer": "https://registry.verra.org/app/search/VCS",
        }
        query_params = {
            "maxResults": 2000,
            "$filter": query_filter,
            "$count": True,
            "$orderby": "",
            "$skip": 0,
        }
        payload = {
            "program": "VCS",
            "assetStatus": "RETIRED",
            "issuanceTypeCodes": ["ISSUE"],
        }
        resp: httpx.Response = client.post(
            url=VERRA_ASSET_SEARCH_URL,
            headers=headers,
            params=query_params,
            json=payload,
            timeout=VERRA_ASSET_SEARCH_TIMEOUT
        )

    retirements_data = format_verra_retirements(resp.text)
    total_amount_retired = sum(
        rtm['vcu_amount'] 
        for rtm in retirements_data['retirements']
    )

    return {'total_amount_retired': total_amount_retired, **retirements_data}


def format_verra_retirements(retirements_payload: str):
    root = Selector(text=retirements_payload)
    total_count: int = int(root.jmespath('totalCount').get(default='0'))
    count_exceeded: bool = True if root.jmespath('countExceeded').get() == 'true' else False
    item_multiselect = """
        value[].{
            issuance_date: issuanceDate, 
            instrument_type: instrumentType,
            vintage_start: vintageStart,
            vintage_end: vintageEnd,
            total_vintage_quantity: totalVintageQuantity,
            vcs_id: resourceIdentifier,
            vcs_name: resourceName,
            vcs_category: protocolCategory,
            vcs_protocol: protocol,
            additional_certifications: additionalCertifications,
            region: region,
            country: country,
            vcu_amount: quantity,
            serial_numbers: serialNumbers,
            retirement_date: retireOrCancelDate,
            retirement_beneficiary: retirementBeneficiary,
            retirement_details: retirementDetails,
            certificate_id: holdingIdentifier
        }
    """
    items = root.jmespath(item_multiselect).getall()

    return {
        'total_count': total_count,
        'count_exceeded': count_exceeded,
        'retirements': items,
    }
