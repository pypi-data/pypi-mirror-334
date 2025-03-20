import sys
from pathlib import Path
# Detect if called from pypi installed package or via cloned github repo (development)
try:
    from cnxcli import (cnx_client,)
except (ImportError, ModuleNotFoundError) as e:
    pkg_dir = Path(__file__).absolute().parent
    if "centralcli" in pkg_dir.parts:
        path_slice = slice(1, pkg_dir.parts.index("centralcli") + 1)
        pkg_path = f'/{"/".join(pkg_dir.parts[path_slice])}'
        if pkg_path not in sys.path:
            sys.path.insert(0, str(pkg_path))
            from centralcli import (cnx_client,)
    else:
        print(pkg_dir.parts)
        print(sys.path)
        raise e

from cnxcli.api import cnxapi
from cnxcli.clioptions import CLIUpdateOptions, CLIArgs

__all__ = [
    cnxapi,
    cnx_client,
    CLIUpdateOptions,
    CLIArgs
]