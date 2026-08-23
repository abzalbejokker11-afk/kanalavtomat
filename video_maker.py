import os
import asyncio
import edge_tts

def create_audio(text):
    audio_path = "temp_audio.mp3"
    
    try:
        clean_text = text.replace("#", "").replace("*", "").replace("❓", "").replace("✅", "").replace("🎙", "").replace("⚠️", "")
        print("Professor/Diktator ovozi (edge-tts) orqali yasalmoqda...")
        
        try:
            # Yangi event loop yaratish (ichki loop bilan conflict bo'lmasligi uchun)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            communicate = edge_tts.Communicate(clean_text, "uz-UZ-MadinaNeural", rate="+5%", pitch="-5Hz")
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
