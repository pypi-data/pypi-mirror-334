#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typer
from rich import print
from rich.markup import escape
from typing import List

from centralcli import cli, utils
from . import cnxapi, cnx_client, CLIUpdateOptions, CLIArgs, auth
from enum import Enum
from centralcli.cnxcli.models.local_management import LocalManagementprofile, Console, AuthenticationMgmt, Authentication, AuthenticationGroupItem, AccessGroupItem, SessionType, AuthInstance

cli_options = CLIUpdateOptions(cli.cache)
cli_args = CLIArgs(cli.cache)

app = typer.Typer()
app.add_typer(auth.app, name="auth")

class DevType(str, Enum):
    ap = "AP"
    gw = "GATEWAYS"
    cx = "SWITCH"
    sw = "SWITCH"

class PasswdFormat(str, Enum):
    clear = "CLEARTEXT"
    cipher = "CIPHERTEXT"
    sha1 = "SHA1"
    sha256 = "SHA256"

class RoleName(str, Enum):
    root = "ROOT"
    guest_provisioning = "GUEST_PROVISIONING"
    network_operations = "NETWORK_OPERATIONS"
    read_only = "READ_ONLY"
    location_api_mgmt = "LOCATION_API_MGMT"
    nbapi_mgmt = "NBAPI_MGMT"
    ap_provisioning = "AP_PROVISIONING"
    standard = "STANDARD"
    local = "LOCAL"

class CXUserGroup(str, Enum):
    administrators = "administrators"
    operators = "operators"
    auditors = "auditors"

class UserMgmtInterface(str, Enum):
    ssh = "ssh"
    telnet = "telnet"
    https_server = "https-server"
    console = "console"

class AliasType(str, Enum):
    ALIAS_HOST = "HOST"
    ALIAS_NETWORK = "NETWORK"
    ALIAS_NETWORK_GROUP = "NETWORK_GROUP"
    ALIAS_SERVICE_GROUP = "SERVICE_GROUP"
    ALIAS_VLAN = "VLAN"
    ALIAS_ESSID = "ESSID"
    ALIAS_ECHO_SOURCE_ADDRESS = "ECHO_SOURCE_ADDRESS"
    ALIAS_HOSTNAME = "HOSTNAME"
    ALIAS_NETWORK_DESTINATION = "NETWORK_DESTINATION"
    ALIAS_IPV4_SYSTEM_VLAN = "IPV4_SYSTEM_VLAN"
    ALIAS_IPV4_PREFIX = "IPV4_PREFIX"
    ALIAS_IPV6_PREFIX = "IPV6_PREFIX"
    ALIAS_L3_VLAN_ADDRESS = "L3_VLAN_ADDRESS"
    ALIAS_DEVICE_SERIAL = "DEVICE_SERIAL"
    ALIAS_VSF_LINK = "VSF_LINK"

