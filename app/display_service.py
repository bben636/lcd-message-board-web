from app.renderer import render_text

class DisplayService:
    def __init__(self, display):
        self._display = display

    def show_text(self, text: str) -> None:
        image = render_text(text)
        self._display.show(image)