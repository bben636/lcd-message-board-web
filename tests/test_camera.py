from unittest.mock import Mock

import pytest

from app import camera


@pytest.fixture
def capture(monkeypatch):
    fake = Mock()
    fake.isOpened.return_value = True
    monkeypatch.setattr(camera.cv2, "VideoCapture", Mock(return_value=fake))
    return fake


def test_close_releases_camera(capture):
    device = camera.UsbCamera()

    device.close()

    capture.release.assert_called_once()


def test_failed_open_releases_camera(capture):
    capture.isOpened.return_value = False

    with pytest.raises(RuntimeError, match="Cannot open camera"):
        camera.UsbCamera()

    capture.release.assert_called_once()


def test_read_returns_jpeg_bytes(capture, monkeypatch):
    frame = object()
    capture.read.return_value = (True, frame)

    encoded = Mock()
    encoded.tobytes.return_value = b"jpeg-data"
    encode = Mock(return_value=(True, encoded))
    monkeypatch.setattr(camera.cv2, "imencode", encode)

    device = camera.UsbCamera()
    try:
        assert device.read_jpeg() == b"jpeg-data"
        encode.assert_called_once_with(".jpg", frame)
    finally:
        device.close()


@pytest.mark.parametrize("frame", [None, object()])
def test_failed_read_raises_error(capture, frame):
    capture.read.return_value = (False, frame)

    device = camera.UsbCamera()
    try:
        with pytest.raises(RuntimeError, match="Failed to read"):
            device.read_jpeg()
    finally:
        device.close()


def test_failed_encoding_raises_error(capture, monkeypatch):
    capture.read.return_value = (True, object())
    monkeypatch.setattr(
        camera.cv2,
        "imencode",
        Mock(return_value=(False, None)),
    )

    device = camera.UsbCamera()
    try:
        with pytest.raises(RuntimeError, match="Failed to encode"):
            device.read_jpeg()
    finally:
        device.close()