import pytest

from epic.jupyter import side_by_side, display_if_ipython, IpythonNotAvailable

from .helpers import ipython_shell


class TestDisplay:
    def test_side_by_side(self):
        html = side_by_side(101)
        assert '>101<' in html.data
        html = side_by_side(101, 102)
        assert '>101<' in html.data and '>102<' in html.data
        sep = html.data.split(">101", 1)[1].split("102<")[0]
        assert "<tr" not in sep
        assert "/td><td" in sep
        assert "<br" not in sep
        html = side_by_side([101, 102])
        assert '>101<' in html.data and '>102<' in html.data
        sep = html.data.split(">101", 1)[1].split("102<")[0]
        assert "<br" in sep
        assert "<tr" not in sep
        assert "<td" not in sep

    def test_display_if_ipython(self, tmp_path):
        yo = 'yo'
        explosive = ExplosiveObject()

        # not in ipython
        # yo
        display_if_ipython(yo)
        display_if_ipython(yo, otherwise='ignore')
        display_if_ipython(yo, otherwise='print')
        with pytest.raises(IpythonNotAvailable):
            display_if_ipython(yo, otherwise='raise')
        with pytest.raises(AssertionError):
            display_if_ipython(yo, otherwise='whatever')
        # explosive
        display_if_ipython(explosive)
        display_if_ipython(explosive, otherwise='ignore')
        with pytest.raises(ExplosiveObject.Exploded):
            display_if_ipython(explosive, otherwise='print')
        with pytest.raises(IpythonNotAvailable):
            display_if_ipython(explosive, otherwise='raise')
        with pytest.raises(AssertionError):
            display_if_ipython(explosive, otherwise='whatever')

        # in ipython
        with ipython_shell(tmp_path):
            # yo
            display_if_ipython(yo)
            display_if_ipython(yo, otherwise='ignore')
            display_if_ipython(yo, otherwise='print')
            display_if_ipython(yo, otherwise='raise')
            with pytest.raises(AssertionError):
                display_if_ipython(yo, otherwise='whatever')
            # explosive
            with pytest.raises(ExplosiveObject.Exploded):
                display_if_ipython(explosive)
            with pytest.raises(ExplosiveObject.Exploded):
                display_if_ipython(explosive, otherwise='ignore')
            with pytest.raises(ExplosiveObject.Exploded):
                display_if_ipython(explosive, otherwise='print')
            with pytest.raises(ExplosiveObject.Exploded):
                display_if_ipython(explosive, otherwise='raise')
            with pytest.raises(AssertionError):
                display_if_ipython(yo, otherwise='whatever')


class ExplosiveObject:
    # we derive from BaseException because Exception subclasses are caught and silenced by display
    class Exploded(BaseException):
        """This object has been asked to represent itself"""

    def __repr__(self):
        raise self.Exploded()

    def __str__(self):
        raise self.Exploded()
