"""Central CNX API

This is temporary, once programatic parsing of openapi specs is complete the api folder will be broken into
numerous files for the various api endpoints
"""

from typing import Literal, List, Dict, Any
from cnxcli import utils, cnx_client
from cnxcli.models.auth_server_global import AuthServerType, PasswordType, AuthServerGlobalConfigProfile
from cnxcli.models.local_management import LocalManagementprofile


from centralcli import Response


ViewType = Literal["LIBRARY", "LOCAL"]
ObjectTypeGet = Literal["LOCAL", "SHARED", "BOTH"]
ObjectType = Literal["LOCAL", "SHARED"]
PersonaType = Literal["SWITCH", "GATEWAYS", "AP", "ALL"]
PasswdFormat = Literal["CLEARTEXT", "CIPHERTEXT", "SHA1", "SHA256"]
RoleName = Literal["ROOT", "GUEST_PROVISIONING", "NETWORK_OPERATIONS", "READ_ONLY", "LOCATION_API_MGMT", "NBAPI_MGMT", "AP_PROVISIONING", "STANDARD", "LOCAL"]
CXUserGroup = Literal["administrators", "operators", "auditors"]
UserMgmtInterface = Literal["ssh", "telnet", "https-server", "console"]
AliasType = Literal[
    "ALIAS_HOST",
    "ALIAS_NETWORK",
    "ALIAS_NETWORK_GROUP",
    "ALIAS_SERVICE_GROUP",
    "ALIAS_VLAN",
    "ALIAS_ESSID",
    "ALIAS_ECHO_SOURCE_ADDRESS",
    "ALIAS_HOSTNAME",
    "ALIAS_NETWORK_DESTINATION",
    "ALIAS_IPV4_SYSTEM_VLAN",
    "ALIAS_IPV4_PREFIX",
    "ALIAS_IPV6_PREFIX",
    "ALIAS_L3_VLAN_ADDRESS",
    "ALIAS_DEVICE_SERIAL",
    "ALIAS_VSF_LINK"
]

# TODO move to api.common
async def _prep_params(view_type: ViewType = None, object_type: ObjectType = None, scope_id: int = None, persona: PersonaType = None, effective: bool = None, detailed: bool = None) -> Dict[str, Any]:
    effective = None if effective is None else str(effective).lower()
    detailed = None if detailed is None else str(detailed).lower()
    params = utils.strip_none(
        {
            "view_type": view_type,
            "object_type": None if not object_type or object_type == "BOTH" else object_type,
            "scope_id": scope_id,
            "persona": None if not persona or persona == "ALL" else persona,
            "effective": effective,
            "detailed": detailed
        }
    )

    return params

async def get_mgmt_users(
    view_type: ViewType = "LIBRARY",
    object_type: ObjectTypeGet = "BOTH",
    scope_id: int = None,
    persona: PersonaType = "ALL",
    effective: bool = False,
    detailed: bool = False,

):
    url = "/network-config/v1alpha1/management-users"
    params = await _prep_params(view_type=view_type, object_type=object_type, scope_id=scope_id, persona=persona, effective=effective, detailed=detailed)

    return await cnx_client.get(url, params=params, data_key="user")

async def get_system_info(
    view_type: ViewType = None,
    object_type: ObjectTypeGet = "BOTH",
    scope_id: int = None,
    persona: PersonaType = "ALL",
    effective: bool = None,
    detailed: bool = None,

):
    url = "/network-config/v1alpha1/system-info"
    params = await _prep_params(view_type=view_type, object_type=object_type, scope_id=scope_id, persona=persona, effective=effective, detailed=detailed)

    return await cnx_client.get(url, params=params)


async def get_aliases(
    view_type: ViewType = None,
    object_type: ObjectTypeGet = "BOTH",
    scope_id: int = None,
    persona: PersonaType = "ALL",
    effective: bool = None,
    detailed: bool = None,

):
    url = "/network-config/v1alpha1/aliases"
    params = await _prep_params(view_type=view_type, object_type=object_type, scope_id=scope_id, persona=persona, effective=effective, detailed=detailed)

    return await cnx_client.get(url, params=params, data_key="alias")


