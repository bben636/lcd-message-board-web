import asyncio
from pathlib import Path
from json import JSONDecodeError
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from app.display import OledDisplay
from app.display_service import DisplayService
from app.message_validation import parse_text_update



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
        app.state.client_lock = asyncio.Lock()
        app.state.active_websocket = None
        
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
    client_lock = websocket.app.state.client_lock

    await websocket.accept()

    async def send_if_active(message):
        async with client_lock:
            if websocket.app.state.active_websocket is not websocket:
                return False
            await websocket.send_json(message)
            return True

    async with client_lock:
        previous_websocket = websocket.app.state.active_websocket
        websocket.app.state.active_websocket = websocket
        if previous_websocket is not None:
            try:
                await previous_websocket.close(
                    code=4001,
                    reason="Display control was taken over by another client.",
                )
            except RuntimeError:
                pass

    try:
        async with display_lock:
            if websocket.app.state.active_websocket is not websocket:
                return
            await asyncio.to_thread(service.show_text, "")

        if not await send_if_active({"type": "ready"}):
            return
        
        while True:
            try:
                # Decode the incoming JSON message.
                data = await websocket.receive_json()

                # Validate its structure and extract the values.
                sequence, text = parse_text_update(data)

                # Update the display only after validation succeeds.
                async with display_lock:
                    if websocket.app.state.active_websocket is not websocket:
                        return
                    await asyncio.to_thread(service.show_text, text)

            except JSONDecodeError:
                if not await send_if_active({
                    "type": "error",
                    "message": "Message must contain valid JSON.",
                }):
                    return
                continue

            except ValueError as exc:
                if not await send_if_active({
                    "type": "error",
                    "message": str(exc),
                }):
                    return
                continue

            # Confirm only after the display update finishes.
            if not await send_if_active({
                "type": "ack",
                "seq": sequence,
                "text": text,
                "length": len(text),
            }):
                return
    except WebSocketDisconnect:
        print("Client disconnected.")
    finally:
        async with client_lock:
            if websocket.app.state.active_websocket is websocket:
                websocket.app.state.active_websocket = None