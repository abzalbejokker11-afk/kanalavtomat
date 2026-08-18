import os
import sys
import time
import schedule
import json
import requests
from threading import Thread

import keep_alive
import news_scraper
import video_maker

# Tizim konfiguratsiyasi
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "BU_YERGA_TOKEN_YOZING")
CHANNEL_ID = "@uzantidoping"

def send_telegram_message(text, image_url=None, video_file=None):
    if video_file:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVideo"
        with open(video_file, 'rb') as f:
            response = requests.post(url, data={"chat_id": CHANNEL_ID, "caption": text}, files={"video": f}).json()
    elif image_url:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        response = requests.post(url, json={"chat_id": CHANNEL_ID, "photo": image_url, "caption": text}).json()
    else:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        response = requests.post(url, json={"chat_id": CHANNEL_ID, "text": text}).json()
        
    if response.get("ok"):
        print("✅ Telegramga muvaffaqiyatli yuborildi!")
    else:
        print(f"❌ Telegram xatosi: {response.get('description')}")

def post_job():
    print("⏳ Post yuborish vaqti keldi!")
    # Oddiy post yaratish logikasini bu yerga import qilamiz
    try:
        # Autopost.py dan yaratish va yuborish mantiqidan foydalanamiz
        # Hozircha posts.json faylidan o'qiymiz
        if os.path.exists("posts.json"):
            with open("posts.json", "r", encoding="utf-8") as f:
                posts = json.load(f)
            if posts:
                post = posts.pop(0)
                text = post.get("text", "") if isinstance(post, dict) else str(post)
                # Rasmli yuborish (Soddalashtirilgan)
                send_telegram_message(text)
                
                with open("posts.json", "w", encoding="utf-8") as f:
                    json.dump(posts, f, ensure_ascii=False, indent=2)
                return
        
        # Agar post yo'q bo'lsa, zaxira xabar
        print("Hozircha tayyor postlar yo'q. 'python autopost.py yarat' ni ishlating.")
    except Exception as e:
        print(f"Xatolik: {e}")

def news_job():
    print("⏳ Yangiliklar vaqti keldi (20:00)!")
    news_text = news_scraper.generate_news_post()
    if news_text:
        send_telegram_message(news_text)
    else:
        print("Bugun uchun yangilik topilmadi.")

def video_job():
    print("⏳ Video yuborish vaqti keldi (12:00)!")
    if os.path.exists("posts.json"):
        with open("posts.json", "r", encoding="utf-8") as f:
            posts = json.load(f)
        if posts:
            post = posts[0] # Videoga birinchi post matnini olamiz
            text = post.get("text", "") if isinstance(post, dict) else str(post)
            img_url = "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500&h=500&fit=crop"
            
            video_file = video_maker.create_video(text, img_url)
            if video_file:
                send_telegram_message(text[:200] + "...", video_file=video_file)
                os.remove(video_file)
                return
                
    print("Video tayyorlash uchun post topilmadi.")

def run_schedule():
    # Kunlik reja:
    schedule.every().day.at("08:00").do(post_job)
    schedule.every().day.at("10:00").do(post_job)
    schedule.every().day.at("12:00").do(video_job)
    schedule.every().day.at("14:00").do(post_job)
    schedule.every().day.at("16:00").do(post_job)
    schedule.every().day.at("18:00").do(post_job)
    schedule.every().day.at("20:00").do(news_job)
    
    print("✅ Jadval ishga tushdi. Bot uzluksiz ishlamoqda...")
    
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    if TELEGRAM_TOKEN == "BU_YERGA_TOKEN_YOZING":
        print("❌ Iltimos, muhit o'zgaruvchilariga TELEGRAM_TOKEN ni kiriting!")
        sys.exit(1)
        
    # Veb serverni ishga tushirish (Render uchun)
    keep_alive.keep_alive()
    
    # Jadvalni ishga tushirish
    run_schedule()
