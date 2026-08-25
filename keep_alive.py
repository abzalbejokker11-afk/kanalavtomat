from flask import Flask
from threading import Thread
import time
import requests
import os

app = Flask('')

@app.route('/')
def home():
    return "Antidoping Telegram Bot is running! 🚀"

def run():
    app.run(host='0.0.0.0', port=8080)

def ping_itself():
    # Render'dagi aniq manzilni olamiz yoki defaultni ishlatamiz
    url = os.environ.get("RENDER_EXTERNAL_URL", "https://kanalavtomat.onrender.com")
    while True:
        time.sleep(600)  # Har 10 daqiqada
        try:
            requests.get(url, timeout=10)
            print(f"Uyquni buzish uchun PING yuborildi: {url}")
        except Exception as e:
            print(f"Ping xatosi: {e}")

def keep_alive():
    t = Thread(target=run, daemon=True)
    t.start()
    
    # Self-ping threadini ishga tushirish (Render uxlamasligi uchun)
    p = Thread(target=ping_itself, daemon=True)
    p.start()
