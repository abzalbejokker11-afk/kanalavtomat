import os
import asyncio
import edge_tts
import requests

def create_audio(text):
    audio_path = "temp_audio.mp3"
    
    try:
        clean_text = text.replace("#", "").replace("*", "")
        print("Professor/Diktator ovozi (edge-tts) orqali yasalmoqda...")
        
        try:
            # rate=+5% (salf pastroq tezlik), pitch=-5Hz (jiddiy professordek ohang)
            communicate = edge_tts.Communicate(clean_text, "uz-UZ-MadinaNeural", rate="+5%", pitch="-5Hz")
            asyncio.run(communicate.save(audio_path))
        except Exception as tts_err:
            print(f"Edge-TTS ishlashda xatolik qildi: {tts_err}. gTTS zaxirasiga o'tilmoqda...")
            from gtts import gTTS
            tts = gTTS(text=clean_text, lang='uz', slow=False)
            tts.save(audio_path)
            
        return audio_path, None
    except Exception as e:
        print(f"Ovoz yaratishda xatolik: {e}")
        return None, str(e)
