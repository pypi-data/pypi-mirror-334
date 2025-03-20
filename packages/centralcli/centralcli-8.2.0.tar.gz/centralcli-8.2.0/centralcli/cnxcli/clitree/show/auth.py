#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typer

from centralcli import cli
from . import cnxapi, cnx_client, CLIGetOptions
from cnxcli.clitree import common


app = typer.Typer()
options = CLIGetOptions(cli.cache)
@app.command()
def servers(
    local: bool = options.local,
    shared: bool = options.shared,
    switch: bool = options.switch,
    ap: bool = options.ap,
    gw: bool = options.gw,
    scope: int = options.scope,
    effective: bool = options.effective,
    _global: bool = typer.Option(False, "-G", "--global", help="Get Auth Server Global Config.  [italic]Not to be confused with Global Scope[/]"),
    verbose: int = cli.options.verbose,
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    params = common.get_params(local=local, shared=shared, scope=scope, switch=switch, ap=ap, gw=gw, detailed=True if verbose else None, effective=effective)
    if not _global:
        resp = cnx_client.request(cnxapi.get_auth_servers, **params)
    else:
        resp = cnx_client.request(cnxapi.get_auth_server_global, **params)

    cli.display_results(resp, title="Auth Servers",)




@app.callback()
def callback():
    """
    Show auth servers/details
    """
    pass


if __name__ == "__main__":
    app()