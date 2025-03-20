from __future__ import annotations

from typing import List, Dict, Any
from centralcli.cleaner import simple_kv_formatter
from . import log

import json

def layer2_vlans(data: List[dict]):
    if not isinstance(data, list):
        return data
    key_order = [
        "vlan",
        "name",
        "description",
        "enable",
        "dhcpv4-snooping",
        "dhcpv6-snooping",

    ]
    all_keys = list(set([key for d in data for key in d.keys()]))
    all_keys = [*key_order, *all_keys]
    # this will ensure all fields have consistent keys and strip nested items where the only values are {enable: bool}
    data = [{k: d.get(k) if not isinstance(d.get(k), dict) or len(d[k]) > 1 else d[k].get("enable", d[k]) for k in all_keys} for d in data]

    return simple_kv_formatter(data, emoji_bools=True)

def mgmt_users(data: List[Dict[str, Any]]) -> List[dict] | Dict[str, Any]:
    return [{k if k != "authorized-key" else "public-keys": v if k != "authorized-key" else [vv.get("public-key", vv) for vv in v] for k, v in d.items()} for d in data]

# TODO need display_results to check for "@" in output attribute and call this
def handle_annotations(data: Dict[str, Any]):
    """When CLI show commands use -v (verbose) we fetch detailed response which includes annotations.  This function formats the annotations for use in the caption.

    Args:
        data (Dict[str, Any]): The Response from CNX API GW

    Returns:
        Tuble[Dict[str, Any], str]: A Tuple with the response with annotations removed, and the caption str with the formatted annotation data.
    """
    if "@" not in data:
        return data

    annotations: Dict[str, Any] = data["@"].copy()
    del data["@"]

    annotations = {
        k.removeprefix("aruba-annotation:"): v for k, v in annotations.items()
    }

    scope_info = None
    if "scope_device_function" in annotations:
        try:
            scope_info: List[Dict[str, str]] = json.loads(annotations["scope_device_function"])
            scope_info = [{f'{k.removeprefix("scope_") if k != "device_function" else "persona"}: {v}' for k, v in d.items()} for d in scope_info]

            # annotations["scope"] = scope_info
            del annotations["scope_device_function"]
        except Exception as e:
            log.exception(f"{e.__class__.__name__} Exception while handling annotations (scope_device_function)\n{e}")

    caption = "|".join([f'{k}: {v}' for k, v in annotations.items()])
    if scope_info:
        scope_info_str = "|".join([f'{k}: {v}' for k, v in scope_info.items()])
        caption = f'{caption}\n[bright_green]Scope Info[/]: {scope_info_str}'

    return data, caption

    # TODO common cleaner for output of -v commands (detailed)
    # Unformatted response from Aruba Central API GW
    # {
    #     '@': {
    #         'aruba-annotation:object_type': 'LOCAL',
    #         'aruba-annotation:scope_device_function': "[{'scope_id': '326437008', 'device_function': 'SWITCH', 'scope_type': 'DEVICE', 'scope_name': 'SG90KN00N5'}]",
    #         'aruba-annotation:inherited': False,
    #         'aruba-annotation:overridden_scope': 'GLOBAL',
    #         'aruba-annotation:overriding_scopes_count': 0,
    #         'aruba-annotation:is_editable': True,
    #         'aruba-annotation:is_default': False,
    #         'aruba-annotation:device_scope_only': False
    #     },
    #     'hostname-alias': 'sys_host_name',
    #     'contact': 'wade@hpe.com',
    #     'location': 'WadeLab Rack1'
    # }