from moviepy.editor import ImageClip, AudioFileClip
from gtts import gTTS
import os
import requests

def create_video(text, image_url, output_filename="post_video.mp4"):
    print("⏳ Video yaratilmoqda...")
    try:
        # 1. Matndan audio yaratish (gTTS)
        # Matn juda uzun bo'lsa videoni zerikarli qiladi, shuning uchun boshlang'ich qismini olamiz
        short_text = text[:500] if len(text) > 500 else text
        tts = gTTS(short_text, lang='uz')
        audio_filename = "temp_audio.mp3"
        tts.save(audio_filename)
        
        # 2. Rasmni yuklab olish
        img_filename = "temp_image.jpg"
        r = requests.get(image_url)
        with open(img_filename, "wb") as f:
            f.write(r.content)
            
        # 3. Video yaratish
        audio_clip = AudioFileClip(audio_filename)
        duration = audio_clip.duration
        
        image_clip = ImageClip(img_filename).set_duration(duration)
        
        video = image_clip.set_audio(audio_clip)
        
        # Ekstremal kichik hajm va tezkor render uchun past fps
        video.write_videofile(output_filename, fps=1, codec="libx264", audio_codec="aac")
        
        # Vaqtinchalik fayllarni o'chirish
        os.remove(audio_filename)
        os.remove(img_filename)
        
        print(f"✅ Video muvaffaqiyatli yaratildi: {output_filename}")
        return output_filename
    except Exception as e:
        print(f"❌ Video yaratishda xatolik: {e}")
        return None

if __name__ == "__main__":
    test_text = "Bu sinov videosi. Doping qoidalari sportchilar uchun juda muhimdir."
    test_img = "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500&h=500&fit=crop"
    create_video(test_text, test_img)
