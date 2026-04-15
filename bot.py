import os
import requests
import time
import json
from datetime import datetime

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
LAST_UPDATE_ID = 0
ADMINS = [7533851056]
TICKETS_FILE = "tickets.json"
FAQ_FILE = "faq.json"

def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        if reply_markup:
            data["reply_markup"] = reply_markup
        requests.post(url, json=data, timeout=10)
        print("✅ Отправлено")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def send_buttons(chat_id, text):
    reply_markup = {
        "keyboard": [
            ["❓ Частые вопросы", "📋 Создать тикет"],
            ["📜 Мои тикеты", "ℹ️ О сервере"],
            ["🌐 Сайт", "📢 Новости"]
        ],
        "resize_keyboard": True
    }
    send_message(chat_id, text, reply_markup)

def get_updates():
    global LAST_UPDATE_ID
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"offset": LAST_UPDATE_ID, "timeout": 10}
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
        return {"ok": False}
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        return {"ok": False}

def save_ticket(ticket):
    try:
        with open(TICKETS_FILE, "r", encoding="utf-8") as f:
            tickets = json.load(f)
    except:
        tickets = []
    tickets.append(ticket)
    with open(TICKETS_FILE, "w", encoding="utf-8") as f:
        json.dump(tickets, f, ensure_ascii=False, indent=2)

def load_tickets(user_id=None):
    try:
        with open(TICKETS_FILE, "r", encoding="utf-8") as f:
            tickets = json.load(f)
        if user_id:
            return [t for t in tickets if t.get("user_id") == user_id]
        return tickets
    except:
        return []

def update_ticket(ticket_id, status, admin_response=None):
    try:
        with open(TICKETS_FILE, "r", encoding="utf-8") as f:
            tickets = json.load(f)
        for t in tickets:
            if t.get("id") == ticket_id:
                t["status"] = status
                if admin_response:
                    t["admin_response"] = admin_response
                    t["response_time"] = datetime.now().isoformat()
                break
        with open(TICKETS_FILE, "w", encoding="utf-8") as f:
            json.dump(tickets, f, ensure_ascii=False, indent=2)
    except:
        pass

