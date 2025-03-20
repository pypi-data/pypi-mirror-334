#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typer

from centralcli import cli
from . import cnxapi, cnx_client, CLIGetOptions
from cnxcli.clitree import common


app = typer.Typer()
options = CLIGetOptions(cli.cache, "switch profiles")
@app.command()
def profiles(
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
    resp = cnx_client.request(cnxapi.get_switch_profiles, **params)
    cli.display_results(resp, title="Switch Profiles",)


app = typer.Typer()
options = CLIGetOptions(cli.cache, "switch system")
@app.command()
def system(
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
    resp = cnx_client.request(cnxapi.get_switch_system, **params)
    cli.display_results(resp, title="Switch System",)




@app.callback()
def callback():
    """
    Show details about switches
    """
    pass


if __name__ == "__main__":
    app()