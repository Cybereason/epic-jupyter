import sys
import pytest


class TestIpython:
    def test_get_ipython(self, tmp_path):
        from epic.jupyter import get_ipython, IpythonNotAvailable
        from .helpers import ipython_shell
        assert get_ipython() is None
        assert get_ipython(strict=False) is None
        with pytest.raises(IpythonNotAvailable):
            get_ipython(strict=True)
        with ipython_shell(tmp_path) as ipython:
            assert get_ipython() is ipython
            assert get_ipython(strict=False) is ipython
            assert get_ipython(strict=True) is ipython

    def test_when_ipython_not_installed(self):
        mod = sys.modules['IPython']
        sys.modules['IPython'] = None
        for k in list(sys.modules):
            if k.startswith("epic.jupyter"):
                sys.modules.pop(k)
        assert 'epic.jupyter' not in sys.modules
        try:
            from epic.jupyter import get_ipython, IpythonNotAvailable
            assert get_ipython() is None
            assert get_ipython(strict=False) is None
            with pytest.raises(IpythonNotAvailable):
                get_ipython(strict=True)
        finally:
            sys.modules['IPython'] = mod
