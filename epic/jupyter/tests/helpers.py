from collections.abc import Generator
from contextlib import contextmanager

from IPython.core.interactiveshell import InteractiveShell


@contextmanager
def ipython_shell(tmp_path) -> Generator[InteractiveShell, None, None]:
    ipython = InteractiveShell.instance(str(tmp_path))
    try:
        yield ipython
    finally:
        InteractiveShell.clear_instance()
