import string

from unicodedata import normalize
from PIL import Image, ImageDraw, ImageFont

WIDTH = 128
HEIGHT = 64

CELL_WIDTH = 6
CELL_HEIGHT = 8

COLUMNS = WIDTH // CELL_WIDTH
ROWS = HEIGHT // CELL_HEIGHT
MAX_CHARS = COLUMNS * ROWS

BASELINE = 6

FONT = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    7,
)

SUPPORTED = set(
    string.ascii_letters
    + string.digits
    + string.punctuation
    + " čćžšđČĆŽŠĐ"
)


def render_text(text: str) -> Image.Image:
    text = normalize("NFC", text)

    if len(text) > MAX_CHARS:
        raise ValueError(
            f"Message can have max: {MAX_CHARS} characters."
        )

    for char in text:
        if char not in SUPPORTED:
            raise ValueError(f"Unsupported character: {char!r}")

    image = Image.new("1", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(image)

    for index, char in enumerate(text):
        column = index % COLUMNS
        row = index // COLUMNS

        x = column * CELL_WIDTH
        y = row * CELL_HEIGHT + BASELINE

        draw.text(
            (x, y),
            char,
            font=FONT,
            fill=1,
            anchor="ls",
        )

    return image