from PIL import Image, ImageDraw, ImageFont

WIDTH = 128
HEIGHT = 64

FONT = ImageFont.load_default()

def render_text_to_image(text: str) -> Image:
    image = Image.new("1", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), text, font=FONT, fill=1)

    return image