import asyncio
import os
import requests
from aiogram import Bot
from aiogram.types import FSInputFile, InputMediaPhoto

# Barcha og'ir vazifalarni (API, TTS, yuklab olish) bajaruvchi modullar:
import news_scraper
import video_maker

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "BU_YERGA_TOKEN_YOZING")
CHANNEL_ID = "@uzantidoping"

async def main():
    if TELEGRAM_TOKEN == "BU_YERGA_TOKEN_YOZING":
        print("Xatolik: TELEGRAM_TOKEN mavjud emas!")
        return

    bot = Bot(token=TELEGRAM_TOKEN)
    
    try:
        print("GitHub Actions: Skript yaratilmoqda...")
        text = news_scraper.generate_video_script()
        
        print("GitHub Actions: Audio va rasm yasalmoqda...")
        img_url = None
        audio_file, images, v_err = video_maker.create_video(text, img_url)
        
        if audio_file and images:
            # 1. Rasmlarni karusel qilib yuborish
            media_group = [InputMediaPhoto(media=FSInputFile(img)) for img in images if os.path.exists(img)]
            if media_group:
                print("GitHub Actions: Rasmlar yuborilmoqda...")
                await bot.send_media_group(chat_id=CHANNEL_ID, media=media_group)
            
            # 2. Ovozli xabarni yuborish
            if os.path.exists(audio_file):
                print("GitHub Actions: Audio yuborilmoqda...")
                voice_input = FSInputFile(audio_file)
                await bot.send_voice(
                    chat_id=CHANNEL_ID, 
                    voice=voice_input, 
                    caption=text[:300] + "...\n\n🎤 *Sardor (Podcast)*", 
                    parse_mode="Markdown"
                )
            
            # Tozalash
            if os.path.exists(audio_file):
                os.remove(audio_file)
            for img in images:
                if os.path.exists(img):
                    os.remove(img)
            
            print("GitHub Actions: Barcha jarayon muvaffaqiyatli yakunlandi!")
        else:
            print(f"GitHub Actions Xatoligi: video_maker {v_err} qaytardi.")
            
    except Exception as e:
        print(f"GitHub Actions Umumiy Xatoligi: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
