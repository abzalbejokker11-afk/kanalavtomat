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

async def async_post_job(bot: Bot = None):
    try:
        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(None, news_scraper.generate_post_script)
        
        if not text or len(text.strip()) < 50:
            print("Matn juda qisqa yoki bo'sh keldi!")
            return False, "Matn generatsiya qilinmadi"
        
        audio_file, v_err = await loop.run_in_executor(None, video_maker.create_audio, text)
        
        if audio_file:
            voice_input = FSInputFile(audio_file)
            
            # Telegram caption limiti 1024 belgi. Agar matn uzun bo'lsa:
            if len(text) <= 1024:
                # Qisqa matn — caption sifatida yuboramiz
                await bot.send_voice(chat_id=CHANNEL_ID, voice=voice_input, caption=text)
            else:
                # Uzun matn — avval ovozni, keyin matnni alohida yuboramiz
                await bot.send_voice(chat_id=CHANNEL_ID, voice=voice_input, caption="🎙 Doping va Sport bo'yicha Podkast — to'liq matn pastda 👇")
                
                # Uzun matnni 4096 belgidan bo'laklarga bo'lib yuboramiz
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
        print(f"Ovozli post yuborishda xato: {e}")
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
