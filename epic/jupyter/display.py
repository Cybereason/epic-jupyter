from html import escape
from typing import Literal, get_args
from collections.abc import Mapping, Collection

from ._utils import fig2html
from .ipython import is_ipython, IpythonNotAvailable

Otherwise = Literal['ignore', 'print', 'raise']


def display_if_ipython(*args, otherwise: Otherwise = 'ignore', **kwargs):
    """
    Display the provided input if IPython is available, otherwise ignore it / print it / raise an error.

    Parameters:
    -----------
    otherwise : {'ignore', 'print', 'raise'}, default 'ignore'
        When IPython is not available, whether to ignore it / print the args / raise an error.

    See IPython.display.display for supported *args and **kwargs format.
    """
    assert otherwise in get_args(Otherwise)
    if is_ipython():
        from IPython.display import display
        return display(*args, **kwargs)
    elif otherwise == 'print':
        for x in args:
            print(x)
    elif otherwise == 'raise':
        raise IpythonNotAvailable()


def markdown(*objs: str):
    """
    Display preformatted Markdown content

    Parameters
    ----------
    *objs : str
        Markdown-formatted texts to display
    """
    from IPython.display import display_markdown
    display_markdown(*objs, raw=True)


def side_by_side(*items, names: Collection | None = None):
    """
    Display items side by side, with optional names as titles.

    Can either provide an optional collection of names for the items, or provide
    a Mapping, mapping names to items for display.

    Parameters
    ----------
    *items :
        Items to display side by side.
        Can also be a Mapping, mapping names to items.
        If a single item is a list, its members will be stacked vertically.

    names : collection, optional
        Names for the given items.

    Returns
    -------
    HTML
    """
    from IPython.display import HTML

    def _to_html(obj) -> str:
        if isinstance(obj, list):
            return "<br/>".join(map(_to_html, obj))
        if isinstance(obj, HTML):
            return obj.data
        if hasattr(obj, 'savefig'):
            return fig2html(obj)
        for method in ('to_html', 'render'):
            if hasattr(obj, method):
                return getattr(obj, method)()
        return escape(str(obj))

    if len(items) == 1 and isinstance(items[0], Mapping) and names is None:
        names, items = zip(*items[0].items())
    elif names is not None and len(names) != len(items):
        raise ValueError("Must provide names for all the objects.")
    # Putting the style in a <style> tag at the <head> doesn't work; must include it in every cell.
    style = 'style="vertical-align:top;text-align:left"'
    data = "".join(f'<td {style}><pre>{_to_html(x)}</pre></td>' for x in items)
    header = f"<tr>{''.join(f'<th {style}>{escape(str(x))}</th>' for x in names)}</tr>" if names is not None else ''
    return HTML(f'<table>{header}<tr>{data}</tr></table>')
