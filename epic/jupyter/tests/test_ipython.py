import pytest

from epic.jupyter import get_ipython, IpythonNotAvailable

from .helpers import ipython_shell


class TestIpython:
    def test_get_ipython(self, tmp_path):
        assert get_ipython() is None
        assert get_ipython(strict=False) is None
        with pytest.raises(IpythonNotAvailable):
            get_ipython(strict=True)
        with ipython_shell(tmp_path) as ipython:
            assert get_ipython() is ipython
            assert get_ipython(strict=False) is ipython
            assert get_ipython(strict=True) is ipython
