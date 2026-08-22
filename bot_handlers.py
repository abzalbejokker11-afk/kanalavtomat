from aiogram import Router, Bot
from aiogram.types import Message, BotCommand, FSInputFile
from aiogram.filters import Command
import os
import asyncio
import news_scraper
import video_maker  # file name is video_maker.py but handles audio now

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
        
        audio_file, v_err = await loop.run_in_executor(None, video_maker.create_audio, text)
        
        if audio_file:
            voice_input = FSInputFile(audio_file)
            await bot.send_voice(chat_id=CHANNEL_ID, voice=voice_input, caption=text, parse_mode="Markdown")
            
            # Tozalash
            os.remove(audio_file)
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
        await msg.edit_text(f"❌ Xatolik yuz berdi:\n\n`{err_text}`", parse_mode="Markdown")
