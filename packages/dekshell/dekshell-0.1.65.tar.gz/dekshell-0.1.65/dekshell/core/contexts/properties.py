import os
import sys
import shutil
import tempfile
from pathlib import Path
from sysconfig import get_paths
from importlib import metadata
from dektools.module import ModuleProxy
from ..redirect import shell_name
from ...utils.serializer import serializer

current_shell = shutil.which(shell_name, path=get_paths()['scripts'])


def make_shell_properties(shell):
    return {
        'shell': shell,
        'sh': {
            'rf': f'{shell} rf',
            'rfc': f'{shell} rfc',
            'rs': f'{shell} rs',
        },
    }


package_name = __name__.partition(".")[0]
path_home = os.path.expanduser('~')
is_on_win = os.name == "nt"
path_root = path_home[:path_home.find(os.sep)] if is_on_win else os.sep

default_properties = {
    'meta': {
        'name': package_name,
        'version': metadata.version(package_name)
    },
    'python': sys.executable,
    **make_shell_properties(current_shell),
    'os': {
        'pid': os.getpid(),
        'win': is_on_win,
        'ps': os.pathsep,
    },
    'path': {
        'root': Path(path_root),
        'home': Path(path_home),
        'temp': Path(tempfile.gettempdir()),
        'sep': os.sep
    },
    'hex': serializer,
    'mp': ModuleProxy(),
}
