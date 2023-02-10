import pytest

from epic.jupyter import event_register_once, IpythonNotAvailable

from .helpers import ipython_shell


class TestEventRegisterOnce:
    def test_no_ipython(self):
        with pytest.raises(IpythonNotAvailable):
            event_register_once('pre_execute', lambda: ...)

    def test_single(self, tmp_path):
        with ipython_shell(tmp_path) as ipython:
            event_register_once('pre_execute', callback := CallbackCounter())
            assert callback.counter == 0
            ipython.run_cell("print('running cell')")
            assert callback.counter == 1
            ipython.run_cell("print('running another cell')")
            assert callback.counter == 1

    def test_multi(self, tmp_path):
        with ipython_shell(tmp_path) as ipython:
            event_register_once('pre_execute', callback1 := CallbackCounter())
            event_register_once('pre_execute', callback2 := CallbackCounter())
            event_register_once('post_execute', callback3 := CallbackCounter())
            assert callback1.counter == callback2.counter == callback3.counter == 0
            ipython.run_cell("print('running cell')")
            assert callback1.counter == callback2.counter == callback3.counter == 1
            ipython.run_cell("print('running another cell')")
            assert callback1.counter == callback2.counter == callback3.counter == 1

    def test_callback_params(self, tmp_path):
        with ipython_shell(tmp_path) as ipython:
            event_register_once('pre_run_cell', callback := CallbackCounter(allow_params=True))
            assert callback.counter == 0
            ipython.run_cell("print('running cell')")
            assert callback.counter == 1
            ipython.run_cell("print('running another cell')")
            assert callback.counter == 1
            args, kwargs = callback.params[0]
            assert len(args) == 1
            assert len(kwargs) == 0

    def test_errors(self, tmp_path):
        with ipython_shell(tmp_path) as ipython:
            with pytest.raises(KeyError):
                event_register_once('invalid', lambda: ...)
        # errors in callback don't prevent cells from running
        with ipython_shell(tmp_path) as ipython:
            ipython.run_cell("flag = 0")
            event_register_once('pre_execute', 'not a function', error='raise')
            ipython.run_cell("flag = 1")
            assert ipython.ev("flag") == 1

    def test_event_timing(self, tmp_path):
        with ipython_shell(tmp_path) as ipython:
            event_register_once('shell_initialized', callback := CallbackCounter())
            assert callback.counter == 0
            ipython.run_cell("print('running cell')")
            assert callback.counter == 0


class CallbackCounter:
    def __init__(self, allow_params=False):
        self.counter = 0
        self.params = []
        self.allow_params = allow_params

    def __call__(self, *args, **kwargs):
        assert self.allow_params or not args and not kwargs
        self.counter += 1
        self.params.append((args, kwargs))
