# -*- coding: utf-8 -*-
from centralcli.cache import Cache
# from centralcli.constants import iden_meta
from rich.markup import escape

import typer


# class CLIArgs:
#     def __init__(self, cache: Cache):
#         self.cache = cache
#         ...

class CLIOptions:
    object_name: str | None = "object"

    @classmethod
    def set_name(cls, name: str):
        cls.object_name: str = name

    def __init__(self, cache: Cache, object_name: str = None):
        self.cache = cache
        if object_name:
            self.object_name = object_name

    # @property
    # def object_name(self) -> str | None:
    #     return self._object_name

    # @object_name.setter
    # def portal(self, object_name: str):
    #     self._object_name = object_name


class CLIArgs(CLIOptions):
    def __init__(self, cache: Cache, object_name: str = None):
        super().__init__(cache, object_name=object_name)
        self.name = typer.Argument(..., help=f"The name of the {self.object_name} to update", show_default=False,)
        self.pvid = typer.Argument(..., help="The PVID of the vlan to update", show_default=False,)

class CLIUpdateOptions(CLIOptions):
    def __init__(self, cache: Cache, object_name: str = None):
        super().__init__(cache, object_name=object_name)
        self.local: bool = typer.Option(False, "-L", "--local", help=f"Update a Local {self.object_name} object, [grey42]{escape('[default: SHARED]')}[/]", show_default=False,)
        self.scope: int = typer.Option(None, help="Mandatory Scope when updating local object, should [red]not[/] be provided if updating SHARED (library) object",)
        self.switch: bool = typer.Option(None, "--sw", "--cx", "--switch", help="Update switch persona")
        self.gw: bool = typer.Option(None, "--gw", help="Update gateway persona")
        self.ap: bool = typer.Option(None, "--ap", help="Update ap persona")
        self.name: str = typer.Option(None, "--name", help=f"Update the {self.object_name} name", show_default=False)
        self.description: str = typer.Option(None, help=f"{self.object_name} description", show_default=False,)

class CLIGetOptions(CLIOptions):
    def __init__(self, cache: Cache, object_name: str = None):
        super().__init__(cache, object_name=object_name)
        self.library: bool = typer.Option(None, "--library", help="Get shared objects in library. [italic]view_type[/]", show_default=False,)
        self.shared: bool = typer.Option(None, "--shared", help="object_type")
        self.local: bool = typer.Option(None, "-L", "--local", help=f"Get Local {self.object_name}, [grey42]{escape('[default: Both Local and Shared objects]')}[/]", show_default=False,)
        self.scope: int = typer.Option(None, help="Scope ID, should [red]not[/] be provided if updating SHARED (library) object", show_default=False,)
        self.switch: bool = typer.Option(None, "--sw", "--cx", "--switch", help=f"Filter on Switch persona items. [grey42]{escape('[default: All personas if [cyan]--local[/] provided and no persona flags provided')}[/]")
        self.gw: bool = typer.Option(None, "--gw", help="Filter on Gateway persona items")
        self.ap: bool = typer.Option(None, "--ap", help="Filter on AP persona items")
        self.effective: bool = typer.Option(None, "-e", "--effective", help="Return effective configuration (i.e hierarchically merged configuration)")
        self.detailed: bool = typer.Option(None, "-D", "--detailed", help="Include annotations to indicate the type of object, scope, and persona")



