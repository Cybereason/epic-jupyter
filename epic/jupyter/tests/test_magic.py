import pytest
from IPython.core.error import UsageError

from epic.jupyter.interpolate import interpolate

from .helpers import ipython_shell


class TestInterpolate:
    def test_interpolate(self, tmp_path):
        with ipython_shell(tmp_path) as ipython:
            with pytest.raises(UsageError):
                interpolate("hello")
            ipython.run_line_magic("load_ext", "epic.jupyter.interpolate")
            assert interpolate("hello") == "hello"
            assert interpolate("") == ""
            assert interpolate("hello {'wor' + 'ld'}") == "hello world"
            ipython.run_line_magic("interpolate", "hello world")
            ipython.run_cell("ld = 'dle'")
            ipython.run_cell("x = %interpolate hello {'wor' + ld}")
            assert ipython.ev("x") == 'hello wordle'
            ipython.run_cell("x = %interpolate hello {undefined}")
            assert ipython.ev("x") == 'hello {undefined}'
            ipython.run_cell("x = %interpolate hello {1 / 0}")
            assert ipython.ev("x") == 'hello {1 / 0}'
            ipython.run_cell("%interpolate hello")
            assert ipython.ev("_") == 'hello'
            ipython.run_cell("%%interpolate\nhello world\nthis is {'sparta'}")
            assert ipython.ev("_") == 'hello world\nthis is sparta\n'
            ipython.run_cell("%%interpolate\nhello {world}\nthis is {sparta}")
            assert ipython.ev("_") == 'hello {world}\nthis is {sparta}\n'

    def test_loadext_epic_jupyter_interpolate(self, tmp_path):
        with ipython_shell(tmp_path) as ipython:
            with pytest.raises(UsageError):
                interpolate("hello")
            ipython.run_line_magic("load_ext", "epic.jupyter.interpolate")
            assert interpolate("hello") == "hello"

    def test_loadext_epic_jupyter(self, tmp_path):
        with ipython_shell(tmp_path) as ipython:
            with pytest.raises(UsageError):
                interpolate("hello")
            ipython.run_line_magic("load_ext", "epic.jupyter")
            assert interpolate("hello") == "hello"
