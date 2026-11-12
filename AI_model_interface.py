
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

url = "http://localhost:11434/api/generate"

html = """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Neo AI Assistant</title>

<style>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: "Segoe UI", Arial, sans-serif;
    background: #080d18;
    color: #e8edf7;
    height: 100vh;
    overflow: hidden;
}

/* MAIN LAYOUT */

.container {
    display: flex;
    height: 100vh;
}

/* SIDEBAR */

.sidebar {
    width: 260px;
    background: #0d1422;
    border-right: 1px solid #263449;
    padding: 25px 18px;
    display: flex;
    flex-direction: column;
    z-index: 5;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 45px;
}

.logo-icon {
    width: 38px;
    height: 38px;
    background: linear-gradient(135deg, #00d9ff, #6966ff);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    box-shadow: 0 0 20px #00d9ff55;
}

.new-chat {
    padding: 14px;
    border: 1px solid #30415c;
    background: #172238;
    color: white;
    border-radius: 12px;
    cursor: pointer;
    font-size: 14px;
    transition: 0.3s;
}

.new-chat:hover {
    background: #203451;
    border-color: #00d9ff;
    box-shadow: 0 0 15px #00d9ff33;
}

.sidebar-heading {
    color: #7888a2;
    font-size: 11px;
    letter-spacing: 2px;
    margin: 35px 0 15px;
}

.history {
    color: #aab6ca;
    padding: 12px;
    border-radius: 9px;
    font-size: 13px;
    cursor: pointer;
}

.history:hover {
    background: #1b2940;
}

.sidebar-bottom {
    margin-top: auto;
    border-top: 1px solid #263449;
    padding-top: 20px;
    color: #8e9bb0;
    font-size: 12px;
}

/* MAIN CONTENT */

.main {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
    position: relative;
    isolation: isolate;
    overflow: hidden;
    background: #080d18;
}

/* ANIMATED BACKGROUND */

.main::before {
    content: "";
    position: absolute;
    inset: -50%;
    z-index: -2;
    pointer-events: none;

    background:
        radial-gradient(circle at 20% 30%, #00d9ff35, transparent 25%),
        radial-gradient(circle at 80% 40%, #6755ff35, transparent 28%),
        radial-gradient(circle at 50% 85%, #00b8ff22, transparent 30%);

    animation: backgroundMove 16s ease-in-out infinite alternate;
}

.main::after {
    content: "";
    position: absolute;
    inset: 0;
    z-index: -1;
    pointer-events: none;

    background-image:
        linear-gradient(#80cfff0a 1px, transparent 1px),
        linear-gradient(90deg, #80cfff0a 1px, transparent 1px);

    background-size: 45px 45px;

    mask-image: linear-gradient(
        to bottom,
        transparent,
        black 25%,
        black 75%,
        transparent
    );

    animation: gridMove 20s linear infinite;
}

@keyframes backgroundMove {

    0% {
        transform: translate(-3%, -2%) rotate(0deg) scale(1);
    }

    50% {
        transform: translate(3%, 2%) rotate(8deg) scale(1.08);
    }

    100% {
        transform: translate(-2%, 4%) rotate(-5deg) scale(1.12);
    }

}

@keyframes gridMove {

    from {
        background-position: 0 0;
    }

    to {
        background-position: 45px 45px;
    }

}

/* FLOATING PARTICLES */

.particles {
    position: absolute;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    overflow: hidden;
}

.particle {
    position: absolute;
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: #42dcff;
    box-shadow: 0 0 12px #00d9ff;
    opacity: 0;
    animation: floatParticle 10s linear infinite;
}

.particle:nth-child(1) {
    left: 10%;
    animation-delay: 0s;
}

.particle:nth-child(2) {
    left: 25%;
    animation-delay: 2s;
}

.particle:nth-child(3) {
    left: 45%;
    animation-delay: 4s;
}

.particle:nth-child(4) {
    left: 65%;
    animation-delay: 1s;
}

.particle:nth-child(5) {
    left: 85%;
    animation-delay: 3s;
}

.particle:nth-child(6) {
    left: 55%;
    animation-delay: 6s;
}

@keyframes floatParticle {

    0% {
        transform: translateY(100vh) scale(0.5);
        opacity: 0;
    }

    15% {
        opacity: 0.8;
    }

    85% {
        opacity: 0.5;
    }

    100% {
        transform: translateY(-100px) scale(1.5);
        opacity: 0;
    }

}

/* HEADER */

.header {
    height: 75px;
    border-bottom: 1px solid #263449;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 35px;
    background: #101827cc;
    backdrop-filter: blur(15px);
    z-index: 2;
}

.header h2 {
    font-size: 17px;
    font-weight: 600;
}

.status {
    display: flex;
    align-items: center;
    gap: 9px;
    font-size: 12px;
    color: #a9b8ca;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #30e7a1;
    border-radius: 50%;
    box-shadow: 0 0 12px #30e7a1;
    animation: blink 1.5s infinite;
}

@keyframes blink {

    50% {
        opacity: 0.3;
    }

}

/* CHAT AREA */

.chat-box {
    flex: 1;
    overflow-y: auto;
    padding: 35px 8%;
    scroll-behavior: smooth;
    z-index: 1;
}

.chat-box::-webkit-scrollbar {
    width: 6px;
}

.chat-box::-webkit-scrollbar-thumb {
    background: #344b68;
    border-radius: 10px;
}

.welcome {
    text-align: center;
    margin: 45px auto 55px;
}

.ai-orb {
    width: 100px;
    height: 100px;
    margin: 0 auto 25px;
    border-radius: 50%;

    background: radial-gradient(
        circle at 30% 30%,
        #9cf5ff,
        #00a9dd 35%,
        #3438a6 75%
    );

    box-shadow:
        0 0 25px #00d9ff88,
        0 0 65px #5755ff55;

    animation: pulse 2.5s ease-in-out infinite;
    position: relative;
}

.ai-orb::after {
    content: "";
    position: absolute;
    inset: -12px;
    border: 1px solid #00d9ff66;
    border-radius: 50%;
    animation: ring 2.5s ease-out infinite;
}

@keyframes pulse {

    0%, 100% {
        transform: scale(1);
        box-shadow: 0 0 25px #00d9ff88, 0 0 65px #5755ff55;
    }

    50% {
        transform: scale(1.08);
        box-shadow: 0 0 40px #00d9ffaa, 0 0 90px #5755ff77;
    }

}

@keyframes ring {

    0% {
        transform: scale(0.9);
        opacity: 1;
    }

    100% {
        transform: scale(1.35);
        opacity: 0;
    }

}

.welcome h1 {
    font-size: 34px;
    background: linear-gradient(90deg, #ffffff, #79dfff, #a69aff);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
    margin-bottom: 12px;
}

.welcome p {
    color: #8c9bb2;
    font-size: 14px;
}

/* MESSAGES */

.message {
    padding: 16px 20px;
    margin-bottom: 22px;
    max-width: 80%;
    line-height: 1.7;
    font-size: 14px;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    animation: messageIn 0.35s ease;
}

@keyframes messageIn {

    from {
        opacity: 0;
        transform: translateY(12px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }

}

.user {
    margin-left: auto;
    background: linear-gradient(135deg, #176d91, #344b9c);
    color: white;
    border-radius: 17px 17px 3px 17px;
}

.ai {
    margin-right: auto;
    background: #172438;
    border: 1px solid #2b405d;
    border-radius: 17px 17px 17px 3px;
}

/* INPUT AREA */

.input-wrapper {
    padding: 20px 8% 25px;
    background: linear-gradient(transparent, #080d18 25%);
    z-index: 2;
}

.input-area {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #131f32;
    border: 1px solid #344761;
    border-radius: 16px;
    padding: 10px;
    transition: 0.3s;
}

.input-area:focus-within {
    border-color: #00cfff;
    box-shadow: 0 0 20px #00cfff22;
}

input {
    flex: 1;
    min-width: 0;
    background: transparent;
    border: none;
    outline: none;
    color: white;
    padding: 12px;
    font-size: 14px;
}

input::placeholder {
    color: #7889a2;
}

.send-button {
    width: 45px;
    height: 45px;
    border-radius: 12px;
    background: linear-gradient(135deg, #00d9ff, #6570ff);
    color: white;
    font-size: 20px;
    transition: 0.3s;
}

.send-button:hover {
    transform: scale(1.07);
    box-shadow: 0 0 18px #00d9ff88;
}

.send-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.footer-text {
    text-align: center;
    font-size: 11px;
    color: #65748a;
    margin-top: 13px;
}

/* THEME BUTTON */

.theme-button {
    background: #1c2a40;
    color: white;
    padding: 10px 13px;
    border-radius: 10px;
    cursor: pointer;
    transition: 0.3s;
}

.theme-button:hover {
    background: #304867;
}

/* LIGHT THEME */

body.light {
    background: #edf2fa;
    color: #18253a;
}

body.light .sidebar {
    background: #f8faff;
    border-color: #dce4f0;
}

body.light .main {
    background: #edf2fa;
}

body.light .main::before {
    background:
        radial-gradient(circle at 20% 30%, #00b8ff30, transparent 25%),
        radial-gradient(circle at 80% 40%, #8975ff25, transparent 28%),
        radial-gradient(circle at 50% 85%, #42d9d022, transparent 30%);
}

body.light .main::after {
    background-image:
        linear-gradient(#426c9910 1px, transparent 1px),
        linear-gradient(90deg, #426c9910 1px, transparent 1px);
}

body.light .header {
    background: #ffffffcc;
    border-color: #dce4f0;
}

body.light .input-area {
    background: #ffffff;
    border-color: #ccd9e9;
}

body.light input {
    color: #18253a;
}

body.light .ai {
    background: #ffffff;
    color: #18253a;
    border-color: #dce4f0;
}

body.light .history {
    color: #45546a;
}

body.light .sidebar-bottom {
    border-color: #dce4f0;
}

body.light .welcome p {
    color: #65748a;
}

body.light .footer-text {
    color: #65748a;
}

body.light .theme-button {
    background: #e1eafa;
    color: #18253a;
}

body.light .sidebar-heading {
    color: #718096;
}

body.light .new-chat {
    background: #e8f0fc;
    color: #18253a;
    border-color: #d0ddeb;
}

body.light .status {
    color: #45546a;
}

body.light .input-wrapper {
    background: linear-gradient(transparent, #edf2fa 25%);
}

/* MOBILE */

@media(max-width: 700px) {

    .sidebar {
        display: none;
    }

    .header {
        padding: 0 18px;
    }

    .chat-box {
        padding: 20px;
    }

    .input-wrapper {
        padding: 15px;
    }

    .welcome h1 {
        font-size: 26px;
    }

    .message {
        max-width: 92%;
    }

}

@media (prefers-reduced-motion: reduce) {

    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
    }

}

</style>

</head>

<body>

<div class="container">

    <!-- SIDEBAR -->

    <aside class="sidebar">

        <div class="logo">

            <div class="logo-icon">✦</div>

            <span>NEO AI</span>

        </div>

        <button class="new-chat" onclick="newChat()">
            + &nbsp; New Conversation
        </button>

        <div class="sidebar-heading">WORKSPACE</div>

        <div class="history">✦ &nbsp; AI Assistant</div>

        <div class="history">◈ &nbsp; Recent Chat</div>

        <div class="sidebar-bottom">

            <p>Powered by Ollama</p>

            <p style="margin-top:8px;">Llama 3.2 • Local AI</p>

        </div>

    </aside>

    <!-- MAIN CONTENT -->

    <main class="main">

        <!-- FLOATING PARTICLES -->

        <div class="particles">

            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>

        </div>

        <!-- HEADER -->

        <header class="header">

            <h2>NEO AI Assistant</h2>

            <div style="display:flex;align-items:center;gap:20px;">

                <div class="status">

                    <span class="status-dot"></span>

                    AI System Online

                </div>

                <button
                    class="theme-button"
                    onclick="toggleTheme()"
                    id="themeButton"
                >
                    ☼
                </button>

            </div>

        </header>

        <!-- CHAT AREA -->

        <div class="chat-box" id="chatBox">

            <div class="welcome" id="welcome">

                <div class="ai-orb"></div>

                <h1>Welcome to NEO AI</h1>

                <p>Your intelligent assistant is ready. What can I help you with?</p>

            </div>

            <div class="message ai">
                Hello! I'm NEO AI. Ask me anything.
            </div>

        </div>

        <!-- INPUT AREA -->

        <div class="input-wrapper">

            <div class="input-area">

                <input
                    type="text"
                    id="userInput"
                    placeholder="Message NEO AI..."
                    autocomplete="off"
                >

                <button
                    class="send-button"
                    id="sendButton"
                    onclick="sendMessage()"
                >
                    ↑
                </button>

            </div>

            <div class="footer-text">
                NEO AI can make mistakes. Verify important information.
            </div>

        </div>

    </main>

</div>

<script>

/* SEND MESSAGE */

async function sendMessage() {

    const input = document.getElementById("userInput");

    const button = document.getElementById("sendButton");

    const chatBox = document.getElementById("chatBox");

    const welcome = document.getElementById("welcome");

    const message = input.value.trim();

    if (message === "") {
        return;
    }

    if (welcome) {
        welcome.style.display = "none";
    }

    const userMessage = document.createElement("div");

    userMessage.className = "message user";

    userMessage.textContent = message;

    chatBox.appendChild(userMessage);

    input.value = "";

    button.disabled = true;

    const loadingMessage = document.createElement("div");

    loadingMessage.className = "message ai";

    loadingMessage.textContent = "✦ NEO AI is thinking...";

    chatBox.appendChild(loadingMessage);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Something went wrong.");
        }

        loadingMessage.textContent =
            result.reply || "Empty response";

    }

    catch (error) {

        loadingMessage.textContent =
            "Error: " + error.message;

    }

    finally {

        button.disabled = false;

        chatBox.scrollTop = chatBox.scrollHeight;

        input.focus();

    }

}

/* DARK AND LIGHT THEME */

function toggleTheme() {

    document.body.classList.toggle("light");

    const button = document.getElementById("themeButton");

    if (document.body.classList.contains("light")) {

        button.textContent = "☾";

    } else {

        button.textContent = "☼";

    }

}

/* NEW CHAT */

function newChat() {

    const chatBox = document.getElementById("chatBox");

    chatBox.innerHTML = `

        <div class="welcome" id="welcome">

            <div class="ai-orb"></div>

            <h1>Welcome to NEO AI</h1>

            <p>Your intelligent assistant is ready. What can I help you with?</p>

        </div>

        <div class="message ai">
            Hello! I'm NEO AI. Ask me anything.
        </div>

    `;

}

/* ENTER KEY */

document.getElementById("userInput").addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);

</script>

</body>

</html>

"""


# HOME PAGE

@app.route("/", methods=["GET"])
def home():

    return render_template_string(html)


# NEO AI RESPONSE

@app.route("/ask", methods=["POST"])
def ask_ai():

    user_message = request.json.get("message", "").strip()

    if not user_message:
        return {"error": "Please enter a message."}, 400

    data = {

        "model": "llama3.2:1b",

        "prompt": user_message,

        "stream": False

    }

    try:

        response = requests.post(
            url,
            json=data,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        return {
            "reply": result.get("response", "Empty response")
        }

    except requests.exceptions.RequestException as e:

        return {
            "error": str(e)
        }, 500


# RUN FLASK

if __name__ == "__main__":

    app.run(debug=True)
 