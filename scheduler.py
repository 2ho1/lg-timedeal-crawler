"""Scheduler for LG Time Deal crawler."""
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from crawler import LGTimedealCrawler
from telegram_sender import TelegramSender
from config import SCHEDULE_HOUR, SCHEDULE_MINUTE

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_crawl_and_send():
    """Run crawler and send notification."""
    logger.info("Starting scheduled crawl and notification")
    
    try:
        # Crawl products
        crawler = LGTimedealCrawler()
        products = crawler.crawl()
        
        if not products:
            logger.warning("No products found")
            return
        
        # Save products
        crawler.save_products(products)
        
        # Send notification
        sender = TelegramSender()
        success = sender.send_products(products)
        
        if success:
            logger.info(f"Successfully sent notification for {len(products)} products")
        else:
            logger.error("Failed to send notification")
            
    except Exception as e:
        logger.error(f"Error in scheduled task: {e}", exc_info=True)


def start_scheduler():
    """Start the scheduler."""
    scheduler = BlockingScheduler()
    
    # Schedule daily at 9:00 AM
    scheduler.add_job(
        run_crawl_and_send,
        trigger=CronTrigger(hour=SCHEDULE_HOUR, minute=SCHEDULE_MINUTE),
        id='lg_timedeal_daily',
        name='LG Time Deal Daily Crawl',
        replace_existing=True
    )
    
    logger.info(f"Scheduler started. Will run daily at {SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d}")
    logger.info("Press Ctrl+C to exit")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    start_scheduler()