async def get_auth_servers(
    view_type: ViewType = None,
    object_type: ObjectTypeGet = "BOTH",
    scope_id: int = None,
    persona: PersonaType = "ALL",
    effective: bool = None,
    detailed: bool = None,

):
    url = "/network-config/v1alpha1/auth-servers"
    params = await _prep_params(view_type=view_type, object_type=object_type, scope_id=scope_id, persona=persona, effective=effective, detailed=detailed)

    return await cnx_client.get(url, params=params, data_key="auth-server")


async def get_auth_server_global(
    view_type: ViewType = None,
    object_type: ObjectTypeGet = "BOTH",
    scope_id: int = None,
    persona: PersonaType = "ALL",
    effective: bool = None,
    detailed: bool = None,

):
    url = "/network-config/v1alpha1/auth-server-global-config"
    params = await _prep_params(view_type=view_type, object_type=object_type, scope_id=scope_id, persona=persona, effective=effective, detailed=detailed)

    return await cnx_client.get(url, params=params, data_key="profile")


async def get_switch_profiles(
    view_type: ViewType = None,
    object_type: ObjectTypeGet = "BOTH",
    scope_id: int = None,
    persona: PersonaType = "ALL",
    effective: bool = None,
    detailed: bool = None,

):
    url = "/network-config/v1alpha1/switch-profiles"
    params = utils.strip_none(
        {
            "view_type": view_type,
            "object_type": None if not object_type or object_type == "BOTH" else object_type,
            "scope_id": scope_id,
            "persona": None if not persona or persona == "ALL" else persona,
            "effective": str(effective).lower(),
            "detailed": str(detailed).lower()
        }
    )

    return await cnx_client.get(url, params=params, data_key="profile")


async def get_switch_system(
    view_type: ViewType = None,
    object_type: ObjectTypeGet = "BOTH",
    scope_id: int = None,
    persona: PersonaType = "ALL",
    effective: bool = None,
    detailed: bool = None,

):
    url = "/network-config/v1alpha1/switch-system"
    params = await _prep_params(view_type=view_type, object_type=object_type, scope_id=scope_id, persona=persona, effective=effective, detailed=detailed)

    return await cnx_client.get(url, params=params, data_key="profile")


async def get_snmp_profiles(
    view_type: ViewType = None,
    object_type: ObjectTypeGet = "BOTH",
    scope_id: int = None,
    persona: PersonaType = "ALL",
    effective: bool = None,
    detailed: bool = None,

):
    url = "/network-config/v1alpha1/snmp"
    params = await _prep_params(view_type=view_type, object_type=object_type, scope_id=scope_id, persona=persona, effective=effective, detailed=detailed)
    return await cnx_client.get(url, params=params, data_key="profile")


async def get_vlans(
    view_type: ViewType = None,
    object_type: ObjectTypeGet = "BOTH",
    scope_id: int = None,
    persona: PersonaType = "ALL",
    effective: bool = None,
    detailed: bool = None,

):
    url = "/network-config/v1alpha1/layer2-vlan"
    params = await _prep_params(view_type=view_type, object_type=object_type, scope_id=scope_id, persona=persona, effective=effective, detailed=detailed)

    return await cnx_client.get(url, params=params, data_key="l2-vlan")


async def get_scopes(
    view_type: ViewType = None,
    object_type: ObjectTypeGet = "BOTH",
    scope_id: int = None,
    persona: PersonaType = "ALL",
    effective: bool = None,
    detailed: bool = None,

):
    url = "/network-config/v1alpha1/scope-maps"
    params = await _prep_params(view_type=view_type, object_type=object_type, scope_id=scope_id, persona=persona, effective=effective, detailed=detailed)

    return await cnx_client.get(url, params=params, data_key="scope-map")


async def get_local_management(
    view_type: ViewType = None,
    object_type: ObjectTypeGet = "BOTH",
    scope_id: int = None,
    persona: PersonaType = "ALL",
    effective: bool = None,
    detailed: bool = None,

):
    url = "/network-config/v1alpha1/local-management"
    params = await _prep_params(view_type=view_type, object_type=object_type, scope_id=scope_id, persona=persona, effective=effective, detailed=detailed)

    return await cnx_client.get(url, params=params, data_key="profile")

