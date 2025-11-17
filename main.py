"""Main entry point for LG Time Deal crawler."""
import argparse
import logging
import sys
from crawler import LGTimedealCrawler
from telegram_sender import TelegramSender
from scheduler import start_scheduler, run_crawl_and_send
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_config():
    """Check if required configuration is set."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set. Please set it in .env file.")
        return False
    if not TELEGRAM_CHAT_ID:
        logger.error("TELEGRAM_CHAT_ID is not set. Please set it in .env file.")
        return False
    return True


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='LG Time Deal Crawler')
    parser.add_argument(
        '--mode',
        choices=['crawl', 'send', 'schedule'],
        default='crawl',
        help='Operation mode: crawl (default), send, or schedule'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode: run once and exit'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'schedule':
        if not check_config():
            sys.exit(1)
        start_scheduler()
    
    elif args.mode == 'crawl':
        logger.info("Running crawler...")
        crawler = LGTimedealCrawler()
        products = crawler.crawl()
        crawler.save_products(products)
        logger.info(f"Crawled {len(products)} products")
        
        if args.test and check_config():
            # Also send notification in test mode
            sender = TelegramSender()
            sender.send_products(products)
    
    elif args.mode == 'send':
        if not check_config():
            sys.exit(1)
        
        logger.info("Sending notification...")
        crawler = LGTimedealCrawler()
        products = crawler.load_products()
        
        if not products:
            logger.warning("No products found. Run crawl first.")
            sys.exit(1)
        
        sender = TelegramSender()
        success = sender.send_products(products)
        
        if success:
            logger.info("Notification sent successfully")
        else:
            logger.error("Failed to send notification")
            sys.exit(1)


if __name__ == "__main__":
    main()

