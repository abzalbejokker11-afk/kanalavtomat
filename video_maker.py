import os
import asyncio
import edge_tts
import requests
import subprocess
import imageio_ffmpeg

async def create_video(text, img_url="https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500&h=500&fit=crop"):
    audio_path = "temp_audio.mp3"
    img_path = "temp_img.jpg"
    out_path = "output_video.mp4"
    
    try:
        # 1. Rasmni yuklab olish
        print("Rasm yuklanmoqda...")
        response = requests.get(img_url, timeout=10)
        with open(img_path, 'wb') as f:
            f.write(response.content)
            
        # Matnni biroz qisqartiramiz (uzun bo'lsa)
        clean_text = text.replace("#", "").replace("*", "")
        if len(clean_text) > 400:
            clean_text = clean_text[:400] + "..."
            
        # 2. Audio generatsiya (Edge TTS - bepul va token kerak emas)
        print("Ovoz yaratilmoqda...")
        communicate = edge_tts.Communicate(clean_text, "uz-UZ-MadinaNeural")
        await communicate.save(audio_path)
        
        # 3. FFMPEG orqali video yasash
        print("Video yig'ilmoqda...")
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        
        cmd = [
            ffmpeg_exe,
            "-loop", "1",
            "-i", img_path,
            "-i", audio_path,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            "-y", out_path
        ]
        
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        # Tozalash
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(img_path):
            os.remove(img_path)
            
        return out_path
    except Exception as e:
        print(f"Video yaratishda xatolik: {e}")
        return None
