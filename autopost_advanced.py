import os
import sys
import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import keep_alive
from bot_handlers import router, set_bot_commands, async_post_job, async_news_job, async_video_job

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "BU_YERGA_TOKEN_YOZING")

async def main():
    if TELEGRAM_TOKEN == "BU_YERGA_TOKEN_YOZING":
        print("❌ Iltimos, muhit o'zgaruvchilariga TELEGRAM_TOKEN ni kiriting!")
        sys.exit(1)
        
    # Veb serverni ishga tushirish (Render uxlamasligi uchun)
    keep_alive.keep_alive()

    # Aiogram 3.x bot va dispatcher ni yaratish
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    
    # Router va Komandalarni o'rnatish
    dp.include_router(router)
    await set_bot_commands(bot)
    
    # APScheduler orqali vaqtga biriktirilgan vazifalarni o'rnatish
    scheduler = AsyncIOScheduler()
    
    # Kunlik reja (Vaqtlar oldingi kelishuv asosida):
    scheduler.add_job(async_post_job, 'cron', hour=8, minute=0, args=[bot])
    scheduler.add_job(async_post_job, 'cron', hour=10, minute=0, args=[bot])
    scheduler.add_job(async_video_job, 'cron', hour=12, minute=0, args=[bot])
    scheduler.add_job(async_post_job, 'cron', hour=14, minute=0, args=[bot])
    scheduler.add_job(async_post_job, 'cron', hour=16, minute=0, args=[bot])
    scheduler.add_job(async_post_job, 'cron', hour=18, minute=0, args=[bot])
    scheduler.add_job(async_news_job, 'cron', hour=20, minute=0, args=[bot])
    
    scheduler.start()
    
    print("✅ Aiogram Bot va Jadval ishga tushdi. Bot xabarlarni kutmoqda...")
    
    # Botni ishga tushirish (Polling)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
