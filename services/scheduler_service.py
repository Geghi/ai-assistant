from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.gmail_service import process_and_summarize_emails
from services.telegram_service import TelegramService
from api.v1.dependencies import get_telegram_service
from fastapi import Depends

# Global scheduler instance
scheduler = AsyncIOScheduler()

def schedule_daily_summary(telegram_service: TelegramService = Depends(get_telegram_service)):
    """
    Schedules the daily email summary job to run at a specific interval.
    For this POC, we'll run it every hour.
    """
    # In a real application, you might want to run this once a day.
    # For demonstration, we run it more frequently.
    scheduler.add_job(
        process_and_summarize_emails,
        'interval',
        hours=1,
        id="daily_email_summary",
        replace_existing=True,
        args=[telegram_service]
    )

def start_scheduler():
    """
    Starts the scheduler and adds the jobs.
    """
    if not scheduler.running:
        scheduler.start()
        # We can't inject the dependency here directly, so we will pass it in the job
        # schedule_daily_summary()
        print("Scheduler started.")

def shutdown_scheduler():
    """
    Shuts down the scheduler.
    """
    if scheduler.running:
        scheduler.shutdown()
        print("Scheduler shut down.")
