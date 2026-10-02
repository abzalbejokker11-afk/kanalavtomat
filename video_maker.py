import os
import asyncio
import edge_tts

def create_audio(text):
    audio_path = "temp_audio.mp3"
    
    try:
        from normalizer import normalize_for_tts
        clean_text = text.replace("#", "").replace("*", "").replace("❓", "").replace("✅", "").replace("🎙", "").replace("⚠️", "")
        clean_text = normalize_for_tts(clean_text)
        print("Professor/Diktator ovozi (edge-tts) orqali yasalmoqda...")
        
        try:
            # Yangi event loop yaratish (ichki loop bilan conflict bo'lmasligi uchun)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            communicate = edge_tts.Communicate(clean_text, "uz-UZ-MadinaNeural", rate="-10%", pitch="-5Hz")
            loop.run_until_complete(communicate.save(audio_path))
            loop.close()
        except Exception as tts_err:
            print(f"Edge-TTS ishlashda xatolik qildi: {tts_err}. gTTS zaxirasiga o'tilmoqda...")
            from gtts import gTTS
            tts = gTTS(text=clean_text, lang='uz', slow=False)
            tts.save(audio_path)
            
        return audio_path, None
    except Exception as e:
        print(f"Ovoz yaratishda xatolik: {e}")
        return None, str(e)

def create_mp4(image_url, audio_path, output_path="temp_video.mp4"):
    import subprocess
    import imageio_ffmpeg
    import requests
    import os
    try:
        print("1. Rasm yuklanmoqda (Video uchun)...")
        img_data = requests.get(image_url).content
        with open("temp_image.jpg", "wb") as f:
            f.write(img_data)
            
        print("2. FFMPEG orqali video yasalmoqda...")
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        
        cmd = [
            ffmpeg_exe, "-y",
            "-loop", "1", "-i", "temp_image.jpg",
            "-i", audio_path,
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest", output_path
        ]
        
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Video muvaffaqiyatli yaratildi!")
        
        if os.path.exists("temp_image.jpg"):
            os.remove("temp_image.jpg")
            
        return output_path
    except Exception as e:
        print(f"Video yaratishda xato: {e}")
        return None
