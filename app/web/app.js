const messageInput = document.getElementById("message");
const status = document.getElementById("status");

const protocol = location.protocol === "https:" ? "wss" : "ws";
const socket = new WebSocket(`${protocol}://${location.host}/ws`);

let sequence = 0;

//every new opening clears the text

input value = "";
input.disabled = true;

socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);

    if (data.type === "ready") {
        input.disabled = false;
        status.textContent = "input connected to OLED display.";
        input.focus();
    } else if (data.type === "ack") {
        recieved.textContent = data.text;
        status.textContent =  `Python recieved #${data.seq} (${data.length}/168).`;
    } else if (data.type === "error") {
        status.textContent = `Error: Not recieved ${data.message}`;
    }
});

input.addEventListener("input", () => {
    if (socket.readyState !== WebSocket.OPEN) {
        input.disabled = true;
        status.textContent = "Change did not go through. Refresh the page and try again.";
        return;
    }
    sequence++;

    socket.send(JSON.stringify({
        seq: sequence,
        text: input.normalize("NFC"),
    }));
});

socket addEventListener("close", () => {
    input.disabled = true;
    status.textContent = "Connection closed. Refresh the page and try again.";
});  

socket.addEventListener("error", () => {
    input.disabled = true;
    status.textContent = "Connection error. Refresh the page and try again.";
}); 

