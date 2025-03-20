"""common helpers and functions used be the CLI
"""
from __future__ import annotations

from typing import Dict, Any
from centralcli import cli, utils
from rich.markup import escape
import typer

from enum import Enum

# FIXME Does not work currently, value.name is correct and is being returned, but you always end up with None
def use_enum_name(ctx: typer.Context, value: Enum | None) -> str:
    if ctx.resilient_parsing or value is None:
        return

    return value.name


# TODO determine what cli options we can remove --library should be able to be removed as we can always gather view_type based on existence of --scope
def get_params(local: bool = None, shared: bool = None, scope: int = None, ap: bool = None, gw: bool = None, switch: bool = None, effective: bool = None, detailed: bool = None, is_update: bool = False) -> Dict[str, Any]:
    """Evaluate CLI command line options and return resulting parameters.

    This function allows for more user friendly options in the CLI, converts them to the parameters the API requires.
    i.e. CLI accepts --scope <id> and will set view_type to local as scope is ignored otherwise

    CNX API needs:
        view_type (Literal["LIBRARY", "LOCAL"]):  Defaults to LIBRARY
        object_type (Literal["LOCAL", "SHARED"]): Defaults to SHARED, Required if view_type LOCAL, ignored if view_type SHARED
        scope_id (int): Fetch configuration at a given scope.  Required if view_type = Local, ignored if view_type = LIBRARY
        persona (Literal["AP", "GATEWAYS", "SWITCH"]): Defaults to All personas if view_type SHARED, Required if view_type LOCAL
        effective (bool): True - Returns effective configuration (i.e hierarchically merged configuration). False - Returns committed configuration at a given scope.  Defaults to False
        detailed (bool, optional): True - Includes annotations in the returned json to indicate the type of object, scope, and persona. Defaults to False (no Annotations).


    Args:
        local (bool, optional): object_type = LOCAL. Defaults to None.
        shared (bool, optional): object_type = SHARED. Defaults to None.
        scope: (int, optional): Configuration at a given scope (global, site, site_collection, device_group, device) by ID.  Defaults to None.
        ap (bool, optional): persona = AP. Defaults to None.
        gw (bool, optional): persona = GATEWAYS. Defaults to None.
        switch (bool, optional): persona = SWITCH. Defaults to None.
        effective (bool, optional): True - Returns effective configuration (i.e hierarchically merged configuration). False - Returns committed configuration at a given scope. Defaults to None.
        detailed (bool, optional): True - Includes annotations in the returned json to indicate the type of object, scope, and persona. Defaults to None API defaults to False (no Annotations).
        is_update (bool, optional): Indicates if this is an update POST/PUT/PATCH. Defaults to False.

    Returns:
        Dict[str, Any]: resulting query parameters required by CNX API with any unset items removed (resulting in API default for that parameter)
    """
    view_type = None # Assuming default by API is LIBRARY
    if scope:
        view_type = "LOCAL"

    if local:
        object_type = view_type = "LOCAL"
    elif shared:
        object_type = "SHARED"
    else:
        object_type = None  # Both / default

    if ap:
        persona = "AP"
    elif gw:
        persona = "GATEWAYS"
    elif switch:
        persona = "SWITCH"
    else:
        persona = None  # Defaults to all personas, only applies if view_type = LOCAL

    if is_update:
        if object_type == "LOCAL" and not all([scope, persona]):
            cli.exit("Scope and persona are [bright_green]both required[/] when updating a [cyan]LOCAL[/] alias.  Neither should be provided when updating a [cyan]SHARED[/] alias")

    params = utils.strip_none(
        {
            "view_type": view_type,
            "object_type": object_type,
            "scope_id": scope,
            "persona": persona,
            "effective": effective,
            "detailed": detailed
        }
    )

    return params

def help_default(default_txt: str) -> str:
    """Helper function that returns properly escaped default text, including rich color markup, for use in CLI help.

    Args:
        default_txt (str): The default value to display in the help text.  Do not include the word 'default: '

    Returns:
        str: Formatted default text.  i.e. [default: some value] (with color markups)
    """
    return f"[grey62]{escape(f'[default: {default_txt}]')}[/grey62]"