def load_faq():
    default_faq = {
        "Как зайти на сервер?": "IP: arm-mine.ru\nПорт: 19132",
        "Как создать тикет?": "Нажми '📋 Создать тикет' и напиши: Тема: текст",
        "Правила сервера": "1. Не гриферить\n2. Не использовать читы\n3. Уважать игроков"
    }
    try:
        with open(FAQ_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        with open(FAQ_FILE, "w", encoding="utf-8") as f:
            json.dump(default_faq, f, ensure_ascii=False, indent=2)
        return default_faq

def send_to_admins(ticket_info, user_info):
    message = f"""🆕 *НОВЫЙ ТИКЕТ!* 🆕

📋 *ID:* `{ticket_info['id']}`
👤 *От:* {user_info.get('first_name', 'Неизвестно')}
📝 *Тема:* {ticket_info.get('subject')}
📄 *Сообщение:* {ticket_info.get('message')}

💬 *Ответь:* /answer_{ticket_info['id']} [текст]"""
    for admin_id in ADMINS:
        send_message(admin_id, message)

def generate_ticket_id():
    return len(load_tickets()) + 1

def ai_response(message, username, user_id):
    msg = message.lower().strip()
    
    if msg == "/start":
        return f"🌟 *Добро пожаловать в ArmMine, {username}!* 🌟\n\n🛡️ *Бот поддержки*\n\nВыбери пункт в меню 👇", "buttons"
    
    if message == "❓ Частые вопросы":
        faq = load_faq()
        text = "📚 *Часто задаваемые вопросы:*\n\n"
        for i, (q, a) in enumerate(faq.items(), 1):
            text += f"{i}. *{q}*\n   {a}\n\n"
        return text
    
    if message == "ℹ️ О сервере":
        return """ℹ️ *О сервере ArmMine*

🎮 Версия: Minecraft Bedrock 1.20+
🌐 IP: arm-mine.ru
🔌 Порт: 19132"""
    
    if message == "🌐 Сайт":
        return "🌐 *Наш сайт:* arm-mine.ru"
    
    if message == "📢 Новости":
        return """📢 *НОВОСТИ БОТА*

✅ Бот поддержки работает
✅ Система тикетов
✅ FAQ
✅ Умные кнопки

🤖 ArmMine Bot — всегда поможет!"""
    
    if message == "📋 Создать тикет" or msg == "/new":
        return "📋 *Создание тикета*\n\nНапиши в формате:\n`Тема: текст`\n\n📌 Пример: `Проблема с донатом: не пришёл`"
    
    if ":" in message and len(message) > 5 and message not in ["❓ Частые вопросы", "📋 Создать тикет", "📜 Мои тикеты", "ℹ️ О сервере", "🌐 Сайт", "📢 Новости"]:
        parts = message.split(":", 1)
        subject = parts[0].strip()
        body = parts[1].strip()
        
        ticket_id = generate_ticket_id()
        ticket = {"id": ticket_id, "user_id": user_id, "username": username, "subject": subject, "message": body, "time": datetime.now().strftime('%d.%m.%Y %H:%M:%S'), "status": "открыт"}
        save_ticket(ticket)
        send_to_admins(ticket, {"id": user_id, "first_name": username})
        return f"✅ *Тикет #{ticket_id} создан!* Администратор скоро ответит."
    
    if message == "📜 Мои тикеты" or msg == "/mytickets":
        tickets = load_tickets(user_id)
        if not tickets:
            return "📜 *У тебя пока нет тикетов*"
        text = "📜 *Твои тикеты:*\n\n"
        for t in tickets:
            status_emoji = "🟢" if t["status"] == "открыт" else "🔴"
            text += f"{status_emoji} *#{t['id']}* — {t['subject']} (статус: {t['status']})\n"
        return text
    
    if msg.startswith("/answer_"):
        if user_id not in ADMINS:
            return "⛔ Нет прав!"
        try:
            parts = msg.split(" ", 1)
            ticket_id = int(parts[0].replace("/answer_", ""))
            admin_text = parts[1] if len(parts) > 1 else ""
            if not admin_text:
                return "❌ Используй: /answer_123 Твой ответ"
            tickets = load_tickets()
            for t in tickets:
                if t.get("id") == ticket_id:
                    update_ticket(ticket_id, "отвечен", admin_text)
                    send_message(t["user_id"], f"📨 *Ответ администратора* на тикет #{ticket_id}\n\n{admin_text}")
                    return f"✅ Ответ отправлен на тикет #{ticket_id}"
            return f"❌ Тикет #{ticket_id} не найден"
        except:
            return "❌ Используй: /answer_123 Твой ответ"
    
    return f"📝 {username}, выбери пункт в меню или /help"

print("="*50)
print("🤖 ARMMINE - БОТ ПОДДЕРЖКИ")
print("="*50)
print("✅ @ArmMine_Bot")
print("🛑 Остановка: Ctrl+C")
print("="*50)

try:
    while True:
        try:
            data = get_updates()
            if data and data.get("ok") and data.get("result"):
                for update in data["result"]:
                    LAST_UPDATE_ID = update["update_id"] + 1
                    if "message" in update and update["message"].get("text"):
                        msg = update["message"]
                        chat_id = msg["chat"]["id"]
                        text = msg["text"]
                        username = msg["chat"].get("first_name", "User")
                        user_id = msg["chat"]["id"]
                        print(f"📨 {username}: {text}")
                        response = ai_response(text, username, user_id)
                        if response:
                            if isinstance(response, tuple):
                                send_buttons(chat_id, response[0])
                            else:
                                send_message(chat_id, response)
            time.sleep(0.5)
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
            time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Бот остановлен!")
  
