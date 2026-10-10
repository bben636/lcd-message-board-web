const messageInput = document.getElementById("message");
const status = document.getElementById("status");

// Clear the browser input and wait for the server's ready message.
messageInput.value = "";
messageInput.disabled = true;
status.textContent = "Connecting...";

const protocol = location.protocol === "https:" ? "wss" : "ws";
const socket = new WebSocket(`${protocol}://${location.host}/ws`);

let sequence = 0;

socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);

    if (data.type === "ready") {
        messageInput.disabled = false;
        status.textContent = "Connected to server.";
        messageInput.focus();
    } else if (data.type === "ack") {
        status.textContent =
            `Python received #${data.seq} (${data.length}/168).`;
    } else if (data.type === "error") {
        status.textContent = `Error: ${data.message}`;
    }
});

// Send the current text after every user edit, including deletion and paste.
messageInput.addEventListener("input", () => {
    if (socket.readyState !== WebSocket.OPEN) {
        messageInput.disabled = true;
        status.textContent =
            "Change was not sent. Refresh the page and try again.";
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
    status.textContent =
        "Connection closed. Refresh the page and try again.";
});

socket.addEventListener("error", () => {
    messageInput.disabled = true;
    status.textContent =
        "Connection error. Refresh the page and try again.";
});

