import pytest
from unittest.mock import MagicMock, patch

import coffee_scale.scale as scale

class DummySerial:
    def __init__(self, port, baudrate, timeout):
        # record what we were called with
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._buffer_cleared = False
        self.closed = False

    def reset_input_buffer(self):
        self._buffer_cleared = True

    def close(self):
        self.closed = True


@pytest.fixture
def dummy_serial(monkeypatch):
    """
    Replace Serial with our DummySerial, and let tests tweak
    DummySerial.readline by monkeypatching instance attributes.
    """
    monkeypatch.setattr(scale, "Serial", DummySerial)
    return DummySerial


def test_read_scale_parses_happy_path(dummy_serial, monkeypatch):
    fake_port = 'COM3'
    fake_line = b"0.75,kg,23.1,\n"
    fake_serial = DummySerial(fake_port, 9600, timeout=1)
    fake_serial.readline = lambda: fake_line

    monkeypatch.setattr(scale, "init_scale", lambda port: fake_serial)

    w = scale.read_scale()
    assert isinstance(w, float)
    assert w == pytest.approx(.75)
    assert fake_serial.closed is True


def test_read_scale_raises_on_malformed_line(dummy_serial, monkeypatch):
    fake_port = 'COM3'
    bad_line = b"not,a,valid,extra\n"
    fake_serial = DummySerial(fake_port, 9600, timeout=1)
    fake_serial.readline = lambda: bad_line

    monkeypatch.setattr(scale, "init_scale", lambda port: fake_serial)

    with pytest.raises(ValueError):
        scale.read_scale()

    assert fake_serial.closed is True