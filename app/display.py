import adafruit_ssd1306
import board
import busio
from PIL import Image

class OledDisplay:
    def __init__(self, address: int = 0x3c):
        self._i2c = busio.I2C(board.SCL, board.SDA)
        
        try:
            self._oled = adafruit_ssd1306.SSD1306_I2C(128, 64, self._i2c, addr=address)
        except Exception as exc:
            self._i2c.deinit()
            raise RuntimeError(f"Failed to initialize OLED display: {exc}")
    
    def show(self, image: Image.Image) -> None:
        """Display a PIL image on the OLED."""
        self._oled.image(image)
        self._oled.show()

    def close(self) -> None:
        """clean display and free resources."""
        try:
            self._oled.fill(0)
            self._oled.show()
        finally:
            # executes if the display was initialized or not, to ensure resources are freed
            self._i2c.deinit()
            