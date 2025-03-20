#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typer
from rich import print
import asyncio


from .. import cli, utils


from .clitree.show import show as cnxshow
from .clitree.update import update as cnxupdate
from .clitree.assign import assign as cnxassign

CONTEXT_SETTINGS = {
    # "token_normalize_func": lambda x: cli.normalize_tokens(x),
    "help_option_names": ["?", "--help"]
}

app = typer.Typer(context_settings=CONTEXT_SETTINGS, rich_markup_mode="rich")
app.add_typer(cnxshow.app, name="show",)
app.add_typer(cnxupdate.app, name="update",)
app.add_typer(cnxassign.app, name="assign",)
color = utils.color


@app.command(short_help="Clone a group")
def group(
    clone_group: str = typer.Argument(..., metavar="[NAME OF GROUP TO CLONE]", autocompletion=cli.cache.group_completion),
    new_group: str = typer.Argument(..., metavar="[NAME OF GROUP TO CREATE]"),
    aos10: bool = typer.Option(None, "--aos10", help="Upgrade new cloned group to AOS10"),
    yes: bool = cli.options.yes,
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    print(f"Clone group: {color(clone_group)} to new group {color(new_group)}")
    if aos10:
        print(f"    Upgrade cloned group to AOS10: {color(True)}")
        print(
            "\n    [dark_orange]:warning:[/dark_orange]  [italic]Upgrade doesn't always work despite "
            f"returning {color('success')},\n    Group is cloned if {color('success')} is returned "
            "but upgrade to AOS10 may not occur.\n    API method appears to have some caveats."
            "\n    Use [cyan]cencli show groups[/] after clone to verify."
        )

    if cli.confirm(yes):
        resp = cli.central.request(cli.central.clone_group, clone_group, new_group)
        cli.display_results(resp, tablefmt="action", exit_on_fail=True)
        groups = cli.cache.groups_by_name
        # API-FLAW clone and upgrade to aos10 does not work via the API
        new_data = {**groups[clone_group], "name": new_group} if not aos10 else {**groups[clone_group], "name": new_group, "AOSVersion": "AOS10", "Architecture": "AOS10"}
        if groups:
            asyncio.run(
                cli.cache.update_group_db(new_data)
            )



@app.callback()
def callback():
    """
    Clone Aruba Central Groups
    """
    pass


if __name__ == "__main__":
    print("hit")
    app()
