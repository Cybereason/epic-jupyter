import random
from IPython.core.magic import Magics, magics_class, line_cell_magic
from IPython import get_ipython


@magics_class
class Interpolate(Magics):
    """
    IPython line/cell magic to apply IPython's internal interpolation on the provided input.

    This is useful when facing interpolation failures with other magics.
    Replace your %magic with %interpolate and get in return the input that's passed to the other magic.
    """
    @line_cell_magic
    def interpolate(self, line, cell=None):
        if cell is not None:
            return interpolate(cell)
        return line


def interpolate(text: str) -> str:
    """
    Apply IPython's built-in interpolation directly on the input

    Note: requires that the '%interpolate' magic in this extension has been loaded.

    Parameters
    ----------
    text : str
        The text to be interpolated, e.g. 'hello {"wor" + "ld"}'.

    Returns
    -------
    str
        The interpolated result.
    """
    randstr = " |%s| " % random.randint(10**5, 10**6-1)
    return get_ipython().run_line_magic("interpolate", text.replace("\n", randstr)).replace(randstr, "\n")


def load_ipython_extension(ipython):
    """
    Load the %interpolate magic.

    Do not call this function directly.
    Instead, use `%loadext epic.jupyter.magic.interpolate` or add it to IPython configuration.
    """
    ipython.register_magics(Interpolate)
