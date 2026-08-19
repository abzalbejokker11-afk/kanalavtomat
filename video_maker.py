import os
import asyncio
import edge_tts
import requests
import random

def download_images(query, count=5):
    images = []
    
    # 1. Wikimedia API orqali qidirish
    print("Wikimedia orqali rasmlar qidirilmoqda...")
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&generator=search&gsrsearch={query}&gsrlimit=10&pithumbsize=500"
    headers = {"User-Agent": "KanalAvtomatBot/1.0"}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            pages = data.get("query", {}).get("pages", {})
            downloaded = 0
            for k, v in pages.items():
                if downloaded >= count:
                    break
                if "thumbnail" in v:
                    img_url = v["thumbnail"]["source"]
                    try:
                        ir = requests.get(img_url, timeout=5)
                        if ir.status_code == 200:
                            filename = f"slide_{downloaded}.jpg"
                            with open(filename, 'wb') as f:
                                f.write(ir.content)
                            images.append(filename)
                            downloaded += 1
                    except:
                        continue
    except Exception as e:
        print("Wikimedia rasm qidirishda xato:", e)
    
    # Zaxira
    if not images:
        images.append("slide_0.jpg") # umidsizlik

    return images

def create_video(text, img_url=None):
    audio_path = "temp_audio.mp3"
    
    try:
        clean_text = text.replace("#", "").replace("*", "")
        # Madina diktatordek o'qishi uchun ohang va balandlikni to'g'rilaymiz
        print("Madina ovozi (edge-tts) orqali yasalmoqda...")
        
        try:
            # rate=+10% tezroq va pitch=-5Hz jiddiyroq
            communicate = edge_tts.Communicate(clean_text, "uz-UZ-MadinaNeural", rate="+10%", pitch="-5Hz")
            asyncio.run(communicate.save(audio_path))
        except Exception as tts_err:
            print(f"Edge-TTS (Madina) ishlashda xatolik qildi: {tts_err}. gTTS zaxirasiga o'tilmoqda...")
            from gtts import gTTS
            tts = gTTS(text=clean_text, lang='uz', slow=False)
            tts.save(audio_path)
            
        print("Rasmlar yuklanmoqda...")
        queries = ["sports competition", "athlete stadium", "running track", "olympics", "doping sports", "wada"]
        images = download_images(random.choice(queries), count=5)
        
        return audio_path, images, None
    except Exception as e:
        print(f"Video yaratishda xatolik: {e}")
        return None, None, str(e)