async def update_mgmt_user(
    name: str,
    object_type: ObjectType = "SHARED",
    scope_id: int = None,
    persona: PersonaType = None,
    *,
    min_passwd_len: int = None,  # pvos 8-64
    aging_period: int = None, # pvos 1-365
    max_concurrent_sessions: int = None, # gw 0-32  0 = unset
    format: PasswdFormat = "CLEARTEXT", # AP, SW ... ap cleartext, ciphertext | pvos ?
    passwd: str = None, # AP CX GW, max 9999
    ciphertext_passwd: str = None, # AP, CX, GW
    old_passwd: str = None,  # AP, CX, GW
    role: RoleName = None,  # GW, AP
    user_group: CXUserGroup = None, # CX
    interfaces: List[UserMgmtInterface] = None, # CX
    public_key: str = None, # CX, SW
) -> Response:
    url = f"/network-config/v1alpha1/management-users/{name}"
    if object_type and object_type.upper() == "LOCAL" and (not scope_id or not persona):
        raise ValueError("scope_id and persona are mandatory if object_type is LOCAL")

    params = utils.strip_none(
        {
            "object_type": object_type,
            "scope_id": scope_id,
            "persona": persona,
        }
    )
    json_data = {
        "name": name,
        "min-password-length": min_passwd_len,
        "aging-period": aging_period,
        "max-concurrent-sessions": max_concurrent_sessions,
        "format": format,
        "password": passwd,
        "ciphertext-password": ciphertext_passwd,
        "old-password": old_passwd,
        "rolename": role,
        "user-group": user_group
    }
    json_data = utils.strip_none(json_data)

    if interfaces:
        interface_names = ["ssh", "telnet", "https-server", "console"]
        json_data["interface"] = {k: True if k in interfaces else False for k in interface_names}

    if public_key:
        json_data["authorized-key"] = [
            {"public-key": public_key}
        ]

    return await cnx_client.patch(url, params=params, json_data=json_data)

async def update_aliases(
    name: str,
    alias_type: AliasType,
    object_type: ObjectType = "SHARED",
    scope_id: int = None,
    persona: PersonaType = None,
    *,
    description: str = None,
    hostname: str = None,
    host_ip: str = None,
    host_ipv6: str = None,
    network: str = None,
    networkv6: str = None,
    vlan_id_ranges: List[str] = None,
    essid: str = None,
    bfd_echo_source: str = None,
    ipv4_system_vlan: int = None
) -> Response:
    url = f"/network-config/v1alpha1/aliases/{name}"
    if object_type and object_type.upper() == "LOCAL" and (not scope_id or not persona):
        raise ValueError("scope_id and persona are mandatory if object_type is LOCAL")

    params = utils.strip_none(
        {
            "object_type": object_type,
            "scope_id": scope_id,
            "persona": persona,
        }
    )
    values = {}
    if host_ip or host_ipv6:
        values["host-address-value"] = {}
        if host_ip:
            values["host-address-value"]["host-ipv4-address"] = host_ip
        if host_ipv6:
            values["host-address-value"]["host-ipv6-address"] = host_ipv6
    if hostname:
        values["hostname-value"] = {"hostname": hostname}
    if network or networkv6:
        values["network-address-value"] = {}
        if network:
            values["network-address-value"]["network-ipv4-address"] = network
        if networkv6:
            values["network-address-value"]["network-ipv6-address"] = networkv6
    if vlan_id_ranges:
        values["vlan-value"]["vlan-id-ranges"] = vlan_id_ranges
    if essid:
        values["essid-value"]["name"] = essid
    if bfd_echo_source:
        values["bfd-echo-source-address"]["name"] = bfd_echo_source
    if ipv4_system_vlan:
        values["ipv4-system-vlan-value"]["vlan-id"] = ipv4_system_vlan

    if not values:
        raise ValueError("No Values provided to update")

    json_data = {
        "name": name,
        "description": description,
        "type": alias_type,
        "default-value": values
    }
    json_data = utils.strip_none(json_data, strip_empty_obj=True)
    return await cnx_client.patch(url, params=params, json_data=json_data)

