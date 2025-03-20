#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typer
from rich import print


from centralcli import cli
from . import cnxapi, cnx_client, CLIGetOptions, auth, switch, cnx_cleaner
from cnxcli.clitree import common
from enum import Enum
from pathlib import Path


app = typer.Typer()
app.add_typer(auth.app, name="auth")
app.add_typer(switch.app, name="switch")

options = CLIGetOptions(cli.cache)


@app.command()
def mgmt_users(
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    resp = cnx_client.request(cnxapi.get_mgmt_users)
    cli.display_results(resp, title="Management Users", cleaner=cnx_cleaner.mgmt_users)


@app.command()
def system_info(
    local: bool = options.local,
    shared: bool = options.shared,
    scope: int = options.scope,
    switch: bool = options.switch,
    ap: bool = options.ap,
    gw: bool = options.gw,
    effective: bool = options.effective,
    verbose: int = cli.options.verbose,
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    params = common.get_params(local=local, shared=shared, scope=scope, switch=switch, ap=ap, gw=gw, detailed=True if verbose else None, effective=effective)
    resp = cnx_client.request(cnxapi.get_system_info, **params)

    cli.display_results(resp, title="System Info",)


@app.command()
def aliases(
    local: bool = options.local,
    shared: bool = options.shared,
    switch: bool = options.switch,
    ap: bool = options.ap,
    gw: bool = options.gw,
    scope: int = options.scope,
    effective: bool = options.effective,
    verbose: int = cli.options.verbose,
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    params = common.get_params(local=local, shared=shared, scope=scope, switch=switch, ap=ap, gw=gw, detailed=True if verbose else None, effective=effective)
    resp = cnx_client.request(cnxapi.get_aliases, **params)
    cli.display_results(resp, title="Aliases",)


@app.command()
def snmp(
    local: bool = options.local,
    shared: bool = options.shared,
    switch: bool = options.switch,
    ap: bool = options.ap,
    gw: bool = options.gw,
    scope: int = options.scope,
    effective: bool = options.effective,
    verbose: int = cli.options.verbose,
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    params = common.get_params(local=local, shared=shared, scope=scope, switch=switch, ap=ap, gw=gw, detailed=True if verbose else None, effective=effective)
    resp = cnx_client.request(cnxapi.get_snmp_profiles, **params)
    cli.display_results(resp, title="SNMP Profiles",)

class SortVlans(str, Enum):
    vlan = "vlan",
    name = "name",
    description = "description",
    enable = "enabled",
    dhcpv4_snooping = "dhcpv4-snooping",
    dhcpv6_snooping = "dhcpv6-snooping",
    voice_enable = "voice",
    is_l3_vlan = "l3"

@app.command()
def vlans(
    local: bool = options.local,
    shared: bool = options.shared,
    switch: bool = options.switch,
    ap: bool = options.ap,
    gw: bool = options.gw,
    scope: int = options.scope,
    effective: bool = options.effective,
    verbose: int = cli.options.verbose,
    sort: SortVlans = cli.options.sort_by,
    pager: bool = cli.options.pager,
    out: Path = cli.options.outfile,
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    params = common.get_params(local=local, shared=shared, scope=scope, switch=switch, ap=ap, gw=gw, detailed=True if verbose else None, effective=effective)
    resp = cnx_client.request(cnxapi.get_vlans, **params)
    cli.display_results(resp, title="VLAN Configuration", cleaner=cnx_cleaner.layer2_vlans)

@app.command()
def scopes(
    local: bool = options.local,
    shared: bool = options.shared,
    switch: bool = options.switch,
    ap: bool = options.ap,
    gw: bool = options.gw,
    scope: int = options.scope,
    effective: bool = options.effective,
    verbose: int = cli.options.verbose,
    sort: SortVlans = cli.options.sort_by,
    pager: bool = cli.options.pager,
    out: Path = cli.options.outfile,
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    params = common.get_params(local=local, shared=shared, scope=scope, switch=switch, ap=ap, gw=gw, detailed=True if verbose else None, effective=effective)
    resp = cnx_client.request(cnxapi.get_scopes, **params)
    # resp = cnx_client.request(cnxapi.get_scopes, **{"view_type": "LIBRARY", **params})
    cli.display_results(resp, title="Scope Maps")

@app.command()
def local_mgmt(
    local: bool = options.local,
    shared: bool = options.shared,
    switch: bool = options.switch,
    ap: bool = options.ap,
    gw: bool = options.gw,
    scope: int = options.scope,
    effective: bool = options.effective,
    verbose: int = cli.options.verbose,
    do_yaml: bool = cli.options.do_yaml,
    do_table: bool = cli.options.do_table,
    do_csv: bool = cli.options.do_csv,
    do_json: bool = cli.options.do_json,
    raw: bool = cli.options.raw,
    sort: str = cli.options.sort_by,
    pager: bool = cli.options.pager,
    out: Path = cli.options.outfile,
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    params = common.get_params(local=local, shared=shared, scope=scope, switch=switch, ap=ap, gw=gw, detailed=True if verbose else None, effective=effective)
    tablefmt = cli.get_format(do_json=do_json, do_yaml=do_yaml, do_csv=do_csv, do_table=do_table, default="yaml")
    resp = cnx_client.request(cnxapi.get_local_management, **params)
    # resp = cnx_client.request(cnxapi.get_scopes, **{"view_type": "LIBRARY", **params})
    cli.display_results(resp, title="Scope Maps", tablefmt=tablefmt, sort=sort)


@app.callback()
def callback():
    """
    Show commands for Central Next Gen objects
    """
    pass


if __name__ == "__main__":
    print("cnx show hit")
    app()
