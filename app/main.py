from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.display import OledDisplay
from app.display_service import DisplayService


WEB_DIR = Path(__file__).resolve().parent / "web"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect to the OLED Hardware
    display = OledDisplay()
    
    try:
        # creating service and make it available in the app state
        service = DisplayService(display)
        app.state.display_service = service
        service.show_text("works")
        print("Display service initialized.")
        
        #available while the app is running
        yield
    finally:
        #release i2c durring shutdown
        display.close()
        print("Display service closed.")


app = FastAPI(title="OLED Web Project", lifespan=lifespan)

@app.get("/", response_class=FileResponse)
def index():
    """Serve the index.html file from the web directory."""
    return FileResponse(
        WEB_DIR / "index.html",
        media_type="text/html",
    )
    
@app.get("/app.js", response_class=FileResponse)
def app_js():
    """Serve the app.js file from the web directory."""
    return FileResponse(
        WEB_DIR / "app.js",
        media_type="application/javascript",
    )
    
    