async def update_vlan(
    pvid: int,
    object_type: ObjectType = "SHARED",
    scope_id: int = None,
    persona: PersonaType = None,
    *,
    name: str = None,
    description: str = None,
    dhcpv4_snooping: bool = None,
    dhcpv6_snooping: bool = None,
    track_ip: bool = None,
    enable: bool = None,
    networkv6: str = None,
    vlan_id_ranges: List[str] = None,
    essid: str = None,
    bfd_echo_source: str = None,
    ipv4_system_vlan: int = None
) -> Response:
    url = f"/network-config/v1alpha1/layer2-vlan/{pvid}"
    if object_type and object_type.upper() == "LOCAL" and (not scope_id or not persona):
        raise ValueError("scope_id and persona are mandatory if object_type is LOCAL")

    params = utils.strip_none(
        {
            "object_type": object_type,
            "scope_id": scope_id,
            "persona": persona,
        }
    )

    json_data = {
        "name": name,
        "description": description,
        "client-ip-tracker-enable": track_ip,
        "enable": enable
    }
    if dhcpv4_snooping is not None:
        json_data["dhcpv4-snooping"] = {"enable": dhcpv4_snooping}
        # TODO ip-binding-enable
    if dhcpv6_snooping is not None:
        json_data["dhcpv6-snooping"] = {"enable": dhcpv6_snooping}

    json_data = utils.strip_none(json_data, strip_empty_obj=True)
    return await cnx_client.patch(url, params=params, json_data=json_data)

async def update_auth_server_global(
    profile: AuthServerGlobalConfigProfile,
    object_type: ObjectType = "SHARED",
    scope_id: int = None,
    persona: PersonaType = None,
    # *,
    # auth_server_type: AuthServerType = None,
    # description: str = None,
    # retries: int = None,
    # shared_secret: str = None,
    # secret_type: PasswordType = None,
    # track_ip: bool = None,
    # enable: bool = None,
    # networkv6: str = None,
    # vlan_id_ranges: List[str] = None,
    # essid: str = None,
    # bfd_echo_source: str = None,
    # ipv4_system_vlan: int = None
) -> Response:
    url = f"/network-config/v1alpha1/auth-server-global-config/{profile.name}"
    if object_type and object_type.upper() == "LOCAL" and (not scope_id or not persona):
        raise ValueError("scope_id and persona are mandatory if object_type is LOCAL")

    params = utils.strip_none(
        {
            "object_type": object_type,
            "scope_id": scope_id,
            "persona": persona,
        }
    )

    json_data = profile.model_dump(by_alias=True)
    json_data = utils.strip_none(json_data, strip_empty_obj=True)

    return await cnx_client.post(url, params=params, json_data=json_data)

async def update_local_mgmt_profile(
    profile: LocalManagementprofile,
    object_type: ObjectType = "SHARED",
    scope_id: int = None,
    persona: PersonaType = None,
) -> Response:
    url = f"/network-config/v1alpha1/local-management/{profile.name}"
    if object_type and object_type.upper() == "LOCAL" and (not scope_id or not persona):
        raise ValueError("scope_id and persona are mandatory if object_type is LOCAL")

    params = utils.strip_none(
        {
            "object_type": object_type,
            "scope_id": scope_id,
            "persona": persona,
        }
    )

    json_data = profile.model_dump(by_alias=True)
    json_data = utils.strip_none(json_data, strip_empty_obj=True)

    return await cnx_client.post(url, params=params, json_data=json_data)


async def assign_profile_to_scope(
    profile_path: str,
    object_type: ObjectType = "SHARED",
    scope_id: int = None,
    persona: PersonaType = None,
) -> Response:
    """Assign Profile (from library) to Scope

    Args:
        profile_name (str): The resource/profile name This is a 2 part path i.e.
        object_type (ObjectType, optional): The Central object_type SHARED or LOCAL. Defaults to "SHARED".
        scope_id (int, optional): Scope id to assign profile to. Defaults to None.
        persona (PersonaType, optional): Central persona SWITCH.  This is an expanded list of personas with multiple device tier personas.  i.e . Defaults to None.

    Raises:
        ValueError: Raises Value Error if updating a local object without all required arguments

    Returns:
        Response: Resonse object
    """
    url = "/network-config/v1alpha1/scope-maps"
    if object_type and object_type.upper() == "LOCAL" and (not scope_id or not persona):
        raise ValueError("scope_id and persona are mandatory if object_type is LOCAL")

    json_data = {
        "scope-map": [
            {
                "scope-name": str(scope_id),
                "persona": persona,
                "resource": profile_path,
            }
        ]
    }

    return await cnx_client.post(url, params={}, json_data=json_data)