import cv2


class UsbCamera:
    def __init__(self, device: str = "/dev/video0"):
        self._capture = cv2.VideoCapture(device, cv2.CAP_V4L2)

        try:
            if not self._capture.isOpened():
                raise RuntimeError(f"Cannot open camera: {device}")

            self._capture.set(
                cv2.CAP_PROP_FOURCC,
                cv2.VideoWriter_fourcc(*"MJPG"),
            )
            self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self._capture.set(cv2.CAP_PROP_FPS, 10)
        except Exception:
            self._capture.release()
            raise

    def read_jpeg(self) -> bytes:
        success, frame = self._capture.read()

        if not success or frame is None:
            raise RuntimeError("Failed to read camera frame.")

        success, encoded = cv2.imencode(".jpg", frame)

        if not success:
            raise RuntimeError("Failed to encode camera frame.")

        return encoded.tobytes()

    def close(self) -> None:
        self._capture.release()