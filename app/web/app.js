const messageInput = document.getElementById("message");
const status = document.getElementById("status");

const setStatus = (message, state = "") => {
    status.textContent = message;
    status.className = `status ${state}`.trim();
};

// Clear the browser input and wait for the server's ready message.
messageInput.value = "";
messageInput.disabled = true;
setStatus("Connecting...", "connecting");

const protocol = location.protocol === "https:" ? "wss" : "ws";
const socket = new WebSocket(`${protocol}://${location.host}/ws`);

let sequence = 0;

socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);

    if (data.type === "ready") {
        messageInput.disabled = false;
        setStatus("Connected to server.", "connected");
        messageInput.focus();
    } else if (data.type === "ack") {
        setStatus(`Display received #${data.seq} (${data.length}/168).`, "connected");
    } else if (data.type === "error") {
        setStatus(`Error: ${data.message}`, "error");
    }
});

// Send the current text after every user edit, including deletion and paste.
messageInput.addEventListener("input", () => {
    if (socket.readyState !== WebSocket.OPEN) {
        messageInput.disabled = true;
        setStatus("Change was not sent. Refresh the page and try again.", "error");
        return;
    }

    sequence++;

    socket.send(JSON.stringify({
        seq: sequence,
        text: messageInput.value.normalize("NFC"),
    }));
});

socket.addEventListener("close", () => {
    messageInput.disabled = true;
    setStatus("Connection closed. Refresh the page and try again.", "error");
});

socket.addEventListener("error", () => {
    messageInput.disabled = true;
    setStatus("Connection error. Refresh the page and try again.", "error");
});

