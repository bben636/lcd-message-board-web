from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

WEB_DIR = Path(__file__).resolve().parent / "web"

app = FastAPI(title="OLED Web Project")

@app.get("/", response_class=FileResponse)
def index():
    """Serve the index.html file from the web directory."""
    return FileResponse(
        WEB_DIR / "index.html",
        media_type="text/html",
    )