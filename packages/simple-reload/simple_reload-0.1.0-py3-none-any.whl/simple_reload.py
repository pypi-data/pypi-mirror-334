from contextlib import suppress
import os
from os.path import abspath, dirname
import sys
from types import ModuleType
from typing import Callable, List, Set, Tuple

import watchfiles
from watchfiles import Change, PythonFilter


def run_simple_reload(
    modules: List[ModuleType],
    on_change: Callable[[Set[Tuple[Change, str]]], None] = lambda _: None,
):
    """
    If this is the parent CLI process, stop the program here and start a child process every time a file changes.
    The child process will run the same command that was run to start the parent process.
    """
    is_direct = bool(int(os.environ.get('SIMPLE_RELOAD_DISABLE') or '0'))
    if is_direct:
        return

    for x in modules:
        if not getattr(x, '__file__', None):
            raise ValueError(f'Could not find source path for module {x}')

    folders = [dirname(abspath(i.__file__)) for i in modules if i.__file__]
    with suppress(Exception):
        watchfiles.run_process(
            *folders,
            watch_filter=PythonFilter(),
            target=_exec_command,
            args=(sys.argv,),
            callback=on_change,
        )
    raise SystemExit(0)


def _exec_command(command):
    executable_path = command[0]
    if not os.access(executable_path, os.X_OK):
        # Assume we are running the current script with the Python interpreter
        executable_path = sys.executable
        command = [sys.executable, *command]
    os.environ['SIMPLE_RELOAD_DISABLE'] = '1'
    os.setsid()
    os.execl(executable_path, *command)


__all__ = ['run_simple_reload', 'Change']
