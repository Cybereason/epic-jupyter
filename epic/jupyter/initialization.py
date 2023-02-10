from collections.abc import Callable
from typing import Literal, get_args

from .ipython import get_ipython


Error = Literal['raise', 'display', 'ignore']


def event_register_once(event: str, callback: Callable, error: Error = 'display') -> None:
    """
    Register an IPython event callback that would only trigger once, and then be unregistered.

    Parameters
    ----------
    event : str
        The event for which to register this callback.

    callback : callable
        A function to be called on the given event. It should take the same
        parameters as the appropriate callback prototype.

    error : {'raise', 'display', 'ignore'}, default 'display'
        How to behave when the callback raises an exception: re-raise it, display it, or quietly ignore it.

    Returns
    -------
    None

    Raises
    ------
    IpythonNotAvailable
        If IPython is not available.
    """
    from IPython.display import display
    ipython = get_ipython(strict=True)
    assert error in get_args(Error)

    def callback_and_unregister(*args, **kwargs):
        try:
            callback(*args, **kwargs)
        except Exception as exc:
            if error == 'raise':
                raise
            elif error == 'display':
                display(f"<<event_register_once: exception {exc} raised from callback and ignored>>")
        finally:
            ipython.events.unregister(event, callback_and_unregister)

    ipython.events.register(event, callback_and_unregister)
