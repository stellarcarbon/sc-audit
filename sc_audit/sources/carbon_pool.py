"""
Fetch the current Carbon Pool inventory from the Verra Registry.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import httpx
from parsel import Selector

from sc_audit.constants import VERRA_REPORT_URL
from sc_audit.db_schema.mint import verra_carbon_pool
from sc_audit.sources.common import verra_default_headers


def get_carbon_pool_state():
    with httpx.Client(headers=verra_default_headers) as client:
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
            "referer": "https://www.stellarcarbon.io/",
        }
        query_params = {
            "r": 205,
            "idSubAccount": verra_carbon_pool.id,
        }
        resp: httpx.Response = client.get(
            url=VERRA_REPORT_URL,
            headers=headers,
            params=query_params,
        )

    inventory_table = parse_inventory_table(resp.text)
    total_inventory_credits = sum(
        quantity_of_credits
        for batch in inventory_table
        if isinstance(quantity_of_credits := batch.get('quantity_of_credits'), int)
    )
    return {
        'total_inventory_credits': total_inventory_credits,
        'credit_batches': inventory_table,
    }


def cast_int(possible_int: str) -> int | str:
    try:
        return int(possible_int)
    except ValueError:
        return possible_int


def parse_inventory_table(report_html: str) -> list[dict[str, int | str]]:
    root = Selector(text=report_html)
    table_header = root.xpath('//td/font[starts-with(text(),"Serial Number")]/ancestor::tr[1]')
    table = table_header.xpath('parent::table')
    batch_rows = table.xpath('tr[position()>1]')

    column_names: list[str] = table_header.xpath('td/font/text()').getall()
    row_keys: list[str] = [
        name.strip().lower().replace(' ', '_').replace('-', '_').replace('/', '_')
        for name in column_names
    ]

    batch_items = [
        dict(zip(row_keys, [
            cast_int(val)
            for val in br.xpath('td/font//text()').getall()
        ]))
        for br in batch_rows
    ]
    return batch_items
