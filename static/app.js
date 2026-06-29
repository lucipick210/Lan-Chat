let currentRoom = "general";
let lastCount = {};

function logout() {
    localStorage.removeItem("username");
    window.location.href = "/login.html";
}

function getMessagesDiv() {
    return document.getElementById("messages");
}

async function loadMessages() {
    const messagesDiv = getMessagesDiv();
    if (!messagesDiv) return;

    const response = await fetch("/messages");
    const data = await response.json();


    const messages = data[currentRoom] || [];

    if (!(currentRoom in lastCount)) {
        lastCount[currentRoom] = -1;
    }

    if (messages.length === lastCount[currentRoom]) return;

    const wasNearBottom =
        messagesDiv.scrollHeight -
        messagesDiv.scrollTop -
        messagesDiv.clientHeight < 80;

    let html = "";

    for (let i = 0; i < messages.length; i++) {
        const msg = messages[i];

        html += `
            <div class="message">
                <b>${msg.username}</b>
                <span class="time">${msg.time || ""}</span>
                <br>
                ${msg.message}
            </div>
        `;
    }

    messagesDiv.innerHTML = html;

    if (wasNearBottom) {
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    lastCount[currentRoom] = messages.length;
}

function sendMessage() {
    const usernameEl = document.getElementById("username");
    const messageEl = document.getElementById("message");

    const username = usernameEl.value;
    const message = messageEl.value;

    if (message.trim() === "") return;

    fetch("/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username,
            message,
            time: new Date().toLocaleTimeString(),
            room: currentRoom
        })
    });

    messageEl.value = "";
    loadMessages();
}

function changeRoom(room, element) {
    currentRoom = room;

    document.querySelectorAll(".room")
        .forEach(r => r.classList.remove("active"));

    if (element) element.classList.add("active");

    const messagesDiv = getMessagesDiv();
    if (messagesDiv) messagesDiv.innerHTML = "";
    document.getElementById("roomTitle").innerText = "#" + room;
    
    lastCount[currentRoom] = -1;

    loadMessages();
}

// enter send
function initChat() {
    const input = document.getElementById("message");

    if (input) {
        input.addEventListener("keypress", e => {
            if (e.key === "Enter") sendMessage();
        });
    }

    // username persist
    const usernameEl = document.getElementById("username");
    if (usernameEl && localStorage.username) {
        usernameEl.value = localStorage.username;
    }

    setInterval(loadMessages, 1000);
    loadMessages();
}

window.addEventListener("DOMContentLoaded", initChat);