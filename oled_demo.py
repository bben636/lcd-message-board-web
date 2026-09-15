import time

from app.display import OledDisplay
from app.renderer import render_text_to_image


def main():
    # Standardni I2C1 pinovi na Raspberry Pi 4.
    display = OledDisplay()

    try:
        text = "Benjamin RUST"

        for count in range(len(text) + 1):
            image = render_text_to_image(text[:count])
            display.show_image(image)
            time.sleep(0.2)

        print("Test je poslan. Provjeri prikazuje li OLED 'Benjamin RUST Behrem'.")
    finally:
        display.close()


if __name__ == "__main__":
    main()