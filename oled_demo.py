import time

from app.display import OledDisplay
from app.renderer import render_text


def main():
    # Standardni I2C1 pinovi na Raspberry Pi 4.
    display = OledDisplay()

    try:
        text = "čćžšđ ČĆŽŠĐ 123456789" * 8

        for count in range(len(text) + 1):
            image = render_text(text[:count])
            display.show(image)
            time.sleep(0.1)

        time.sleep(2)
        display.show(render_text("Kratko."))
        time.sleep(3)

    finally:
        display.close()


if __name__ == "__main__":
    main()