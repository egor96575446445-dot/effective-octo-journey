import requests
import time
import random
import re

TOKEN = "8797631228:AAH5ddV8v1FwQ0ACsn-vDPWjDFdQdR7Xq80"
LAST_UPDATE_ID = 0

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=5)
        print(f"✅ Отправлено")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def send_buttons(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    reply_markup = {
        "keyboard": [
            ["🔍 Поиск", "📊 Пример", "😂 Шутка"],
            ["💻 Код", "📰 Новости", "💰 Курс"],
            ["🌤️ Погода", "🎵 Музыка", "⏰ Напомни"],
            ["❓ Помощь", "ℹ️ Инфо", "🎨 Нарисовать"]
        ],
        "resize_keyboard": True
    }
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text, "reply_markup": reply_markup}, timeout=5)
    except:
        pass

def get_updates():
    global LAST_UPDATE_ID
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"offset": LAST_UPDATE_ID, "timeout": 15}
    try:
        r = requests.get(url, params=params, timeout=20)
        if r.status_code == 200:
            return r.json()
        return {"ok": False}
    except:
        return {"ok": False}

def generate_image(prompt):
    try:
        encoded = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.content
        return None
    except:
        return None

def send_photo(chat_id, photo_data, caption=""):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        files = {"photo": ("image.jpg", photo_data, "image/jpeg")}
        data = {"chat_id": chat_id, "caption": caption}
        requests.post(url, data=data, files=files, timeout=30)
        return True
    except:
        return False

def ai_response(message, username):
    msg = message.lower().strip()
    
    # Обработка кнопок с эмодзи
    if "🔍 поиск" in msg or msg == "поиск":
        return "🔍 *Что ищем?*\n\nНапиши: *найди Python*"
    
    if "📊 пример" in msg or msg == "пример":
        return "📊 *Напиши пример:*\n\nНапример: *15 + 30*"
    
    if "😂 шутка" in msg or msg == "шутка":
        jokes = [
            "🐍 Почему Python популярен? Потому что он удав!",
            "💡 Сколько программистов нужно для лампочки? Ни одного!",
            "🌍 Hello, World! — первое слово каждого программиста!"
        ]
        return f"😂 {random.choice(jokes)}"
    
    if "💻 код" in msg or msg == "код":
        return "💻 *Напиши, что создать:*\n\n• калькулятор\n• игру\n• бота"
    
    if "📰 новости" in msg or msg == "новости":
        return "📰 *Новости*\n\n• Python 3.15 вышел\n• ИИ развивается\n• Render.com — отличный хостинг!"
    
    if "💰 курс" in msg or msg == "курс валют" or msg == "курс":
        return "💰 *Курс валют*\n\n💵 Доллар: ~90 руб\n💶 Евро: ~98 руб"
    
    if "🌤️ погода" in msg or msg == "погода":
        return "🌤️ *Погода*\n\nНапиши: *погода Москва*"
    
    if "🎵 музыка" in msg or msg == "музыка":
        return "🎵 *Музыка*\n\nНапиши: *музыка Imagine Dragons*"
    
    if "⏰ напомни" in msg or msg.startswith("напомни"):
        return "⏰ *Напоминания*\n\nНапиши: *напомни купить хлеб через 10 мин*"
    
    if "❓ помощь" in msg or msg == "помощь" or msg == "/help":
        return """📖 *Команды:*

🎨 нарисуй кота
😂 шутка
🔍 найди Python
📊 15 + 30
🌤️ погода Москва
💰 курс валют
📰 новости
🎵 музыка Imagine Dragons
⏰ напомни... через 10 мин
📅 сколько время"""
    
    if "ℹ️ инфо" in msg or msg == "инфо" or msg == "/info":
        return "ℹ️ *SimpleBot*\n\n✅ Работаю 24/7\n🎨 Генерация картинок\n🐍 Python 3.14\n📍 Хостинг: Render.com"
    
    if "🎨 нарисовать" in msg:
        return "🎨 *Что нарисовать?*\n\nНапиши: *нарисуй кота в космосе*"
    
    # Приветствия
    if msg in ["привет", "здравствуй", "хай", "hello", "ку", "здаров"]:
        return f"Привет, {username}! 👋\n\nЯ работаю 24/7!\n\n• нарисуй кота\n• шутка\n• помощь"
    
    if "как дела" in msg:
        return f"У меня всё отлично, {username}! А у тебя? 😊"
    
    if "спасибо" in msg:
        return f"Пожалуйста, {username}! 😊"
    
    if "пока" in msg:
        return f"До свидания, {username}! 👋"
    
    # Генерация картинок
    if "нарисуй" in msg or "сгенерируй" in msg:
        prompt = re.sub(r'^(нарисуй|сгенерируй)\s*', '', message).strip()
        if prompt and len(prompt) > 2:
            send_message(username, f"🎨 Рисую: {prompt}...")
            image = generate_image(prompt)
            if image:
                send_photo(username, image, f"🎨 {prompt}")
                return None
            return "❌ Не удалось нарисовать. Попробуй другой запрос!"
        return "🎨 Напиши: *нарисуй кота в космосе*"
    
    # Поиск
    if "найди" in msg:
        query = message.replace("найди", "").strip()
        if query:
            return f"🔍 *{query}*\n\nИщу в интернете...\n(скоро добавлю полноценный поиск)"
        return "🔍 Напиши: *найди Python*"
    
    # Математика
    if "+" in msg:
        try:
            parts = msg.split("+")
            if len(parts) == 2:
                a = int(parts[0].strip())
                b = int(parts[1].strip())
                return f"📊 {a} + {b} = {a + b} ✅"
        except:
            pass
    
    if "-" in msg:
        try:
            parts = msg.split("-")
            if len(parts) == 2:
                a = int(parts[0].strip())
                b = int(parts[1].strip())
                return f"📊 {a} - {b} = {a - b} ✅"
        except:
            pass
    
    # /start
    if msg == "/start":
        return f"🌟 Привет, {username}! 🌟\n\nЯ SimpleBot — твой помощник!\n\n👇 Используй кнопки ниже!"
    
    # Стандартный ответ
    return f"📝 {username}, ты написал: {message}\n\nНапиши *помощь* для списка команд!"

print("="*50)
print("🤖 SIMPLEBOT ЗАПУЩЕН!")
print("✅ @SimpleBot_2025_bot")
print("🎨 Генерация картинок: ВКЛ")
print("🔘 Кнопки: ВКЛ")
print("="*50)

# Отправляем приветствие с кнопками
print("🚀 Бот готов к работе!")

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
                    
                    print(f"📨 {username}: {text}")
                    
                    response = ai_response(text, username)
                    if response:
                        # Если команда /start - отправляем с кнопками
                        if text == "/start":
                            send_buttons(chat_id, response)
                        else:
                            send_message(chat_id, response)
        
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(1)
