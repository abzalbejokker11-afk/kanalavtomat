from aiogram import Router, Bot
from aiogram.types import Message, BotCommand, FSInputFile
from aiogram.filters import Command
import os
import json
import asyncio
import news_scraper
import video_maker

router = Router()
CHANNEL_ID = "@uzantidoping"

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="post", description="📝 Doping bo'yicha post chiqarish"),
        BotCommand(command="video", description="🎬 Video tayyorlash"),
        BotCommand(command="news", description="📰 Yangiliklarni tekshirish")
    ]
    await bot.set_my_commands(commands)

# Yordamchi funksiyalar (Sinxron kodlarni asinxron tarzda ishlatish uchun)
async def async_post_job(bot: Bot):
    try:
        if os.path.exists("posts.json"):
            with open("posts.json", "r", encoding="utf-8") as f:
                posts = json.load(f)
            if posts:
                post = posts.pop(0)
                text = post.get("text", "") if isinstance(post, dict) else str(post)
                
                await bot.send_message(chat_id=CHANNEL_ID, text=text)
                
                with open("posts.json", "w", encoding="utf-8") as f:
                    json.dump(posts, f, ensure_ascii=False, indent=2)
                return True
        return False
    except Exception as e:
        print(f"Xatolik: {e}")
        return False

async def async_news_job(bot: Bot):
    # Sinxron funksiyani event loop da ishlatish
    loop = asyncio.get_event_loop()
    news_text = await loop.run_in_executor(None, news_scraper.generate_news_post)
    
    if news_text:
        await bot.send_message(chat_id=CHANNEL_ID, text=news_text)
        return True
    return False

async def async_video_job(bot: Bot):
    if os.path.exists("posts.json"):
        with open("posts.json", "r", encoding="utf-8") as f:
            posts = json.load(f)
        if posts:
            post = posts[0]
            text = post.get("text", "") if isinstance(post, dict) else str(post)
            img_url = "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=500&h=500&fit=crop"
            
            video_file = await video_maker.create_video(text, img_url)
            
            if video_file:
                video_input = FSInputFile(video_file)
                await bot.send_video(chat_id=CHANNEL_ID, video=video_input, caption=text[:200] + "...")
                os.remove(video_file)
                return True
    return False

# --- HANDLERLAR ---

@router.message(Command("post"))
async def cmd_post(message: Message, bot: Bot):
    msg = await message.reply("⏳ Post tayyorlanmoqda va kanalga yuborilmoqda...")
    success = await async_post_job(bot)
    if success:
        await msg.edit_text("✅ Post muvaffaqiyatli kanalga yuborildi!")
    else:
        await msg.edit_text("❌ Hozircha tayyor postlar yo'q. 'posts.json' ni tekshiring.")

@router.message(Command("video"))
async def cmd_video(message: Message, bot: Bot):
    msg = await message.reply("⏳ Video yig'ilmoqda (bu biroz vaqt olishi mumkin)...")
    success = await async_video_job(bot)
    if success:
        await msg.edit_text("✅ Video muvaffaqiyatli tayyorlandi va kanalga yuborildi!")
    else:
        await msg.edit_text("❌ Video tayyorlash uchun post topilmadi yoki xatolik yuz berdi.")

@router.message(Command("news"))
async def cmd_news(message: Message, bot: Bot):
    msg = await message.reply("⏳ Yangiliklar qidirilmoqda va tahlil qilinmoqda...")
    success = await async_news_job(bot)
    if success:
        await msg.edit_text("✅ Yangiliklar muvaffaqiyatli kanalga yuborildi!")
    else:
        await msg.edit_text("❌ Bugun uchun yangilik topilmadi yoki xatolik yuz berdi.")
