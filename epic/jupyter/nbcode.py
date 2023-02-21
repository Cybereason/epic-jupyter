import binascii
import inspect
import os
from pathlib import Path

from .ipython import get_ipython


def use_notebook_code(*file_paths: str | Path):
    """
    Register "notebook code" python files to be loaded and then reloaded (using `exec`) whenever they change.

    Notebook code files should help maintaining separation of concerns. When a significant amount of relatively generic
    code is developed for the purposes of a notebook, keeping it in an adjacent file keeps the notebook itself focused
    on the research narrative. The automatic reload mechanism in turn frees the user from having to go back and run
    random code cells whenever some change is made to the underlying code.

    Ultimately, any useful code should make its way into a general purpose library.
    During that time when its scope is limited to a specific notebook - notebook code files are here for you.

    Calling this function would _remove_ all previously registered notebook code files, and then register the new ones.

    Parameters
    ----------
    *file_paths : str or Path
        one or more paths to notebook code source files.

    Returns
    -------
    None
    """
    missing_files = [fp for fp in file_paths if not os.path.exists(fp)]
    if missing_files:
        raise FileNotFoundError(f"missing notebook code file(s): {missing_files}")
    NotebookCode.force_unregister_all()
    for fp in file_paths:
        NotebookCode(fp).register().load()


class NotebookCode:
    def __init__(self, path):
        self.path = path
        self.abspath = os.path.abspath(str(path))
        self.last_crc = None

    def register(self):
        self._ipython().events.register('pre_run_cell', self.on_pre_run_cell)
        return self

    def unregister(self):
        self._ipython().events.unregister('pre_run_cell', self.on_pre_run_cell)
        return self

    def load(self):
        self._trigger_reload()
        self.last_crc = self._crc()
        return self

    def on_pre_run_cell(self, *_args):
        new_crc = self._crc()
        if new_crc != self.last_crc:
            self._trigger_reload()
        self.last_crc = new_crc

    def _crc(self):
        return binascii.crc32(open(self.abspath, "rb").read())

    def _trigger_reload(self):
        print(f"** reloading modified notebook code from '{self.path}' **")
        result = self._ipython().run_cell(f"exec(open({repr(self.abspath)}, 'rb').read())", silent=True)
        if not result.success:
            # note: although we raise here, callback errors are always printed and then silenced.
            # so this unfortunately does NOT prevent cell execution.
            print(f"** failed reloading notebook code from '{self.path}' **")
            result.raise_error()

    @classmethod
    def force_unregister_all(cls):
        for callback in cls._ipython().events.callbacks['pre_run_cell'][:]:
            if inspect.ismethod(callback) and (s := callback.__self__) is not None and isinstance(s, cls):
                cls._ipython().events.unregister('pre_run_cell', callback)
        # a good time to verify this is set to False
        cls._currently_reloading_code = False

    @staticmethod
    def _ipython():
        return get_ipython(strict=True)
