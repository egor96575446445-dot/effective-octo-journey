<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Chat AI Web</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
:root {
    --bg-dark: #0b0d17;
    --bg-light: #f5f5f5;
    --text-dark: #ffffff;
    --text-light: #020617;
    --accent: #38bdf8;
    --accent-dark: #22d3ee;
    --glass: rgba(255,255,255,0.08);
    --border: rgba(255,255,255,0.15);
}

* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: Inter, system-ui, sans-serif;
    background: var(--bg-dark);
    color: var(--text-dark);
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    transition: 0.3s;
}

body.light { background: var(--bg-light); color: var(--text-light); }

.app {
    width: 100%;
    max-width: 480px;
    height: 90vh;
    background: var(--glass);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 26px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 30px 70px rgba(0,0,0,0.6);
}

.header {
    padding: 18px;
    text-align: center;
    border-bottom: 1px solid var(--border);
}

.header h1 { margin: 0; font-size: 22px; }
.header button {
    position: absolute;
    top: 18px;
    right: 20px;
    padding: 6px 12px;
    border-radius: 12px;
    border: none;
    background: var(--accent);
    color: #020617;
    cursor: pointer;
    font-weight: 600;
}

.chat {
    flex: 1;
    padding: 16px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.msg {
    max-width: 80%;
    padding: 12px 14px;
    border-radius: 16px;
    line-height: 1.4;
    animation: fadeUp 0.3s ease;
}

.user { align-self: flex-end; background: linear-gradient(135deg, var(--accent), var(--accent-dark)); color: #020617; font-weight: 600; }
.ai { align-self: flex-start; background: rgba(255,255,255,0.12); color: white; }
.thinking { font-size: 13px; opacity: 0.7; font-style: italic; }

.input { display: flex; gap: 10px; padding: 14px; border-top: 1px solid var(--border); }
input {
    flex: 1;
    padding: 12px 14px;
    border-radius: 14px;
    border: none;
    outline: none;
    background: rgba(255,255,255,0.15);
    color: inherit;
    font-size: 14px;
}

button.send {
    padding: 12px 16px;
    border-radius: 14px;
    border: none;
    cursor: pointer;
    background: linear-gradient(135deg, var(--accent), var(--accent-dark));
    font-weight: 700;
    color: #020617;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px);}
    to { opacity: 1; transform: translateY(0);}
}
</style>
</head>
<body>

<div class="app">
    <div class="header">
        <h1>Chat AI Web</h1>
        <button onclick="toggleTheme()">Тема</button>
    </div>

    <div class="chat" id="chat">
        <div class="msg ai">Привет! Я Chat AI Web, похожий на ChatGPT. Задай мне любой вопрос.</div>
    </div>

    <div class="input">
        <input id="text" placeholder="Напиши сообщение..." autocomplete="off">
        <button class="send" onclick="send()">➤</button>
    </div>
</div>

<script>
const chat = document.getElementById("chat");
const input = document.getElementById("text");
let knowledge = JSON.parse(localStorage.getItem("aiKnowledge")) || {};

function send() {
    const text = input.value.trim();
    if (!text) return;
    addMsg(text, "user");
    input.value = "";

    const thinking = addMsg("Нейросеть думает...", "ai");
    thinking.classList.add("thinking");

    setTimeout(() => {
        thinking.remove();
        const answer = generateAnswer(text);
        addMsg(answer, "ai");
    }, 800);
}

function addMsg(text, type) {
    const div = document.createElement("div");
    div.className = "msg " + type;
    div.textContent = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    return div;
}

function generateAnswer(q) {
    const lowerQ = q.toLowerCase();
    if (knowledge[lowerQ]) return knowledge[lowerQ];
    const defaults = [
        "Интересно! Можешь научить меня этому?",
        "Я пока не знаю ответа. Давай обучим меня!",
        "Хочешь, чтобы я запомнил правильный ответ?",
        "Пока не знаю, но скоро научусь!"
    ];
    setTimeout(() => teach(lowerQ), 300);
    return defaults[Math.floor(Math.random() * defaults.length)];
}

function teach(question) {
    const answer = prompt("Я не знаю, как ответить на:\n“" + question + "”\nНапиши, что мне отвечать:");
    if (answer) {
        knowledge[question] = answer;
        localStorage.setItem("aiKnowledge", JSON.stringify(knowledge));
        addMsg("Запомнил! В следующий раз отвечу: " + answer, "ai");
    }
}

// Отправка по Enter
input.addEventListener("keydown", e => { if(e.key==="Enter") send(); });

// Переключение темы
function toggleTheme() {
    document.body.classList.toggle("light");
}
</script>

</body>
</html>
