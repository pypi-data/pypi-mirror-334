#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typer
from rich import print

from centralcli import cli
from . import cnxapi, cnx_client, CLIUpdateOptions, CLIArgs
from cnxcli.clitree import common
from enum import Enum

cli_options = CLIUpdateOptions(cli.cache, "profile")
cli_args = CLIArgs(cli.cache, "profile")

app = typer.Typer()

class Persona(str, Enum):
    MOBILITY_GW = "mobility-gw"
    BRANCH_GW = "branch-gw"
    VPNC = "vpnc"
    CAMPUS_AP = "campus-ap"
    MICROBRANCH_AP = "microbranch-ap"
    SWITCH = "switch"
    ALL = "all"
    SERVICE_PERSONA = "service-persona"
    BRIDGE = "bridge"
    IOT = "iot"
    HYBRID_NAC = "hybrid-nac"
    CORE_SWITCH = "core-switch"
    AGG_SWITCH = "agg-switch"


@app.command()
def profile(
    profile_path: str = typer.Argument(..., help="The resource_path/profile to assign.  Should be in the format 'RESOURCE_PATH/PROFILE_NAME. i.e. 'auth-server-global-config/global-auth'", show_default=False,),
    scope: int = typer.Argument(..., help="Scope to assign profile to", show_default=False,),
    persona: Persona = typer.Option(None, "-P", "--persona", help=f"Persona to associate profile to {common.help_default('ALL')}", show_default=False,),
    local: bool = typer.Option(False, "-L", "--local", help=f"Update Local Object {common.help_default('SHARED')}", show_default=False,),
    # switch: bool = typer.Option(None, "--sw", "--cx", "--switch", help="Update mgmt user for switch persona"),
    # gw: bool = typer.Option(None, help="Update mgmt user for gateway persona"),
    # ap: bool = typer.Option(None, help="Update mgmt user for gateway persona"),
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    """Assign Library profile to scope/persona"""
    object_type = None if not local else "LOCAL"  # defaults to SHARED
    if "/" not in profile_path:
        cli.exit("The resource should include the path and the profile name.  i.e. 'system-info/name-of-profile'")

    kwargs = {
        "object_type": object_type,
        "scope_id": scope,
        "persona": persona if not persona else persona.name,
    }

    # NOTE: had to send name as 'auth-server-global-config/global-auth' for it to work.
    resp = cnx_client.request(
        cnxapi.assign_profile_to_scope, profile_path, **kwargs
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
