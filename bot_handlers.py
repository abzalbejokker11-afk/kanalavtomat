from aiogram import Router, Bot
from aiogram.types import Message, BotCommand, FSInputFile
from aiogram.filters import Command
import os
import asyncio
import news_scraper
import video_maker

router = Router()
CHANNEL_ID = "@uzantidoping"

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="post", description="📝 Doping bo'yicha audio post chiqarish")
    ]
    await bot.set_my_commands(commands)

from urllib.parse import quote
from aiogram.types import URLInputFile

async def async_post_job(bot: Bot = None, make_video: bool = False):
    try:
        loop = asyncio.get_event_loop()
        text, img_prompt = await loop.run_in_executor(None, news_scraper.generate_post_script)
        
        if not text or len(text.strip()) < 50:
            print("Matn juda qisqa yoki bo'sh keldi!")
            return False, "Matn generatsiya qilinmadi"
            
        # Rasm URL shakllantirish (Pollinations AI) - YouTube Shorts uchun 1080x1920 qilib so'raymiz
        image_url = f"https://image.pollinations.ai/prompt/{quote(img_prompt)}?width=1080&height=1920&nologo=true"
        
        audio_file, v_err = await loop.run_in_executor(None, video_maker.create_audio, text)
        
        if audio_file:
            if make_video:
                print("Video yaratilmoqda (YouTube Shorts formati)...")
                video_file = await loop.run_in_executor(None, video_maker.create_mp4, image_url, audio_file)
                if video_file:
                    try:
                        video_input = FSInputFile(video_file)
                        await bot.send_video(chat_id=CHANNEL_ID, video=video_input, caption="🎬 Doping va Sport (Maxsus Video) — to'liq matn pastda 👇")
                        for i in range(0, len(text), 4000):
                            await bot.send_message(chat_id=CHANNEL_ID, text=text[i:i+4000])
                    except Exception as ve:
                        print(f"Video yuborishda xato: {ve}")
                    
                    try:
                        os.remove(video_file)
                    except Exception:
                        pass
                else:
                    print("Video yaratish muvaffaqiyatsiz bo'ldi, oddiy xabar yuborilmoqda...")
                    make_video = False
                    
            if not make_video:
                # 1. Rasmni yuborish
                try:
                    await bot.send_photo(chat_id=CHANNEL_ID, photo=URLInputFile(image_url))
                except Exception as pe:
                    print(f"Rasm yuborishda xato: {pe}")
                    
                # 2. Ovozni yuborish
                voice_input = FSInputFile(audio_file)
                
                # Telegram caption limiti 1024 belgi. Agar matn uzun bo'lsa:
                if len(text) <= 1024:
                    await bot.send_voice(chat_id=CHANNEL_ID, voice=voice_input, caption=text)
                else:
                    await bot.send_voice(chat_id=CHANNEL_ID, voice=voice_input, caption="🎙 Doping va Sport bo'yicha Podkast — to'liq matn pastda 👇")
                    for i in range(0, len(text), 4000):
                        chunk = text[i:i+4000]
                        await bot.send_message(chat_id=CHANNEL_ID, text=chunk)
            
            # Tozalash
            try:
                os.remove(audio_file)
            except Exception:
                pass
            return True, "✅ Muvaffaqiyatli"
        return False, f"Ovoz yaratilmadi. Xato: {v_err}"
    except Exception as e:
        print(f"Post yuborishda xato: {e}")
        return False, str(e)

# --- HANDLERLAR ---

@router.message(Command("post"))
async def cmd_post(message: Message, bot: Bot):
    msg = await message.reply("⏳ Savol-javobli professor podkasti tayyorlanmoqda (Madina ovozi)...")
    success, err_text = await async_post_job(bot)
    if success:
        await msg.edit_text("✅ Audio podkast muvaffaqiyatli kanalga yuborildi!")
    else:
        await msg.edit_text(f"❌ Xatolik yuz berdi:\n\n{err_text}")
