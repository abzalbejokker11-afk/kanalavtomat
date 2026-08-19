from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot_handlers import async_video_job

def setup_scheduler(bot):
    scheduler = AsyncIOScheduler()
    
    # Har kuni soat 07:00 dan 22:00 gacha HAR SOATDA post (video/ovozli) tashlanadi!
    # minute=0 degani soat boshi (07:00, 08:00, 09:00 ...)
    scheduler.add_job(async_video_job, 'cron', hour='7-22', minute=0, args=[bot])
    
    scheduler.start()
    return scheduler
