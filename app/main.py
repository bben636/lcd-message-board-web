import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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
        app.state.display_lock = asyncio.Lock()
        
        service.show_text("")
        print("Display initialized.")
        
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
 
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    service = websocket.app.state.display_service
    display_lock = websocket.app.state.display_lock

    # Accept the connection before exchanging messages.
    await websocket.accept()

    try:
        # Clear the display before enabling the browser input.
        async with display_lock:
            await asyncio.to_thread(service.show_text, "")

        await websocket.send_json({"type": "ready"})

        while True:
            data = await websocket.receive_json()
            text = data["text"]
            sequence = data["seq"]

            try:
                # Allow one display update at a time.
                async with display_lock:
                    await asyncio.to_thread(service.show_text, text)
            except ValueError as exc:
                await websocket.send_json({
                    "type": "error",
                    "message": str(exc),
                })
                continue

            # Confirm only after the display update finishes.
            await websocket.send_json({
                "type": "ack",
                "seq": sequence,
                "text": text,
                "length": len(text),
            })
    except WebSocketDisconnect:
        print("Client disconnected.")