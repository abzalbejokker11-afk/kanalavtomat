import os
import sys
import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import keep_alive
from bot_handlers import router, set_bot_commands, async_post_job

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")

async def main():
    if not TELEGRAM_TOKEN:
        print("❌ Iltimos, muhit o'zgaruvchilariga TELEGRAM_TOKEN ni kiriting!")
        sys.exit(1)
        
    # Veb serverni ishga tushirish (Render uxlamasligi uchun)
    keep_alive.keep_alive()

    # Aiogram bot va dispatcher
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    
    # Router va Komandalarni o'rnatish
    dp.include_router(router)
    await set_bot_commands(bot)
    
    # APScheduler orqali vaqtga biriktirilgan vazifalarni o'rnatish
    scheduler = AsyncIOScheduler()
    
    # Aniq belgilangan soatlarda (09:00, 13:00, 17:00, 21:00) post yuborish
    scheduler.add_job(async_post_job, 'cron', hour='9,13,17,21', minute=0, args=[bot])
    
    scheduler.start()
    
    print("✅ Aiogram Bot va Jadval ishga tushdi. Bot xabarlarni kutmoqda...")
    
    # Botni ishga tushirish (Polling)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
