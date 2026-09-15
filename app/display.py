import adafruit_ssd1306
import board
import busio
from PIL import Image


class OledDisplay:
    def __init__(self, address: int = 0x3c):
        self._i2c = busio.I2C(board.SCL, board.SDA)

        try:
            self._oled = adafruit_ssd1306.SSD1306_I2C(128, 64, self._i2c, addr=address)
        except Exception as e:
            self._i2c.deinit()
            raise RuntimeError(f"Failed to initialize OLED display: {e}") from e

    def show_image(self, image: Image.Image) -> None:
        self._oled.image(image)
        self._oled.show()

    def close(self) -> None:
        if hasattr(self, "_i2c"):
            self._i2c.deinit()