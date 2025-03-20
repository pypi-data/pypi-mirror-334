#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typer

from centralcli import cli, utils
from . import cnxapi, cnx_client, CLIUpdateOptions, CLIArgs
from cnxcli.clitree import common
from cnxcli.models.auth_server_global import AuthServerGlobalConfigProfile, SharedSecretConfig, AuthenticationType
from rich.markup import escape
from enum import Enum


app = typer.Typer()
options = CLIUpdateOptions(cli.cache, "Auth Server Global")
args = CLIArgs(cli.cache, "Auth Server Global")


class AuthServerType(str, Enum):
    RADIUS = 'radius'
    LDAP = 'ldap'
    TACACS = 'tacacs'
    WINDOWS = 'windows'
    RFC3576 = 'rfc3576'
    XMLAPI = 'xmlapi'
    RADSEC = 'radsec'
    LOCAL = 'local'

@app.command(name="global")
def _global(
    local: bool = options.local,
    switch: bool = options.switch,
    ap: bool = options.ap,
    gw: bool = options.gw,
    scope: int = options.scope,
    name: str = args.name,
    description: str = options.description,
    dyn_auth: bool = typer.Option(None, help="Enable Dynamic Authorization RFC3576", show_default=False,),
    dyn_auth_port: int = typer.Option(None, help="UDP Port to use for Dynamic Authorization RFC3576. [grey42]{escape('[default: 3799 if dyn_auth enabled and not provided]')}[/]"),
    radsec: bool = typer.Option(None, help="Enable/Disable RadSec", show_default=False,),
    auth_type: AuthenticationType = typer.Option(None, help="Protocol used to communicate with RADIUS or TACACS Server.", show_default=False),
    retries: int = typer.Option(None, show_default=False),
    svc_type_in_rqst: bool = typer.Option(None, "--ST", help="Include Service-Type in Access Request", show_default=False,),
    status_svr_interval: int = typer.Option(None, "--status-interval", help="status server interval", show_default=False,),
    _type: AuthServerType = typer.Option(None, "-T", "--type", help="Auth Server Type", show_default=False,),
    shared_secret: str = typer.Option(None, "--secret", help="Shared Secret. [italic]Use single quotes to avoid shell interpreting any specials characters[/]", show_default=False),
    ciphertext: bool = typer.Option(False, "-C", "--cipher", help=f"Indicates provided password is CIPHER_TEXT [grey42]{escape('[default: PLAIN_TEXT]')}[/]"),
    yes: bool = cli.options.yes,
    debug: bool = cli.options.debug,
    default: bool = cli.options.default,
    account: str = cli.options.account,
) -> None:
    params = common.get_params(local=local, scope=scope, switch=switch, ap=ap, gw=gw, is_update=True)

    secret_config = None
    if shared_secret:
        if not ciphertext:
            secret_config = SharedSecretConfig(secret_type="PLAIN_TEXT", plaintext_value=shared_secret)
        else:
            secret_config = SharedSecretConfig(secret_type="CIPHER_TEXT", ciphertext_value=shared_secret)
    if dyn_auth and not dyn_auth_port:
        dyn_auth_port = 3799

    profile = AuthServerGlobalConfigProfile(
        name=name,
        description=description,
        type=None if not _type else _type.name,
        enable_radsec=radsec,
        authentication_type=auth_type,
        retries=retries,
        service_type_in_access_request=svc_type_in_rqst,
        status_server_interval=status_svr_interval,
        # single_connection_mode=None,
        # timeout=None,
        # tls_initial_connection_timeout=None,
        # tracking_enable=False,
        # tracking_mode=None,
        # tracking_req_packet=None,
        # tracking_interval=None,
        # tracking_user_name=None,
        # tracking_password_config=None,
        enable=dyn_auth,
        udp_port=dyn_auth_port,
        # udp_port=None,
        # deadtime=None,
        # infinite_deadtime=None,
        shared_secret_config=secret_config,
        # access_request_include=None,
        # fqdn_retry_interval=None,
        # ordering_sequence=None,
        # vsa_disable=None
    )
    # def _mask_secrets(value: dict | str) -> str:
    #     if not isinstance(value, dict):
    #         return value



    conf_msg = "Create Global Auth Server Profile with the follwing:"
    conf_items = "\n".join(
        [f'   [bright_green]{k if k != "enable" else "dyn-auth"}[/]: [bright_green]{str(v) if not k.endswith("secret") else "*******"}[/]' for k, v in utils.strip_none(profile.model_dump(by_alias=True), strip_empty_obj=True).items()]
    )
    cli.econsole.print(f'{conf_msg}\n{conf_items}')
    if cli.confirm(yes):
        resp = cnx_client.request(cnxapi.update_auth_server_global, profile=profile, **params)

    cli.display_results(resp, title="Auth Servers", tablefmt="action")




@app.callback()
def callback():
    """
    Update auth servers/details
    """
    pass


if __name__ == "__main__":
    app()