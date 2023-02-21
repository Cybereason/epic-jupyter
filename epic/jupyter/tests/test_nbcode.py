from epic.jupyter.nbcode import use_notebook_code
from epic.jupyter.ipython import get_ipython

from .helpers import ipython_shell


class TestNotebookCode:
    def test_it(self, tmp_path):
        with ipython_shell(tmp_path):
            ipython = get_ipython()

            open(tmp_path / "code1.py", "w").write("a = 123")
            result = ipython.run_cell("b = a")
            assert not result.success

            use_notebook_code(tmp_path / "code1.py")
            result = ipython.run_cell("b = a")
            assert result.success
            assert ipython.ev("b") == 123

            open(tmp_path / "code1.py", "w").write("a = 456")
            result = ipython.run_cell("b = a")
            assert result.success
            assert ipython.ev("b") == 456

            open(tmp_path / "code1.py", "w").write("a = !")
            result = ipython.run_cell("b = a")
            # TODO: make bad book code stop the cell execution somehow
            # assert not result.success

            open(tmp_path / "code1.py", "w").write("a = 789")
            ipython.run_cell("b = a")
            assert result.success
            assert ipython.ev("b") == 789

            use_notebook_code()
            open(tmp_path / "code1.py", "w").write("a = -1")
            result = ipython.run_cell("b = a")
            assert result.success
            assert ipython.ev("b") == 789