CLIUpdateOptions.set_name("mgmt-user")
@app.command()
def mgmt_users(
    name: str = typer.Argument(..., help="The name of the existing mgmt user to update", show_default=False,),
    local: bool = typer.Option(False, "-L", "--local", help=f"Update Local Object, [grey42]{escape('[default: SHARED]')}[/]", show_default=False,),
    scope: int = typer.Option(None, help="Mandatory Scope when updating local object, should bot be provided if updating SHARED (library) object",),
    # dev_type: DevType = typer.Option(None, help="Mandatory when updating local object, should bot be provided if updating SHARED (library) object",),
    switch: bool = typer.Option(None, "--sw", "--cx", "--switch", help="Update mgmt user for switch persona"),
    gw: bool = typer.Option(None, help="Update mgmt user for gateway persona"),
    ap: bool = typer.Option(None, help="Update mgmt user for gateway persona"),
    min_passwd_len: int = typer.Option(None, "--min-len"),
    aging_period: int = typer.Option(None,),
    max_concurrent_sessions: int = typer.Option(None, "--max-sessions"),
    format: PasswdFormat = typer.Option(None, "-F", "--format"),
    passwd: str = typer.Option(None),
    old_passwd: str = typer.Option(None),
    role: RoleName = typer.Option(None,),
    cx_group: CXUserGroup = typer.Option(None,),
    interfaces: List[UserMgmtInterface] = typer.Option(None, "-i", "--interfaces",),
    public_key: str = typer.Option(None, "-k", "--key"),
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    object_type = None if not local else "LOCAL"  # defaults to SHARED
    persona = None
    if any([switch, ap, gw]):
        if switch:
            persona = "SWITCH"
        elif ap:
            persona = "AP"
        elif gw:
            persona = "GATEWAYS"

    kwargs = {
        "object_type": object_type,
        "scope_id": scope,
        "persona": persona,
        "min_passwd_len": min_passwd_len,
        "aging_period": aging_period,
        "max_concurrent_sessions": max_concurrent_sessions,
        "format": None if not format else format.value,
        "old_passwd": old_passwd,
        "role": role,
        "user_group": cx_group,
        "interfaces": interfaces,
        "public_key": public_key,
    }
    if passwd:
        if format and format == PasswdFormat.cipher and persona in ["SWITCH", "AP", "GATEWAYS"]:
            kwargs["ciphertext-passwd"] = passwd
        else:
            kwargs["passwd"] = passwd

    resp = cnx_client.request(
        cnxapi.update_mgmt_user, name, **kwargs
    )
    cli.display_results(resp, tablefmt="action",)


CLIUpdateOptions.set_name("alias")
@app.command()
def alias(
    name: str = cli_args.name,
    local: bool = cli_options.local,
    scope: int = cli_options.scope,
    switch: bool = cli_options.switch,
    gw: bool = cli_options.gw,
    ap: bool = cli_options.ap,
    alias_type: AliasType = typer.Option(None, "--type",),
    description: str = typer.Option(None),
    hostname: str = typer.Option(None, "--hostname"),
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    # TODO need to fetch and or cache aliases we can derive the type from the response
    if name == "sys_host_name" and not alias_type:
        alias_type = AliasType.ALIAS_HOSTNAME

    object_type = None if not local else "LOCAL"  # defaults to SHARED

    # TODO catch for all if object_type = local and no scope is provided
    persona = None
    if any([switch, ap, gw]):
        if switch:
            persona = "SWITCH"
        elif ap:
            persona = "AP"
        elif gw:
            persona = "GATEWAYS"

    if (scope or persona) and not object_type:
        object_type = "LOCAL"
    if object_type == "LOCAL" and not all([scope, persona]):
        cli.exit("Scope and persona are [bright_green]both required[/] when updating a [cyan]LOCAL[/] alias.  Neither should be provided when updating a [cyan]SHARED[/] alias")

    kwargs = {
        "object_type": object_type,
        "scope_id": scope,
        "persona": persona,
        "alias_type": alias_type.name,
        "description": description,
        "hostname": hostname,
    }


    resp = cnx_client.request(
        cnxapi.update_aliases, name, **kwargs
    )
    cli.display_results(resp, title="Management Users",)


cli_options = CLIUpdateOptions(cli.cache, "VLAN")
@app.command()
def vlan(
    pvid: str = cli_args.pvid,
    local: bool = cli_options.local,
    scope: int = cli_options.scope,
    switch: bool = cli_options.switch,
    gw: bool = cli_options.gw,
    ap: bool = cli_options.ap,
    name: str = cli_options.name,
    description: str = typer.Option(None, help="update the VLAN description", show_default=False,),
    dhcpv4_snoop: bool = typer.Option(None, help="Disable/Enable DHCPv4 Snooping", show_default=False,),
    dhcpv6_snoop: bool = typer.Option(None, help="Disable/Enable DHCPv6 Snooping", show_default=False,),
    track_ip: bool = typer.Option(None, help="Disable/Enable IP client tracker", show_default=False,),
    enable: bool = typer.Option(None, "-E", "--enable", help="admin enable the VLAN", show_default=False,),
    disable: bool = typer.Option(None, "-D", "--disable", help="admin disable the VLAN", show_default=False,),
    yes: bool = cli.options.yes,
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    object_type = None if not local else "LOCAL"  # defaults to SHARED

    # TODO catch for all if object_type = local and no scope is provided
    persona = None
    if any([switch, ap, gw]):
        if switch:
            persona = "SWITCH"
        elif ap:
            persona = "AP"
        elif gw:
            persona = "GATEWAYS"

    if (scope or persona) and not object_type:
        object_type = "LOCAL"
    if object_type == "LOCAL" and not all([scope, persona]):
        cli.exit("Scope and persona are [bright_green]both required[/] when updating a [cyan]LOCAL[/] alias.  Neither should be provided when updating a [cyan]SHARED[/] alias")

    _enable = None
    if enable:
        if disable:
            cli.exit("You can't [cyan]--enable[/] [bold]AND[/] [cyan]--disable[/] a VLAN.  Pick one!")
        _enable = True
    elif disable:
        _enable = False

    kwargs = {
        "object_type": object_type,
        "scope_id": scope,
        "persona": persona,
        "description": description,
        "track_ip": track_ip,
        "name": name,
        "enable": _enable,
        "dhcpv4_snooping": dhcpv4_snoop,
        "dhcpv6_snooping": dhcpv6_snoop
    }

    # TODO common confirmation builder for scope
    conf_msg = f"Updat{'e' if not yes else 'ing'} VLAN [cyan]{pvid}[/] with the following:"
    conf_items = utils.color([f'{k}[reset]: [bright_green]{str(v)}[/]' for k, v in kwargs.items() if v is not None], pad_len=4, sep="\n")
    cli.econsole.print(f'{conf_msg}\n{conf_items}')
    if cli.confirm(yes):
        ... # confrim aborts
    resp = cnx_client.request(
        cnxapi.update_vlan, pvid, **kwargs
    )
    cli.display_results(resp, tablefmt="action")


cli_options = CLIUpdateOptions(cli.cache, "local mgmt profile")
@app.command()
def local_mgmt(
    name: str = cli_args.name,
    description: str = cli_options.description,
    login_session_timeout: int = typer.Option(None,),
    ssh_primary_auth_group: str = typer.Option(None,),
    ssh_secondary_auth_group: str = typer.Option(None,),
    # ssh_timeout: int = typer.Option(None,),
    console_primary_auth_group: str = typer.Option(None,),
    console_secondary_auth_group: str = typer.Option(None,),
    console_timeout: int = typer.Option(None,),
    local: bool = cli_options.local,
    scope: int = cli_options.scope,
    switch: bool = cli_options.switch,
    gw: bool = cli_options.gw,
    ap: bool = cli_options.ap,
    yes: bool = cli.options.yes,
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    object_type = None if not local else "LOCAL"  # defaults to SHARED

    # TODO catch for all if object_type = local and no scope is provided
    persona = None
    if any([switch, ap, gw]):
        if switch:
            persona = "SWITCH"
        elif ap:
            persona = "AP"
        elif gw:
            persona = "GATEWAYS"

    if (scope or persona) and not object_type:
        object_type = "LOCAL"
    if object_type == "LOCAL" and not all([scope, persona]):
        cli.exit("Scope and persona are [bright_green]both required[/] when updating a [cyan]LOCAL[/] alias.  Neither should be provided when updating a [cyan]SHARED[/] alias")

    con_auth_config = None
    if any(console_secondary_auth_group):
        auth_primary = AuthInstance(seq_id=1, auth_method="LOCAL")
        auth_secondary = AuthInstance(seq_id=2, auth_method="TACACS", mgmt_server_group=console_secondary_auth_group)
        con_ag = AccessGroupItem(access_type="LOGIN",  auth_instances=[auth_primary, auth_secondary], )
        con_auth_group = AuthenticationGroupItem(session="CONSOLE", access_group=[con_ag])
        con_auth_config = Authentication(authentication_group=[con_auth_group], enable=True)

    console_cfg = None if not console_timeout else Console(idle_timeout=console_timeout)


    profile = LocalManagementprofile(
        name=name,
        description=description,
        login_session_timeout=login_session_timeout,
        authentication=con_auth_config,
        console=console_cfg,
    )


    kwargs = {
        "profile": profile,
        "object_type": object_type,
        "scope_id": scope,
        "persona": persona
    }

    conf_msg = f"Updat{'e' if not yes else 'ing'} local mgmt profile [cyan]{name}[/] with the following:"
    conf_items = utils.color([f'{k}[reset]: [bright_green]{str(v)}[/]' for k, v in kwargs.items() if v is not None], pad_len=4, sep="\n")
    cli.econsole.print(f'{conf_msg}\n{conf_items}')
    if cli.confirm(yes):
        ... # confrim aborts
    resp = cnx_client.request(
        cnxapi.update_local_mgmt_profile, **kwargs
    )
    cli.display_results(resp, tablefmt="action")




@app.callback()
def callback():
    """
    update CNX stuff
    """
    pass


if __name__ == "__main__":
    print("cnx show hit")
    app()
