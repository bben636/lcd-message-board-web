import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app import main


class FakeDisplay:
    def __init__(self):
        self.images = []

    def show(self, image):
        self.images.append(image)

    def close(self):
        pass


def test_new_websocket_takes_control(monkeypatch):
    display = FakeDisplay()
    monkeypatch.setattr(main, "OledDisplay", lambda: display)

    with TestClient(main.app) as client:
        with client.websocket_connect("/ws") as first_client:
            assert first_client.receive_json() == {"type": "ready"}

            with client.websocket_connect("/ws") as second_client:
                assert second_client.receive_json() == {"type": "ready"}
                with pytest.raises(WebSocketDisconnect) as disconnect:
                    first_client.receive_json()
                assert disconnect.value.code == 4001

                second_client.send_json({"seq": 1, "text": "Active tab"})
                assert second_client.receive_json()["type"] == "ack"

        assert len(display.images) == 3