import requests
import time

TOKEN = "8797631228:AAH5ddV8v1FwQ0ACsn-vDPWjDFdQdR7Xq80"
LAST_UPDATE_ID = 0

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=5)
        print("✅ Отправлено")
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

print("="*50)
print("🤖 Бот @SimpleBot_2025_bot запущен!")
print("✅ Работаю 24/7 на Render.com")
print("="*50)

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
                    
                    if text.lower() == "привет":
                        reply = f"Привет, {username}! 👋\n\nЯ работаю 24/7 на Render.com!"
                    else:
                        reply = f"📝 {username}, ты написал: {text}"
                    
                    send_message(chat_id, reply)
        
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(1)
