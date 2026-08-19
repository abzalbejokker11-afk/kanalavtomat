import os
import asyncio
import edge_tts
import requests
import subprocess
import imageio_ffmpeg
import random
try:
    from duckduckgo_search import DDGS
except ImportError:
    pass

async def download_images(query, count=5):
    images = []
    
    # 1. Wikimedia API orqali qidirish (100% tekin va bloklanmaydi)
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
    
    # 2. Agar baribir rasm topilmasa, zaxira rasmlar (ko'plikda)
    if not images:
        fallback_urls = [
            "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1526506190242-25952f447703?w=500&h=500&fit=crop"
        ]
        for i, url in enumerate(fallback_urls):
            try:
                r = requests.get(url, timeout=5)
                filename = f"slide_{i}.jpg"
                with open(filename, "wb") as f:
                    f.write(r.content)
                images.append(filename)
            except:
                pass
                
    # Yana bo'sh bo'lsa (bunday bo'lmasligi kerak)
    if not images:
        images.append("slide_0.jpg") # umidsizlik

    return images

async def create_video(text, img_url=None):
    audio_path = "temp_audio.mp3"
    out_path = "output_video.mp4"
    slides_txt = "slides.txt"
    images = []
    
    try:
        # Matnni tozalash va tayyorlash
        clean_text = text.replace("#", "").replace("*", "")
        if len(clean_text) > 400:
            clean_text = clean_text[:400] + "..."
            
        print("Ovoz yaratilmoqda...")
        communicate = edge_tts.Communicate(clean_text, "uz-UZ-SardorNeural") # SardorNeural (Erkak ovozi)
        await communicate.save(audio_path)
        
        print("Rasmlar yuklanmoqda...")
        queries = ["sports competition", "athlete stadium", "running track", "olympics"]
        images = await download_images(random.choice(queries), count=5)
        
        print("Slideshow fayli yozilmoqda...")
        # Har bir rasm 4 soniya turadi. Audio uzun bo'lishi mumkinligini inobatga olib, rasmlarni 10 marta takrorlaymiz
        with open(slides_txt, "w") as f:
            for _ in range(10):
                for img in images:
                    f.write(f"file '{img}'\n")
                    f.write("duration 4.0\n")
            # Oxirgi rasm majburiy qoida
            f.write(f"file '{images[-1]}'\n")
            
        print("Video yig'ilmoqda (FFMPEG slideshow)...")
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        
        # -shortest orqali audio tugaganda video ham tugaydi
        cmd = [
            ffmpeg_exe,
            "-f", "concat",
            "-safe", "0",
            "-i", slides_txt,
            "-i", audio_path,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-y", out_path
        ]
        
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        # Tozalash
        for f in [audio_path, slides_txt] + images:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass
            
        return out_path
    except Exception as e:
        print(f"Video yaratishda xatolik: {e}")
        return None
