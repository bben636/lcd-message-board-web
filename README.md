# Raspberry Pi OLED Web — Architecture Learning Project

An educational project for learning and demonstrating software architecture by building a working system, one module at a time.

The application will let users type in a web interface and see every accepted change appear on a physical OLED display connected to a Raspberry Pi. A USB camera will provide a live view of the display and record its changes during typing.

**Status: In development. The scope below includes planned functionality and learning goals; not all features are implemented yet.**

## Planned Functionality

- A web interface built with HTML, CSS, and JavaScript.
- A Python backend using FastAPI and Uvicorn.
- WebSocket communication that sends each input change immediately, including typing, deletion, pasting, and replacement, without a submit button.
- A maximum of 168 characters, using a software layout of 21 columns and 8 rows on a 128 × 64 OLED display.
- Text rendering with Pillow and display communication through I²C using the SSD1306 driver.
- Validation of text length and supported characters on the server, alongside browser input limits.
- One active editor at a time. A new client takes control, clears the previous message, and starts with an empty input field and display.
- Revocation of the previous client's control and invalidation of its pending updates.
- Ordered processing of accepted edits, with bounded queues and explicit handling of overload and connection failures.
- Change sequence numbers and acknowledgements after the corresponding display write completes.
- A USB camera connected to the Raspberry Pi, with live video embedded in the web interface and recording of display changes during typing.
- Coordination between display clearing, camera capture, and client handover so a new visitor is not shown the previous user's message or buffered video frames.
- Public internet access over HTTPS through a tunnel.
- Automatic application startup and restart management with systemd.
- User login and access control for the website, WebSocket connection, and video endpoints. Cookie sessions and JWT-based approaches will be evaluated during the security phase.
- Input and message-size limits, rate limiting, error handling, and operational logging.

## Architecture and Engineering Goals

- Build a modular monolith: one application with clear boundaries between the web interface, transport, application logic, rendering, hardware access, camera, and authentication.
- Separate responsibilities so each module can be understood and tested independently.
- Coordinate asynchronous network communication with blocking hardware I/O through one dedicated display worker.
- Manage hardware initialization, connection cleanup, and graceful shutdown.
- Use dependency injection and simulated hardware to test application behavior without a Raspberry Pi.
- Add automated tests with pytest for rendering, validation, ownership changes, update ordering, error handling, and HTTP/WebSocket behavior.
- Verify hardware behavior separately on the Raspberry Pi.
- Use Git and GitHub for version control, branches, commits, and pull requests.
- Build GitHub Actions pipelines that run automated tests and code-quality checks on pushes and pull requests.
- Document setup, execution, testing, deployment, and architectural decisions in the repository.

## Hardware

- Raspberry Pi 4 running Debian 12 (Bookworm).
- GERUI 0.96-inch, 128 × 64 I²C OLED display.
- GPIO breakout board and connecting wires.
- USB camera, to be added during the camera phase.
