class IpythonNotAvailable(Exception):
    """Ipython is not available"""


def get_ipython(strict=False):
    """
    Get IPython's global InteractiveShell instance, if IPython is installed and an InteractiveShell has been created.

    Parameters
    ----------
    strict : bool, default False
        If set, an IpythonNotAvailable error is raised when IPython is not available

    Returns
    -------
    InteractiveShell or None
        The value returned by IPython.get_ipython(), or None if IPython is not installed and strict is False.

    Raises
    ------
    IpythonNotAvailable
        If IPython is not available and `strict` is True.
    """
    try:
        import IPython
    except ModuleNotFoundError:
        result = None
    else:
        from IPython import get_ipython
        result = get_ipython()
    if result is None and strict:
        raise IpythonNotAvailable()
    return result


def is_ipython() -> bool:
    """
    Get whether an IPython interactive shell has been initialized (either console or jupyter notebook).

    Returns
    -------
    bool
        True iff IPython is installed and a shell has been initialized (i.e. `get_ipython()` returns a non-None value).
    """
    return get_ipython() is not None


def is_jupyter_notebook() -> bool:
    """
    Test whether we're running inside a Jupyter notebook kernel.

    Returns
    -------
    bool
        True if this is a Jupyter notebook kernel process, False otherwise.
    """
    ipython = get_ipython()
    if ipython is None:
        return False
    # Based on the suggestion at https://github.com/ipython/ipython/issues/9732
    return ipython.has_trait('kernel')
