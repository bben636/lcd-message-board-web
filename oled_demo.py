import time

import adafruit_ssd1306
import board
import busio
from app.renderer import render_text_to_image


def main():
    # Standardni I2C1 pinovi na Raspberry Pi 4.
    i2c = busio.I2C(board.SCL, board.SDA)

    try:
        oled = adafruit_ssd1306.SSD1306_I2C(
            128, 64, i2c, addr=0x3C
        )

        
        text = "Benjamin RUST Behrem"

        for count in range(len(text)):
            image = render_text_to_image(text[:count])

            oled.image(image)
            oled.show()

            time.sleep(0.2)

        print("Test je poslan. Provjeri prikazuje li OLED 'Benjamin RUST Behrem'.")

    finally:
        i2c.deinit()


if __name__ == "__main__":
    main()