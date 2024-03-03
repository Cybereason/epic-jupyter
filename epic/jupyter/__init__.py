from .ipython import IpythonNotAvailable, get_ipython, is_ipython, is_jupyter_notebook
from .display import display_if_ipython, markdown, side_by_side
from .initialization import event_register_once
from .nbcode import use_notebook_code


def load_ipython_extension(ipython):
    """
    Load all magics in this package.

    Do not call this function directly.
    Instead, use `%load_ext epic.jupyter` or add it to IPython configuration.
    """
    from .interpolate import load_ipython_extension as load_interpolate_extension
    load_interpolate_extension(ipython)
